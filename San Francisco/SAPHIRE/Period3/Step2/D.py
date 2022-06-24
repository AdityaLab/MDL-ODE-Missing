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

  Reported = np.array(Reported[:41])

  ReportedP = []
  UnreportedP = []
  
  with open('output/result-original.csv','r') as CSVFile:
    DataFile = csv.reader(CSVFile)
    next(DataFile)
    for Sentence in DataFile:
      _,_,_,_,_,_,_,_,case,uncase = Sentence
      ReportedP.append(int(case))
      UnreportedP.append(int(uncase))

  ReportedP = np.array(ReportedP[:40])
  UnreportedP = np.array(UnreportedP[:40])

  ParameterP = [np.sum(ReportedP)/(np.sum(ReportedP)+np.sum(UnreportedP))]
  ParameterP = np.array(ParameterP)

  def MDL(D, ParameterP, warm=False):

    with open ('data/Covid19CasesWH.csv','w') as CSVFileW:
      SolutionFile = csv.writer(CSVFileW)
      with open ('data/data.csv','r') as CSVFileR:
        DataFile = csv.reader(CSVFileR)
        Sentence = next(DataFile)
        SolutionFile.writerow(['OnsetDate','CaseNum','CaseSum','UncaseNum','UncaseSum'])
        for counter in range(41):
          Sentence = next(DataFile)
          X,date,county,state,fips,cases,deaths = Sentence
          SolutionFile.writerow([date,str(Reported[counter]),str(int(np.sum(Reported[:1+counter]))),str(int(D[counter])-int(Reported[counter])),str(int(np.sum(D[:1+counter]))-int(np.sum(Reported[:1+counter])))]) 
    
    if(True):
      if(True):
        os.system("Rscript scripts_main/Run_SEIR_main_analysis.R")

        ReportedPP = []
        UnreportedPP = []

        with open('output/result.csv','r') as CSVFile:
          DataFile = csv.reader(CSVFile)
          next(DataFile)
          for Sentence in DataFile:
            _,_,_,_,_,_,_,_,case,uncase = Sentence
            ReportedPP.append(int(case))
            UnreportedPP.append(int(uncase))

        ReportedPP = np.array(ReportedPP[:40])
        UnreportedPP = np.array(UnreportedPP[:40])
      
        ParameterPP = [np.sum(ReportedPP)/(np.sum(ReportedPP)+np.sum(UnreportedPP))]
        ParameterPP = np.array(ParameterPP)

        ReportRate = ParameterPP[0]
        
        ModelCost1 = VectorCost(ParameterP)
        ModelCost2 = VectorCost(ParameterPP - ParameterP)
        ModelCost3 = TimeSeriesCost(ReportRate*D[1:41] - ReportedP)
        DataCost = TimeSeriesCost(((D[1:41]-Reported[1:41])/(1.0-ReportRate))-(ReportedPP+UnreportedPP))
        MDLCost = ModelCost1 + ModelCost2 + ModelCost3 + DataCost
      #  break
      #except:
      #  pass

    with open('D.txt','a+') as WriteFile:
      WriteFile.write(str(list(D)))
      WriteFile.write('\t')
      WriteFile.write(str(MDLCost))
      WriteFile.write('\n')

    return MDLCost

  def MDL_step2(D,D_start,ParameterP):
      D_scaled = fix_magnitude(D,D_start)
      cost =  MDL(D_scaled,ParameterP,True)
      return cost
  
  def fix_magnitude(D,D_start):
      D = np.array(D)
      scale_factor = np.sum(D_start) / (np.sum(D)) 
      D = D * scale_factor
      return D
    
  def wavelet_fit(dim,cat,cdt,w,alpha_hat,D_reported):
      cat = np.concatenate((np.zeros((dim- cat.shape[0])),cat))
      fit = pywt.idwt(cat, cdt, w)[1:]
      return fix_magnitude(fit,alpha_hat,D_reported)   
    
  def MDL_wavelet(cat,cdt,dim,w,Parameter_P,alpha_hat,D_reported):
        fit =  wavelet_fit(dim,cat,cdt,w,alpha_hat,D_reported)
        cost =  MDL(fit,Parameter_P)
        f= open("optimization_log.txt", "a+")
        f.write("%d\r\n" % (cost))
        fit_write = [f for f in fit]
        f.write(str(fit_write))
        f.write("\n")
        f.close()
        return cost
  
  alpha_star = 0.16
  D_start = np.copy(Reported) / alpha_star

  MDL(D_start,ParameterP,True)
 
  res = minimize(fun=MDL_step2, x0=D_start, args=(D_start,ParameterP), method='nelder-mead', options={'maxiter':10, 'xatol':2500, 'fatol':100})
  
  D_star = res.x

  with open('D_star.txt','a+') as WriteFile:
    WriteFile.write(str(list(D_star)))
    WriteFile.write('\n')