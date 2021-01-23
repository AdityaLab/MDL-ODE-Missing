import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

if __name__ == "__main__":

    figure = plt.figure(figsize=(10.24,7.68))
    plt.title("Total infections", fontsize=20)

    future = 31
    
    DataFile = pd.read_csv("data.csv")
    ReportedSum = DataFile["cases"][0:96+future].to_list()
    Date = DataFile["date"][0:96+future].to_list()
    X = range(len(Date))

    Reported = []
    Reported.append(ReportedSum[0])
    for counter in range(1,len(ReportedSum)):
        Reported.append(ReportedSum[counter] - ReportedSum[counter-1])
    Reported = np.array(Reported)
    
    plt.scatter(X,Reported,label=r'$D_{reported}$',marker='+',color='#000000')
    
    XNumber = []
    XDate = []
    for counter in range(0,len(Date),7):
        XNumber.append(X[counter])
        XDate.append(Date[counter])

    DataFile = pd.read_csv("result-original.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP = np.array(DataSelected["I_new_sympt"].to_list()[:96+future])
    UnreportedP = np.array(DataSelected["I_new_asympt"].to_list()[:96+future])
    
    #plt.plot(X,ReportedP+UnreportedP,label="D(p)",linewidth=2,color='#1f77b4')
    plt.plot(X,ReportedP,label=r"$D_{reported}$"+"(p)",linewidth=2,linestyle="dashdot",color='#1f77b4')

    DataFile = pd.read_csv("result.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP = np.array(DataSelected["I_new_sympt"].to_list()[:96+future])
    UnreportedPP = np.array(DataSelected["I_new_asympt"].to_list()[:96+future])
    
    #plt.plot(X,ReportedPP+UnreportedPP,label="D(p')",linewidth=2,color='#2ca02c')
    plt.plot(X,ReportedPP,label=r"$D_{reported}$"+"(p')",linewidth=2,linestyle="dashdot",color='#2ca02c')

    plt.axvline(x = 96,color='#FF6100',linewidth=2,linestyle="dashed")
    plt.text(96-2,2,'Training Data',color='#FF6100',horizontalalignment='right')
    plt.text(96+2,2,'Testing Data',color='#FF6100',horizontalalignment='left')

    plt.xlabel('Date', fontsize=15)
    plt.ylabel('Number of infections', fontsize=15)

    plt.xticks(XNumber,XDate,rotation=45)
    
    plt.legend(fontsize=15)
    plt.tight_layout()
    plt.show()
    
    print (np.linalg.norm(Reported[0:96]-ReportedP[0:96]),np.linalg.norm(Reported[0:96]-ReportedPP[0:96]))
    print (np.linalg.norm(Reported[96:96+future]-ReportedP[96:96+future]),np.linalg.norm(Reported[96:96+future]-ReportedPP[65:65+future]))
