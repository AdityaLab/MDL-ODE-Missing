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

    figure = plt.figure(figsize=(18,4.8))

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

    DataFile = pd.read_csv("Philadelphia/result.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP = np.array(DataSelected["D_new_reported"].to_list()[:49+future])
    UnreportedPP = np.array(DataSelected["D_new_unreported"].to_list()[:49+future])
       
    plt.subplot(1,4,1)
    plt.title("Philadelphia (SEIR+HD)", fontsize=14)
    #plt.title(" \n ", fontsize=50)

    plt.scatter(X,Reported,label=r'\textsc{NYT-R}'+r'$\mathrm{inf}$',marker='+',s=25,color='#000000')

    plt.plot(X,ReportedP,label=r'\textsc{BaseParam}'+r'$_{\mathrm{Rinf}}$',linewidth=3,color='#2166AC')

    plt.plot(X,ReportedPP,label=r'\textsc{MdlParam}'+r'$_{\mathrm{Rinf}}$',linewidth=3,color='#EA604D')


    plt.axvline(x = 48,color='#929591',linewidth=1,linestyle="dashdot")
    #plt.text(48-2,1,'Training Data',color='#FF6100',horizontalalignment='right')
    #plt.text(48+2,1,'Testing Data',color='#FF6100',horizontalalignment='left')

    #plt.xlabel('Date', fontsize=16)
    plt.xlabel('(a)', fontsize=22)
    plt.ylabel('Reported infections', fontsize=18)

    plt.xticks(XNumber,XDate,fontsize=16)
    plt.yticks([0,200,400,600,800,1000],fontsize=16)
    plt.ylim(0,1000)

    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    plt.gca().yaxis.set_major_formatter(mf)
    plt.gca().yaxis.get_offset_text().set(size=16)
    
    plt.legend(fontsize=15,loc=2)

    TrainingRMSEP.append(np.linalg.norm(Reported[0:49]-ReportedP[0:49]))
    TrainingRMSEPP.append(np.linalg.norm(Reported[0:49]-ReportedPP[0:49]))
    TestingRMSEP.append(np.linalg.norm(Reported[49:49+future]-ReportedP[49:49+future]))
    TestingRMSEPP.append(np.linalg.norm(Reported[49:49+future]-ReportedPP[49:49+future]))

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
    SymptomP = np.array(DataSelected["Is"].to_list()[:45+future]) + np.array(DataSelected["Im"].to_list()[:45+future])

    DataFile = pd.read_csv("Washington/result.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP = np.array(DataSelected["D_new_reported"].to_list()[:45+future])
    UnreportedPP = np.array(DataSelected["D_new_unreported"].to_list()[:45+future])
    SymptomPP = np.array(DataSelected["Is"].to_list()[:45+future]) + np.array(DataSelected["Im"].to_list()[:45+future])
       
    plt.subplot(1,4,2)
    plt.title("Western Washington (SEIR+HD)", fontsize=14)
    #plt.title(" \n ", fontsize=50)
    
    plt.scatter(X,Reported,label=r'\textsc{NYT-R}'+r'$\mathrm{inf}$',marker='+',s=25,color='#000000')

    plt.plot(X,ReportedP,label=r'\textsc{BaseParam}'+r'$_{\mathrm{Rinf}}$',linewidth=3,color='#2166AC')

    plt.plot(X,ReportedPP,label=r'\textsc{MdlParam}'+r'$_{\mathrm{Rinf}}$',linewidth=3,color='#EA604D')

    plt.axvline(x = 44,color='#929591',linewidth=1,linestyle="dashdot")
    #plt.text(36-2,1,'Training Data',color='#FF6100',horizontalalignment='right')
    #plt.text(36+2,1,'Testing Data',color='#FF6100',horizontalalignment='left')

    #plt.xlabel('Date', fontsize=16)
    plt.xlabel('(b)', fontsize=22)
    #plt.ylabel('Reported infections', fontsize=16)
    #plt.ylabel(" \n ", fontsize=16)

    plt.xticks(XNumber,XDate,fontsize=16)
    plt.yticks([0,200,400,600,800],fontsize=16)
    plt.ylim(0,800)

    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    plt.gca().yaxis.set_major_formatter(mf)
    plt.gca().yaxis.get_offset_text().set(size=16)
    
    #plt.legend(fontsize=16,loc=2)

    TrainingRMSEP.append(np.linalg.norm(Reported[0:44]-ReportedP[0:44]))
    TrainingRMSEPP.append(np.linalg.norm(Reported[0:44]-ReportedPP[0:44]))
    TestingRMSEP.append(np.linalg.norm(Reported[44:44+future]-ReportedP[44:44+future]))
    TestingRMSEPP.append(np.linalg.norm(Reported[44:44+future]-ReportedPP[44:44+future]))

    plt.subplot(1,4,3)

    #plt.bar([0.8,1.8],np.array(TrainingRMSEP),width=0.4,label="Baseline RMSE",color='#1f77b4')
    plt.bar([1,2],np.array(TrainingRMSEP)/np.array(TrainingRMSEPP),width=0.4,label=r'$\rho_{\mathrm{Rinf}}$',color='#33CC33')
    
    plt.xticks([1,2],['(a)','(b)'], fontsize=16)
    plt.yticks([0,1,2,3],fontsize=16)
    plt.ylim(0,3)

    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    plt.gca().yaxis.set_major_formatter(mf)
    plt.gca().yaxis.get_offset_text().set(size=16)

    plt.axhline(y = 1,color='#929591',linewidth=1,linestyle="dashdot")
    
    plt.xlim(0,3)
    plt.xlabel("(c)", fontsize=22)
    plt.ylabel('\nPerformance '+r'$\rho_{\mathrm{Rinf}}$', fontsize=18)
    plt.title("Observed Period (Before grey dash line)", fontsize=14)
    plt.legend(fontsize=18,loc=2)

    plt.subplot(1,4,4)

    #plt.bar([0.8,1.8],np.array(TestingRMSEP),width=0.4,label="Baseline RMSE",color='#1f77b4')
    plt.bar([1,2],np.array(TestingRMSEP)/np.array(TestingRMSEPP),width=0.4,label="Our method RMSE",color='#33CC33')

    plt.xticks([1,2],['(a)','(b)'], fontsize=16)
    plt.yticks([0,1,2,3,4,5,6],fontsize=16)
    plt.ylim(0,6)
    
    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    plt.gca().yaxis.set_major_formatter(mf)
    plt.gca().yaxis.get_offset_text().set(size=16)

    plt.axhline(y = 1,color='#929591',linewidth=1,linestyle="dashdot")
    
    plt.xlim(0,3)
    plt.xlabel("(d)", fontsize=22)
    #plt.ylabel('\nPerformance '+r'$\rho_{\mathrm{Rinf}}$', fontsize=16)
    plt.title("Future Period (After grey dash line)", fontsize=14)
    #plt.legend(fontsize=16)

    #plt.figtext(0.26,0.995,'County level',va='top',ha='center', fontsize=40)
    #plt.figtext(0.75,0.995,'Metro area level',va='top',ha='center', fontsize=40)
    #plt.figtext(0.75,0.67,'State level',va='top',ha='center', fontsize=40)
    #plt.figtext(0.75,0.35,'Training RMSE Ratio vs. Testing RMSE Ratio',va='top',ha='center', fontsize=40)

    plt.tight_layout()
    #figure.add_artist(lines.Line2D([0.5,1],[0.355,0.355],color='#000000',linestyle='dashdot',linewidth=1,alpha=0.5))
    #figure.add_artist(lines.Line2D([0.5,1],[0.675,0.675],color='#000000',linestyle='dashdot',linewidth=1,alpha=0.5))
    #figure.add_artist(lines.Line2D([0.5,0.5],[0,1],color='#000000',linestyle='dashdot',linewidth=1,alpha=0.5))

    plt.savefig('Reported.pdf')
    plt.show()
