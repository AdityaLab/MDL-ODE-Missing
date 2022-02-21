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

    RMSE = []

    figure = plt.figure(figsize=(18,6))

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
    SymptomP = np.array(DataSelected["Is"].to_list()[:49+future]) + np.array(DataSelected["Im"].to_list()[:49+future])

    DataFile = pd.read_csv("Philadelphia/result.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP = np.array(DataSelected["D_new_reported"].to_list()[:49+future])
    UnreportedPP = np.array(DataSelected["D_new_unreported"].to_list()[:49+future])
    SymptomPP = np.array(DataSelected["Is"].to_list()[:49+future]) + np.array(DataSelected["Im"].to_list()[:49+future])
   
    ax = plt.subplot(1,3,1)
    
    ax.set_title("Philadelphia (SEIR+HD)", fontsize=16)
    
    ax.plot(X,np.cumsum(ReportedP+UnreportedP),label=r'\textsc{BaseParam}'+r'$_{\mathrm{Tinf}}$',linewidth=3,color='#2166AC')
    ax.plot(X,np.cumsum(ReportedPP+UnreportedPP),label=r'\textsc{MdlParam}'+r'$_{\mathrm{Tinf}}$',linewidth=3,color='#EA604D')

    ax.plot([45,45], [49101.39*1.7, 49101.39*5.2],linewidth=3,color='#000000',label=r'\textsc{SeroStudy}'+r'$_{\mathrm{Tinf}}$')
    ax.scatter([45],[49101.39*3.2],s=80,color='#000000')
    ax.plot([44,46], [49101.39*1.7, 49101.39*1.7],linewidth=3,color='#000000')
    ax.plot([44,46], [49101.39*5.2, 49101.39*5.2],linewidth=3,color='#000000')

    RMSE.append(np.linalg.norm(np.cumsum(ReportedP+UnreportedP)[45]-49101.39*3.2)/np.linalg.norm(np.cumsum(ReportedPP+UnreportedPP)[45]-49101.39*3.2))

    ax.axvline(x = 48,color='#929591',linewidth=1,linestyle="dashdot")

    ax.set_xlabel('(a)', fontsize=22)
    ax.set_ylabel('Cumulative values', fontsize=18)

    ax.set_xticks(XNumber)
    ax.set_xticklabels(XDate)
    ax.xaxis.set_tick_params(labelsize=16)
    ax.set_yticks([0,100000,200000,300000])
    ax.yaxis.set_tick_params(labelsize=16)
    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    ax.yaxis.set_major_formatter(mf)
    ax.yaxis.get_offset_text().set(size=16)
    ax.set_ylim(0,300000)

    ax.legend(fontsize=18,loc=2)
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
    SymptomP = np.array(DataSelected["Is"].to_list()[:45+future]) + np.array(DataSelected["Im"].to_list()[:45+future])

    DataFile = pd.read_csv("Washington/result.csv")
    DataSelected = DataFile[(DataFile[".id"] == "median")]
    ReportedPP = np.array(DataSelected["D_new_reported"].to_list()[:45+future])
    UnreportedPP = np.array(DataSelected["D_new_unreported"].to_list()[:45+future])
    SymptomPP = np.array(DataSelected["Is"].to_list()[:45+future]) + np.array(DataSelected["Im"].to_list()[:45+future])
      
    ax = plt.subplot(1,3,2)
    
    ax.set_title("Western Washington (SEIR+HD)", fontsize=16)
    
    ax.plot(X,np.cumsum(ReportedP+UnreportedP),label=r'\textsc{BaseParam}'+r'$_{\mathrm{Tinf}}$',linewidth=3,color='#2166AC')
    ax.plot(X,np.cumsum(ReportedPP+UnreportedPP),label=r'\textsc{MdlParam}'+r'$_{\mathrm{Tinf}}$',linewidth=3,color='#EA604D')
    
    ax.plot([56,56], [42735.48*0.7, 42735.48*1.9],linewidth=3,color='#000000',label=r'\textsc{SeroStudy}'+r'$_{\mathrm{Tinf}}$')
    ax.scatter([56],[42735.48*1.1],s=80,color='#000000')
    ax.plot([55,57], [42735.48*0.7, 42735.48*0.7],linewidth=3,color='#000000')
    ax.plot([55,57], [42735.48*1.9, 42735.48*1.9],linewidth=3,color='#000000')

    RMSE.append(np.linalg.norm(np.cumsum(ReportedP+UnreportedP)[56]-42735.48*1.1)/np.linalg.norm(np.cumsum(ReportedPP+UnreportedPP)[56]-42735.48*1.1))

    ax.axvline(x = 44,color='#929591',linewidth=1,linestyle="dashdot")

    ax.set_xlabel('(b)', fontsize=22)
    #ax.set_ylabel('Cumulative values', fontsize=16)

    ax.set_xticks(XNumber)
    ax.set_xticklabels(XDate)
    ax.xaxis.set_tick_params(labelsize=16)
    ax.set_yticks([0,100000,200000,300000,400000,500000])
    ax.yaxis.set_tick_params(labelsize=16)
    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    ax.yaxis.set_major_formatter(mf)
    ax.yaxis.get_offset_text().set(size=16)
    ax.set_ylim(0,500000)

    plt.tight_layout()
    
    plt.subplot(1,3,3)

    print (RMSE)

    plt.bar([1,2],np.array(RMSE),width=0.4,label=r'$\rho_{\mathrm{Tinf}}$',color='#33CC33')
    
    plt.xticks([1,2],['(a)','(b)'], fontsize=16)
    plt.yticks([0,1,2],fontsize=16)
    plt.ylim(0,2)

    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    plt.gca().yaxis.set_major_formatter(mf)
    plt.gca().yaxis.get_offset_text().set(size=16)

    plt.axhline(y = 1,color='#929591',linewidth=1,linestyle="dashdot")
    
    plt.xlim(0,3)
    plt.xlabel('(c)', fontsize=22)
    plt.ylabel('\nPerformance '+r'$\rho_{\mathrm{Tinf}}$', fontsize=18)
    plt.title('Performance '+r'$\rho_{\mathrm{Tinf}}$'+' in different region', fontsize=16)
    plt.legend(fontsize=16,loc=2)

    plt.tight_layout()

    plt.savefig('Serological.pdf')
    plt.show()
