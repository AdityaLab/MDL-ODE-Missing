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

  ReportedSum = []
  with open('us-counties-source.txt','r') as DataFile:
    Sentence = DataFile.readline()
    for counter in range(37):
      Sentence = DataFile.readline()
      if not Sentence:
        print ("Error!")
      Sentence = Sentence.split(',')
      ReportedSum.append(int(Sentence[5]))

  Reported = [0]*37
  Reported[0] = ReportedSum[0]
  for counter in range(1,37):
    Reported[counter] = ReportedSum[counter] - ReportedSum[counter-1]
  Reported = np.array(Reported)
  
  DataFile = pd.read_csv("result-original.csv")

  DataSelected = DataFile[(DataFile[".id"] == "median")]
  DataSelected = DataSelected["D_new_reported"].tolist()
  ReportedP = DataSelected[1:37]
  ReportedP = np.array(ReportedP)
    
  DataSelected = DataFile[(DataFile[".id"] == "median")]
  DataSelected = DataSelected["D_new_unreported"].tolist()
  UnreportedP = DataSelected[1:37]
  UnreportedP = np.array(UnreportedP)

  DataFile = pd.read_csv("parameter-original.csv")
  DataSelected = DataFile[(DataFile["sim_start"] == "2020-10-01")]
  ParameterP = [DataSelected["beta0est"].to_list()[4], DataSelected["alphaest"].to_list()[4], DataSelected["alpha1est"].to_list()[4], DataSelected["E_init"].to_list()[4]]
  ParameterP = np.array(ParameterP)

  def MDL(D, ParameterP):

    SumD = [0]*37
    SumD[0] = D[0]
    for counter in range(1,37):
      SumD[counter] = SumD[counter-1] + D[counter]
    
    with open('us-counties.txt','w') as WriteFile:
      with open('us-counties-source.txt','r') as ReadFile:
        Sentence = ReadFile.readline()
        Sentence = Sentence[0:len(Sentence)-1] + ',uncases\n'
        WriteFile.write(Sentence)
        for counter in range(37):
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
        DataSelected = DataSelected["D_new_reported"].tolist()
        ReportedPP = DataSelected[1:37]
        ReportedPP = np.array(ReportedPP)
        
        DataSelected = DataFile[(DataFile[".id"] == "median")]
        DataSelected = DataSelected["D_new_unreported"].tolist()
        UnreportedPP = DataSelected[1:37]
        UnreportedPP = np.array(UnreportedPP)

        DataSelected = DataFile[(DataFile[".id"] == "median")]
        DataSelected = DataSelected["dIpIs_save"].tolist()
        dIpIs = DataSelected[1:37]
        dIpIs = np.array(dIpIs)

        DataSelected = DataFile[(DataFile[".id"] == "median")]
        DataSelected = DataSelected["dIpIm_save"].tolist()
        dIpIm = DataSelected[1:37]
        dIpIm = np.array(dIpIm)

        DataSelected = DataFile[(DataFile[".id"] == "median")]
        DataSelected = DataSelected["dEIa_save"].tolist()
        dEIa = DataSelected[1:37]
        dEIa = np.array(dEIa)
      
        DataFile = pd.read_csv("parameter.csv")
        DataSelected = DataFile[(DataFile["sim_start"] == "2020-10-01")]
        ParameterPP = [DataSelected["beta0est"].to_list()[4], DataSelected["alphaest"].to_list()[4], DataSelected["alpha1est"].to_list()[4], DataSelected["E_init"].to_list()[4]]
        ParameterPP = np.array(ParameterPP)

        ReportRate = (ParameterPP[2]*(np.sum(dIpIs)+np.sum(dIpIm)))/(np.sum(dIpIs)+np.sum(dIpIm)+np.sum(dEIa))

        ModelCost1 = VectorCost(ParameterP)
        ModelCost2 = VectorCost(ParameterPP - ParameterP)
        ModelCost3 = TimeSeriesCost(ReportRate*D - ReportedP)
        DataCost = TimeSeriesCost(((D-Reported)/(1.0-ReportRate))-(ReportedPP+UnreportedPP))
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
    
    SumD = [0]*37
    SumD[0] = D[0]
    for counter in range(1,37):
      SumD[counter] = SumD[counter-1] + D[counter]
    
    with open('us-counties.txt','w') as WriteFile:
      with open('us-counties-source.txt','r') as ReadFile:
        Sentence = ReadFile.readline()
        Sentence = Sentence[0:len(Sentence)-1] + ',uncases\n'
        WriteFile.write(Sentence)
        for counter in range(37):
          Sentence = ReadFile.readline()
          if not Sentence:
            print ("Error!")
          Sentence = Sentence[0:len(Sentence)-1] + ',' + str(int(SumD[counter]-ReportedSum[counter])) + '\n'
          WriteFile.write(Sentence)
          
    while(True):
      try:
        subprocess.check_call("Rscript COVID_fit_warm.R")

        with open('result/result-'+str(alpha)+'.csv','w') as WriteFile:
          with open('result.csv','r') as ReadFile:
            while (True):
              Sentence = ReadFile.readline()
              if not Sentence:
                break
              else:
                WriteFile.write(Sentence)

        with open('parameter/parameter-'+str(alpha)+'.csv','w') as WriteFile:
          with open('parameter.csv','r') as ReadFile:
            while (True):
              Sentence = ReadFile.readline()
              if not Sentence:
                break
              else:
                WriteFile.write(Sentence)

        DataFile = pd.read_csv("result.csv")
        
        DataSelected = DataFile[(DataFile[".id"] == "median")]
        DataSelected = DataSelected["D_new_reported"].tolist()
        ReportedPP = DataSelected[1:37]
        ReportedPP = np.array(ReportedPP)
        
        DataSelected = DataFile[(DataFile[".id"] == "median")]
        DataSelected = DataSelected["D_new_unreported"].tolist()
        UnreportedPP = DataSelected[1:37]
        UnreportedPP = np.array(UnreportedPP)

        DataSelected = DataFile[(DataFile[".id"] == "median")]
        DataSelected = DataSelected["dIpIs_save"].tolist()
        dIpIs = DataSelected[1:37]
        dIpIs = np.array(dIpIs)

        DataSelected = DataFile[(DataFile[".id"] == "median")]
        DataSelected = DataSelected["dIpIm_save"].tolist()
        dIpIm = DataSelected[1:37]
        dIpIm = np.array(dIpIm)

        DataSelected = DataFile[(DataFile[".id"] == "median")]
        DataSelected = DataSelected["dEIa_save"].tolist()
        dEIa = DataSelected[1:37]
        dEIa = np.array(dEIa)
      
        DataFile = pd.read_csv("parameter.csv")
        DataSelected = DataFile[(DataFile["sim_start"] == "2020-10-01")]
        ParameterPP = [DataSelected["beta0est"].to_list()[4], DataSelected["alphaest"].to_list()[4], DataSelected["alpha1est"].to_list()[4], DataSelected["E_init"].to_list()[4]]
        ParameterPP = np.array(ParameterPP)

        ReportRate = (ParameterPP[2]*(np.sum(dIpIs)+np.sum(dIpIm)))/(np.sum(dIpIs)+np.sum(dIpIm)+np.sum(dEIa))

        ModelCost1 = VectorCost(ParameterP)
        ModelCost2 = VectorCost(ParameterPP - ParameterP)
        ModelCost3 = TimeSeriesCost(ReportRate*(ReportedPP+UnreportedPP) - ReportedP)
        DataCost = TimeSeriesCost((((ReportedPP+UnreportedPP)-Reported[1:37])/(1.0-ReportRate))-(ReportedPP+UnreportedPP))
        MDLCost = ModelCost1 + ModelCost2 + ModelCost3 + DataCost
        break
      except:
        pass

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
  MDL_alpha(0.20, ParameterP)