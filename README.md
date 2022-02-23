# MDLINFER: Information Theoretic Model Selection for Accurately Estimating Unreported COVID-19 Infections



Link to paper: https://www.medrxiv.org/content/10.1101/2021.09.14.21263467v2

To use this code, please cite the paper:
```
Jiaming Cui, Arash Haddadan, A S M Ahsan-Ul Haque, Bijaya Adhikari, Anil Vullikanti, and B. Aditya Prakash. "Information Theoretic Model Selection for Accurately Estimating Unreported COVID-19 Infections." medRxiv (2021): 2021-09.
```

This code showcases that the optimal parameterization identified by our MDL framework MDLINFER is superior to baseline parameterization in (A) estimating total infections, (B) future projections on reported infections, and (C) predicting COVID-19 symptomatic rate trends. 

We replicate our methods on multiple epidemiological models (SAPHIRE model and SEIR+HD model), multiple locations (South Florida and Minneapolis), and multiple periods (spring to summer 2020, and fall 2020). To account for the stochasticity in the calibration and simulation, we run the SAPHIRE model with 10000 MCMC runs and report the average. For SEIR+HD model, we run with 1200 particles and 200 simulations and report the average. In the experiments for each region, we divide the timeline into two time periods: (i) observed period, when only the number of reported infections are available, and the models are calibrated to learn the parameterizations, and (ii) future period, where we evaluate the forecasts generated by the epidemiological models and calibrated parameterizations learned in the observed period. Hence, for the experiments to estimate the total infections, our methods were performed without access to the serological studies. Similarly for the experiments to estimate the future reported infections and symptomatic rate trends, our methods were performed without access to the future reported infections and symptomatic rate surveillance data.

This code showcases MDLINFER using two different ODE-based epidemiological models: SAPHIRE model (Hao, X. et al. Reconstruction of the full transmission dynamics of covid-19 in wuhan. Nature 584, 420–424 (2020). Github link: https://github.com/chaolongwang/SAPHIRE) and SEIR+HD model (Kain, M. P., Childs, M. L., Becker, A. D. & Mordecai, E. A. Chopping the tail: How preventing superspreading can help to maintain covid-19 control. Epidemics 34, 100430 (2021). GitHub link: https://github.com/morgankain/COVID_interventions).

## Setup

The code is running on Python 3.8.6 and R 4.0.3.
We are using the following packages in the code. These packages can be installed via pip (for Python) or install.packages() command (for R). The installation of these packages will cost around 1 hour.

```
Python:
numpy
scipy
matplotlib
pandas

R:
BayesianTools
vioplot
corrplot
readr
cairoDevice
pomp
plyr
dplyr
ggplot2
magrittr
scales
lubridate
tidyr
foreach
doParallel
data.table
```

## Directory structure

```
- Figure2 -> This folder allows you to reproduce the Figure 2 in the main article.
	- Minneapolis-Nature -> Saved SAPHIRE Model Results for Minneapolis.
	- Minneapolis-Mordecai -> Saved SEIR+HD Model Results for Minneapolis.
	- Florida-Nature -> Saved SAPHIRE Model Results for South Florida.
	- Florida-Mordecai -> Saved SEIR+HD Model Results for South Florida.
	- Figure2.py -> Running this code directly will reproduce the Figure 2.
```
```
-Figure3 -> This folder allows you to reproduce the Figure 3 in the main article.
	- Figure3.py -> Running this code directly will reproduce the Figure 3.
```
```
-Figure4 -> This folder allows you to reproduce the Figure 4 in the main article.
	- Figure4.py -> Running this code directly will reproduce the Figure 4.
```
```
-Figure5 -> This folder allows you to reproduce the Figure 5 in the main article.
	- Figure5.py  -> Running this code directly will reproduce the Figure 5.
```
```
- Minnesota
	- SAPHIRE
		- Period1
			-Step 1
				-alpha.py -> Step 1 algorithm code
			-Step 2
				-D.py -> Step 2 algorithm code
		- Period2
		- ...
	- SEIR+HD
- South Florida
	- ...
```

```
- Demo -> The demo code
- Pseudocode.pdf -> The pseudo code for our algorithm (Step 1 and Step 2)
```
## Dataset

  The dataset used in this article are: 

### New York Times reported infections

This dataset consists of the daily time sequence of reported COVID-19 infections and the mortality (cumulative values) for each county in the US starting from January 21, 2020 to current. As of Feb 21, 2022, the number of reported infections is 78434184 and the mortality is 934659. More details can be found in: https://github.com/nytimes/covid-19-data.
	
### Serological studies
	
This dataset consists of the point and 95% confidence interval estimates of the prevalence of antibodies to SARS-CoV-2 in 10 US locations every 3–4 weeks from March to July 2020. For each location, CDC works with commercial laboratories to collect blood specimens in the population and test about 1800 collected specimens every 3–4 weeks. More details can be found in: https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/commercial-lab-surveys.html.
	
### Symptomatic surveillance

This dataset consists of the point estimate (and standard error) of the COVID-related symptomatic rate for each county in the US starting from April 6, 2020 to date. The survey asks a series of questions on randomly sampled social media (Facebook) users to estimate the percentage of people who have a COVID-like symptoms such as the fever along with cough or shortness of breath or difficulty breathing on a given day. As of November 2021, the average number of Facebook survey responses each day is about 40,000, and overall it consists over 25 million survey responses. More details can be found in: https://cmu-delphi.github.io/delphi-epidata/api/covidcast-signals/fb-survey.html.
	
We integrate the datasets into each testbed, hence the datasets are in each folder.

## Running the MDLINFER code

### Step 1 of the MDLINFER: Finding the reported rate alpha*

The step 1 of the MDLINFER is to find a good reported rate alpha*. You can run the step 1 algorithm in the step1 folder. The steps are as follow: 

(1) For SAPHIRE model, please set the code_root in scripts_main/Run_SEIR_main_analysis.R as the step1 folder.  
(2) Run 'alpha.py' to do a linear search to find a good reported rate alpha*.  
(3) You can find the reported rate alpha* saved in the alpha.txt.

### Step 2 of the MDLINFER: Finding the total infections D*

The step 2 of the MDLINFER is to find the total infections D*. You can run the step 2 algorithm in the step2 folder. The steps are as follow: 

(1) For SAPHIRE model, please similarly set the code_root in scripts_main/Run_SEIR_main_analysis.R as the step2 folder.  
(2) Copy the result.csv corresponding to the alpha* and paste to step 2 folder as a warm start.  
(3) Set the alpha_star as the alpha* found in step 1 in getting_D.py.  
(4) Run 'D.py' to use the Nelder-Mead to find the D* that minimizes MDL cost with reported rate constraints.    
(5) You can find the total infections D* saved in D_star.txt.

### Demo Code of the MDLINFER

We also provide a demo code to run the MDLINFER. The steps are as follow: 

(1) Please set the code_root in scripts_main/Run_SEIR_main_analysis.R as the step1 folder and step2 folder path.  
(2) Run the MDLINFER.sh to run the code.  
(3) You can find the total infections D* saved in D_star.txt.

This demo code is for South Florida from May 28, 2020 to June 28, 2020 on SAPHIRE model. Here, we save the step 1 calibration results of attempting different reported rate alpha. The demo code usually take 1-2 hours to run.
