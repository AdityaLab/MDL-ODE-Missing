from mpl_toolkits.axes_grid1.inset_locator import mark_inset
import matplotlib.pyplot as plt
import matplotlib.ticker
import matplotlib as mpl
from matplotlib import rcParams
mpl.rcParams['text.usetex'] = True
mpl.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}']
import pandas as pd
import numpy as np
import math

PopulationDictionary = {
42017:628270,
42029:524989,
42041:253370,
42045:566747,
42071:545724,
42091:830915,
42101:1584064,
53027:75061,
53033:2252782,
53035:271473,
53053:904980,
53061:822083,
36005:1418207,
36047:2559903,
36059:1356924,
36061:1628706,
36081:2253858
}

if __name__ == "__main__":

    RMSE = []

    figure = plt.figure(figsize=(9,4))

    ### Philadelphia Metro Area

    future = 16
    
    DataFile = pd.read_csv("Philadelphia/data.csv")
    ReportedSum = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]+DataFile["cases"][0:35+future].to_list()
    Date = ['2021-02-21','2021-02-22','2021-02-23','2021-02-24','2021-02-25','2021-02-26','2021-02-27','2021-02-28','2021-02-29','2021-03-01','2021-03-02','2021-03-03','2021-03-04','2021-03-05'] + DataFile["date"][0:35+future].to_list()
    X = range(len(Date))

    Reported = []
    Reported.append(ReportedSum[0])
    for counter in range(1,len(ReportedSum)):
        Reported.append(ReportedSum[counter] - ReportedSum[counter-1])
    Reported = np.array(Reported)

    XNumber = [9,40]
    XDate = []
    for DateNow in XNumber:
        XDate.append(Date[DateNow])
    XDate = ["Mar 1","Apr 1"]

    DataFile = pd.read_csv("Philadelphia/covidcast-fb-survey-smoothed_wcli-2020-04-06-to-2020-06-30.csv")

    SymptomRate = []
    SymptomError = []
    
    for DateNow in Date:
        DataSelected = DataFile[DataFile["time_value"] == DateNow]
        FIPSList = DataSelected["geo_value"].to_list()
        SymptomRateList = DataSelected["value"].to_list()
        SymptomErrorList = DataSelected["stderr"].to_list()
        if (len(FIPSList) != 0):
            SymptomRateNow = 0
            SymptomErrorNow = 0
            PopulationList = []
            for FIPSListNow in FIPSList:
                PopulationList.append(PopulationDictionary[FIPSListNow])
            for counter in range(len(FIPSList)):
                SymptomRateNow = SymptomRateNow + PopulationList[counter]*SymptomRateList[counter]
                SymptomErrorNow = SymptomErrorNow + PopulationList[counter]*SymptomErrorList[counter]
            SymptomRateNow = SymptomRateNow / np.sum(PopulationList)
            SymptomErrorNow = SymptomErrorNow / np.sum(PopulationList)
            SymptomRate.append(SymptomRateNow)
            SymptomError.append(SymptomErrorNow)            
        else:
            SymptomRate.append(0)
            SymptomError.append(0)

    SymptomRate = np.array(SymptomRate)
    SymptomError = np.array(SymptomError)
    
    DataFile = pd.read_csv("Philadelphia/result-original.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP = np.array(DataSelected["D_new_reported"].to_list()[:49+future])
    UnreportedP = np.array(DataSelected["D_new_unreported"].to_list()[:49+future])
    SymptomP = np.array(DataSelected["Is"].to_list()[:49+future]) + np.array(DataSelected["Im"].to_list()[:49+future])

    DataFile = pd.read_csv("Philadelphia/result.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP = np.array(DataSelected["D_new_reported"].to_list()[:49+future])
    UnreportedPP = np.array(DataSelected["D_new_unreported"].to_list()[:49+future])
    SymptomPP = np.array(DataSelected["Is"].to_list()[:49+future]) + np.array(DataSelected["Im"].to_list()[:49+future])

    ax = plt.subplot(1,2,1)
    ax.set_title("Philadelphia (SEIR+HD)", fontsize=14)

    ax.plot(X,SymptomP/49101.39,label=r'\textsc{BaseParam}'+r'$_{\mathrm{Symp}}$',linewidth=3,color='#2166AC')
    ax.plot(X,SymptomPP/49101.39,label=r'\textsc{MdlParam}'+r'$_{\mathrm{Symp}}$',linewidth=3,color='#EA604D')

    ax.scatter(X[45:],SymptomRate[45:],label=r'\textsc{Rate}'+r'$_{\mathrm{Symp}}$',marker='+',s=25,color='#000000')
    ax.fill_between(X[45:],(SymptomRate[45:]-SymptomError[45:]),(SymptomRate[45:]+SymptomError[45:]),color='#000000',alpha=0.25)
    
    ax.axvline(x = 48,color='#929591',linewidth=1,linestyle="dashdot")
    #ax.text(48-2,1,'Training Data',color='#FF6100',horizontalalignment='right')
    #ax.text(48+2,1,'Testing Data',color='#FF6100',horizontalalignment='left')

    ax.set_xlabel('(a)', fontsize=20)
    ax.set_ylabel('Symptomatic rate', fontsize=16)

    ax.set_xticks(XNumber)
    ax.set_xticklabels(XDate)
    ax.xaxis.set_tick_params(labelsize=14)
    ax.set_yticks([0,0.2,0.4,0.6,0.8,1.0])
    ax.set_yticklabels(["0","0.002","0.004","0.006","0.008","0.01"])
    ax.yaxis.set_tick_params(labelsize=16)
    ax.set_ylim(0,1)
    
    ax.legend(fontsize=14,loc=2)
    plt.tight_layout()
    
    
    ### Western Washington

    future = 35
    
    DataFile = pd.read_csv("Washington/data.csv")
    ReportedSum = DataFile["cases"][0:45+future].to_list()
    Date = DataFile["date"][0:45+future].to_list()
    X = range(len(Date))

    Reported = []
    Reported.append(ReportedSum[0])
    for counter in range(1,len(ReportedSum)):
        Reported.append(ReportedSum[counter] - ReportedSum[counter-1])
    Reported = np.array(Reported)

    XNumber = [11,40,71]
    XDate = []
    for DateNow in XNumber:
        XDate.append(Date[DateNow])
    XDate = ["Feb 1","Mar 1","Apr 1"]

    DataFile = pd.read_csv("Washington/covidcast-fb-survey-smoothed_wcli-2020-04-06-to-2020-06-30.csv")

    SymptomRate = []
    SymptomError = []
    
    for DateNow in Date:
        DataSelected = DataFile[DataFile["time_value"] == DateNow]
        FIPSList = DataSelected["geo_value"].to_list()
        SymptomRateList = DataSelected["value"].to_list()
        SymptomErrorList = DataSelected["stderr"].to_list()
        if (len(FIPSList) != 0):
            SymptomRateNow = 0
            SymptomErrorNow = 0
            PopulationList = []
            for FIPSListNow in FIPSList:
                PopulationList.append(PopulationDictionary[FIPSListNow])
            for counter in range(len(FIPSList)):
                SymptomRateNow = SymptomRateNow + PopulationList[counter]*SymptomRateList[counter]
                SymptomErrorNow = SymptomErrorNow + PopulationList[counter]*SymptomErrorList[counter]
            SymptomRateNow = SymptomRateNow / np.sum(PopulationList)
            SymptomErrorNow = SymptomErrorNow / np.sum(PopulationList)
            SymptomRate.append(SymptomRateNow)
            SymptomError.append(SymptomErrorNow)            
        else:
            SymptomRate.append(0)
            SymptomError.append(0)

    SymptomRate = np.array(SymptomRate)
    SymptomError = np.array(SymptomError)
    
    DataFile = pd.read_csv("Washington/result-original.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP = np.array(DataSelected["D_new_reported"].to_list()[:45+future])
    UnreportedP = np.array(DataSelected["D_new_unreported"].to_list()[:45+future])
    SymptomP = np.array(DataSelected["Is"].to_list()[:45+future]) + np.array(DataSelected["Im"].to_list()[:45+future])

    DataFile = pd.read_csv("Washington/result.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP = np.array(DataSelected["D_new_reported"].to_list()[:45+future])
    UnreportedPP = np.array(DataSelected["D_new_unreported"].to_list()[:45+future])
    SymptomPP = np.array(DataSelected["Is"].to_list()[:45+future]) + np.array(DataSelected["Im"].to_list()[:45+future])
      
    ax = plt.subplot(1,2,2)
    ax.set_title("Western Washington (SEIR+HD)", fontsize=14)

    ax.plot(X,SymptomP/42735.48,label=r'\textsc{BaseParam}'+r'$_{\mathrm{Symp}}$',linewidth=3,color='#2166AC')
    ax.plot(X,SymptomPP/42735.48,label=r'\textsc{MdlParam}'+r'$_{\mathrm{Symp}}$',linewidth=3,color='#EA604D')

    ax.scatter(X[77:],SymptomRate[77:],label=r'\textsc{Rate}'+r'$_{\mathrm{Symp}}$',marker='+',s=25,color='#000000')
    ax.fill_between(X[77:],(SymptomRate[77:]-SymptomError[77:]),(SymptomRate[77:]+SymptomError[77:]),color='#000000',alpha=0.25)
     
    ax.axvline(x = 44,color='#929591',linewidth=1,linestyle="dashdot")
    #ax.text(45-2,1,'Training Data',color='#FF6100',horizontalalignment='right')
    #ax.text(45+2,1,'Testing Data',color='#FF6100',horizontalalignment='left')

    ax.set_xlabel('(b)', fontsize=20)
    #ax.set_ylabel('Symptomatic rate', fontsize=16)

    ax.set_xticks(XNumber)
    ax.set_xticklabels(XDate)
    ax.xaxis.set_tick_params(labelsize=14)
    ax.set_yticks([0,1.0,2.0,3.0,4.0,5.0])
    ax.set_yticklabels(["0","0.01","0.02","0.03","0.04","0.05"])
    ax.yaxis.set_tick_params(labelsize=14)
    ax.set_ylim(0,5)

    #ax.legend(fontsize=14)
    plt.tight_layout()
    
    plt.savefig('Symptomatic.pdf')
    plt.show()
