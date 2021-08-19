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
import time

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
    for counter in range(96):
      Sentence = DataFile.readline()
      if not Sentence:
        print ("Error!")
      Sentence = Sentence.split(',')
      ReportedSum.append(int(Sentence[5]))

  Reported = [0]*96
  Reported[0] = ReportedSum[0]
  for counter in range(1,96):
    Reported[counter] = ReportedSum[counter] - ReportedSum[counter-1]
  Reported = np.array(Reported)
  
  DataFile = pd.read_csv("result-original.csv")

  DataSelected = DataFile[(DataFile[".id"] == "median")]
  DataSelected = DataSelected["I_new_sympt"].tolist()
  ReportedP = DataSelected[0:96]
  ReportedP = np.array(ReportedP)
    
  DataSelected = DataFile[(DataFile[".id"] == "median")]
  DataSelected = DataSelected["I_new_asympt"].tolist()
  UnreportedP = DataSelected[0:96]
  UnreportedP = np.array(UnreportedP)

  DataFile = pd.read_csv("parameter-original.csv")
  DataSelected = DataFile[(DataFile["sim_start"] == "2020-01-26")]
  ParameterP = [DataSelected["beta0est"].to_list()[0], DataSelected["alphaest"].to_list()[0], DataSelected["muest"].to_list()[0], DataSelected["deltaest"].to_list()[0]]
  ParameterP = np.array(ParameterP)

  
  def MDL(D, ParameterP,warm=False):
        
    if warm:
      to_run = 'COVID_fit_read'
    else:
      to_run = 'COVID_fit'

    SumD = [0]*96
    SumD[0] = D[0]
    for counter in range(1,96):
      SumD[counter] = SumD[counter-1] + D[counter]
    print("Reading...",end=": ")
    sys.stdout.flush() 
    with open('us-counties.txt','w') as WriteFile:
      with open('us-counties-source.txt','r') as ReadFile:
        Sentence = ReadFile.readline()
        Sentence = Sentence[0:len(Sentence)-1] + ',uncases\n'
        WriteFile.write(Sentence)
        for counter in range(96):
          Sentence = ReadFile.readline()
          if not Sentence:
            print ("Error!")
          Sentence = Sentence[0:len(Sentence)-1] + ',' + str(int(SumD[counter]-ReportedSum[counter])) + '\n'
          WriteFile.write(Sentence)
    print("Ended reading...",end=": ")
    sys.stdout.flush()   
    while_counter = 0
    while(while_counter < 100):
      try:
        now = time.time()
        print("Calibrating...",end=": ")
        sys.stdout.flush() 
        subprocess.call("Rscript {}.R".format(to_run), shell=True)
      
        print("Time: {}".format(time.time() - now))
        sys.stdout.flush() 
        while_counter += 1
   
        
        DataFile = pd.read_csv("result.csv")
        
        DataSelected = DataFile[(DataFile[".id"] == "median")]
        DataSelected = DataSelected["I_new_sympt"].tolist()
        ReportedPP = DataSelected[0:96]
        ReportedPP = np.array(ReportedPP)
           
        print("Time 2: {}".format(time.time() - now))
        sys.stdout.flush() 

        DataSelected = DataFile[(DataFile[".id"] == "median")]
        DataSelected = DataSelected["I_new_asympt"].tolist()
        UnreportedPP = DataSelected[0:96]
        UnreportedPP = np.array(UnreportedPP)
        
        print("Time 3: {}".format(time.time() - now))
        sys.stdout.flush() 

        DataFile = pd.read_csv("parameter.csv")
        DataSelected = DataFile[(DataFile["sim_start"] == "2020-01-26")]
        ParameterPP = [DataSelected["beta0est"].to_list()[0], DataSelected["alphaest"].to_list()[0], DataSelected["muest"].to_list()[0], DataSelected["deltaest"].to_list()[0]]
        ParameterPP = np.array(ParameterPP)

        ParameterPP[1] = 1.0 - ParameterPP[1]
        
        print("Time 4: {}".format(time.time() - now))
        sys.stdout.flush() 

        ModelCost1 = VectorCost(ParameterP)
        print("Time 5: {}".format(time.time() - now))
        print("{} - {}".format(list(ParameterP), list(ParameterPP)))
        sys.stdout.flush() 
        ModelCost2 = VectorCost(ParameterPP - ParameterP)
        print("Time 6: {}".format(time.time() - now))
        sys.stdout.flush()
        ModelCost3 = TimeSeriesCost(ParameterPP[1]*D - ReportedP)
        print("Time 7: {}".format(time.time() - now))
        sys.stdout.flush()
        DataCost = TimeSeriesCost(((D-Reported)/(1.0-ParameterPP[1]))-(ReportedPP+UnreportedPP))
        print("Time 8: {}".format(time.time() - now))
        sys.stdout.flush()
        MDLCost = ModelCost1 + ModelCost2 + ModelCost3 + DataCost
        print("Time 9: {}".format(time.time() - now))
        sys.stdout.flush()
        
        while_counter = 100
      
      except:
        pass
    print("OUT FOR LOOP Time: {}".format(time.time() - now))
    sys.stdout.flush() 
    with open('D.txt','a+') as WriteFile:
      WriteFile.write(str(list(D)))
      WriteFile.write('\t')
      WriteFile.write(str(MDLCost))
      WriteFile.write('\n')

    return MDLCost

  def MDL_alpha(alpha, ParameterP,warm=False):
    
    if warm:
      to_run = 'COVID_fit-read'
    else:
      to_run = 'COVID_fit'
    
    D = Reported / alpha
    
    SumD = [0]*96
    SumD[0] = D[0]
    for counter in range(1,96):
      SumD[counter] = SumD[counter-1] + D[counter]
    
    with open('us-counties.txt','w') as WriteFile:
      with open('us-counties-source.txt','r') as ReadFile:
        Sentence = ReadFile.readline()
        Sentence = Sentence[0:len(Sentence)-1] + ',uncases\n'
        WriteFile.write(Sentence)
        for counter in range(96):
          Sentence = ReadFile.readline()
          if not Sentence:
            print ("Error!")
          Sentence = Sentence[0:len(Sentence)-1] + ',' + str(int(SumD[counter]-ReportedSum[counter])) + '\n'
          WriteFile.write(Sentence)
          
    while(True):
      try:
        subprocess.call("Rscript COVID-fit.R", shell=True)

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
        DataSelected = DataSelected["I_new_sympt"].tolist()
        ReportedPP = DataSelected[7:60]
        ReportedPP = np.array(ReportedPP)
        
        DataSelected = DataFile[(DataFile[".id"] == "median")]
        DataSelected = DataSelected["I_new_asympt"].tolist()
        UnreportedPP = DataSelected[7:60]
        UnreportedPP = np.array(UnreportedPP)
      
        DataFile = pd.read_csv("parameter.csv")
        DataSelected = DataFile[(DataFile["sim_start"] == "2020-01-25")]
        ParameterPP = [DataSelected["beta0est"].to_list()[0], DataSelected["alphaest"].to_list()[0], DataSelected["muest"].to_list()[0], DataSelected["deltaest"].to_list()[0]]
        ParameterPP = np.array(ParameterPP)

        ParameterPP[1] = 1.0 - ParameterPP[1]

        ModelCost1 = VectorCost(ParameterP)
        ModelCost2 = VectorCost(ParameterPP - ParameterP)
        ModelCost3 = TimeSeriesCost(ParameterPP[1]*(ReportedPP+UnreportedPP) - ReportedP)
        DataCost = TimeSeriesCost((((ReportedPP+UnreportedPP)-Reported)/(1.0-ParameterPP[1]))-(ReportedPP+UnreportedPP))
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
    
  def MDL_step2(D,D_start,ParameterP):
      D_scaled = fix_magnitude(D,D_start)
      cost =  MDL(D_scaled,ParameterP,True)
      print("MDLCOST : {}".format(cost))
      sys.stdout.flush()  
      f= open("optimization_log.txt", "a+")
      f.write("%d\r\n" % (cost))
      D_write = list(D_scaled)
      f.write(str(D_write))
      f.write("\n")
      f.close()
      return cost
  

  
  def fix_magnitude(D,D_start):
        D = np.array(D)
        scale_factor = np.sum(D_start) / (np.sum(D)) 
        D = D * scale_factor
        return D
    
  def wavelet_fit(dim,cat,cdt,w,alpha_hat,D_reported):
        cat = np.concatenate((np.zeros((dim- cat.shape[0])),cat))
        #cdt = np.concatenate((np.zeros((dim- cdt.shape[0])),cdt))
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


  '''
  file = open('D_ground_truth.txt','r')
  D_gt = []
  line = file.readline()
  D_gt = np.array([float(x) for x in line[1:-1].split(",")])
  print(list(D_gt))
  print(MDL(D_gt,ParameterP))

  
  '''
  
  
  
  alpha_hat = 0.1
  D_start = np.copy(Reported) / alpha_hat
  noisy_D_start = np.maximum(D_start  + np.multiply(D_start,np.random.normal(0,0.06,size=D_start.shape)),np.zeros_like(D_start))
  noisy_D_start = fix_magnitude(noisy_D_start,D_start)
  
  print(list(noisy_D_start))
  sys.stdout.flush()
  
  
  cost = MDL(noisy_D_start,ParameterP,warm=False)
  print(cost)
  sys.stdout.flush()
  

  
  f= open("noisy_D_start.txt", "w")
  f.write("%d\r\n" % (cost))
  f.write(str(list(noisy_D_start)))
  f.write("\n")
  f.close()

  #print(MDL(D_start,ParameterP))
  #sys.stdout.flush()  
  
  
  '''
  

  #print([d for d in D_start])
  #print("MDL initial:")
  #sys.stdout.flush()

  #print(MDL(D_start,ParameterP,warm=False))
  print("Starting OPTI")
  sys.stdout.flush()
  
  
  res = minimize(fun=MDL_step2, 
               x0=D_start, 
               args=(D_start,ParameterP),
               method='nelder-mead',
               options={'maxiter': 600,'xtol':0.1, 'ftol':0.1,'adaptive': True})
  print("FINISHEd OPTI")
  
  D_end = res.x
  print(list(D_end))
  print("OPT finished")
  sys.stdout.flush()
  

  
  D_tapped = np.array([0]+list(D_start))
  w = 'haar'
  (ca, cd) = pywt.dwt(D_tapped,w)
  cat = pywt.threshold(ca, np.std(ca)/2, mode='soft')
  cdt = pywt.threshold(cd, np.std(cd)/2, mode='soft')
  j = 6
  cat0 = cat[-j:]
  fit0 = wavelet_fit(D_tapped.shape[0]//2,cat0,cdt,w,alpha_hat,D_tapped*alpha_hat)

  
  res = minimize(fun=MDL_wavelet, 
               x0=cat0, 
               args=(cdt,D_tapped.shape[0]//2, w,ParameterP,alpha_hat,D_tapped*alpha_hat),
               method='nelder-mead',
               options={'maxiter': 100,'xtol':0.000001, 'ftol':0.0000001,'adaptive': True})
  print("FINISHEd OPTI")
  cat_star = res.x
  
  
  fit_final = wavelet_fit(D_tapped.shape[0]//2,cat_star,cdt,w,alpha_hat,D_tapped*alpha_hat)

  print([d for d in D_start])
  print(" ")
  print([d for d in fit0]) 
  print(" ")
  print([d for d in fit_final])
  sys.stdout.flush()
  
  '''
