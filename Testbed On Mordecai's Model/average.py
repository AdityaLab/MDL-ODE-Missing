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

  def MDL_alpha(alpha):
    
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

    Counter = 0
    AlphaList = []
    RMSEList = []

    while (Counter < 20):
      while(True):
        try:
          subprocess.check_call("Rscript COVID_fit.R")

          DataFile = pd.read_csv("result.csv")
          
          DataSelected = DataFile[(DataFile[".id"] == "median")]
          DataSelected = DataSelected["I_new_sympt"].tolist()
          ReportedPP = DataSelected[7:60]
          ReportedPP = np.array(ReportedPP)
        
          DataFile = pd.read_csv("parameter.csv")
          DataSelected = DataFile[(DataFile["sim_start"] == "2020-01-25")]
          ParameterPP = [DataSelected["beta0est"].to_list()[0], DataSelected["alphaest"].to_list()[0], DataSelected["muest"].to_list()[0], DataSelected["deltaest"].to_list()[0]]
          ParameterPP = np.array(ParameterPP)

          ParameterPP[1] = 1.0 - ParameterPP[1]

          AlphaList.append(ParameterPP[1])
          RMSEList.append(np.linalg.norm(ReportedPP-Reported))
          Counter = Counter + 1

          with open('result/result-'+str(alpha)+'-'+str(Counter)+'.csv','w') as WriteFile:
            with open('result.csv','r') as ReadFile:
              while (True):
                Sentence = ReadFile.readline()
                if not Sentence:
                  break
                else:
                  WriteFile.write(Sentence)

          with open('parameter/parameter-'+str(alpha)+'-'+str(Counter)+'.csv','w') as WriteFile:
            with open('parameter.csv','r') as ReadFile:
              while (True):
                Sentence = ReadFile.readline()
                if not Sentence:
                  break
                else:
                  WriteFile.write(Sentence)

          break
        except:
          pass

    with open('average.txt','a+') as WriteFile:
      WriteFile.write(str(alpha))
      WriteFile.write(',')
      WriteFile.write(str(np.mean(AlphaList)))
      WriteFile.write(',')
      WriteFile.write(str(np.mean(RMSEList)))
      WriteFile.write('\n')

    return 0

  MDL_alpha(0.002)
  MDL_alpha(0.004)
  MDL_alpha(0.006)
  MDL_alpha(0.008)
  MDL_alpha(0.01)
  MDL_alpha(0.02)
  MDL_alpha(0.03)
  MDL_alpha(0.04)
  MDL_alpha(0.05)
  MDL_alpha(0.06)
  MDL_alpha(0.07)
  MDL_alpha(0.08)
  MDL_alpha(0.09)
  MDL_alpha(0.10)
  MDL_alpha(0.15)
  MDL_alpha(0.20)
  MDL_alpha(0.25)
  MDL_alpha(0.30)
  MDL_alpha(0.35)
  MDL_alpha(0.40)
  MDL_alpha(0.45)
  MDL_alpha(0.50)