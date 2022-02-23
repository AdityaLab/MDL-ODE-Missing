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

    figure = plt.figure(figsize=(18,6))

    future = 14
    
    DataFile = pd.read_csv("Minneapolis-Mordecai/data.csv")
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

    DataFile = pd.read_csv("Minneapolis-Mordecai/result-original.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP = DataSelected["D_new_reported"].to_list()[25:67+future]
    UnreportedP = DataSelected["D_new_unreported"].to_list()[25:67+future]

    DataFile = pd.read_csv("Minneapolis-Mordecai/result-original-reported.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPR = DataSelected["D_new_reported"].to_list()[25:67+future]
    UnreportedPR = DataSelected["D_new_unreported"].to_list()[25:67+future]

    DataFile = pd.read_csv("Minneapolis-Mordecai/result-original-symptomatic.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPS = DataSelected["D_new_reported"].to_list()[25:67+future]
    UnreportedPS = DataSelected["D_new_unreported"].to_list()[25:67+future]

    DataFile = pd.read_csv("Minneapolis-Mordecai/result-original-0.25.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP25 = DataSelected["D_new_reported"].to_list()[25:67+future]
    UnreportedP25 = DataSelected["D_new_unreported"].to_list()[25:67+future]

    DataFile = pd.read_csv("Minneapolis-Mordecai/result-original-0.5.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP50 = DataSelected["D_new_reported"].to_list()[25:67+future]
    UnreportedP50 = DataSelected["D_new_unreported"].to_list()[25:67+future]

    DataFile = pd.read_csv("Minneapolis-Mordecai/result-original-0.75.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP75 = DataSelected["D_new_reported"].to_list()[25:67+future]
    UnreportedP75 = DataSelected["D_new_unreported"].to_list()[25:67+future]
    
    DataFile = pd.read_csv("Minneapolis-Mordecai/result.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP = DataSelected["D_new_reported"].to_list()[25:67+future]
    UnreportedPP = DataSelected["D_new_unreported"].to_list()[25:67+future]

    DataFile = pd.read_csv("Minneapolis-Mordecai/result-reported.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPPR = DataSelected["D_new_reported"].to_list()[25:67+future]
    UnreportedPPR = DataSelected["D_new_unreported"].to_list()[25:67+future]

    DataFile = pd.read_csv("Minneapolis-Mordecai/result-symptomatic.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPPS = DataSelected["D_new_reported"].to_list()[25:67+future]
    UnreportedPPS = DataSelected["D_new_unreported"].to_list()[25:67+future]

    DataFile = pd.read_csv("Minneapolis-Mordecai/result-0.25.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP25 = DataSelected["D_new_reported"].to_list()[25:67+future]
    UnreportedPP25 = DataSelected["D_new_unreported"].to_list()[25:67+future]

    DataFile = pd.read_csv("Minneapolis-Mordecai/result-0.5.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP50 = DataSelected["D_new_reported"].to_list()[25:67+future]
    UnreportedPP50 = DataSelected["D_new_unreported"].to_list()[25:67+future]

    DataFile = pd.read_csv("Minneapolis-Mordecai/result-0.75.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP75 = DataSelected["D_new_reported"].to_list()[25:67+future]
    UnreportedPP75 = DataSelected["D_new_unreported"].to_list()[25:67+future]
    
    plt.subplot(1,3,2)
    plt.title("Minneapolis (SEIR+HD) " + r'\textsc{BaseParam}'+" simulation", fontsize=14)

    plt.plot(X,ReportedP75,label="Isolate 75\% pre/asymptomatic infections",linewidth=3,color='#33CC33')
    plt.plot(X,ReportedP50,label="Isolate 50\% pre/asymptomatic infections",linewidth=3,color='#7BDE2F')
    plt.plot(X,ReportedP25,label="Isolate 25\% pre/asymptomatic infections",linewidth=3,color='#CDF224')
    plt.plot(X,ReportedPS,label="Isolate reported \& symptomatic infections",linewidth=3,color='#F8FD0F')
    plt.plot(X,ReportedPR,label="Isolate reported infections",linewidth=3,color='#FFFF00')
    plt.plot(X,ReportedP,label=r'\textsc{BaseParam}'+r'$_{\mathrm{Rinf}}$',linewidth=3,color='#2166AC')

    plt.axvline(x = 41,color='#929591',linewidth=1,linestyle="dashdot")

    plt.xlabel('(b)', fontsize=18)
    plt.ylabel('Reported infections', fontsize=18)

    plt.xticks(XNumber,XDate,fontsize=14)
    plt.yticks([0,50,100,150,200],fontsize=14)
    plt.ylim(0,200)

    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    plt.gca().yaxis.set_major_formatter(mf)
    plt.gca().yaxis.get_offset_text().set(size=14)
    
    plt.legend(fontsize=14)
    plt.tight_layout()
    
    plt.subplot(1,3,3)
    plt.title("Minneapolis (SEIR+HD) " + r'\textsc{MdlParam}'+" simulation", fontsize=14)

    plt.plot(X,ReportedPP75,label="Isolate 75\% pre/asymptomatic infections",linewidth=3,color='#33CC33')
    plt.plot(X,ReportedPP50,label="Isolate 50\% pre/asymptomatic infections",linewidth=3,color='#7BDE2F')
    plt.plot(X,ReportedPP25,label="Isolate 25\% pre/asymptomatic infections",linewidth=3,color='#CDF224')
    plt.plot(X,ReportedPPS,label="Isolate reported \& symptomatic infections",linewidth=3,color='#F8FD0F')
    plt.plot(X,ReportedPPR,label="Isolate reported infections",linewidth=3,color='#FFFF00')
    plt.plot(X,ReportedPP,label=r'\textsc{MdlParam}'+r'$_{\mathrm{Rinf}}$',linewidth=3,color='#EA604D')

    plt.axvline(x = 41,color='#929591',linewidth=1,linestyle="dashdot")

    plt.xlabel('(c)', fontsize=18)
    plt.ylabel('Reported infections', fontsize=18)

    plt.xticks(XNumber,XDate,fontsize=14)
    plt.yticks([0,50,100,150,200],fontsize=14)
    plt.ylim(0,200)

    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    plt.gca().yaxis.set_major_formatter(mf)
    plt.gca().yaxis.get_offset_text().set(size=14)
    
    plt.legend(fontsize=14)
    plt.tight_layout()

    plt.subplot(1,3,1)
    plt.title("Minneapolis (SEIR+HD) " + "cumulative reported rate", fontsize=14)

    plt.plot(X,np.array(ReportedSum)/np.cumsum(np.array(ReportedP)+np.array(UnreportedP)),label=r'\textsc{BaseParam}'+r'$_{\mathrm{Rate}}$',linewidth=3,color='#2166AC')
    plt.plot(X,np.array(ReportedSum)/np.cumsum(np.array(ReportedPP)+np.array(UnreportedPP)),label=r'\textsc{MdlParam}'+r'$_{\mathrm{Rate}}$',linewidth=3,color='#EA604D')

    plt.plot([48,48], [ReportedSum[49]/(38574.79*1.0), ReportedSum[49]/(38574.79*4.5)],linewidth=2,color='#000000',label=r'\textsc{SeroStudy}'+r'$_{\mathrm{Rate}}$')
    plt.scatter([48],[ReportedSum[49]/(38574.79*2.4)],s=50,color='#000000')
    plt.plot([47,49], [ReportedSum[49]/(38574.79*1.0), ReportedSum[49]/(38574.79*1.0)],linewidth=2,color='#000000')
    plt.plot([47,49], [ReportedSum[49]/(38574.79*4.5), ReportedSum[49]/(38574.79*4.5)],linewidth=2,color='#000000')

    plt.axvline(x = 41,color='#929591',linewidth=1,linestyle="dashdot")

    plt.xlabel('(a)', fontsize=18)
    plt.ylabel('Cumulative reported rate', fontsize=18)

    plt.xticks(XNumber,XDate,fontsize=14)
    plt.yticks([0,0.05,0.10,0.15,0.20],fontsize=14)
    plt.ylim(0,0.2)

    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    plt.gca().yaxis.set_major_formatter(mf)
    plt.gca().yaxis.get_offset_text().set(size=14)
    
    plt.legend(fontsize=14)
    plt.tight_layout()

    plt.savefig('Figure5.pdf')
    plt.show()
