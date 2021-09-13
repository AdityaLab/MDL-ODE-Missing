# MDL-Missing-Infections

Link to paper: 

## Setup

The code is running on python 3 and R.
Most python packages and R packages used in the code can be installed directly via pip (for python) or install.packages() command (for R). Specially, running the ODE model code needs the pomp page of R, the detail of this package can be found here: https://kingaa.github.io/pomp/

## Directory structure

```
-Testbed-On-Mordecai-Model
	- Santa Clara, CA -> testbed for Santa Clara, CA
   		- result -> Saved ODE output for step 1 result
  		- parameter -> Saved ODE parameter for step 1 result
    		- alpha.py -> Step 1 algorithm code
    		- D.py -> Step 2 algorithm code
```
## Dataset

  The dataset is 'us-counties-source.txt'. It contains csv file for the county that contains daily time sequence of reported infections Dreported and the mortality Dmortality (cumulative values) for the testbed starting from January 21, 2020.

## Running the code

### Step 1 Algorithm

Run 'alpha.py' to do a linear search to find a good reported alpha_reported.

### Step 2 Algorithm

Given the alpha_reported found in step 1, run 'D.py' to use an optimization method to find the D* that minimizes L(Dreported,D,p’,p) with alpha_reported constraints.


