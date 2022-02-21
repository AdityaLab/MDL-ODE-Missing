# MDL-ODE-Missing-Infections

Link to paper: 

## Setup

The code is running on python 3 and R.
Most python packages and R packages used in the code can be installed directly via pip (for python) or install.packages() command (for R). Specially, running the SEIR+HD model code needs the pomp page of R, the detail of this package can be found here: https://kingaa.github.io/pomp/

## Directory structure

```
- Figure2
	- Minneapolis-Nature -> SAPHIRE Model Result for Minneapolis
	- Minneapolis-Mordecai -> SEIR+HD Model Result for Minneapolis
	- Florida-Nature -> SAPHIRE Model Result for South Florida
	- Florida-Mordecai -> SEIR+HD Model Result for South Florida
	- Figure2.py -> Figure 2 in the article
-Figure3
	- Figure3.py -> Figure 3 in the article
-Figure4
	- Figure4.py -> Figure 4 in the article
-Figure5
	- Figure5.py -> Figure 5 in the article
- SI Figure

- Minnesota
	- alpha.py -> Step 1 algorithm code
	- D.py -> Step 2 algorithm code
- South Florida
- Philadelphia
- Washington

```
## Dataset

  The dataset used in this article are: 

### New York Times reported infections
	daily time sequence of reported COVID-19 infections.
	Link: https://github.com/nytimes/covid-19-data
### Serological studies
	Serological studies from CDC and commerical laboratories to estimate the prevalence of antibodies to SARS-CoV-2 in 10 US locations every 3–4 weeks from March to July 2020.
	Link: https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/commercial-lab-surveys.html
### Symptomatic surveillance
	COVID-like symptoms survey by Facebook.
	Link: https://delphi.cmu.edu

## Running the code

### Step 1 Algorithm

Run 'alpha.py' to do a linear search to find a good reported rate.

### Step 2 Algorithm

Given the alpha_reported found in step 1, run 'D.py' to use an optimization method to find the D* that minimizes MDL cost with reported rate constraints.