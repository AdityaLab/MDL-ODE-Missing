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

    figure = plt.figure(figsize=(18,10.5))#(10.24*3,8.96*2))

    ### Minneapolis 0.4

    future = 14
    
    DataFile = pd.read_csv("0.5/data.csv")
    ReportedSum = DataFile["cases"][0:42+future].to_list()
    Date = DataFile["date"][0:42+future].to_list()
    X = range(len(Date))

    Reported = []
    Reported.append(ReportedSum[0])
    for counter in range(1,len(ReportedSum)):
        Reported.append(ReportedSum[counter] - ReportedSum[counter-1])
    Reported = np.array(Reported)

    XNumber = [26,56]
    XDate = ["Apr 1","May 1"]
    
    DataFile = pd.read_csv("0.4/result-original.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP = np.array(DataSelected["D_new_reported"].to_list()[25:67+future])
    UnreportedP = np.array(DataSelected["D_new_unreported"].to_list()[25:67+future])

    DataFile = pd.read_csv("0.4/result-original-reported.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPR = np.array(DataSelected["D_new_reported"].to_list()[25:67+future])
    UnreportedPR = np.array(DataSelected["D_new_unreported"].to_list()[25:67+future])

    DataFile = pd.read_csv("0.4/result-original-symptomatic.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPS = np.array(DataSelected["D_new_reported"].to_list()[25:67+future])
    UnreportedPS = np.array(DataSelected["D_new_unreported"].to_list()[25:67+future])

    DataFile = pd.read_csv("0.4/result-original-0.25.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP25 = np.array(DataSelected["D_new_reported"].to_list()[25:67+future])
    UnreportedP25 = np.array(DataSelected["D_new_unreported"].to_list()[25:67+future])

    DataFile = pd.read_csv("0.4/result-original-0.5.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP50 = np.array(DataSelected["D_new_reported"].to_list()[25:67+future])
    UnreportedP50 = np.array(DataSelected["D_new_unreported"].to_list()[25:67+future])

    DataFile = pd.read_csv("0.4/result-original-0.75.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP75 = np.array(DataSelected["D_new_reported"].to_list()[25:67+future])
    UnreportedP75 = np.array(DataSelected["D_new_unreported"].to_list()[25:67+future])
    
    DataFile = pd.read_csv("0.4/result.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP = np.array(DataSelected["D_new_reported"].to_list()[25:67+future])
    UnreportedPP = np.array(DataSelected["D_new_unreported"].to_list()[25:67+future])

    DataFile = pd.read_csv("0.4/result-reported.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPPR = np.array(DataSelected["D_new_reported"].to_list()[25:67+future])
    UnreportedPPR = np.array(DataSelected["D_new_unreported"].to_list()[25:67+future])

    DataFile = pd.read_csv("0.4/result-symptomatic.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPPS = np.array(DataSelected["D_new_reported"].to_list()[25:67+future])
    UnreportedPPS = np.array(DataSelected["D_new_unreported"].to_list()[25:67+future])

    DataFile = pd.read_csv("0.4/result-0.25.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP25 = np.array(DataSelected["D_new_reported"].to_list()[25:67+future])
    UnreportedPP25 = np.array(DataSelected["D_new_unreported"].to_list()[25:67+future])

    DataFile = pd.read_csv("0.4/result-0.5.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP50 = np.array(DataSelected["D_new_reported"].to_list()[25:67+future])
    UnreportedPP50 = np.array(DataSelected["D_new_unreported"].to_list()[25:67+future])

    DataFile = pd.read_csv("0.4/result-0.75.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP75 = np.array(DataSelected["D_new_reported"].to_list()[25:67+future])
    UnreportedPP75 = np.array(DataSelected["D_new_unreported"].to_list()[25:67+future])
    
    plt.subplot(2,3,1)
    plt.title(r'\textsc{BaseParam}'+" Simulation Reduction: 0.4", fontsize=16)

    plt.plot(X,ReportedP75,label="Isolate 75\% pre/asymptomatic infections",linewidth=3,color='#33CC33')
    plt.plot(X,ReportedP50,label="Isolate 50\% pre/asymptomatic infections",linewidth=3,color='#7BDE2F')
    plt.plot(X,ReportedP25,label="Isolate 25\% pre/asymptomatic infections",linewidth=3,color='#CDF224')
    plt.plot(X,ReportedPS,label="Isolate reported \& symptomatic infections",linewidth=3,color='#F8FD0F')
    plt.plot(X,ReportedPR,label="Isolate reported infections",linewidth=3,color='#FFFF00')
    plt.plot(X,ReportedP,label=r'\textsc{BaseParam}'+r'$_{\mathrm{Rinf}}$',linewidth=3,color='#2166AC')

    plt.axvline(x = 41,color='#929591',linewidth=1,linestyle="dashdot")

    plt.xlabel('(a)', fontsize=22)
    plt.ylabel('Reported infections', fontsize=20)

    plt.xticks(XNumber,XDate,fontsize=16)
    plt.yticks([0,50,100,150,200],fontsize=16)
    plt.ylim(0,200)

    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    plt.gca().yaxis.set_major_formatter(mf)
    plt.gca().yaxis.get_offset_text().set(size=16)
    
    plt.legend(fontsize=16)
    plt.tight_layout()
    
    plt.subplot(2,3,4)
    plt.title(r'\textsc{MdlParam}'+" Simulation Reduction: 0.4", fontsize=16)

    plt.plot(X,ReportedPP75,label="Isolate 75\% pre/asymptomatic infections",linewidth=3,color='#33CC33')
    plt.plot(X,ReportedPP50,label="Isolate 50\% pre/asymptomatic infections",linewidth=3,color='#7BDE2F')
    plt.plot(X,ReportedPP25,label="Isolate 25\% pre/asymptomatic infections",linewidth=3,color='#CDF224')
    plt.plot(X,ReportedPPS,label="Isolate reported \& symptomatic infections",linewidth=3,color='#F8FD0F')
    plt.plot(X,ReportedPPR,label="Isolate reported infections",linewidth=3,color='#FFFF00')
    plt.plot(X,ReportedPP,label=r'\textsc{MdlParam}'+r'$_{\mathrm{Rinf}}$',linewidth=3,color='#EA604D')

    plt.axvline(x = 41,color='#929591',linewidth=1,linestyle="dashdot")

    plt.xlabel('(d)', fontsize=22)
    plt.ylabel('Reported infections', fontsize=20)

    plt.xticks(XNumber,XDate,fontsize=16)
    plt.yticks([0,50,100,150,200],fontsize=16)
    plt.ylim(0,200)

    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    plt.gca().yaxis.set_major_formatter(mf)
    plt.gca().yaxis.get_offset_text().set(size=16)
    
    plt.legend(fontsize=16)
    plt.tight_layout()

    ### Minneapolis 0.5

    future = 14
    
    DataFile = pd.read_csv("0.5/data.csv")
    ReportedSum = DataFile["cases"][0:42+future].to_list()
    Date = DataFile["date"][0:42+future].to_list()
    X = range(len(Date))

    Reported = []
    Reported.append(ReportedSum[0])
    for counter in range(1,len(ReportedSum)):
        Reported.append(ReportedSum[counter] - ReportedSum[counter-1])
    Reported = np.array(Reported)

    XNumber = [26,56]
    XDate = ["Apr 1","May 1"]
    
    DataFile = pd.read_csv("0.5/result-original.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP = np.array(DataSelected["D_new_reported"].to_list()[25:67+future])
    UnreportedP = np.array(DataSelected["D_new_unreported"].to_list()[25:67+future])

    DataFile = pd.read_csv("0.5/result-original-reported.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPR = np.array(DataSelected["D_new_reported"].to_list()[25:67+future])
    UnreportedPR = np.array(DataSelected["D_new_unreported"].to_list()[25:67+future])

    DataFile = pd.read_csv("0.5/result-original-symptomatic.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPS = np.array(DataSelected["D_new_reported"].to_list()[25:67+future])
    UnreportedPS = np.array(DataSelected["D_new_unreported"].to_list()[25:67+future])

    DataFile = pd.read_csv("0.5/result-original-0.25.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP25 = np.array(DataSelected["D_new_reported"].to_list()[25:67+future])
    UnreportedP25 = np.array(DataSelected["D_new_unreported"].to_list()[25:67+future])

    DataFile = pd.read_csv("0.5/result-original-0.5.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP50 = np.array(DataSelected["D_new_reported"].to_list()[25:67+future])
    UnreportedP50 = np.array(DataSelected["D_new_unreported"].to_list()[25:67+future])

    DataFile = pd.read_csv("0.5/result-original-0.75.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP75 = np.array(DataSelected["D_new_reported"].to_list()[25:67+future])
    UnreportedP75 = np.array(DataSelected["D_new_unreported"].to_list()[25:67+future])
    
    DataFile = pd.read_csv("0.5/result.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP = np.array(DataSelected["D_new_reported"].to_list()[25:67+future])
    UnreportedPP = np.array(DataSelected["D_new_unreported"].to_list()[25:67+future])

    DataFile = pd.read_csv("0.5/result-reported.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPPR = np.array(DataSelected["D_new_reported"].to_list()[25:67+future])
    UnreportedPPR = np.array(DataSelected["D_new_unreported"].to_list()[25:67+future])

    DataFile = pd.read_csv("0.5/result-symptomatic.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPPS = np.array(DataSelected["D_new_reported"].to_list()[25:67+future])
    UnreportedPPS = np.array(DataSelected["D_new_unreported"].to_list()[25:67+future])

    DataFile = pd.read_csv("0.5/result-0.25.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP25 = np.array(DataSelected["D_new_reported"].to_list()[25:67+future])
    UnreportedPP25 = np.array(DataSelected["D_new_unreported"].to_list()[25:67+future])

    DataFile = pd.read_csv("0.5/result-0.5.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP50 = np.array(DataSelected["D_new_reported"].to_list()[25:67+future])
    UnreportedPP50 = np.array(DataSelected["D_new_unreported"].to_list()[25:67+future])

    DataFile = pd.read_csv("0.5/result-0.75.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP75 = np.array(DataSelected["D_new_reported"].to_list()[25:67+future])
    UnreportedPP75 = np.array(DataSelected["D_new_unreported"].to_list()[25:67+future])
    
    plt.subplot(2,3,2)
    plt.title(r'\textsc{BaseParam}'+" Simulation Reduction: 0.5", fontsize=16)

    plt.plot(X,ReportedP75,label="Isolate 75\% pre/asymptomatic infections",linewidth=3,color='#33CC33')
    plt.plot(X,ReportedP50,label="Isolate 50\% pre/asymptomatic infections",linewidth=3,color='#7BDE2F')
    plt.plot(X,ReportedP25,label="Isolate 25\% pre/asymptomatic infections",linewidth=3,color='#CDF224')
    plt.plot(X,ReportedPS,label="Isolate reported \& symptomatic infections",linewidth=3,color='#F8FD0F')
    plt.plot(X,ReportedPR,label="Isolate reported infections",linewidth=3,color='#FFFF00')
    plt.plot(X,ReportedP,label=r'\textsc{BaseParam}'+r'$_{\mathrm{Rinf}}$',linewidth=3,color='#2166AC')

    plt.axvline(x = 41,color='#929591',linewidth=1,linestyle="dashdot")

    plt.xlabel('(b)', fontsize=22)
    #plt.ylabel('Reported infections', fontsize=16)

    plt.xticks(XNumber,XDate,fontsize=16)
    plt.yticks([0,50,100,150,200],fontsize=16)
    plt.ylim(0,200)

    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    plt.gca().yaxis.set_major_formatter(mf)
    plt.gca().yaxis.get_offset_text().set(size=16)
    
    #plt.legend(fontsize=16)
    plt.tight_layout()
    
    plt.subplot(2,3,5)
    plt.title(r'\textsc{MdlParam}'+" Simulation Reduction: 0.5", fontsize=16)

    plt.plot(X,ReportedPP75,label="Isolate 75\% pre/asymptomatic infections",linewidth=3,color='#33CC33')
    plt.plot(X,ReportedPP50,label="Isolate 50\% pre/asymptomatic infections",linewidth=3,color='#7BDE2F')
    plt.plot(X,ReportedPP25,label="Isolate 25\% pre/asymptomatic infections",linewidth=3,color='#CDF224')
    plt.plot(X,ReportedPPS,label="Isolate reported \& symptomatic infections",linewidth=3,color='#F8FD0F')
    plt.plot(X,ReportedPPR,label="Isolate reported infections",linewidth=3,color='#FFFF00')
    plt.plot(X,ReportedPP,label=r'\textsc{MdlParam}'+r'$_{\mathrm{Rinf}}$',linewidth=3,color='#EA604D')

    plt.axvline(x = 41,color='#929591',linewidth=1,linestyle="dashdot")

    plt.xlabel('(e)', fontsize=22)
    #plt.ylabel('Reported infections', fontsize=16)

    plt.xticks(XNumber,XDate,fontsize=16)
    plt.yticks([0,50,100,150,200],fontsize=16)
    plt.ylim(0,200)

    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    plt.gca().yaxis.set_major_formatter(mf)
    plt.gca().yaxis.get_offset_text().set(size=16)
    
    #plt.legend(fontsize=16)
    plt.tight_layout()

    ### Minneapolis 0.6

    future = 14
    
    DataFile = pd.read_csv("0.5/data.csv")
    ReportedSum = DataFile["cases"][0:42+future].to_list()
    Date = DataFile["date"][0:42+future].to_list()
    X = range(len(Date))

    Reported = []
    Reported.append(ReportedSum[0])
    for counter in range(1,len(ReportedSum)):
        Reported.append(ReportedSum[counter] - ReportedSum[counter-1])
    Reported = np.array(Reported)

    XNumber = [26,56]
    XDate = ["Apr 1","May 1"]
    
    DataFile = pd.read_csv("0.6/result-original.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP = np.array(DataSelected["D_new_reported"].to_list()[25:67+future])
    UnreportedP = np.array(DataSelected["D_new_unreported"].to_list()[25:67+future])

    DataFile = pd.read_csv("0.6/result-original-reported.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPR = np.array(DataSelected["D_new_reported"].to_list()[25:67+future])
    UnreportedPR = np.array(DataSelected["D_new_unreported"].to_list()[25:67+future])

    DataFile = pd.read_csv("0.6/result-original-symptomatic.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPS = np.array(DataSelected["D_new_reported"].to_list()[25:67+future])
    UnreportedPS = np.array(DataSelected["D_new_unreported"].to_list()[25:67+future])

    DataFile = pd.read_csv("0.6/result-original-0.25.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP25 = np.array(DataSelected["D_new_reported"].to_list()[25:67+future])
    UnreportedP25 = np.array(DataSelected["D_new_unreported"].to_list()[25:67+future])

    DataFile = pd.read_csv("0.6/result-original-0.5.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP50 = np.array(DataSelected["D_new_reported"].to_list()[25:67+future])
    UnreportedP50 = np.array(DataSelected["D_new_unreported"].to_list()[25:67+future])

    DataFile = pd.read_csv("0.6/result-original-0.75.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP75 = np.array(DataSelected["D_new_reported"].to_list()[25:67+future])
    UnreportedP75 = np.array(DataSelected["D_new_unreported"].to_list()[25:67+future])
    
    DataFile = pd.read_csv("0.6/result.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP = np.array(DataSelected["D_new_reported"].to_list()[25:67+future])
    UnreportedPP = np.array(DataSelected["D_new_unreported"].to_list()[25:67+future])

    DataFile = pd.read_csv("0.6/result-reported.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPPR = np.array(DataSelected["D_new_reported"].to_list()[25:67+future])
    UnreportedPPR = np.array(DataSelected["D_new_unreported"].to_list()[25:67+future])

    DataFile = pd.read_csv("0.6/result-symptomatic.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPPS = np.array(DataSelected["D_new_reported"].to_list()[25:67+future])
    UnreportedPPS = np.array(DataSelected["D_new_unreported"].to_list()[25:67+future])

    DataFile = pd.read_csv("0.6/result-0.25.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP25 = np.array(DataSelected["D_new_reported"].to_list()[25:67+future])
    UnreportedPP25 = np.array(DataSelected["D_new_unreported"].to_list()[25:67+future])

    DataFile = pd.read_csv("0.6/result-0.5.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP50 = np.array(DataSelected["D_new_reported"].to_list()[25:67+future])
    UnreportedPP50 = np.array(DataSelected["D_new_unreported"].to_list()[25:67+future])

    DataFile = pd.read_csv("0.6/result-0.75.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP75 = np.array(DataSelected["D_new_reported"].to_list()[25:67+future])
    UnreportedPP75 = np.array(DataSelected["D_new_unreported"].to_list()[25:67+future])
    
    plt.subplot(2,3,3)
    plt.title(r'\textsc{BaseParam}'+" Simulation Reduction: 0.6", fontsize=16)

    plt.plot(X,ReportedP75,label="Isolate 75\% pre/asymptomatic infections",linewidth=3,color='#33CC33')
    plt.plot(X,ReportedP50,label="Isolate 50\% pre/asymptomatic infections",linewidth=3,color='#7BDE2F')
    plt.plot(X,ReportedP25,label="Isolate 25\% pre/asymptomatic infections",linewidth=3,color='#CDF224')
    plt.plot(X,ReportedPS,label="Isolate reported \& symptomatic infections",linewidth=3,color='#F8FD0F')
    plt.plot(X,ReportedPR,label="Isolate reported infections",linewidth=3,color='#FFFF00')
    plt.plot(X,ReportedP,label=r'\textsc{BaseParam}'+r'$_{\mathrm{Rinf}}$',linewidth=3,color='#2166AC')

    plt.axvline(x = 41,color='#929591',linewidth=1,linestyle="dashdot")

    plt.xlabel('(c)', fontsize=22)
    #plt.ylabel('Reported infections', fontsize=16)

    plt.xticks(XNumber,XDate,fontsize=16)
    plt.yticks([0,50,100,150,200],fontsize=16)
    plt.ylim(0,200)

    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    plt.gca().yaxis.set_major_formatter(mf)
    plt.gca().yaxis.get_offset_text().set(size=16)
    
    #plt.legend(fontsize=16)
    plt.tight_layout()
    
    plt.subplot(2,3,6)
    plt.title(r'\textsc{MdlParam}'+" Simulation Reduction: 0.6", fontsize=16)

    plt.plot(X,ReportedPP75,label="Isolate 75\% pre/asymptomatic infections",linewidth=3,color='#33CC33')
    plt.plot(X,ReportedPP50,label="Isolate 50\% pre/asymptomatic infections",linewidth=3,color='#7BDE2F')
    plt.plot(X,ReportedPP25,label="Isolate 25\% pre/asymptomatic infections",linewidth=3,color='#CDF224')
    plt.plot(X,ReportedPPS,label="Isolate reported \& symptomatic infections",linewidth=3,color='#F8FD0F')
    plt.plot(X,ReportedPPR,label="Isolate reported infections",linewidth=3,color='#FFFF00')
    plt.plot(X,ReportedPP,label=r'\textsc{MdlParam}'+r'$_{\mathrm{Rinf}}$',linewidth=3,color='#EA604D')

    plt.axvline(x = 41,color='#929591',linewidth=1,linestyle="dashdot")

    plt.xlabel('(f)', fontsize=22)
    #plt.ylabel('Reported infections', fontsize=16)

    plt.xticks(XNumber,XDate,fontsize=16)
    plt.yticks([0,50,100,150,200],fontsize=16)
    plt.ylim(0,200)

    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    plt.gca().yaxis.set_major_formatter(mf)
    plt.gca().yaxis.get_offset_text().set(size=16)
    
    #plt.legend(fontsize=16)
    plt.tight_layout()

    plt.savefig('Minneapolis.pdf')
    plt.show()
