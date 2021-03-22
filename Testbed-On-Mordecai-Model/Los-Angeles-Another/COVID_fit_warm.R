##################################
## Fit COVID epidemic with pomp ##
##################################

set.seed(10001)
fitting           <- TRUE     ## Small change in pomp objects if fitting or simulating
fit.minus         <- 0        ## Use data until X days prior to the present
more.params.uncer <- FALSE    ## Fit with more (FALSE) or fewer (TRUE) point estimates for a number of parameters
fit.E0            <- TRUE     ## Also fit initial # that starts the epidemic?
## more.params.uncer = FALSE is more supported, uses parameter ranges with more research and reacts to choice of focal.county if possible
## !!!!! For FALSE update parameters in location_params.csv
## more.params.uncer = TRUE  is less suppored, raw parameter values that can be adjusted manually
usable.cores      <- 2        ## Number of cores to use to fit
fit.with          <- "D"      ## Fit with D (deaths) or H (hospitalizations) 
fit_to_sip        <- TRUE     ## Fit beta0 and shelter in place simultaneously?
import_cases      <- FALSE    ## Use importation of cases?
n.mif_runs        <- 2        ## mif2 fitting parameters
n.mif_length      <- 30
n.mif_particles   <- 60
n.mif_rw.sd       <- 0.002
focal.county      <- "Los Angeles"  ## County to fit to
## !!! Curently parameters exist for Santa Clara, Miami-Dade, New York City, King, Los Angeles
## !!! But only Santa Clara explored
# county.N        <- 1.938e6         ## County population size
## !!! Now contained within location_params.csv
nparams           <- 5               ## number of parameter sobol samples (more = longer)
nsim              <- 1000             ## number of simulations for each fitted beta0 for dynamics

needed_packages <- c(
    "pomp"
  , "plyr"
  , "dplyr"
  , "ggplot2"
  , "magrittr"
  , "scales"
  , "lubridate"
  , "tidyr"
  , "foreach"
  , "doParallel"
  , "data.table")

lapply(needed_packages, require, character.only = TRUE)

## Be very careful here, adjust according to your machine
registerDoParallel(cores = usable.cores)

## Bring in pomp objects
source("COVID_pomp.R")
 
if (fit.with == "D") {
#deaths <- fread("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv")
deaths  <- read.csv("us-counties.txt")
deaths  <- deaths %>% mutate(date = as.Date(date)) %>% filter(county == focal.county)
#deaths  <- deaths %>% dplyr::filter(date < max(date) - fit.minus)
} else if (fit.with == "H") {
## !! Not supported right now for SCC, but placing here for completeness
   ## !! Right now only usable for CCC
hospit     <- read.csv("contra_costa/ccc_data.csv")
hospit     <- hospit %>% 
  mutate(date = as.Date(REPORT_DATE)) %>% 
  filter(CURRENT_HOSPITALIZED != "NULL") %>% 
  mutate(ch = as.numeric(as.character(CURRENT_HOSPITALIZED))) %>% 
  dplyr::select(date, ch)
hospit    <- hospit %>% dplyr::filter(date < max(date) - fit.minus)  
}

if (!more.params.uncer) {
params <- read.csv("params.csv", stringsAsFactors = FALSE)
} else {
params <- read.csv("params_wide.csv", stringsAsFactors = FALSE) 
}
params <- params %>% mutate(Value = sapply(est, function(x) eval(parse(text = x))))

fixed_params        <- params$Value
names(fixed_params) <- params$Parameter
if (!import_cases) {fixed_params["import_rate"] <- 0}

location_params     <- read.csv("location_params.csv", stringsAsFactors = FALSE)
location_params     <- location_params %>% filter(location == focal.county)

## debug
#location_params[location_params$Parameter == "sim_start", ]$lwr <- 38
#location_params[location_params$Parameter == "sim_start", ]$upr <- 53

fixed_params        <- c(fixed_params
  , N = location_params[location_params$Parameter == "N", ]$est)

if (more.params.uncer) {
source("variable_params_more.R")
} else {
source("variable_params_less.R")
}

## Run parameters
sim_start  <- variable_params$sim_start
sim_length <- 92
sim_end    <- sim_start + sim_length

## containers for results
SEIR.sim.ss.t.ci <- data.frame(
  name     = character(0)
, lwr      = numeric(0)
, est      = numeric(0)
, upr      = numeric(0)
, paramset = numeric(0))

