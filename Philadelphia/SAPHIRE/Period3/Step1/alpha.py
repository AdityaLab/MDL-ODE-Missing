from scipy import integrate, optimize
from scipy.optimize import minimize
from scipy.optimize import basinhopping
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random
import math
import csv
import subprocess
import os

def IntegerCost(x):
  Sum = math.log(2.865,2)+1
  if (abs(x) > 1.01):
    add = math.log(abs(x),2)
    while (add > 1.01):
      Sum = Sum + add
      add = math.log(add,2)
  return Sum

def RealNumberCost(x):
  delta = 0.1
  return IntegerCost(math.floor(abs(x)))-math.log(delta,2)+1 

def VectorCost(x):
  Sum = 0
  for xnow in x:
    Sum = Sum + RealNumberCost(xnow)
  return Sum

def TimeSeriesCost(x):
  Sum = 0
  for xnow in x:
    Sum = Sum + RealNumberCost(xnow)
  return Sum

if __name__ == "__main__":

  Reported = []
  with open ('data/data.csv','r') as CSVFileR:
    DataFile = csv.reader(CSVFileR)
    Sentence = next(DataFile)
    casesyesterday = 0
    for Sentence in DataFile:
      X,date,county,state,fips,cases,deaths = Sentence
      Reported.append(int(cases)-int(casesyesterday))
      casesyesterday = cases
      
  Reported = np.array(Reported[:11])

  ReportedP = []
  UnreportedP = []

  with open('output/result-original.csv','r') as CSVFile:
    DataFile = csv.reader(CSVFile)
    next(DataFile)
    for Sentence in DataFile:
      _,_,_,_,_,_,_,_,case,uncase = Sentence
      ReportedP.append(int(case))
      UnreportedP.append(int(uncase))

  ReportedP = np.array(ReportedP[:10])
  UnreportedP = np.array(UnreportedP[:10])

  ParameterP = [np.sum(ReportedP)/(np.sum(ReportedP)+np.sum(UnreportedP))]
  ParameterP = np.array(ParameterP)

  def MDL_alpha(alpha, ParameterP):
    
    D = Reported / alpha
    
    with open ('data/Covid19CasesWH.csv','w') as CSVFileW:
      SolutionFile = csv.writer(CSVFileW)
      with open ('data/data.csv','r') as CSVFileR:
        DataFile = csv.reader(CSVFileR)
        Sentence = next(DataFile)
        SolutionFile.writerow(['OnsetDate','CaseNum','CaseSum','UncaseNum','UncaseSum'])
        for counter in range(11):
          Sentence = next(DataFile)
          X,date,county,state,fips,cases,deaths = Sentence
          SolutionFile.writerow([date,str(Reported[counter]),str(int(np.sum(Reported[:1+counter]))),str(int(D[counter])-int(Reported[counter])),str(int(np.sum(D[:1+counter]))-int(np.sum(Reported[:1+counter])))]) 

    if(True):
      if(True):
        os.system("Rscript scripts_main/Run_SEIR_main_analysis.R")

        with open('output/result/result-'+str(alpha)+'.csv','w') as WriteFile:
          with open('output/result.csv','r') as ReadFile:
            while (True):
              Sentence = ReadFile.readline()
              if not Sentence:
                break
              else:
                WriteFile.write(Sentence)

        ReportedPP = []
        UnreportedPP = []

        with open('output/result.csv','r') as CSVFile:
          DataFile = csv.reader(CSVFile)
          next(DataFile)
          for Sentence in DataFile:
            _,_,_,_,_,_,_,_,case,uncase = Sentence
            ReportedPP.append(int(case))
            UnreportedPP.append(int(uncase))

        ReportedPP = np.array(ReportedPP[:10])
        UnreportedPP = np.array(UnreportedPP[:10])
      
        ParameterPP = [np.sum(ReportedPP)/(np.sum(ReportedPP)+np.sum(UnreportedPP))]
        ParameterPP = np.array(ParameterPP)

        ReportRate = ParameterPP[0]
        
        ModelCost1 = VectorCost(ParameterP)
        ModelCost2 = VectorCost(ParameterPP - ParameterP)
        ModelCost3 = TimeSeriesCost(ReportRate*(ReportedPP+UnreportedPP) - ReportedP)
        DataCost = TimeSeriesCost((((ReportedPP+UnreportedPP)-Reported[1:11])/(1.0-ReportRate))-(ReportedPP+UnreportedPP))
        MDLCost = ModelCost1 + ModelCost2 + ModelCost3 + DataCost
      #  break
      #except:
      #  pass

    with open('alpha.txt','a+') as WriteFile:
      WriteFile.write(str(alpha))
      WriteFile.write(',')
      WriteFile.write(str(ReportRate))
      WriteFile.write(',')
      WriteFile.write(str(ModelCost1))
      WriteFile.write(',')
      WriteFile.write(str(ModelCost2))
      WriteFile.write(',')
      WriteFile.write(str(ModelCost3))
      WriteFile.write(',')
      WriteFile.write(str(DataCost))
      WriteFile.write(',')
      WriteFile.write(str(MDLCost))
      WriteFile.write('\n')

    return MDLCost

  MDL_alpha(0.01, ParameterP)
  MDL_alpha(0.02, ParameterP)
  MDL_alpha(0.03, ParameterP)
  MDL_alpha(0.04, ParameterP)
  MDL_alpha(0.05, ParameterP)
  MDL_alpha(0.06, ParameterP)
  MDL_alpha(0.07, ParameterP)
  MDL_alpha(0.08, ParameterP)
  MDL_alpha(0.09, ParameterP)
  MDL_alpha(0.10, ParameterP)
  MDL_alpha(0.11, ParameterP)
  MDL_alpha(0.12, ParameterP)
  MDL_alpha(0.13, ParameterP)
  MDL_alpha(0.14, ParameterP)
  MDL_alpha(0.15, ParameterP)
  MDL_alpha(0.16, ParameterP)
  MDL_alpha(0.17, ParameterP)
  MDL_alpha(0.18, ParameterP)
  MDL_alpha(0.19, ParameterP)
  MDL_alpha(0.20, ParameterP)
  MDL_alpha(0.21, ParameterP)
  MDL_alpha(0.22, ParameterP)
  MDL_alpha(0.23, ParameterP)
  MDL_alpha(0.24, ParameterP)
  MDL_alpha(0.25, ParameterP)
  MDL_alpha(0.30, ParameterP)
  MDL_alpha(0.35, ParameterP)
  MDL_alpha(0.40, ParameterP)
  MDL_alpha(0.50, ParameterP)