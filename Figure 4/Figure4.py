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

PopulationDictionary = {27003:356921,
27009:40889,
27019:105089,
27025:56579,
27037:429021,
27049:46340,
27053:1265843,
27059:40596,
27079:28887,
27085:35893,
27095:26277,
27123:550321,
27131:66972,
27139:149013,
27141:97238,
27145:161075,
27147:36649,
27163:262440,
27171:138377,
12086:2716940,
12011:1952778,
12099:1496770,
12085:161000,
42101:1584064,
42091:830915,
42017:628270,
42011:421164,
42095:305285,
42029:524989,
42071:545724,
42077:369318,
42045:566747,
42041:253370,
42043:278299,
42133:79255,
66001:1671329,
66013:1153526,
66041:258826,
66075:881549,
66081:766573,
66085:1927852
}

if __name__ == "__main__":
    
    figure = plt.figure(figsize=(18,4.5))

    ### Minneapolis Metro Area, Mordecai Model

    future = 14
    
    DataFile = pd.read_csv("Minneapolis-Mordecai/data.csv")
    ReportedSum = DataFile["cases"][0:131+future].to_list()
    Date = DataFile["date"][0:131+future].to_list()
    X = range(len(Date))

    Reported = []
    Reported.append(ReportedSum[0])
    for counter in range(1,len(ReportedSum)):
        Reported.append(ReportedSum[counter] - ReportedSum[counter-1])
    Reported = np.array(Reported)

    XNumber = [26,56,87,117]
    XDate = ["Apr 1\n","May 1\n","Jun 1\n","Jul 1\n"]

    DataFile = pd.read_csv("Minneapolis-Mordecai/covidcast-fb-survey-smoothed_wcli-2020-04-06-to-2022-01-06.csv")

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
                SymptomRateNow = SymptomRateNow + SymptomRateList[counter]
                SymptomErrorNow = SymptomErrorNow + SymptomErrorList[counter]
            #SymptomRateNow = SymptomRateNow / np.sum(PopulationList)
            #SymptomErrorNow = SymptomErrorNow / np.sum(PopulationList)
            SymptomRate.append(SymptomRateNow)
            SymptomError.append(SymptomErrorNow)            
        else:
            SymptomRate.append(0)
            SymptomError.append(0)

    SymptomRate = np.array(SymptomRate)
    SymptomError = np.array(SymptomError)

    DataFile = pd.read_csv("Minneapolis-Mordecai/result-original-1.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP1 = DataSelected["D_new_reported"].to_list()[25:67+future]
    UnreportedP1 = DataSelected["D_new_unreported"].to_list()[25:67+future]
    SymptomP1 = list(np.array(DataSelected["Is"].to_list()[25:67+future]) + np.array(DataSelected["Im"].to_list()[25:67+future]))

    DataFile = pd.read_csv("Minneapolis-Mordecai/result-original-2.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP2 = DataSelected["D_new_reported"].to_list()[1:34+future]
    UnreportedP2 = DataSelected["D_new_unreported"].to_list()[1:34+future]
    SymptomP2 = list(np.array(DataSelected["Is"].to_list()[1:34+future]) + np.array(DataSelected["Im"].to_list()[1:34+future]))

    DataFile = pd.read_csv("Minneapolis-Mordecai/result-original-3.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP3 = DataSelected["D_new_reported"].to_list()[1:33+future]
    UnreportedP3 = DataSelected["D_new_unreported"].to_list()[1:33+future]
    SymptomP3 = list(np.array(DataSelected["Is"].to_list()[1:33+future]) + np.array(DataSelected["Im"].to_list()[1:33+future]))

    DataFile = pd.read_csv("Minneapolis-Mordecai/result-original-4.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP4 = DataSelected["D_new_reported"].to_list()[1:25+future]
    UnreportedP4 = DataSelected["D_new_unreported"].to_list()[1:25+future]
    SymptomP4 = list(np.array(DataSelected["Is"].to_list()[1:25+future]) + np.array(DataSelected["Im"].to_list()[1:25+future]))

    ReportedP = np.array(ReportedP1[:42] + ReportedP2[:33] + ReportedP3[:32] + ReportedP4[:24+future])
    UnreportedP = np.array(UnreportedP1[:42] + UnreportedP2[:33] + UnreportedP3[:32] + UnreportedP4[:24+future])
    SymptomP = np.array(SymptomP1[:42] + SymptomP2[:33] + SymptomP3[:32] + SymptomP4[:24+future]) / 38574.79

    DataFile = pd.read_csv("Minneapolis-Mordecai/result-1.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP1 = DataSelected["D_new_reported"].to_list()[25:67+future]
    UnreportedPP1 = DataSelected["D_new_unreported"].to_list()[25:67+future]
    SymptomPP1 = list(np.array(DataSelected["Is"].to_list()[25:67+future]) + np.array(DataSelected["Im"].to_list()[25:67+future]))

    DataFile = pd.read_csv("Minneapolis-Mordecai/result-2.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP2 = DataSelected["D_new_reported"].to_list()[1:34+future]
    UnreportedPP2 = DataSelected["D_new_unreported"].to_list()[1:34+future]
    SymptomPP2 = list(np.array(DataSelected["Is"].to_list()[1:34+future]) + np.array(DataSelected["Im"].to_list()[1:34+future]))

    DataFile = pd.read_csv("Minneapolis-Mordecai/result-3.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP3 = DataSelected["D_new_reported"].to_list()[1:33+future]
    UnreportedPP3 = DataSelected["D_new_unreported"].to_list()[1:33+future]
    SymptomPP3 = list(np.array(DataSelected["Is"].to_list()[1:33+future]) + np.array(DataSelected["Im"].to_list()[1:33+future]))

    DataFile = pd.read_csv("Minneapolis-Mordecai/result-4.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP4 = DataSelected["D_new_reported"].to_list()[1:25+future]
    UnreportedPP4 = DataSelected["D_new_unreported"].to_list()[1:25+future]
    SymptomPP4 = list(np.array(DataSelected["Is"].to_list()[1:25+future]) + np.array(DataSelected["Im"].to_list()[1:25+future]))

    ReportedPP = np.array(ReportedPP1[:42] + ReportedPP2[:33] + ReportedPP3[:32] + ReportedPP4[:24+future])
    UnreportedPP = np.array(UnreportedPP1[:42] + UnreportedPP2[:33] + UnreportedPP3[:32] + UnreportedPP4[:24+future])
    SymptomPP = np.array(SymptomPP1[:42] + SymptomPP2[:33] + SymptomPP3[:32] + SymptomPP4[:24+future]) / 38574.79
    
    ax = plt.subplot(1,4,1)
    ax.set_title("\n", fontsize=12)

    ax.plot(X,SymptomP,label=r'\textsc{BaseParam}'+r'$_{\mathrm{Symp}}$',linewidth=3,color='#2166AC')
    ax.plot(X,SymptomPP,label=r'\textsc{MdlParam}'+r'$_{\mathrm{Symp}}$',linewidth=3,color='#EA604D')
    ax.scatter([0],[100],label=r'\textsc{Rate}'+r'$_{\mathrm{Symp}}$',marker='+',s=25,color='#000000')
    
    #ax.axvline(x = 130,color='#929591',linewidth=1,linestyle="dashdot")
    
    ax.set_xlabel('\n', fontsize=18)
    ax.set_ylabel('Symptomatic rate',fontsize=18)

    ax.set_xticks(XNumber)
    ax.set_xticklabels(XDate)
    ax.xaxis.set_tick_params(labelsize=12)
    ax.set_yticks([0,0.5,1.0,1.5])
    ax.set_yticklabels(["0","0.005","0.01","0.015"])
    ax.yaxis.set_tick_params(labelsize=12)
    ax.set_ylim(0,1.5)

    ax.legend(fontsize=14, loc=2)

    ax2 = ax.twinx()
    ax2.scatter(X[31:],SymptomRate[31:],label=r'\textsc{Rate}'+r'$_{\mathrm{Symp}}$',marker='+',s=25,color='#000000')
    ax2.fill_between(X[31:],(SymptomRate[31:]-SymptomError[31:]),(SymptomRate[31:]+SymptomError[31:]),color='#000000',alpha=0.25)

    ax2.set_xticks(XNumber)
    ax2.set_xticklabels(XDate)
    ax2.xaxis.set_tick_params(labelsize=12)
    ax2.set_yticks([0,5,10,15])
    ax2.set_yticklabels(["0","0.05","0.1","0.15"])
    ax2.yaxis.set_tick_params(labelsize=12)
    ax2.set_ylim(0,15)

    plt.tight_layout()


    ### Minneapolis Metro Area Fall, Mordecai Model

    future = 14
    
    DataFile = pd.read_csv("Minneapolis-Mordecai-Fall/data.csv")
    ReportedSum = DataFile["cases"][0:31+future].to_list()
    Date = DataFile["date"][1:31+future].to_list()
    X = range(len(Date))

    Reported = []
    Reported.append(ReportedSum[0])
    for counter in range(1,len(ReportedSum)):
        Reported.append(ReportedSum[counter] - ReportedSum[counter-1])
    Reported = np.array(Reported[1:31+future])

    XNumber = [5,35]
    XDate = ["Sep 15\n","Oct 15\n"]

    DataFile = pd.read_csv("Minneapolis-Mordecai-Fall/covidcast-fb-survey-smoothed_wcli-2020-04-06-to-2022-01-06.csv")

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
                SymptomRateNow = SymptomRateNow + SymptomRateList[counter]
                SymptomErrorNow = SymptomErrorNow + SymptomErrorList[counter]
            #SymptomRateNow = SymptomRateNow / np.sum(PopulationList)
            #SymptomErrorNow = SymptomErrorNow / np.sum(PopulationList)
            SymptomRate.append(SymptomRateNow)
            SymptomError.append(SymptomErrorNow)            
        else:
            SymptomRate.append(0)
            SymptomError.append(0)

    SymptomRate = np.array(SymptomRate)
    SymptomError = np.array(SymptomError)

    DataFile = pd.read_csv("Minneapolis-Mordecai-Fall/result-original.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP = np.array(DataSelected["D_new_reported"].to_list()[1:31+future])
    UnreportedP = np.array(DataSelected["D_new_unreported"].to_list()[1:31+future])
    SymptomP = (np.array(DataSelected["Is"].to_list()[1:31+future]) + np.array(DataSelected["Im"].to_list()[1:31+future])) / 38574.79

    DataFile = pd.read_csv("Minneapolis-Mordecai-Fall/result.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP = np.array(DataSelected["D_new_reported"].to_list()[1:31+future])
    UnreportedPP = np.array(DataSelected["D_new_unreported"].to_list()[1:31+future])
    SymptomPP = (np.array(DataSelected["Is"].to_list()[1:31+future]) + np.array(DataSelected["Im"].to_list()[1:31+future])) / 38574.79

    ax = plt.subplot(1,4,2)
    ax.set_title("\n", fontsize=12)

    ax.plot(X,SymptomP,label=r'\textsc{BaseParam}'+r'$_{\mathrm{Symp}}$',linewidth=3,color='#2166AC')
    ax.plot(X,SymptomPP,label=r'\textsc{MdlParam}'+r'$_{\mathrm{Symp}}$',linewidth=3,color='#EA604D')
    
    #ax.axvline(x = 130,color='#929591',linewidth=1,linestyle="dashdot")
    
    ax.set_xlabel('\n', fontsize=18)

    ax.set_xticks(XNumber)
    ax.set_xticklabels(XDate)
    ax.xaxis.set_tick_params(labelsize=12)
    ax.set_yticks([0,0.1,0.2])
    ax.set_yticklabels(["0","0.001","0.002"])
    ax.yaxis.set_tick_params(labelsize=12)
    ax.set_ylim(0,0.2)
    
    ax2 = ax.twinx()
    ax2.scatter(X,SymptomRate,label=r'\textsc{Rate}'+r'$_{\mathrm{Symp}}$',marker='+',s=25,color='#000000')
    ax2.fill_between(X,(SymptomRate-SymptomError),(SymptomRate+SymptomError),color='#000000',alpha=0.25)

    ax2.set_xticks(XNumber)
    ax2.set_xticklabels(XDate)
    ax2.xaxis.set_tick_params(labelsize=12)
    ax2.set_yticks([0,5,10,15,20])
    ax2.set_yticklabels(["0","0.05","0.1","0.15","0.2"])
    ax2.yaxis.set_tick_params(labelsize=12)
    ax2.set_ylim(0,20)

    plt.tight_layout()


    ### South Florida, Mordecai Model

    future = 16
    
    DataFile = pd.read_csv("Florida-Mordecai/data.csv")
    ReportedSum = DataFile["cases"][0:114+future].to_list()
    Date = DataFile["date"][0:114+future].to_list()
    X = range(len(Date))

    Reported = []
    Reported.append(ReportedSum[0])
    for counter in range(1,len(ReportedSum)):
        Reported.append(ReportedSum[counter] - ReportedSum[counter-1])
    Reported = np.array(Reported)

    XNumber = [26,56,87,117]
    XDate = ["Apr 1\n","May 1\n","Jun 1\n","Jul 1\n"]
    
    DataFile = pd.read_csv("Florida-Mordecai/covidcast-fb-survey-smoothed_wcli-2020-04-06-to-2022-01-06.csv")

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
                SymptomRateNow = SymptomRateNow + SymptomRateList[counter]
                SymptomErrorNow = SymptomErrorNow + SymptomErrorList[counter]
            #SymptomRateNow = SymptomRateNow / np.sum(PopulationList)
            #SymptomErrorNow = SymptomErrorNow / np.sum(PopulationList)
            SymptomRate.append(SymptomRateNow)
            SymptomError.append(SymptomErrorNow)            
        else:
            SymptomRate.append(0)
            SymptomError.append(0)

    SymptomRate = np.array(SymptomRate)
    SymptomError = np.array(SymptomError)

    DataFile = pd.read_csv("Florida-Mordecai/result-original-1.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP1 = DataSelected["D_new_reported"].to_list()[14:34+future]
    UnreportedP1 = DataSelected["D_new_unreported"].to_list()[14:34+future]
    SymptomP1 = list(np.array(DataSelected["Is"].to_list()[14:34+future]) + np.array(DataSelected["Im"].to_list()[14:34+future]))
    
    DataFile = pd.read_csv("Florida-Mordecai/result-original-2.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP2 = DataSelected["D_new_reported"].to_list()[1:11+future]
    UnreportedP2 = DataSelected["D_new_unreported"].to_list()[1:11+future]
    SymptomP2 = list(np.array(DataSelected["Is"].to_list()[1:11+future]) + np.array(DataSelected["Im"].to_list()[1:11+future]))

    DataFile = pd.read_csv("Florida-Mordecai/result-original-3.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP3 = DataSelected["D_new_reported"].to_list()[1:25+future]
    UnreportedP3 = DataSelected["D_new_unreported"].to_list()[1:25+future]
    SymptomP3 = list(np.array(DataSelected["Is"].to_list()[1:25+future]) + np.array(DataSelected["Im"].to_list()[1:25+future]))

    DataFile = pd.read_csv("Florida-Mordecai/result-original-4.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP4 = DataSelected["D_new_reported"].to_list()[1:31+future]
    UnreportedP4 = DataSelected["D_new_unreported"].to_list()[1:31+future]
    SymptomP4 = list(np.array(DataSelected["Is"].to_list()[1:31+future]) + np.array(DataSelected["Im"].to_list()[1:31+future]))

    DataFile = pd.read_csv("Florida-Mordecai/result-original-5.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP5 = DataSelected["D_new_reported"].to_list()[1:31+future]
    UnreportedP5 = DataSelected["D_new_unreported"].to_list()[1:31+future]
    SymptomP5 = list(np.array(DataSelected["Is"].to_list()[1:31+future]) + np.array(DataSelected["Im"].to_list()[1:31+future]))

    ReportedP = np.array(ReportedP1[:20] + ReportedP2[:10] + ReportedP3[:24] + ReportedP4[:30] + ReportedP5[:30+future])
    UnreportedP = np.array(UnreportedP1[:20] + UnreportedP2[:10] + UnreportedP3[:24] + UnreportedP4[:30] + UnreportedP5[:30+future])
    SymptomP = np.array(SymptomP1[:20] + SymptomP2[:10] + SymptomP3[:24] + SymptomP4[:30] + SymptomP5[:30+future]) / 63453.45

    DataFile = pd.read_csv("Florida-Mordecai/result-1.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP1 = DataSelected["D_new_reported"].to_list()[14:34+future]
    UnreportedPP1 = DataSelected["D_new_unreported"].to_list()[14:34+future]
    SymptomPP1 = list(np.array(DataSelected["Is"].to_list()[14:34+future]) + np.array(DataSelected["Im"].to_list()[14:34+future]))
    
    DataFile = pd.read_csv("Florida-Mordecai/result-2.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP2 = DataSelected["D_new_reported"].to_list()[1:11+future]
    UnreportedPP2 = DataSelected["D_new_unreported"].to_list()[1:11+future]
    SymptomPP2 = list(np.array(DataSelected["Is"].to_list()[1:11+future]) + np.array(DataSelected["Im"].to_list()[1:11+future]))

    DataFile = pd.read_csv("Florida-Mordecai/result-3.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP3 = DataSelected["D_new_reported"].to_list()[1:25+future]
    UnreportedPP3 = DataSelected["D_new_unreported"].to_list()[1:25+future]
    SymptomPP3 = list(np.array(DataSelected["Is"].to_list()[1:25+future]) + np.array(DataSelected["Im"].to_list()[1:25+future]))

    DataFile = pd.read_csv("Florida-Mordecai/result-4.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP4 = DataSelected["D_new_reported"].to_list()[1:31+future]
    UnreportedPP4 = DataSelected["D_new_unreported"].to_list()[1:31+future]
    SymptomPP4 = list(np.array(DataSelected["Is"].to_list()[1:31+future]) + np.array(DataSelected["Im"].to_list()[1:31+future]))

    DataFile = pd.read_csv("Florida-Mordecai/result-5.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP5 = DataSelected["D_new_reported"].to_list()[1:31+future]
    UnreportedPP5 = DataSelected["D_new_unreported"].to_list()[1:31+future]
    SymptomPP5 = list(np.array(DataSelected["Is"].to_list()[1:31+future]) + np.array(DataSelected["Im"].to_list()[1:31+future]))

    ReportedPP = np.array(ReportedPP1[:20] + ReportedPP2[:10] + ReportedPP3[:24] + ReportedPP4[:30] + ReportedPP5[:30+future])
    UnreportedPP = np.array(UnreportedPP1[:20] + UnreportedPP2[:10] + UnreportedPP3[:24] + UnreportedPP4[:30] + UnreportedPP5[:30+future])
    SymptomPP = np.array(SymptomPP1[:20] + SymptomPP2[:10] + SymptomPP3[:24] + SymptomPP4[:30] + SymptomPP5[:30+future]) / 63453.45

    ax = plt.subplot(1,4,3)
    ax.set_title("\n", fontsize=12)

    ax.plot(X,SymptomP,label=r'\textsc{BaseParam}'+r'$_{\mathrm{Symp}}$',linewidth=3,color='#2166AC')
    ax.plot(X,SymptomPP,label=r'\textsc{MdlParam}'+r'$_{\mathrm{Symp}}$',linewidth=3,color='#EA604D')
    
    #ax.axvline(x = 130,color='#929591',linewidth=1,linestyle="dashdot")
    
    ax.set_xlabel('\n', fontsize=18)

    ax.set_xticks(XNumber)
    ax.set_xticklabels(XDate)
    ax.xaxis.set_tick_params(labelsize=12)
    ax.set_yticks([0,1.0,2,3])
    ax.set_yticklabels(["0","0.01","0.02","0.03"])
    ax.yaxis.set_tick_params(labelsize=12)
    ax.set_ylim(0,3)

    ax2 = ax.twinx()
    ax2.scatter(X[31:],SymptomRate[31:],label=r'\textsc{Rate}'+r'$_{\mathrm{Symp}}$',marker='+',s=25,color='#000000')
    ax2.fill_between(X[31:],(SymptomRate[31:]-SymptomError[31:]),(SymptomRate[31:]+SymptomError[31:]),color='#000000',alpha=0.25)

    ax2.set_xticks(XNumber)
    ax2.set_xticklabels(XDate)
    ax2.xaxis.set_tick_params(labelsize=12)
    ax2.set_yticks([0,2,4,6,8])
    ax2.set_yticklabels(["0","0.02","0.04","0.06","0.08"])
    ax2.yaxis.set_tick_params(labelsize=12)
    ax2.set_ylim(0,8)

    plt.tight_layout()


    ### South Florida Fall, Mordecai Model

    future = 14
    
    DataFile = pd.read_csv("Florida-Mordecai-Fall/data.csv")
    ReportedSum = DataFile["cases"][0:31+future].to_list()
    Date = DataFile["date"][1:31+future].to_list()
    X = range(len(Date))

    Reported = []
    Reported.append(ReportedSum[0])
    for counter in range(1,len(ReportedSum)):
        Reported.append(ReportedSum[counter] - ReportedSum[counter-1])
    Reported = np.array(Reported[1:31+future])

    XNumber = [0,31]
    XDate = ["Oct 15\n","Nov 15\n"]
    
    DataFile = pd.read_csv("Florida-Mordecai-Fall/covidcast-fb-survey-smoothed_wcli-2020-04-06-to-2022-01-06.csv")

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
                SymptomRateNow = SymptomRateNow + SymptomRateList[counter]
                SymptomErrorNow = SymptomErrorNow + SymptomErrorList[counter]
            #SymptomRateNow = SymptomRateNow / np.sum(PopulationList)
            #SymptomErrorNow = SymptomErrorNow / np.sum(PopulationList)
            SymptomRate.append(SymptomRateNow)
            SymptomError.append(SymptomErrorNow)            
        else:
            SymptomRate.append(0)
            SymptomError.append(0)

    SymptomRate = np.array(SymptomRate)
    SymptomError = np.array(SymptomError)

    DataFile = pd.read_csv("Florida-Mordecai-Fall/result-original.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP = np.array(DataSelected["D_new_reported"].to_list()[1:31+future])
    UnreportedP = np.array(DataSelected["D_new_unreported"].to_list()[1:31+future])
    SymptomP = (np.array(DataSelected["Is"].to_list()[1:31+future]) + np.array(DataSelected["Im"].to_list()[1:31+future])) / 63453.45

    DataFile = pd.read_csv("Florida-Mordecai-Fall/result.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP = np.array(DataSelected["D_new_reported"].to_list()[1:31+future])
    UnreportedPP = np.array(DataSelected["D_new_unreported"].to_list()[1:31+future])
    SymptomPP = (np.array(DataSelected["Is"].to_list()[1:31+future]) + np.array(DataSelected["Im"].to_list()[1:31+future])) / 63453.45

    ax = plt.subplot(1,4,4)
    ax.set_title("\n", fontsize=12)

    ax.plot(X,SymptomP,label=r'\textsc{BaseParam}'+r'$_{\mathrm{Symp}}$',linewidth=3,color='#2166AC')
    ax.plot(X,SymptomPP,label=r'\textsc{MdlParam}'+r'$_{\mathrm{Symp}}$',linewidth=3,color='#EA604D')
    
    #ax.axvline(x = 130,color='#929591',linewidth=1,linestyle="dashdot")
    
    ax.set_xlabel('\n', fontsize=18)

    ax.set_xticks(XNumber)
    ax.set_xticklabels(XDate)
    ax.xaxis.set_tick_params(labelsize=12)
    ax.set_yticks([0,0.1,0.2,0.3,0.4,0.5])
    ax.set_yticklabels(["0","0.001","0.002","0.003","0.004","0.005"])
    ax.yaxis.set_tick_params(labelsize=12)
    ax.set_ylim(0,0.5)

    ax2 = ax.twinx()
    ax2.scatter(X,SymptomRate,label=r'\textsc{Rate}'+r'$_{\mathrm{Symp}}$',marker='+',s=25,color='#000000')
    ax2.fill_between(X,(SymptomRate-SymptomError),(SymptomRate+SymptomError),color='#000000',alpha=0.25)

    ax2.set_xticks(XNumber)
    ax2.set_xticklabels(XDate)
    ax2.xaxis.set_tick_params(labelsize=12)
    ax2.set_yticks([0,2,4,6,8,10])
    ax2.set_yticklabels(["0","0.02","0.04","0.06","0.08","0.1"])
    ax2.yaxis.set_tick_params(labelsize=12)
    ax2.set_ylim(0,10)

    plt.tight_layout()

    
    plt.figtext(x=0.02, y=0.95 ,s=r'$\textbf{a}$'+' Minneapolis-Spring-20',ha='left',va='center',fontsize=20)
    plt.figtext(x=0.27, y=0.95 ,s=r'$\textbf{b}$'+' Minneapolis-Fall-20',ha='left',va='center',fontsize=20)
    plt.figtext(x=0.52, y=0.95 ,s=r'$\textbf{c}$'+' South Florida-Spring-20',ha='left',va='center',fontsize=20)
    plt.figtext(x=0.77, y=0.95 ,s=r'$\textbf{d}$'+' South Florida-Fall-20',ha='left',va='center',fontsize=20)

    plt.tight_layout()

    plt.savefig('Figure4.pdf')
    plt.show()
