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
  if (math.floor(abs(x)) == 0):
    return 1-math.log(delta,2) 
  else:
    return IntegerCost(math.floor(abs(x)))-math.log(delta,2)+1 

def VectorCost(x):
  Sum = 0
  for xnow in x:
    Sum = Sum + RealNumberCost(xnow)
  return Sum

def TimeSeriesCost(x):
  Sum = 0
  Length = x.shape[0]
  x_grad = np.around(np.gradient(x))
  T, Tcount = np.unique(x_grad, return_counts = True)
  XDictionary = {}
  for counter in range(len(T)):
    XDictionary[int(T[counter])] = int(Tcount[counter]) 
  for keys in XDictionary.keys():
    Sum = Sum + 1.0*XDictionary[keys]/Length*math.log(1.0*Length/XDictionary[keys],2)
  Sum = Length * Sum
  for keys in XDictionary.keys():
    Sum = Sum + IntegerCost(int(keys))
  return Sum

if __name__ == "__main__":

  ReportedSum = []
  with open('us-counties-source.txt','r') as DataFile:
    Sentence = DataFile.readline()
    for counter in range(53):
      Sentence = DataFile.readline()
      if not Sentence:
        print ("Error!")
      Sentence = Sentence.split(',')
      ReportedSum.append(int(Sentence[5]))

  Reported = [0]*53
  Reported[0] = ReportedSum[0]
  for counter in range(1,53):
    Reported[counter] = ReportedSum[counter] - ReportedSum[counter-1]
  Reported = np.array(Reported)
  
  DataFile = pd.read_csv("result-original.csv")

  DataSelected = DataFile[(DataFile[".id"] == "median")]
  DataSelected = DataSelected["I_new_sympt"].tolist()
  ReportedP = DataSelected[7:60]
  ReportedP = np.array(ReportedP)
    
  DataSelected = DataFile[(DataFile[".id"] == "median")]
  DataSelected = DataSelected["I_new_asympt"].tolist()
  UnreportedP = DataSelected[7:60]
  UnreportedP = np.array(UnreportedP)

  DataFile = pd.read_csv("parameter-original.csv")
  ParameterP = [np.mean(DataFile["beta0est"].to_list()), np.mean(DataFile["alphaest"].to_list()), np.mean(DataFile["muest"].to_list()), np.mean(DataFile["deltaest"].to_list())]
  ParameterP = np.array(ParameterP)

  def MDL(D, ParameterP):

    SumD = [0]*53
    SumD[0] = D[0]
    for counter in range(1,53):
      SumD[counter] = SumD[counter-1] + D[counter]
    
    with open('us-counties.txt','w') as WriteFile:
      with open('us-counties-source.txt','r') as ReadFile:
        Sentence = ReadFile.readline()
        Sentence = Sentence[0:len(Sentence)-1] + ',uncases\n'
        WriteFile.write(Sentence)
        for counter in range(53):
          Sentence = ReadFile.readline()
          if not Sentence:
            print ("Error!")
          Sentence = Sentence[0:len(Sentence)-1] + ',' + str(int(SumD[counter]-ReportedSum[counter])) + '\n'
          WriteFile.write(Sentence)
          
    while(True):
      try:
        subprocess.check_call("Rscript COVID_fit.R")

        DataFile = pd.read_csv("result.csv")
        
        DataSelected = DataFile[(DataFile[".id"] == "median")]
        DataSelected = DataSelected["I_new_sympt"].tolist()
        ReportedPP = DataSelected[7:60]
        ReportedPP = np.array(ReportedPP)
        
        DataSelected = DataFile[(DataFile[".id"] == "median")]
        DataSelected = DataSelected["I_new_asympt"].tolist()
        UnreportedPP = DataSelected[7:60]
        UnreportedPP = np.array(UnreportedPP)
      
        DataFile = pd.read_csv("parameter.csv")
        ParameterPP = [np.mean(DataFile["beta0est"].to_list()), np.mean(DataFile["alphaest"].to_list()), np.mean(DataFile["muest"].to_list()), np.mean(DataFile["deltaest"].to_list())]
        ParameterPP = np.array(ParameterPP)

        ParameterPP[1] = 1.0 - ParameterPP[1]

        ModelCost1 = VectorCost(ParameterP)
        ModelCost2 = VectorCost(ParameterPP - ParameterP)
        ModelCost3 = TimeSeriesCost(ParameterPP[1]*D - ReportedP)
        DataCost = TimeSeriesCost(((D-Reported)/(1.0-ParameterPP[1]))-(ReportedPP+UnreportedPP))
        MDLCost = ModelCost1 + ModelCost2 + ModelCost3 + DataCost

        break
      except:
        pass

    with open('D.txt','a+') as WriteFile:
      WriteFile.write(str(list(D)))
      WriteFile.write('\t')
      WriteFile.write(str(MDLCost))
      WriteFile.write('\n')

    return MDLCost

  def MDL_alpha(alpha, ParameterP):
    
    D = Reported / alpha
    
    SumD = [0]*53
    SumD[0] = D[0]
    for counter in range(1,53):
      SumD[counter] = SumD[counter-1] + D[counter]
    
    with open('us-counties.txt','w') as WriteFile:
      with open('us-counties-source.txt','r') as ReadFile:
        Sentence = ReadFile.readline()
        Sentence = Sentence[0:len(Sentence)-1] + ',uncases\n'
        WriteFile.write(Sentence)
        for counter in range(53):
          Sentence = ReadFile.readline()
          if not Sentence:
            print ("Error!")
          Sentence = Sentence[0:len(Sentence)-1] + ',' + str(int(SumD[counter]-ReportedSum[counter])) + '\n'
          WriteFile.write(Sentence)
          
    while(True):
      try:
        subprocess.check_call("Rscript COVID_fit.R")

        DataFile = pd.read_csv("result.csv")
        
        DataSelected = DataFile[(DataFile[".id"] == "median")]
        DataSelected = DataSelected["I_new_sympt"].tolist()
        ReportedPP = DataSelected[7:60]
        ReportedPP = np.array(ReportedPP)
        
        DataSelected = DataFile[(DataFile[".id"] == "median")]
        DataSelected = DataSelected["I_new_asympt"].tolist()
        UnreportedPP = DataSelected[7:60]
        UnreportedPP = np.array(UnreportedPP)
      
        DataFile = pd.read_csv("parameter.csv")
        ParameterPP = [np.mean(DataFile["beta0est"].to_list()), np.mean(DataFile["alphaest"].to_list()), np.mean(DataFile["muest"].to_list()), np.mean(DataFile["deltaest"].to_list())]
        ParameterPP = np.array(ParameterPP)

        ParameterPP[1] = 1.0 - ParameterPP[1]

        ModelCost1 = VectorCost(ParameterP)
        ModelCost2 = VectorCost(ParameterPP - ParameterP)
        ModelCost3 = TimeSeriesCost(ParameterPP[1]*D - ReportedP)
        DataCost = TimeSeriesCost(((D-Reported)/(1.0-ParameterPP[1]))-(ReportedPP+UnreportedPP))
        MDLCost = ModelCost1 + ModelCost2 + ModelCost3 + DataCost

        break
      except:
        pass

    with open('alpha.txt','a+') as WriteFile:
      WriteFile.write(str(alpha))
      WriteFile.write(',')
      WriteFile.write(str(ParameterPP[1]))
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

  MDL_alpha(0.002, ParameterP)
  MDL_alpha(0.004, ParameterP)
  MDL_alpha(0.006, ParameterP)
  MDL_alpha(0.008, ParameterP)
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
  MDL_alpha(0.15, ParameterP)
  MDL_alpha(0.20, ParameterP)
  MDL_alpha(0.25, ParameterP)
  MDL_alpha(0.30, ParameterP)
  MDL_alpha(0.35, ParameterP)
  MDL_alpha(0.40, ParameterP)
  MDL_alpha(0.45, ParameterP)
  MDL_alpha(0.50, ParameterP)