param_array <- array(
  data = 0
, dim  = c(nparams, n.mif_runs, 15))
dimnames(param_array)[[3]] <- c("beta0", "alpha", "mu", "delta", "soc_dist_level_sip", "loglik", "E_init", "Ia_init", "Ip_init", "Is_init", "Im_init", "Hr_init", "Hd_init", "R0_init", "D0_init")  

for (i in 5:nrow(variable_params)) {

if (fit.with == "D") {
  
  ## Adjust the data for the current start date
county.data <- deaths %>% 
  mutate(day = as.numeric(date - variable_params[i, ]$sim_start)) %>% 
  filter(day > 0) %>%
  dplyr::select(day, date, deaths, cases, uncases) %>% 
  mutate(deaths_cum = deaths) %>% 
  mutate(deaths = deaths_cum - lag(deaths_cum)) %>% 
  replace_na(list(deaths = 0)) %>%
  dplyr::select(-deaths_cum) %>%
  mutate(cases_cum = cases) %>% 
  mutate(cases = cases_cum - lag(cases_cum)) %>% 
  replace_na(list(cases = 0)) %>%
  dplyr::select(-cases_cum) %>%
  mutate(uncases_cum = uncases) %>% 
  mutate(uncases = uncases_cum - lag(uncases_cum)) %>% 
  replace_na(list(uncases = 0)) %>%
  dplyr::select(-uncases_cum)
  
## Add days from the start of the sim to the first recorded day in the dataset
#county.data <- rbind(
#  data.frame(
#    day    = seq(1:(min(county.data$day) - 1))
#  , date   = as.Date(seq(1:(min(county.data$day) - 1)), origin = variable_params[i, ]$sim_start)
#  , deaths = 0
#  )
#, county.data
#  )

} else if (fit.with == "H") {
  
## Adjust the data for the current start date
county.data <- hospit %>% mutate(day = as.numeric(date - variable_params[i, ]$sim_start)) 
names(county.data)[2] <- "hosp"  

}

## Create intervention covariate table for the full forecast
if (fit_to_sip) {
  intervention.forecast <- with(variable_params[i, ], {

 covariate_table(
  day              = 1:sim_length
  
, intervention     = c(
      # No intervention until intervention start time
    rep(0, sim_length)                   
)
  
, isolation        = rep(NA, sim_length)
, iso_severe_level = rep(NA, sim_length)      # % of contats that severe cases maintain
, iso_mild_level   = rep(NA, sim_length)   # % of contats that mild cases maintain

, soc_dist_level_wfh = rep(soc_dist_level_wfh, sim_length) 

, thresh_H_start   = rep(NA, sim_length)
, thresh_H_end     = rep(NA, sim_length)

, thresh_int_level = rep(NA, sim_length)
, back_int_level   = rep(NA, sim_length)
  
, order            = "constant"
, times            = "day"
  )

})
} else {
  intervention.forecast <- with(variable_params[i, ], {

 covariate_table(
  day              = 1:sim_length
  
, intervention     = c(
      # No intervention until intervention start time
    rep(0, int_start1 - sim_start)                   
      # Intervention style 1
  , rep(1, int_length1)
      # Intervention style 2
  , rep(2, sim_length - (int_start2 - sim_start))
      # Post intervention close
)
  
, isolation        = rep(NA, sim_length)
, iso_severe_level = rep(NA, sim_length)      # % of contats that severe cases maintain
, iso_mild_level   = rep(NA, sim_length)   # % of contats that mild cases maintain

, soc_dist_level_wfh = rep(soc_dist_level_wfh, sim_length) 
, soc_dist_level_sip = rep(soc_dist_level_sip, sim_length)

, thresh_H_start   = rep(NA, sim_length)
, thresh_H_end     = rep(NA, sim_length)

, thresh_int_level = rep(NA, sim_length)
, back_int_level   = rep(NA, sim_length)
  
, order            = "constant"
, times            = "day"
  )

})  
}

covid.fitting <- pomp(
    data       = county.data %>% select(day, deaths, cases, uncases)
  , time       = "day"
  , t0         = 1
  , covar      = intervention.forecast
  , rprocess   = euler(sir_step, delta.t = 1/6)
  , rmeasure   = { 
   if (fit.with == "D") { rmeas_deaths } else if (fit.with == "H") { rmeas_hosp }
  }
  , dmeasure   = {
   if (fit.with == "D") { dmeas_deaths } else if (fit.with == "H") { dmeas_hosp }
  }
  , rinit      = sir_init
  , partrans   = par_trans
  , accumvars  = accum_names
  , paramnames = param_names
  , statenames = state_names) 

read_params <- read.csv(file = 'parameter.csv')
read_parameters <- read_params[5, ]
beta_read = read_parameters[["beta0est"]]
alpha_read = read_parameters[["alphaest"]]
mu_read = read_parameters[["muest"]]
delta_read = read_parameters[["deltaest"]]
soc_dist_read = read_parameters[["soc_dist_level_sip"]]
E_init_read = read_parameters[["E_init"]]    
Ia_init_read = read_parameters[["Ia_init"]]  
Ip_init_read = read_parameters[["Ip_init"]]  
Is_init_read = read_parameters[["Is_init"]]  
Im_init_read = read_parameters[["Im_init"]]  
Hr_init_read = read_parameters[["Hr_init"]]  
Hd_init_read = read_parameters[["Hd_init"]]  
R0_init_read = read_parameters[["R0_init"]]  
D0_init_read = read_parameters[["D0_init"]]
    
if (variable_params[i, ]$beta0est == 0) {

if (!more.params.uncer) {

checktime <- system.time({
mifs_local <- foreach(j = 1:n.mif_runs, .combine = c) %dopar%  {
    
library(pomp)
library(dplyr)

  covid.fitting %>%
  mif2(
    t0      = 1
  , params  = c(
    c(fixed_params
    , Ca    = variable_params[i, ]$Ca
      )
  , {
    c(beta0              = beta_read
    , alpha              = alpha_read
    , mu                 = mu_read
    , delta              = delta_read
    , soc_dist_level_sip = soc_dist_read
    , E_init             = E_init_read
    , Ia_init            = Ia_init_read
    , Ip_init            = Ip_init_read
    , Is_init            = Is_init_read
    , Im_init            = Im_init_read
    , Hr_init            = Hr_init_read
    , Hd_init            = Hd_init_read
    , R0_init            = R0_init_read
    , D0_init            = D0_init_read
    )
  }
  )
  , Np     = n.mif_particles
  , Nmif   = n.mif_length
  , cooling.fraction.50 = 0.5
  , rw.sd  = {
    rw.sd(beta0 = n.mif_rw.sd, alpha = n.mif_rw.sd, mu = n.mif_rw.sd, delta = n.mif_rw.sd, soc_dist_level_sip = n.mif_rw.sd, E_init = n.mif_rw.sd, Ia_init = n.mif_rw.sd, Ip_init = n.mif_rw.sd, Is_init = n.mif_rw.sd, Im_init = n.mif_rw.sd, Hr_init = n.mif_rw.sd, Hd_init = n.mif_rw.sd, R0_init = n.mif_rw.sd, D0_init = n.mif_rw.sd)        
  }
        )

}

})

if (fit_to_sip) {
 variable_params[i, "soc_dist_level_sip"] <- mean(coef(mifs_local)[which(dimnames(coef(mifs_local))$parameter == "soc_dist_level_sip"), ])
 param_array[i,,"soc_dist_level_sip"]     <- coef(mifs_local)[which(dimnames(coef(mifs_local))$parameter == "soc_dist_level_sip"), ]
}
if (fit.E0) {
variable_params[i, "E_init"] <- mean(coef(mifs_local)[which(dimnames(coef(mifs_local))$parameter == "E_init"), ])
param_array[i,,"E_init"]     <- coef(mifs_local)[which(dimnames(coef(mifs_local))$parameter == "E_init"), ]
variable_params[i, "Ia_init"] <- mean(coef(mifs_local)[which(dimnames(coef(mifs_local))$parameter == "Ia_init"), ])
param_array[i,,"Ia_init"]     <- coef(mifs_local)[which(dimnames(coef(mifs_local))$parameter == "Ia_init"), ]
variable_params[i, "Ip_init"] <- mean(coef(mifs_local)[which(dimnames(coef(mifs_local))$parameter == "Ip_init"), ])
param_array[i,,"Ip_init"]     <- coef(mifs_local)[which(dimnames(coef(mifs_local))$parameter == "Ip_init"), ]
variable_params[i, "Is_init"] <- mean(coef(mifs_local)[which(dimnames(coef(mifs_local))$parameter == "Is_init"), ])
param_array[i,,"Is_init"]     <- coef(mifs_local)[which(dimnames(coef(mifs_local))$parameter == "Is_init"), ]
variable_params[i, "Im_init"] <- mean(coef(mifs_local)[which(dimnames(coef(mifs_local))$parameter == "Im_init"), ])
param_array[i,,"Im_init"]     <- coef(mifs_local)[which(dimnames(coef(mifs_local))$parameter == "Im_init"), ]
variable_params[i, "Hr_init"] <- mean(coef(mifs_local)[which(dimnames(coef(mifs_local))$parameter == "Hr_init"), ])
param_array[i,,"Hr_init"]     <- coef(mifs_local)[which(dimnames(coef(mifs_local))$parameter == "Hr_init"), ]
variable_params[i, "Hd_init"] <- mean(coef(mifs_local)[which(dimnames(coef(mifs_local))$parameter == "Hd_init"), ])
param_array[i,,"Hd_init"]     <- coef(mifs_local)[which(dimnames(coef(mifs_local))$parameter == "Hd_init"), ]
variable_params[i, "R0_init"] <- mean(coef(mifs_local)[which(dimnames(coef(mifs_local))$parameter == "R0_init"), ])
param_array[i,,"R0_init"]     <- coef(mifs_local)[which(dimnames(coef(mifs_local))$parameter == "R0_init"), ]
variable_params[i, "D0_init"] <- mean(coef(mifs_local)[which(dimnames(coef(mifs_local))$parameter == "D0_init"), ])
param_array[i,,"D0_init"]     <- coef(mifs_local)[which(dimnames(coef(mifs_local))$parameter == "D0_init"), ]

}

} else {
  
checktime  <- system.time({
mifs_local <- foreach(j = 1:n.mif_runs, .combine = c) %dopar%  {
    
library(pomp)
library(dplyr)

  covid.fitting %>%
  mif2(
    t0     = 1
  , params = c(
    c(fixed_params
      , Ca       = variable_params[i, ]$Ca
      , lambda_a = variable_params[i, ]$lambda_a
      , lambda_s = variable_params[i, ]$lambda_s
      , lambda_m = variable_params[i, ]$lambda_m  
      )
  , {
    if (fit_to_sip) {
      if (fit.E0) {
    c(beta0              = rlnorm(1, log(0.5), 0.17)
    , alpha              = 0.96
    , mu                 = 0.975
    , delta              = 0.05
    , soc_dist_level_sip = rlnorm(1, log(0.2), 0.2)
    , E_init             = rpois(1, 2))
      } else {
    c(beta0              = rlnorm(1, log(0.5), 0.17)
    , alpha              = 0.96
    , mu                 = 0.975
    , delta              = 0.05
    , soc_dist_level_sip = rlnorm(1, log(0.2), 0.2)
    , E0                 = variable_params[i, ]$E0)        
      }
    } else {
      if (fit.E0) {
    c(beta0              = rlnorm(1, log(0.5), 0.17)
    , alpha              = 0.96
    , mu                 = 0.975
    , delta              = 0.05
    , E_init             = rpois(1, 2))
      } else {
    c(beta0              = rlnorm(1, log(0.5), 0.17)
    , alpha              = 0.96
    , mu                 = 0.975
    , delta              = 0.05
    , E0                 = variable_params[i, ]$E0)        
      }
    }
  }
  )
  , Np     = n.mif_particles
  , Nmif   = n.mif_length
  , cooling.fraction.50 = 0.5
  , rw.sd  = {
    if (fit_to_sip) {
      if (fit.E0) {
    rw.sd(beta0 = n.mif_rw.sd, alpha = n.mif_rw.sd, mu = n.mif_rw.sd, delta = n.mif_rw.sd, soc_dist_level_sip = n.mif_rw.sd, E_init = n.mif_rw.sd)        
      } else {
    rw.sd(beta0 = n.mif_rw.sd, alpha = n.mif_rw.sd, mu = n.mif_rw.sd, delta = n.mif_rw.sd, soc_dist_level_sip = n.mif_rw.sd)        
      }
    } else {
      if (fit.E0) {
    rw.sd(beta0 = n.mif_rw.sd, alpha = n.mif_rw.sd, mu = n.mif_rw.sd, delta = n.mif_rw.sd, E_init = n.mif_rw.sd)        
      } else {
    rw.sd(beta0 = n.mif_rw.sd, alpha = n.mif_rw.sd, mu = n.mif_rw.sd, delta = n.mif_rw.sd)        
      }
    }
  }
        )

}

})  
  
}
  
gg.fit <- mifs_local %>%
  traces() %>%
  melt() %>%
  filter(
    variable == "loglik" | 
    variable == "beta0" | 
    variable == "alpha" |
    variable == "mu" |
    variable == "delta" | 
    variable == "soc_dist_level_sip" |
    variable == "E_init") %>% 
  ggplot(aes(x = iteration, y = value, group = L1, colour = factor(L1)))+
  geom_line() +
  guides(color = FALSE) +
  facet_wrap(~variable, scales = "free_y") +
  theme_bw()

## !! Still not using uncertainty in beta which should be corrected soon
variable_params[i, "beta0est"] <- mean(coef(mifs_local)[which(dimnames(coef(mifs_local))$parameter == "beta0"), ])
param_array[i,,"beta0"]        <- coef(mifs_local)[which(dimnames(coef(mifs_local))$parameter == "beta0"), ] 
variable_params[i, "alphaest"] <- mean(coef(mifs_local)[which(dimnames(coef(mifs_local))$parameter == "alpha"), ])
param_array[i,,"alpha"]        <- coef(mifs_local)[which(dimnames(coef(mifs_local))$parameter == "alpha"), ] 
variable_params[i, "muest"] <- mean(coef(mifs_local)[which(dimnames(coef(mifs_local))$parameter == "mu"), ])
param_array[i,,"mu"]        <- coef(mifs_local)[which(dimnames(coef(mifs_local))$parameter == "mu"), ] 
variable_params[i, "deltaest"] <- mean(coef(mifs_local)[which(dimnames(coef(mifs_local))$parameter == "delta"), ])
param_array[i,,"delta"] 

loglik.out    <- numeric(length(mifs_local))
for (k in seq_along(loglik.out)) {
loglik.out[k] <- mifs_local[[k]]@loglik
}

variable_params[i, "log_lik"]  <- mean(loglik.out)
param_array[i,,"loglik"]       <- loglik.out

}

SEIR.sim <- do.call(
  pomp::simulate
  , list(
    object         = covid.fitting
    , times        = intervention.forecast@times
    , params = {
    if (!more.params.uncer) {
      c(fixed_params, c(
      beta0 = variable_params[i, "beta0est"]
    , alpha = variable_params[i, "alphaest"]
    , mu    = variable_params[i, "muest"]
    , delta = variable_params[i, "deltaest"]
    , soc_dist_level_sip = variable_params[i, "soc_dist_level_sip"]
    , Ca    = variable_params[i, ]$Ca
      )
      , if (fit.E0) { 
          c(E_init = variable_params[i, ]$E_init
          , Ia_init = variable_params[i, ]$Ia_init
          , Ip_init = variable_params[i, ]$Ip_init
          , Is_init = variable_params[i, ]$Is_init
          , Im_init = variable_params[i, ]$Im_init
          , Hr_init = variable_params[i, ]$Hr_init
          , Hd_init = variable_params[i, ]$Hd_init
          , R0_init = variable_params[i, ]$R0_init
          , D0_init = variable_params[i, ]$D0_init)
        } else {
          c(E0     = variable_params[i, ]$E0)     
        }
        )
      } else {
      c(fixed_params, c(
      beta0    = variable_params[i, "beta0est"]
    , alpha = variable_params[i, "alphaest"]
    , mu    = variable_params[i, "muest"]
    , delta = variable_params[i, "deltaest"]
    , soc_dist_level_sip = variable_params[i, "soc_dist_level_sip"]
      , alpha    = variable_params[i, ]$alpha
      , lambda_a = variable_params[i, ]$lambda_a
      , lambda_s = variable_params[i, ]$lambda_s
      , lambda_m = variable_params[i, ]$lambda_m 
      )
      , if (fit.E0) { 
          c(E_init = variable_params[i, ]$E_init)
        } else {
          c(E0     = variable_params[i, ]$E0)     
        }
        ) 
      }}
    , nsim         = nsim
    , format       = "d"
    , include.data = F
    , seed         = 1001)) %>% {
      rbind(.,
         group_by(., day) %>%
           dplyr::select(-.id) %>%
           summarise_all(median) %>%
                    mutate(.id = "median"))
    }

## summarize epidemic
{
SEIR.sim.s  <- SEIR.sim  %>% 
  dplyr::group_by(.id) %>% 
  dplyr::summarize(total_H = sum(H))

SEIR.sim    <- left_join(SEIR.sim, SEIR.sim.s, by = ".id")

SEIR.sim    <- SEIR.sim %>% 
  dplyr::filter(
    total_H > 10
  ) %>% droplevels()

}

}

write.csv(SEIR.sim,file="result.csv",quote=F,row.names = F)
write.csv(variable_params,file="parameter.csv",quote=F,row.names = F) 
