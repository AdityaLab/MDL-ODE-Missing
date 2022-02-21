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

if __name__ == "__main__":

    figure = plt.figure(figsize=(18,16))#(10.24*3,8.96*2))

    ### Philadelphia Metro Area

    future = 14
    
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
    
    DataFile = pd.read_csv("Philadelphia/result-original.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP = np.array(DataSelected["D_new_reported"].to_list()[:49+future])
    UnreportedP = np.array(DataSelected["D_new_unreported"].to_list()[:49+future])

    DataFile = pd.read_csv("Philadelphia/result-original-reported.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPR = np.array(DataSelected["D_new_reported"].to_list()[:49+future])
    UnreportedPR = np.array(DataSelected["D_new_unreported"].to_list()[:49+future])

    DataFile = pd.read_csv("Philadelphia/result-original-symptomatic.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPS = np.array(DataSelected["D_new_reported"].to_list()[:49+future])
    UnreportedPS = np.array(DataSelected["D_new_unreported"].to_list()[:49+future])

    DataFile = pd.read_csv("Philadelphia/result-original-0.25.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP25 = np.array(DataSelected["D_new_reported"].to_list()[:49+future])
    UnreportedP25 = np.array(DataSelected["D_new_unreported"].to_list()[:49+future])

    DataFile = pd.read_csv("Philadelphia/result-original-0.5.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP50 = np.array(DataSelected["D_new_reported"].to_list()[:49+future])
    UnreportedP50 = np.array(DataSelected["D_new_unreported"].to_list()[:49+future])

    DataFile = pd.read_csv("Philadelphia/result-original-0.75.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP75 = np.array(DataSelected["D_new_reported"].to_list()[:49+future])
    UnreportedP75 = np.array(DataSelected["D_new_unreported"].to_list()[:49+future])
    
    DataFile = pd.read_csv("Philadelphia/result.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP = np.array(DataSelected["D_new_reported"].to_list()[:49+future])
    UnreportedPP = np.array(DataSelected["D_new_unreported"].to_list()[:49+future])

    DataFile = pd.read_csv("Philadelphia/result-reported.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPPR = np.array(DataSelected["D_new_reported"].to_list()[:49+future])
    UnreportedPPR = np.array(DataSelected["D_new_unreported"].to_list()[:49+future])

    DataFile = pd.read_csv("Philadelphia/result-symptomatic.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPPS = np.array(DataSelected["D_new_reported"].to_list()[:49+future])
    UnreportedPPS = np.array(DataSelected["D_new_unreported"].to_list()[:49+future])

    DataFile = pd.read_csv("Philadelphia/result-0.25.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP25 = np.array(DataSelected["D_new_reported"].to_list()[:49+future])
    UnreportedPP25 = np.array(DataSelected["D_new_unreported"].to_list()[:49+future])

    DataFile = pd.read_csv("Philadelphia/result-0.5.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP50 = np.array(DataSelected["D_new_reported"].to_list()[:49+future])
    UnreportedPP50 = np.array(DataSelected["D_new_unreported"].to_list()[:49+future])

    DataFile = pd.read_csv("Philadelphia/result-0.75.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP75 = np.array(DataSelected["D_new_reported"].to_list()[:49+future])
    UnreportedPP75 = np.array(DataSelected["D_new_unreported"].to_list()[:49+future])
    
    plt.subplot(2,2,1)
    plt.title('Philadelphia (SEIR+HD) '+r'\textsc{BaseParam}'+" Simulation", fontsize=20)

    plt.plot(X,ReportedP75,label="Isolate 75\% pre/asymptomatic infections",linewidth=3,color='#33CC33')
    plt.plot(X,ReportedP50,label="Isolate 50\% pre/asymptomatic infections",linewidth=3,color='#7BDE2F')
    plt.plot(X,ReportedP25,label="Isolate 25\% pre/asymptomatic infections",linewidth=3,color='#CDF224')
    plt.plot(X,ReportedPS,label="Isolate reported \& symptomatic infections",linewidth=3,color='#F8FD0F')
    plt.plot(X,ReportedPR,label="Isolate reported infections",linewidth=3,color='#FFFF00')
    plt.plot(X,ReportedP,label=r'\textsc{BaseParam}'+r'$_{\mathrm{Rinf}}$',linewidth=3,color='#2166AC')

    plt.axvline(x = 48,color='#929591',linewidth=1,linestyle="dashdot")
    #plt.text(48-2,1,'Training Data',color='#FF6100',horizontalalignment='right')
    #plt.text(48+2,1,'Testing Data',color='#FF6100',horizontalalignment='left')

    plt.xlabel('(a)', fontsize=22)
    plt.ylabel('Reported infections', fontsize=24)

    plt.xticks(XNumber,XDate,fontsize=18)
    plt.yticks([0,200,400,600,800,1000],fontsize=18)
    plt.ylim(0,1000)

    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    plt.gca().yaxis.set_major_formatter(mf)
    plt.gca().yaxis.get_offset_text().set(size=18)
    
    plt.legend(fontsize=20)
    plt.tight_layout()
    
    plt.subplot(2,2,2)
    plt.title('Philadelphia (SEIR+HD) '+r'\textsc{MdlParam}'+" Simulation", fontsize=20)

    plt.plot(X,ReportedPP75,label="Isolate 75\% pre/asymptomatic infections",linewidth=3,color='#33CC33')
    plt.plot(X,ReportedPP50,label="Isolate 50\% pre/asymptomatic infections",linewidth=3,color='#7BDE2F')
    plt.plot(X,ReportedPP25,label="Isolate 25\% pre/asymptomatic infections",linewidth=3,color='#CDF224')
    plt.plot(X,ReportedPPS,label="Isolate reported \& symptomatic infections",linewidth=3,color='#F8FD0F')
    plt.plot(X,ReportedPPR,label="Isolate reported infections",linewidth=3,color='#FFFF00')
    plt.plot(X,ReportedPP,label=r'\textsc{MdlParam}'+r'$_{\mathrm{Rinf}}$',linewidth=3,color='#EA604D')

    plt.axvline(x = 48,color='#929591',linewidth=1,linestyle="dashdot")
    #plt.text(48-2,1,'Training Data',color='#FF6100',horizontalalignment='right')
    #plt.text(48+2,1,'Testing Data',color='#FF6100',horizontalalignment='left')

    plt.xlabel('(b)', fontsize=22)
    #plt.ylabel('Reported infections', fontsize=18)

    plt.xticks(XNumber,XDate,fontsize=18)
    plt.yticks([0,200,400,600,800,1000],fontsize=18)
    plt.ylim(0,1000)

    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    plt.gca().yaxis.set_major_formatter(mf)
    plt.gca().yaxis.get_offset_text().set(size=18)
    
    plt.legend(fontsize=20)
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
    
    DataFile = pd.read_csv("Washington/result-original.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP = np.array(DataSelected["D_new_reported"].to_list()[:45+future])
    UnreportedP = np.array(DataSelected["D_new_unreported"].to_list()[:45+future])

    DataFile = pd.read_csv("Washington/result-original-reported.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPR = np.array(DataSelected["D_new_reported"].to_list()[:45+future])
    UnreportedPR = np.array(DataSelected["D_new_unreported"].to_list()[:45+future])

    DataFile = pd.read_csv("Washington/result-original-symptomatic.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPS = np.array(DataSelected["D_new_reported"].to_list()[:45+future])
    UnreportedPS = np.array(DataSelected["D_new_unreported"].to_list()[:45+future])

    DataFile = pd.read_csv("Washington/result-original-0.25.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP25 = np.array(DataSelected["D_new_reported"].to_list()[:45+future])
    UnreportedP25 = np.array(DataSelected["D_new_unreported"].to_list()[:45+future])

    DataFile = pd.read_csv("Washington/result-original-0.5.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP50 = np.array(DataSelected["D_new_reported"].to_list()[:45+future])
    UnreportedP50 = np.array(DataSelected["D_new_unreported"].to_list()[:45+future])

    DataFile = pd.read_csv("Washington/result-original-0.75.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP75 = np.array(DataSelected["D_new_reported"].to_list()[:45+future])
    UnreportedP75 = np.array(DataSelected["D_new_unreported"].to_list()[:45+future])
    
    DataFile = pd.read_csv("Washington/result.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP = np.array(DataSelected["D_new_reported"].to_list()[:45+future])
    UnreportedPP = np.array(DataSelected["D_new_unreported"].to_list()[:45+future])

    DataFile = pd.read_csv("Washington/result-reported.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPPR = np.array(DataSelected["D_new_reported"].to_list()[:45+future])
    UnreportedPPR = np.array(DataSelected["D_new_unreported"].to_list()[:45+future])

    DataFile = pd.read_csv("Washington/result-symptomatic.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPPS = np.array(DataSelected["D_new_reported"].to_list()[:45+future])
    UnreportedPPS = np.array(DataSelected["D_new_unreported"].to_list()[:45+future])

    DataFile = pd.read_csv("Washington/result-0.25.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP25 = np.array(DataSelected["D_new_reported"].to_list()[:45+future])
    UnreportedPP25 = np.array(DataSelected["D_new_unreported"].to_list()[:45+future])

    DataFile = pd.read_csv("Washington/result-0.5.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP50 = np.array(DataSelected["D_new_reported"].to_list()[:45+future])
    UnreportedPP50 = np.array(DataSelected["D_new_unreported"].to_list()[:45+future])

    DataFile = pd.read_csv("Washington/result-0.75.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP75 = np.array(DataSelected["D_new_reported"].to_list()[:45+future])
    UnreportedPP75 = np.array(DataSelected["D_new_unreported"].to_list()[:45+future])
    
    plt.subplot(2,2,3)
    plt.title('Western Washington (SEIR+HD) '+r'\textsc{BaseParam}'+" Simulation", fontsize=20)

    plt.plot(X,ReportedP75,label="Isolate 75\% pre/asymptomatic infections",linewidth=3,color='#33CC33')
    plt.plot(X,ReportedP50,label="Isolate 50\% pre/asymptomatic infections",linewidth=3,color='#7BDE2F')
    plt.plot(X,ReportedP25,label="Isolate 25\% pre/asymptomatic infections",linewidth=3,color='#CDF224')
    plt.plot(X,ReportedPS,label="Isolate reported \& symptomatic infections",linewidth=3,color='#F8FD0F')
    plt.plot(X,ReportedPR,label="Isolate reported infections",linewidth=3,color='#FFFF00')
    plt.plot(X,ReportedP,label=r'\textsc{BaseParam}'+r'$_{\mathrm{Rinf}}$',linewidth=3,color='#2166AC')

    plt.axvline(x = 44,color='#929591',linewidth=1,linestyle="dashdot")
    #plt.text(36-2,1,'Training Data',color='#FF6100',horizontalalignment='right')
    #plt.text(36+2,1,'Testing Data',color='#FF6100',horizontalalignment='left')

    plt.xlabel('(c)', fontsize=22)
    plt.ylabel('Reported infections', fontsize=24)

    plt.xticks(XNumber,XDate,fontsize=16)
    plt.yticks([0,200,400,600,800],fontsize=16)
    plt.ylim(0,800)

    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    plt.gca().yaxis.set_major_formatter(mf)
    plt.gca().yaxis.get_offset_text().set(size=18)
    
    #plt.legend(fontsize=18)
    plt.tight_layout()
    
    plt.subplot(2,2,4)
    plt.title('Western Washington (SEIR+HD) '+r'\textsc{MdlParam}'+" Simulation", fontsize=20)

    plt.plot(X,ReportedPP75,label="Isolate 75\% pre/asymptomatic infections",linewidth=3,color='#33CC33')
    plt.plot(X,ReportedPP50,label="Isolate 50\% pre/asymptomatic infections",linewidth=3,color='#7BDE2F')
    plt.plot(X,ReportedPP25,label="Isolate 25\% pre/asymptomatic infections",linewidth=3,color='#CDF224')
    plt.plot(X,ReportedPPS,label="Isolate reported \& symptomatic infections",linewidth=3,color='#F8FD0F')
    plt.plot(X,ReportedPPR,label="Isolate reported infections",linewidth=3,color='#FFFF00')
    plt.plot(X,ReportedPP,label=r'\textsc{MdlParam}'+r'$_{\mathrm{Rinf}}$',linewidth=3,color='#EA604D')

    plt.axvline(x = 44,color='#929591',linewidth=1,linestyle="dashdot")
    #plt.text(36-2,1,'Training Data',color='#FF6100',horizontalalignment='right')
    #plt.text(36+2,1,'Testing Data',color='#FF6100',horizontalalignment='left')

    plt.xlabel('(d)', fontsize=22)
    #plt.ylabel('Reported infections', fontsize=18)

    plt.xticks(XNumber,XDate,fontsize=16)
    plt.yticks([0,200,400,600,800],fontsize=16)
    plt.ylim(0,800)

    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    plt.gca().yaxis.set_major_formatter(mf)
    plt.gca().yaxis.get_offset_text().set(size=18)
    
    #plt.legend(fontsize=18)
    plt.tight_layout()

    plt.savefig('NPI.pdf')
    plt.show()
