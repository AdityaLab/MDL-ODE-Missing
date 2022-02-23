from mpl_toolkits.axes_grid1.inset_locator import mark_inset
import matplotlib.lines as lines
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

    TrainingRMSEP = []
    TrainingRMSEPP = []
    TestingRMSEP = []
    TestingRMSEPP = []

    figure = plt.figure(figsize=(18,7.2))

    ### Minneapolis Metro Area, Nature Model

    future = 14
    
    DataFile = pd.read_csv("Minneapolis-Nature/data.csv")
    ReportedSum = DataFile["cases"][0:131+future].to_list()
    Date = DataFile["date"][0:131+future].to_list()
    X = range(len(Date))

    Reported = []
    Reported.append(ReportedSum[0])
    for counter in range(1,len(ReportedSum)):
        Reported.append(ReportedSum[counter] - ReportedSum[counter-1])
    Reported = np.array(Reported)

    XNumber = [26,56,87,117]
    XDate = ["Apr 1","May 1","Jun 1","Jul 1"]
    
    DataFile = pd.read_csv("Minneapolis-Nature/result-original-1.csv")
    ReportedP1 = DataFile["Onset_expect"].to_list()[:42+future]
    UnreportedP1 = DataFile["Onset_unreported_expect"].to_list()[:42+future]
    
    DataFile = pd.read_csv("Minneapolis-Nature/result-original-2.csv")
    ReportedP2 = DataFile["Onset_expect"].to_list()[:33+future]
    UnreportedP2 = DataFile["Onset_unreported_expect"].to_list()[:33+future]
    
    DataFile = pd.read_csv("Minneapolis-Nature/result-original-3.csv")
    ReportedP3 = DataFile["Onset_expect"].to_list()[:32+future]
    UnreportedP3 = DataFile["Onset_unreported_expect"].to_list()[:32+future]
    
    DataFile = pd.read_csv("Minneapolis-Nature/result-original-4.csv")
    ReportedP4 = DataFile["Onset_expect"].to_list()[:24+future]
    UnreportedP4 = DataFile["Onset_unreported_expect"].to_list()[:24+future]
    
    ReportedP = np.array(ReportedP1[:42] + ReportedP2[:33] + ReportedP3[:32] + ReportedP4[:24+future])
    UnreportedP = np.array(UnreportedP1[:42] + UnreportedP2[:33] + UnreportedP3[:32] + UnreportedP4[:24+future])
    
    DataFile = pd.read_csv("Minneapolis-Nature/result-1.csv")
    ReportedPP1 = DataFile["Onset_expect"].to_list()[:42+future]
    UnreportedPP1 = DataFile["Onset_unreported_expect"].to_list()[:42+future]
    
    DataFile = pd.read_csv("Minneapolis-Nature/result-2.csv")
    ReportedPP2 = DataFile["Onset_expect"].to_list()[:33+future]
    UnreportedPP2 = DataFile["Onset_unreported_expect"].to_list()[:33+future]
    
    DataFile = pd.read_csv("Minneapolis-Nature/result-3.csv")
    ReportedPP3 = DataFile["Onset_expect"].to_list()[:32+future]
    UnreportedPP3 = DataFile["Onset_unreported_expect"].to_list()[:32+future]
    
    DataFile = pd.read_csv("Minneapolis-Nature/result-4.csv")
    ReportedPP4 = DataFile["Onset_expect"].to_list()[:24+future]
    UnreportedPP4 = DataFile["Onset_unreported_expect"].to_list()[:24+future]
    
    ReportedPP = np.array(ReportedPP1[:42] + ReportedPP2[:33] + ReportedPP3[:32] + ReportedPP4[:24+future])
    UnreportedPP = np.array(UnreportedPP1[:42] + UnreportedPP2[:33] + UnreportedPP3[:32] + UnreportedPP4[:24+future])
    
    plt.subplot(2,5,1)
    plt.title("Minneapolis (SAPHIRE)", fontsize=12)
    
    plt.scatter(X,Reported,label=r'\textsc{NYT-R}'+r'$\mathrm{inf}$',marker='+',s=25,color='#000000')

    plt.plot(X,ReportedP,label=r'\textsc{BaseParam}'+r'$_{\mathrm{Rinf}}$',linewidth=3,color='#2166AC')

    plt.plot(X,ReportedPP,label=r'\textsc{MdlParam}'+r'$_{\mathrm{Rinf}}$',linewidth=3,color='#EA604D')

    plt.axvline(x = 130,color='#929591',linewidth=1,linestyle="dashdot")

    plt.xlabel('(a)', fontsize=18)
    plt.ylabel('Reported infections', fontsize=18)

    plt.xticks(XNumber,XDate,fontsize=12)
    plt.yticks([0,200,400,600,800],fontsize=12)
    plt.ylim(0,800)

    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    plt.gca().yaxis.set_major_formatter(mf)
    plt.gca().yaxis.get_offset_text().set(size=12)
    
    plt.legend(fontsize=14,loc=2)

    TrainingRMSEP.append(np.sqrt(np.mean((Reported[0:131]-ReportedP[0:131])**2)))
    TrainingRMSEPP.append(np.sqrt(np.mean((Reported[0:131]-ReportedPP[0:131])**2)))
    TestingRMSEP.append(np.sqrt(np.mean((Reported[131:131+future]-ReportedP[131:131+future])**2)))
    TestingRMSEPP.append(np.sqrt(np.mean((Reported[131:131+future]-ReportedPP[131:131+future])**2)))

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
    XDate = ["Apr 1","May 1","Jun 1","Jul 1"]
    
    DataFile = pd.read_csv("Minneapolis-Mordecai/result-original-1.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP1 = DataSelected["D_new_reported"].to_list()[25:67+future]
    UnreportedP1 = DataSelected["D_new_unreported"].to_list()[25:67+future]
    
    DataFile = pd.read_csv("Minneapolis-Mordecai/result-original-2.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP2 = DataSelected["D_new_reported"].to_list()[1:34+future]
    UnreportedP2 = DataSelected["D_new_unreported"].to_list()[1:34+future]
    
    DataFile = pd.read_csv("Minneapolis-Mordecai/result-original-3.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP3 = DataSelected["D_new_reported"].to_list()[1:33+future]
    UnreportedP3 = DataSelected["D_new_unreported"].to_list()[1:33+future]
    
    DataFile = pd.read_csv("Minneapolis-Mordecai/result-original-4.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP4 = DataSelected["D_new_reported"].to_list()[1:25+future]
    UnreportedP4 = DataSelected["D_new_unreported"].to_list()[1:25+future]
    
    ReportedP = np.array(ReportedP1[:42] + ReportedP2[:33] + ReportedP3[:32] + ReportedP4[:24+future])
    UnreportedP = np.array(UnreportedP1[:42] + UnreportedP2[:33] + UnreportedP3[:32] + UnreportedP4[:24+future])
    
    DataFile = pd.read_csv("Minneapolis-Mordecai/result-1.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP1 = DataSelected["D_new_reported"].to_list()[25:67+future]
    UnreportedPP1 = DataSelected["D_new_unreported"].to_list()[25:67+future]
    
    DataFile = pd.read_csv("Minneapolis-Mordecai/result-2.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP2 = DataSelected["D_new_reported"].to_list()[1:34+future]
    UnreportedPP2 = DataSelected["D_new_unreported"].to_list()[1:34+future]
    
    DataFile = pd.read_csv("Minneapolis-Mordecai/result-3.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP3 = DataSelected["D_new_reported"].to_list()[1:33+future]
    UnreportedPP3 = DataSelected["D_new_unreported"].to_list()[1:33+future]
    
    DataFile = pd.read_csv("Minneapolis-Mordecai/result-4.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP4 = DataSelected["D_new_reported"].to_list()[1:25+future]
    UnreportedPP4 = DataSelected["D_new_unreported"].to_list()[1:25+future]
    
    ReportedPP = np.array(ReportedPP1[:42] + ReportedPP2[:33] + ReportedPP3[:32] + ReportedPP4[:24+future])
    UnreportedPP = np.array(UnreportedPP1[:42] + UnreportedPP2[:33] + UnreportedPP3[:32] + UnreportedPP4[:24+future])
    
    plt.subplot(2,5,2)
    plt.title("Minneapolis (SEIR+HD)", fontsize=12)
    
    plt.scatter(X,Reported,label=r'\textsc{NYT-R}'+r'$\mathrm{inf}$',marker='+',s=25,color='#000000')

    plt.plot(X,ReportedP,label=r'\textsc{BaseParam}'+r'$_{\mathrm{Rinf}}$',linewidth=3,color='#2166AC')

    plt.plot(X,ReportedPP,label=r'\textsc{MdlParam}'+r'$_{\mathrm{Rinf}}$',linewidth=3,color='#EA604D')

    plt.axvline(x = 130,color='#929591',linewidth=1,linestyle="dashdot")

    plt.xlabel('(b)', fontsize=18)

    plt.xticks(XNumber,XDate,fontsize=12)
    plt.yticks([0,200,400,600,800],fontsize=12)
    plt.ylim(0,800)

    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    plt.gca().yaxis.set_major_formatter(mf)
    plt.gca().yaxis.get_offset_text().set(size=12)

    TrainingRMSEP.append(np.sqrt(np.mean((Reported[0:131]-ReportedP[0:131])**2)))
    TrainingRMSEPP.append(np.sqrt(np.mean((Reported[0:131]-ReportedPP[0:131])**2)))
    TestingRMSEP.append(np.sqrt(np.mean((Reported[131:131+future]-ReportedP[131:131+future])**2)))
    TestingRMSEPP.append(np.sqrt(np.mean((Reported[131:131+future]-ReportedPP[131:131+future])**2)))

    ### South Florida, Nature Model

    future = 16
    
    DataFile = pd.read_csv("Florida-Nature/data.csv")
    ReportedSum = DataFile["cases"][0:114+future].to_list()
    Date = DataFile["date"][0:114+future].to_list()
    X = range(len(Date))

    Reported = []
    Reported.append(ReportedSum[0])
    for counter in range(1,len(ReportedSum)):
        Reported.append(ReportedSum[counter] - ReportedSum[counter-1])
    Reported = np.array(Reported)

    XNumber = [26,56,87,117]
    XDate = ["Apr 1","May 1","Jun 1","Jul 1"]
    
    DataFile = pd.read_csv("Florida-Nature/result-original-1.csv")
    ReportedP1 = DataFile["Onset_expect"].to_list()[:20+future]
    UnreportedP1 = DataFile["Onset_unreported_expect"].to_list()[:20+future]
    
    DataFile = pd.read_csv("Florida-Nature/result-original-2.csv")
    ReportedP2 = DataFile["Onset_expect"].to_list()[:10+future]
    UnreportedP2 = DataFile["Onset_unreported_expect"].to_list()[:10+future]
    
    DataFile = pd.read_csv("Florida-Nature/result-original-3.csv")
    ReportedP3 = DataFile["Onset_expect"].to_list()[:24+future]
    UnreportedP3 = DataFile["Onset_unreported_expect"].to_list()[:24+future]
    
    DataFile = pd.read_csv("Florida-Nature/result-original-4.csv")
    ReportedP4 = DataFile["Onset_expect"].to_list()[:30+future]
    UnreportedP4 = DataFile["Onset_unreported_expect"].to_list()[:30+future]
    
    DataFile = pd.read_csv("Florida-Nature/result-original-5.csv")
    ReportedP5 = DataFile["Onset_expect"].to_list()[:30+future]
    UnreportedP5 = DataFile["Onset_unreported_expect"].to_list()[:30+future]
    
    ReportedP = np.array(ReportedP1[:20] + ReportedP2[:10] + ReportedP3[:24] + ReportedP4[:30] + ReportedP5[:30+future])
    UnreportedP = np.array(UnreportedP1[:20] + UnreportedP2[:10] + UnreportedP3[:24] + UnreportedP4[:30] + UnreportedP5[:30+future])
    
    DataFile = pd.read_csv("Florida-Nature/result-1.csv")
    ReportedPP1 = DataFile["Onset_expect"].to_list()[:20+future]
    UnreportedPP1 = DataFile["Onset_unreported_expect"].to_list()[:20+future]
    
    DataFile = pd.read_csv("Florida-Nature/result-2.csv")
    ReportedPP2 = DataFile["Onset_expect"].to_list()[:10+future]
    UnreportedPP2 = DataFile["Onset_unreported_expect"].to_list()[:10+future]
    
    DataFile = pd.read_csv("Florida-Nature/result-3.csv")
    ReportedPP3 = DataFile["Onset_expect"].to_list()[:24+future]
    UnreportedPP3 = DataFile["Onset_unreported_expect"].to_list()[:24+future]
    
    DataFile = pd.read_csv("Florida-Nature/result-4.csv")
    ReportedPP4 = DataFile["Onset_expect"].to_list()[:30+future]
    UnreportedPP4 = DataFile["Onset_unreported_expect"].to_list()[:30+future]
    
    DataFile = pd.read_csv("Florida-Nature/result-5.csv")
    ReportedPP5 = DataFile["Onset_expect"].to_list()[:30+future]
    UnreportedPP5 = DataFile["Onset_unreported_expect"].to_list()[:30+future]
    
    ReportedPP = np.array(ReportedPP1[:20] + ReportedPP2[:10] + ReportedPP3[:24] + ReportedPP4[:30] + ReportedPP5[:30+future])
    UnreportedPP = np.array(UnreportedPP1[:20] + UnreportedPP2[:10] + UnreportedPP3[:24] + UnreportedPP4[:30] + UnreportedPP5[:30+future])
    
    plt.subplot(2,5,3)
    plt.title("South Florida (SAPHIRE)", fontsize=12)
    
    plt.scatter(X,Reported,label=r'\textsc{NYT-R}'+r'$\mathrm{inf}$',marker='+',s=25,color='#000000')

    plt.plot(X,ReportedP,label=r'\textsc{BaseParam}'+r'$_{\mathrm{Rinf}}$',linewidth=3,color='#2166AC')

    plt.plot(X,ReportedPP,label=r'\textsc{MdlParam}'+r'$_{\mathrm{Rinf}}$',linewidth=3,color='#EA604D')

    plt.axvline(x = 113,color='#929591',linewidth=1,linestyle="dashdot")

    plt.xlabel('(c)', fontsize=18)

    plt.xticks(XNumber,XDate,fontsize=12)
    plt.yticks([0,1000,2000,3000,4000,5000],fontsize=12)
    plt.ylim(0,5000)

    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    plt.gca().yaxis.set_major_formatter(mf)
    plt.gca().yaxis.get_offset_text().set(size=12)

    TrainingRMSEP.append(np.sqrt(np.mean((Reported[0:114]-ReportedP[0:114])**2)))
    TrainingRMSEPP.append(np.sqrt(np.mean((Reported[0:114]-ReportedPP[0:114])**2)))
    TestingRMSEP.append(np.sqrt(np.mean((Reported[114:114+future]-ReportedP[114:114+future])**2)))
    TestingRMSEPP.append(np.sqrt(np.mean((Reported[114:114+future]-ReportedPP[114:114+future])**2)))

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
    XDate = ["Apr 1","May 1","Jun 1","Jul 1"]
    
    DataFile = pd.read_csv("Florida-Mordecai/result-original-1.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP1 = DataSelected["D_new_reported"].to_list()[14:34+future]
    UnreportedP1 = DataSelected["D_new_unreported"].to_list()[14:34+future]
     
    DataFile = pd.read_csv("Florida-Mordecai/result-original-2.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP2 = DataSelected["D_new_reported"].to_list()[1:11+future]
    UnreportedP2 = DataSelected["D_new_unreported"].to_list()[1:11+future]
    
    DataFile = pd.read_csv("Florida-Mordecai/result-original-3.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP3 = DataSelected["D_new_reported"].to_list()[1:25+future]
    UnreportedP3 = DataSelected["D_new_unreported"].to_list()[1:25+future]
    
    DataFile = pd.read_csv("Florida-Mordecai/result-original-4.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP4 = DataSelected["D_new_reported"].to_list()[1:31+future]
    UnreportedP4 = DataSelected["D_new_unreported"].to_list()[1:31+future]
    
    DataFile = pd.read_csv("Florida-Mordecai/result-original-5.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP5 = DataSelected["D_new_reported"].to_list()[1:31+future]
    UnreportedP5 = DataSelected["D_new_unreported"].to_list()[1:31+future]
    
    ReportedP = np.array(ReportedP1[:20] + ReportedP2[:10] + ReportedP3[:24] + ReportedP4[:30] + ReportedP5[:30+future])
    UnreportedP = np.array(UnreportedP1[:20] + UnreportedP2[:10] + UnreportedP3[:24] + UnreportedP4[:30] + UnreportedP5[:30+future])
    
    DataFile = pd.read_csv("Florida-Mordecai/result-1.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP1 = DataSelected["D_new_reported"].to_list()[14:34+future]
    UnreportedPP1 = DataSelected["D_new_unreported"].to_list()[14:34+future]
     
    DataFile = pd.read_csv("Florida-Mordecai/result-2.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP2 = DataSelected["D_new_reported"].to_list()[1:11+future]
    UnreportedPP2 = DataSelected["D_new_unreported"].to_list()[1:11+future]
    
    DataFile = pd.read_csv("Florida-Mordecai/result-3.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP3 = DataSelected["D_new_reported"].to_list()[1:25+future]
    UnreportedPP3 = DataSelected["D_new_unreported"].to_list()[1:25+future]
    
    DataFile = pd.read_csv("Florida-Mordecai/result-4.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP4 = DataSelected["D_new_reported"].to_list()[1:31+future]
    UnreportedPP4 = DataSelected["D_new_unreported"].to_list()[1:31+future]
    
    DataFile = pd.read_csv("Florida-Mordecai/result-5.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP5 = DataSelected["D_new_reported"].to_list()[1:31+future]
    UnreportedPP5 = DataSelected["D_new_unreported"].to_list()[1:31+future]
    
    ReportedPP = np.array(ReportedPP1[:20] + ReportedPP2[:10] + ReportedPP3[:24] + ReportedPP4[:30] + ReportedPP5[:30+future])
    UnreportedPP = np.array(UnreportedPP1[:20] + UnreportedPP2[:10] + UnreportedPP3[:24] + UnreportedPP4[:30] + UnreportedPP5[:30+future])
    
    plt.subplot(2,5,4)
    plt.title("South Florida (SEIR+HD)", fontsize=12)
    
    plt.scatter(X,Reported,label=r'\textsc{NYT-R}'+r'$\mathrm{inf}$',marker='+',s=25,color='#000000')

    plt.plot(X,ReportedP,label=r'\textsc{BaseParam}'+r'$_{\mathrm{Rinf}}$',linewidth=3,color='#2166AC')

    plt.plot(X,ReportedPP,label=r'\textsc{MdlParam}'+r'$_{\mathrm{Rinf}}$',linewidth=3,color='#EA604D')

    plt.axvline(x = 113,color='#929591',linewidth=1,linestyle="dashdot")

    plt.xlabel('(d)', fontsize=18)

    plt.xticks(XNumber,XDate,fontsize=12)
    plt.yticks([0,1000,2000,3000,4000,5000],fontsize=12)
    plt.ylim(0,5000)

    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    plt.gca().yaxis.set_major_formatter(mf)
    plt.gca().yaxis.get_offset_text().set(size=12)

    TrainingRMSEP.append(np.sqrt(np.mean((Reported[0:114]-ReportedP[0:114])**2)))
    TrainingRMSEPP.append(np.sqrt(np.mean((Reported[0:114]-ReportedPP[0:114])**2)))
    TestingRMSEP.append(np.sqrt(np.mean((Reported[114:114+future]-ReportedP[114:114+future])**2)))
    TestingRMSEPP.append(np.sqrt(np.mean((Reported[114:114+future]-ReportedPP[114:114+future])**2)))

    ### Minneapolis Metro Area Fall, Nature Model

    future = 14
    
    DataFile = pd.read_csv("Minneapolis-Nature-Fall/data.csv")
    ReportedSum = DataFile["cases"][0:31+future].to_list()
    Date = DataFile["date"][1:31+future].to_list()
    X = range(len(Date))

    Reported = []
    Reported.append(ReportedSum[0])
    for counter in range(1,len(ReportedSum)):
        Reported.append(ReportedSum[counter] - ReportedSum[counter-1])
    Reported = np.array(Reported[1:31+future])

    XNumber = [5,35]
    XDate = ["Sep 15","Oct 15"]
    
    DataFile = pd.read_csv("Minneapolis-Nature-Fall/result-original.csv")
    ReportedP = np.array(DataFile["Onset_expect"].to_list()[:30+future])
    UnreportedP = np.array(DataFile["Onset_unreported_expect"].to_list()[:30+future])
 
    DataFile = pd.read_csv("Minneapolis-Nature-Fall/result.csv")
    ReportedPP = np.array(DataFile["Onset_expect"].to_list()[:30+future])
    UnreportedPP = np.array(DataFile["Onset_unreported_expect"].to_list()[:30+future])
    
    plt.subplot(2,5,6)
    plt.title("Minneapolis Fall (SAPHIRE)", fontsize=12)
    
    plt.scatter(X,Reported,label=r'\textsc{NYT-R}'+r'$\mathrm{inf}$',marker='+',s=25,color='#000000')

    plt.plot(X,ReportedP,label=r'\textsc{BaseParam}'+r'$_{\mathrm{Rinf}}$',linewidth=3,color='#2166AC')

    plt.plot(X,ReportedPP,label=r'\textsc{MdlParam}'+r'$_{\mathrm{Rinf}}$',linewidth=3,color='#EA604D')

    plt.axvline(x = 29,color='#929591',linewidth=1,linestyle="dashdot")

    plt.xlabel('(f)', fontsize=18)
    plt.ylabel('Reported infections', fontsize=18)

    plt.xticks(XNumber,XDate,fontsize=12)
    plt.yticks([0,200,400,600,800,1000,1200],fontsize=12)
    plt.ylim(0,1200)

    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    plt.gca().yaxis.set_major_formatter(mf)
    plt.gca().yaxis.get_offset_text().set(size=12)

    TrainingRMSEP.append(np.sqrt(np.mean((Reported[0:31]-ReportedP[0:31])**2)))
    TrainingRMSEPP.append(np.sqrt(np.mean((Reported[0:31]-ReportedPP[0:31])**2)))
    TestingRMSEP.append(np.sqrt(np.mean((Reported[31:31+future]-ReportedP[31:31+future])**2)))
    TestingRMSEPP.append(np.sqrt(np.mean((Reported[31:31+future]-ReportedPP[31:31+future])**2)))

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
    XDate = ["Sep 15","Oct 15"]
    
    DataFile = pd.read_csv("Minneapolis-Mordecai-Fall/result-original.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP = np.array(DataSelected["D_new_reported"].to_list()[1:31+future])
    UnreportedP = np.array(DataSelected["D_new_unreported"].to_list()[1:31+future])

    DataFile = pd.read_csv("Minneapolis-Mordecai-Fall/result.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP = np.array(DataSelected["D_new_reported"].to_list()[1:31+future])
    UnreportedPP = np.array(DataSelected["D_new_unreported"].to_list()[1:31+future])

    plt.subplot(2,5,7)
    plt.title("Minneapolis Fall (SEIR+HD)", fontsize=12)
    
    plt.scatter(X,Reported,label=r'\textsc{NYT-R}'+r'$\mathrm{inf}$',marker='+',s=25,color='#000000')

    plt.plot(X,ReportedP,label=r'\textsc{BaseParam}'+r'$_{\mathrm{Rinf}}$',linewidth=3,color='#2166AC')

    plt.plot(X,ReportedPP,label=r'\textsc{MdlParam}'+r'$_{\mathrm{Rinf}}$',linewidth=3,color='#EA604D')

    plt.axvline(x = 29,color='#929591',linewidth=1,linestyle="dashdot")

    plt.xlabel('(g)', fontsize=18)

    plt.xticks(XNumber,XDate,fontsize=12)
    plt.yticks([0,200,400,600,800,1000,1200],fontsize=12)
    plt.ylim(0,1200)

    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    plt.gca().yaxis.set_major_formatter(mf)
    plt.gca().yaxis.get_offset_text().set(size=12)

    TrainingRMSEP.append(np.sqrt(np.mean((Reported[0:31]-ReportedP[0:31])**2)))
    TrainingRMSEPP.append(np.sqrt(np.mean((Reported[0:31]-ReportedPP[0:31])**2)))
    TestingRMSEP.append(np.sqrt(np.mean((Reported[31:31+future]-ReportedP[31:31+future])**2)))
    TestingRMSEPP.append(np.sqrt(np.mean((Reported[31:31+future]-ReportedPP[31:31+future])**2)))

    ### South Florida Fall, Nature Model

    future = 14
    
    DataFile = pd.read_csv("Florida-Nature-Fall/data.csv")
    ReportedSum = DataFile["cases"][0:31+future].to_list()
    Date = DataFile["date"][1:31+future].to_list()
    X = range(len(Date))

    Reported = []
    Reported.append(ReportedSum[0])
    for counter in range(1,len(ReportedSum)):
        Reported.append(ReportedSum[counter] - ReportedSum[counter-1])
    Reported = np.array(Reported[1:31+future])

    XNumber = [0,31]
    XDate = ["Oct 15","Nov 15"]
    
    DataFile = pd.read_csv("Florida-Nature-Fall/result-original.csv")
    ReportedP = np.array(DataFile["Onset_expect"].to_list()[:30+future])
    UnreportedP = np.array(DataFile["Onset_unreported_expect"].to_list()[:30+future])
 
    DataFile = pd.read_csv("Florida-Nature-Fall/result.csv")
    ReportedPP = np.array(DataFile["Onset_expect"].to_list()[:30+future])
    UnreportedPP = np.array(DataFile["Onset_unreported_expect"].to_list()[:30+future])
    
    plt.subplot(2,5,8)
    plt.title("South Florida Fall (SAPHIRE)", fontsize=12)
    
    plt.scatter(X,Reported,label=r'\textsc{NYT-R}'+r'$\mathrm{inf}$',marker='+',s=25,color='#000000')

    plt.plot(X,ReportedP,label=r'\textsc{BaseParam}'+r'$_{\mathrm{Rinf}}$',linewidth=3,color='#2166AC')

    plt.plot(X,ReportedPP,label=r'\textsc{MdlParam}'+r'$_{\mathrm{Rinf}}$',linewidth=3,color='#EA604D')

    plt.axvline(x = 29,color='#929591',linewidth=1,linestyle="dashdot")

    plt.xlabel('(h)', fontsize=18)

    plt.xticks(XNumber,XDate,fontsize=12)
    plt.yticks([0,1000,2000,3000,4000],fontsize=12)
    plt.ylim(0,4000)

    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    plt.gca().yaxis.set_major_formatter(mf)
    plt.gca().yaxis.get_offset_text().set(size=12)

    TrainingRMSEP.append(np.sqrt(np.mean((Reported[0:31]-ReportedP[0:31])**2)))
    TrainingRMSEPP.append(np.sqrt(np.mean((Reported[0:31]-ReportedPP[0:31])**2)))
    TestingRMSEP.append(np.sqrt(np.mean((Reported[31:31+future]-ReportedP[31:31+future])**2)))
    TestingRMSEPP.append(np.sqrt(np.mean((Reported[31:31+future]-ReportedPP[31:31+future])**2)))

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
    XDate = ["Oct 15","Nov 15"]
    
    DataFile = pd.read_csv("Florida-Mordecai-Fall/result-original.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedP = np.array(DataSelected["D_new_reported"].to_list()[1:31+future])
    UnreportedP = np.array(DataSelected["D_new_unreported"].to_list()[1:31+future])

    DataFile = pd.read_csv("Florida-Mordecai-Fall/result.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP = np.array(DataSelected["D_new_reported"].to_list()[1:31+future])
    UnreportedPP = np.array(DataSelected["D_new_unreported"].to_list()[1:31+future])

    plt.subplot(2,5,9)
    plt.title("South Florida Fall (SEIR+HD)", fontsize=12)
    
    plt.scatter(X,Reported,label=r'\textsc{NYT-R}'+r'$\mathrm{inf}$',marker='+',s=25,color='#000000')

    plt.plot(X,ReportedP,label=r'\textsc{BaseParam}'+r'$_{\mathrm{Rinf}}$',linewidth=3,color='#2166AC')

    plt.plot(X,ReportedPP,label=r'\textsc{MdlParam}'+r'$_{\mathrm{Rinf}}$',linewidth=3,color='#EA604D')

    plt.axvline(x = 29,color='#929591',linewidth=1,linestyle="dashdot")

    plt.xlabel('(i)', fontsize=18)

    plt.xticks(XNumber,XDate,fontsize=12)
    plt.yticks([0,1000,2000,3000,4000],fontsize=12)
    plt.ylim(0,4000)

    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    plt.gca().yaxis.set_major_formatter(mf)
    plt.gca().yaxis.get_offset_text().set(size=12)

    TrainingRMSEP.append(np.sqrt(np.mean((Reported[0:31]-ReportedP[0:31])**2)))
    TrainingRMSEPP.append(np.sqrt(np.mean((Reported[0:31]-ReportedPP[0:31])**2)))
    TestingRMSEP.append(np.sqrt(np.mean((Reported[31:31+future]-ReportedP[31:31+future])**2)))
    TestingRMSEPP.append(np.sqrt(np.mean((Reported[31:31+future]-ReportedPP[31:31+future])**2)))

    plt.subplot(2,5,5)

    plt.bar([1,2,3,4,5,6,7,8],np.array(TrainingRMSEP)/np.array(TrainingRMSEPP),width=0.4,label=r'$\rho_{\mathrm{Rinf}}$',color='#33CC33')
    
    plt.xticks([1,2,3,4,5,6,7,8],['(a)','(b)','(c)','(d)','(f)','(g)','(h)','(i)'], fontsize=12)
    plt.yticks([0,1,2,3,4,5,7,8],fontsize=12)
    plt.ylim(0,4)

    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    plt.gca().yaxis.set_major_formatter(mf)
    plt.gca().yaxis.get_offset_text().set(size=12)

    plt.axhline(y = 1,color='#929591',linewidth=1,linestyle="dashdot")
    
    plt.xlim(0,9)
    plt.xlabel("(e)", fontsize=18)
    plt.ylabel('\nPerformance '+r'$\rho_{\mathrm{Rinf}}$', fontsize=18)
    plt.title("Observed Period (Before grey dash line)", fontsize=12)
    plt.legend(fontsize=16,loc=2)

    plt.subplot(2,5,10)

    plt.bar([1,2,3,4,5,6,7,8],np.array(TestingRMSEP)/np.array(TestingRMSEPP),width=0.4,label="Our method RMSE",color='#33CC33')

    plt.xticks([1,2,3,4,5,6,7,8],['(a)','(b)','(c)','(d)','(f)','(g)','(h)','(i)'], fontsize=12)
    plt.yticks([0,1,2,3,4,5,7,8],fontsize=12)
    plt.ylim(0,4)
    
    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    plt.gca().yaxis.set_major_formatter(mf)
    plt.gca().yaxis.get_offset_text().set(size=12)

    plt.axhline(y = 1,color='#929591',linewidth=1,linestyle="dashdot")
    
    plt.xlim(0,9)
    plt.xlabel("(j)", fontsize=18)
    plt.ylabel('\nPerformance '+r'$\rho_{\mathrm{Rinf}}$', fontsize=18)
    plt.title("Future Period (After grey dash line)", fontsize=12)

    plt.tight_layout()
    
    plt.savefig('Figure3.pdf')
    plt.show()
