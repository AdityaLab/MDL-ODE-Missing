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

    figure = plt.figure(figsize=(9,4))

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
   
    plt.subplot(1,2,1)
    plt.title("Philadelphia (SEIR+HD)", fontsize=14)

    plt.plot(X,np.array(ReportedSum)/np.cumsum(np.array(ReportedP)+np.array(UnreportedP)),label=r'\textsc{BaseParam}'+r'$_{\mathrm{Rate}}$',linewidth=3,color='#2166AC')
    plt.plot(X,np.array(ReportedSum)/np.cumsum(np.array(ReportedPP)+np.array(UnreportedPP)),label=r'\textsc{MdlParam}'+r'$_{\mathrm{Rate}}$',linewidth=3,color='#EA604D')
    
    plt.plot([45,45], [7656/(49101.39*1.7), 7656/(49101.39*5.2)],linewidth=2,color='#000000',label=r'\textsc{SeroStudy}'+r'$_{\mathrm{Rate}}$')
    plt.scatter([45],[7656/(49101.39*3.2)],s=50,color='#000000')
    plt.plot([44,46], [7656/(49101.39*1.7), 7656/(49101.39*1.7)],linewidth=2,color='#000000')
    plt.plot([44,46], [7656/(49101.39*5.2), 7656/(49101.39*5.2)],linewidth=2,color='#000000')

    plt.axvline(x = 48,color='#929591',linewidth=1,linestyle="dashdot")
    #plt.text(48-2,1,'Training Data',color='#FF6100',horizontalalignment='right')
    #plt.text(48+2,1,'Testing Data',color='#FF6100',horizontalalignment='left')

    plt.xlabel('(a)', fontsize=20)
    plt.ylabel('Cumulative reported rate', fontsize=16)

    plt.xticks(XNumber,XDate,fontsize=14)
    plt.yticks([0,0.05,0.10,0.15,0.20],fontsize=14)
    plt.ylim(0,0.2)

    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    plt.gca().yaxis.set_major_formatter(mf)
    plt.gca().yaxis.get_offset_text().set(size=14)
    
    plt.legend(fontsize=14,loc=2)
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
   
    plt.subplot(1,2,2)
    plt.title("Western Washington (SEIR+HD)", fontsize=14)

    plt.plot(X,np.array(ReportedSum)/np.cumsum(np.array(ReportedP)+np.array(UnreportedP)),label=r'\textsc{BaseParam}'+r'$_{\mathrm{Rate}}$',linewidth=3,color='#2166AC')
    plt.plot(X,np.array(ReportedSum)/np.cumsum(np.array(ReportedPP)+np.array(UnreportedPP)),label=r'\textsc{MdlParam}'+r'$_{\mathrm{Rate}}$',linewidth=3,color='#EA604D')
    
    plt.plot([56,56], [766/(42735.48*0.7), 766/(42735.48*1.9)],linewidth=2,color='#000000',label=r'\textsc{SeroStudy}'+" reported rate")
    plt.scatter([56],[766/(42735.48*1.1)],s=50,color='#000000')
    plt.plot([55,57], [766/(42735.48*0.7), 766/(42735.48*0.7)],linewidth=2,color='#000000')
    plt.plot([55,57], [766/(42735.48*1.9), 766/(42735.48*1.9)],linewidth=2,color='#000000')
    
    plt.axvline(x = 44,color='#929591',linewidth=1,linestyle="dashdot")
    #plt.text(36-2,1,'Training Data',color='#FF6100',horizontalalignment='right')
    #plt.text(36+2,1,'Testing Data',color='#FF6100',horizontalalignment='left')

    plt.xlabel('(b)', fontsize=20)
    #plt.ylabel('Reported rate', fontsize=14)

    plt.xticks(XNumber,XDate,fontsize=14)
    plt.yticks([0,0.01,0.02,0.03,0.04],['0','0.01','0.02','0.03','0.04'],fontsize=14)
    plt.ylim(0,0.04)

    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    plt.gca().yaxis.set_major_formatter(mf)
    plt.gca().yaxis.get_offset_text().set(size=14)
    
    #plt.legend(fontsize=25)
    plt.tight_layout()
    
    plt.savefig('Rate.pdf')
    plt.show()
