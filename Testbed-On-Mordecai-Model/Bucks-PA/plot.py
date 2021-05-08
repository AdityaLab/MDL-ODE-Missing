import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

if __name__ == "__main__":

    future = 18
    
    DataFile = pd.read_csv("data.csv")
    ReportedSum = DataFile["cases"][0:18+future].to_list()
    Date = DataFile["date"][0:18+future].to_list()
    X = range(len(Date))

    Reported = []
    Reported.append(ReportedSum[0])
    for counter in range(1,len(ReportedSum)):
        Reported.append(ReportedSum[counter] - ReportedSum[counter-1])
    Reported = np.array(Reported)

    XNumber = []
    XDate = []
    for counter in range(0,len(Date),7):
        XNumber.append(X[counter])
        XDate.append(Date[counter])
    
    DataFile = pd.read_csv("parameter-original.csv")
    DataSelected = DataFile[(DataFile["sim_start"] == "2020-02-20")]
    ParameterP = [DataSelected["beta0est"].to_list()[0], DataSelected["alphaest"].to_list()[0], DataSelected["alpha1est"].to_list()[0], DataSelected["E_init"].to_list()[0]]
    ParameterP = np.array(ParameterP)
    
    DataFile = pd.read_csv("result-original.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP = np.array(DataSelected["D_new_reported"].to_list()[20:38+future])
    UnreportedP = np.array(DataSelected["D_new_unreported"].to_list()[20:38+future])
    dIpIs = np.array(DataSelected["dIpIs_save"].to_list()[20:38+future])
    dIpIm = np.array(DataSelected["dIpIm_save"].to_list()[20:38+future])
    dEIa = np.array(DataSelected["dEIa_save"].to_list()[20:38+future])

    ReportRate = (ParameterP[2]*(np.sum(dIpIs)+np.sum(dIpIm)))/(np.sum(dIpIs)+np.sum(dIpIm)+np.sum(dEIa))
    print (ReportRate)

    DataFile = pd.read_csv("parameter.csv")
    DataSelected = DataFile[(DataFile["sim_start"] == "2020-02-20")]
    ParameterPP = [DataSelected["beta0est"].to_list()[0], DataSelected["alphaest"].to_list()[0], DataSelected["alpha1est"].to_list()[0], DataSelected["E_init"].to_list()[0]]
    ParameterPP = np.array(ParameterPP)
    
    DataFile = pd.read_csv("result.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP = np.array(DataSelected["D_new_reported"].to_list()[20:38+future])
    UnreportedPP = np.array(DataSelected["D_new_unreported"].to_list()[20:38+future])
    dIpIs = np.array(DataSelected["dIpIs_save"].to_list()[20:38+future])
    dIpIm = np.array(DataSelected["dIpIm_save"].to_list()[20:38+future])
    dEIa = np.array(DataSelected["dEIa_save"].to_list()[20:38+future])
      
    ReportRate = (ParameterPP[2]*(np.sum(dIpIs)+np.sum(dIpIm)))/(np.sum(dIpIs)+np.sum(dIpIm)+np.sum(dEIa))
    print (ReportRate)

    figure = plt.figure(figsize=(10.24,8.96))

    #plt.scatter(X,Reported/0.02,label=r'$D_{reported}$',marker='+',color='#000000')
    #plt.plot(X,ReportedP+UnreportedP,label=r"$D_{reported}$"+"(p')",linewidth=2,linestyle="dashdot",color='#1f77b4')
    #plt.plot(X,ReportedPP+UnreportedPP,label=r"$D_{reported}$"+"(p')",linewidth=2,linestyle="dashdot",color='#2ca02c')
    
    plt.scatter(X,Reported,label=r'$D_{reported}$',marker='+',color='#000000')
    plt.plot(X,ReportedP,label=r"$D_{reported}$"+"(p')",linewidth=2,linestyle="dashdot",color='#1f77b4')
    plt.plot(X,ReportedPP,label=r"$D_{reported}$"+"(p')",linewidth=2,linestyle="dashdot",color='#2ca02c')

    plt.axvline(x = 17,color='#FF6100',linewidth=2,linestyle="dashed")
    plt.text(17-2,10,'Training Data',color='#FF6100',horizontalalignment='right')
    plt.text(17+2,10,'Testing Data',color='#FF6100',horizontalalignment='left')

    plt.xlabel('Date', fontsize=15)
    plt.ylabel('Number of reported cases', fontsize=15)

    plt.xticks(XNumber,XDate,rotation=45)
    
    plt.legend(fontsize=15)
    plt.tight_layout()

    #print (np.linalg.norm(Reported[0:18]-ReportedP[0:18]),np.linalg.norm(Reported[0:18]-ReportedPP[0:18]))
    #print (np.linalg.norm(Reported[18:18+future]-ReportedP[18:18+future]),np.linalg.norm(Reported[18:18+future]-ReportedPP[18:18+future]))
 
    plt.show()
