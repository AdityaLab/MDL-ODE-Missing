import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

if __name__ == "__main__":

    future = 14
    
    DataFile = pd.read_csv("data.csv")
    ReportedSum = [0,0,0,0,0,0] + DataFile["cases"][0:53+future].to_list()
    Date = ["2020-01-25","2020-01-26","2020-01-27","2020-01-28","2020-01-29","2020-01-30"] + DataFile["date"][0:53+future].to_list()
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
    
    DataFile = pd.read_csv("result-original.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP = np.array(DataSelected["D_new_reported"].to_list()[:59+future])
    UnreportedP = np.array(DataSelected["D_new_unreported"].to_list()[:59+future])

    DataFile = pd.read_csv("result.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP = np.array(DataSelected["D_new_reported"].to_list()[:59+future])
    UnreportedPP = np.array(DataSelected["D_new_unreported"].to_list()[:59+future])
       
    figure = plt.figure(figsize=(10.24,8.96))

    plt.scatter(X,Reported,label=r"$D_{reported}$",marker="+",color="#000000")
    plt.plot(X,ReportedP,label=r"$D_{reported}(p)$",linewidth=2,linestyle="dashdot",color="#1f77b4")
    plt.plot(X,ReportedPP,label=r"$D_{reported}$"+"(p')",linewidth=2,linestyle="dashdot",color="#2ca02c")

    plt.axvline(x = 59,color="#FF6100",linewidth=2,linestyle="dashed")
    #plt.text(59-2,10,"Training Data",color="#FF6100",horizontalalignment="right")
    #plt.text(59+2,10,"Testing Data",color="#FF6100",horizontalalignment="left")

    plt.xlabel("Date", fontsize=15)
    plt.ylabel("Number of reported cases", fontsize=15)
    
    plt.xticks(XNumber,XDate,rotation=45)
    
    plt.legend(fontsize=15)
    plt.tight_layout()

    #print (np.linalg.norm(Reported[0:59]-ReportedP[0:59]),np.linalg.norm(Reported[0:59]-ReportedPP[0:59]))
    #print (np.linalg.norm(Reported[59:59+future]-ReportedP[59:59+future]),np.linalg.norm(Reported[59:59+future]-ReportedPP[59:59+future]))
 
    plt.show()
