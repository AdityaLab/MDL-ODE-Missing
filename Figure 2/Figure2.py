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

    TINFRMSE = []

    figure = plt.figure(figsize=(18,4))

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
   
    ax = plt.subplot(1,5,1)
    ax.set_title("Minneapolis (SAPHIRE)", fontsize=13)
    
    ax.plot(X,np.cumsum(ReportedP+UnreportedP),label=r'\textsc{BaseParam}'+r'$_{\mathrm{Tinf}}$',linewidth=3,color='#2166AC')
    ax.plot(X,np.cumsum(ReportedPP+UnreportedPP),label=r'\textsc{MdlParam}'+r'$_{\mathrm{Tinf}}$',linewidth=3,color='#EA604D')

    print (np.cumsum(Reported)[5])
    print (np.cumsum(ReportedP+UnreportedP)[5])
    print (np.cumsum(ReportedPP+UnreportedPP)[5])
    print (Date[5])

    #print (Date[48])
    #print (Date[73])
    #print (Date[94])
    #print (Date[115])
    #print (Date[136])

    plt.plot([48,48],[38574.79*1.0,38574.79*4.5],linewidth=2,color='#000000',label=r'\textsc{SeroStudy}'+r'$_{\mathrm{Tinf}}$')
    plt.scatter([48],[38574.79*2.4],s=50,color='#000000')
    plt.plot([47,49],[38574.79*1.0,38574.79*1.0],linewidth=2,color='#000000')
    plt.plot([47,49],[38574.79*4.5,38574.79*4.5],linewidth=2,color='#000000')

    plt.plot([73,73],[38574.79*1.4,38574.79*3.3],linewidth=2,color='#000000')
    plt.scatter([73],[38574.79*2.2],s=50,color='#000000')
    plt.plot([72,74],[38574.79*1.4,38574.79*1.4],linewidth=2,color='#000000')
    plt.plot([72,74],[38574.79*3.3,38574.79*3.3],linewidth=2,color='#000000')

    plt.plot([94,94],[38574.79*3.4,38574.79*5.8],linewidth=2,color='#000000')
    plt.scatter([94],[38574.79*4.3],s=50,color='#000000')
    plt.plot([93,95],[38574.79*3.4,38574.79*3.4],linewidth=2,color='#000000')
    plt.plot([93,95],[38574.79*5.8,38574.79*5.8],linewidth=2,color='#000000')

    plt.plot([115,115],[38574.79*4.4,38574.79*8.3],linewidth=2,color='#000000')
    plt.scatter([115],[38574.79*6.1],s=50,color='#000000')
    plt.plot([114,116],[38574.79*4.4,38574.79*4.4],linewidth=2,color='#000000')
    plt.plot([114,116],[38574.79*8.3,38574.79*8.3],linewidth=2,color='#000000')

    plt.plot([136,136],[38574.79*6.6,38574.79*11.2],linewidth=2,color='#000000')
    plt.scatter([136],[38574.79*8.8],s=50,color='#000000')
    plt.plot([135,137],[38574.79*6.6,38574.79*6.6],linewidth=2,color='#000000')
    plt.plot([135,137],[38574.79*11.2,38574.79*11.2],linewidth=2,color='#000000')

    Sero = np.array([38574.79*2.4,38574.79*2.2,38574.79*4.3,38574.79*6.1,38574.79*8.8])
    SeroP = np.cumsum(ReportedP+UnreportedP)
    SeroPP = np.cumsum(ReportedPP+UnreportedPP)
    SeroP = np.array([SeroP[48],SeroP[73],SeroP[94],SeroP[115],SeroP[136]])
    SeroPP = np.array([SeroPP[48],SeroPP[73],SeroPP[94],SeroPP[115],SeroPP[136]])

    TINFRMSE.append(np.sqrt(np.mean((SeroP-Sero)**2))/np.sqrt(np.mean((SeroPP-Sero)**2)))
    print (np.sqrt(np.mean((SeroP-Sero)**2)),np.sqrt(np.mean((SeroPP-Sero)**2)))

    ax.axvline(x = 130,color='#929591',linewidth=1,linestyle="dashdot")

    ax.set_xlabel('(a)', fontsize=18)
    ax.set_ylabel('Cumulative values', fontsize=18)
    
    ax.set_xticks(XNumber)
    ax.set_xticklabels(XDate)
    ax.xaxis.set_tick_params(labelsize=12)
    ax.set_yticks([0,100000,200000,300000,400000,500000])
    ax.yaxis.set_tick_params(labelsize=12)
    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    ax.yaxis.set_major_formatter(mf)
    ax.yaxis.get_offset_text().set(size=12)
    ax.set_ylim(0,500000)

    ax.legend(fontsize=14, loc=2)
    plt.tight_layout()


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
    
    ax = plt.subplot(1,5,2)
    ax.set_title("Minneapolis (SEIR+HD)", fontsize=13)
    
    ax.plot(X,np.cumsum(ReportedP+UnreportedP),label=r'\textsc{BaseParam}'+r'$_{\mathrm{Tinf}}$',linewidth=3,color='#2166AC')
    ax.plot(X,np.cumsum(ReportedPP+UnreportedPP),label=r'\textsc{MdlParam}'+r'$_{\mathrm{Tinf}}$',linewidth=3,color='#EA604D')

    #print (Date[48])
    #print (Date[73])
    #print (Date[94])
    #print (Date[115])
    #print (Date[136])

    plt.plot([48,48],[38574.79*1.0,38574.79*4.5],linewidth=2,color='#000000',label=r'\textsc{SeroStudy}'+r'$_{\mathrm{Tinf}}$')
    plt.scatter([48],[38574.79*2.4],s=50,color='#000000')
    plt.plot([47,49],[38574.79*1.0,38574.79*1.0],linewidth=2,color='#000000')
    plt.plot([47,49],[38574.79*4.5,38574.79*4.5],linewidth=2,color='#000000')

    plt.plot([73,73],[38574.79*1.4,38574.79*3.3],linewidth=2,color='#000000')
    plt.scatter([73],[38574.79*2.2],s=50,color='#000000')
    plt.plot([72,74],[38574.79*1.4,38574.79*1.4],linewidth=2,color='#000000')
    plt.plot([72,74],[38574.79*3.3,38574.79*3.3],linewidth=2,color='#000000')

    plt.plot([94,94],[38574.79*3.4,38574.79*5.8],linewidth=2,color='#000000')
    plt.scatter([94],[38574.79*4.3],s=50,color='#000000')
    plt.plot([93,95],[38574.79*3.4,38574.79*3.4],linewidth=2,color='#000000')
    plt.plot([93,95],[38574.79*5.8,38574.79*5.8],linewidth=2,color='#000000')

    plt.plot([115,115],[38574.79*4.4,38574.79*8.3],linewidth=2,color='#000000')
    plt.scatter([115],[38574.79*6.1],s=50,color='#000000')
    plt.plot([114,116],[38574.79*4.4,38574.79*4.4],linewidth=2,color='#000000')
    plt.plot([114,116],[38574.79*8.3,38574.79*8.3],linewidth=2,color='#000000')

    plt.plot([136,136],[38574.79*6.6,38574.79*11.2],linewidth=2,color='#000000')
    plt.scatter([136],[38574.79*8.8],s=50,color='#000000')
    plt.plot([135,137],[38574.79*6.6,38574.79*6.6],linewidth=2,color='#000000')
    plt.plot([135,137],[38574.79*11.2,38574.79*11.2],linewidth=2,color='#000000')

    Sero = np.array([38574.79*2.4,38574.79*2.2,38574.79*4.3,38574.79*6.1,38574.79*8.8])
    SeroP = np.cumsum(ReportedP+UnreportedP)
    SeroPP = np.cumsum(ReportedPP+UnreportedPP)
    SeroP = np.array([SeroP[48],SeroP[73],SeroP[94],SeroP[115],SeroP[136]])
    SeroPP = np.array([SeroPP[48],SeroPP[73],SeroPP[94],SeroPP[115],SeroPP[136]])

    TINFRMSE.append(np.sqrt(np.mean((SeroP-Sero)**2))/np.sqrt(np.mean((SeroPP-Sero)**2)))
    print (np.sqrt(np.mean((SeroP-Sero)**2)),np.sqrt(np.mean((SeroPP-Sero)**2)))

    ax.axvline(x = 130,color='#929591',linewidth=1,linestyle="dashdot")

    ax.set_xlabel('(b)', fontsize=18)
    
    ax.set_xticks(XNumber)
    ax.set_xticklabels(XDate)
    ax.xaxis.set_tick_params(labelsize=12)
    ax.set_yticks([0,100000,200000,300000,400000,500000])
    ax.yaxis.set_tick_params(labelsize=12)
    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    ax.yaxis.set_major_formatter(mf)
    ax.yaxis.get_offset_text().set(size=12)
    ax.set_ylim(0,500000)

    plt.tight_layout()


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

    DataFile = pd.read_csv("Minneapolis-Nature/result-1.csv")
    ReportedPP1 = DataFile["Onset_expect"].to_list()[:20+future]
    UnreportedPP1 = DataFile["Onset_unreported_expect"].to_list()[:20+future]

    DataFile = pd.read_csv("Minneapolis-Nature/result-2.csv")
    ReportedPP2 = DataFile["Onset_expect"].to_list()[:10+future]
    UnreportedPP2 = DataFile["Onset_unreported_expect"].to_list()[:10+future]

    DataFile = pd.read_csv("Minneapolis-Nature/result-3.csv")
    ReportedPP3 = DataFile["Onset_expect"].to_list()[:24+future]
    UnreportedPP3 = DataFile["Onset_unreported_expect"].to_list()[:24+future]
 
    DataFile = pd.read_csv("Minneapolis-Nature/result-4.csv")
    ReportedPP4 = DataFile["Onset_expect"].to_list()[:30+future]
    UnreportedPP4 = DataFile["Onset_unreported_expect"].to_list()[:30+future]
 
    DataFile = pd.read_csv("Florida-Nature/result-5.csv")
    ReportedPP5 = DataFile["Onset_expect"].to_list()[:30+future]
    UnreportedPP5 = DataFile["Onset_unreported_expect"].to_list()[:30+future]
 
    ReportedPP = np.array(ReportedPP1[:20] + ReportedPP2[:10] + ReportedPP3[:24] + ReportedPP4[:30] + ReportedPP5[:30+future])
    UnreportedPP = np.array(UnreportedPP1[:20] + UnreportedPP2[:10] + UnreportedPP3[:24] + UnreportedPP4[:30] + UnreportedPP5[:30+future])
     
    ax = plt.subplot(1,5,3)
    ax.set_title("South Florida (SAPHIRE)", fontsize=13)
    
    ax.plot(X,np.cumsum(ReportedP+UnreportedP),label=r'\textsc{BaseParam}'+r'$_{\mathrm{Tinf}}$',linewidth=3,color='#2166AC')
    ax.plot(X,np.cumsum(ReportedPP+UnreportedPP),label=r'\textsc{MdlParam}'+r'$_{\mathrm{Tinf}}$',linewidth=3,color='#EA604D')

    #print (Date[24])
    #print (Date[38])
    #print (Date[67])
    #print (Date[129])

    plt.plot([24,24],[63453.45*1.0,63453.45*3.2],linewidth=2,color='#000000',label=r'$SeroStudy_{Tinf}$')
    plt.scatter([24],[63453.45*1.9],s=50,color='#000000')
    plt.plot([23,25],[63453.45*1.0,63453.45*1.0],linewidth=2,color='#000000')
    plt.plot([23,25],[63453.45*3.2,63453.45*3.2],linewidth=2,color='#000000')

    plt.plot([38,38],[63453.45*1.9,63453.45*4.3],linewidth=2,color='#000000')
    plt.scatter([38],[63453.45*2.8],s=50,color='#000000')
    plt.plot([37,39],[63453.45*1.9,63453.45*1.9],linewidth=2,color='#000000')
    plt.plot([37,39],[63453.45*4.3,63453.45*4.3],linewidth=2,color='#000000')

    plt.plot([67,67],[63453.45*2.8,63453.45*6.2],linewidth=2,color='#000000')
    plt.scatter([67],[63453.45*4.2],s=50,color='#000000')
    plt.plot([66,68],[63453.45*2.8,63453.45*2.8],linewidth=2,color='#000000')
    plt.plot([66,68],[63453.45*6.2,63453.45*6.2],linewidth=2,color='#000000')

    plt.plot([129,129],[63453.45*10.5,63453.45*16.2],linewidth=2,color='#000000')
    plt.scatter([129],[63453.45*13.3],s=50,color='#000000')
    plt.plot([128,130],[63453.45*10.5,63453.45*10.5],linewidth=2,color='#000000')
    plt.plot([128,130],[63453.45*16.2,63453.45*16.2],linewidth=2,color='#000000')

    Sero = np.array([63453.45*1.9,63453.45*2.8,63453.45*4.2,63453.45*13.3])
    SeroP = np.cumsum(ReportedP+UnreportedP)
    SeroPP = np.cumsum(ReportedPP+UnreportedPP)
    SeroP = np.array([SeroP[24],SeroP[38],SeroP[67],SeroP[129]])
    SeroPP = np.array([SeroPP[24],SeroPP[38],SeroPP[67],SeroPP[129]])

    TINFRMSE.append(np.sqrt(np.mean((SeroP-Sero)**2))/np.sqrt(np.mean((SeroPP-Sero)**2)))
    print (np.sqrt(np.mean((SeroP-Sero)**2)),np.sqrt(np.mean((SeroPP-Sero)**2)))

    ax.axvline(x = 113,color='#929591',linewidth=1,linestyle="dashdot")

    ax.set_xlabel('(c)', fontsize=18)
    
    ax.set_xticks(XNumber)
    ax.set_xticklabels(XDate)
    ax.xaxis.set_tick_params(labelsize=12)
    ax.set_yticks([0,1000000,2000000,3000000])
    ax.yaxis.set_tick_params(labelsize=12)
    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    ax.yaxis.set_major_formatter(mf)
    ax.yaxis.get_offset_text().set(size=12)
    ax.set_ylim(0,3000000)

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
    
    ax = plt.subplot(1,5,4)
    ax.set_title("South Florida (SEIR+HD)", fontsize=13)
    
    ax.plot(X,np.cumsum(ReportedP+UnreportedP),label=r'\textsc{BaseParam}'+r'$_{\mathrm{Tinf}}$',linewidth=3,color='#2166AC')
    ax.plot(X,np.cumsum(ReportedPP+UnreportedPP),label=r'\textsc{MdlParam}'+r'$_{\mathrm{Tinf}}$',linewidth=3,color='#EA604D')

    #print (Date[24])
    #print (Date[38])
    #print (Date[67])
    #print (Date[129])

    plt.plot([24,24],[63453.45*1.0,63453.45*3.2],linewidth=2,color='#000000',label=r'$SeroStudy_{Tinf}$')
    plt.scatter([24],[63453.45*1.9],s=50,color='#000000')
    plt.plot([23,25],[63453.45*1.0,63453.45*1.0],linewidth=2,color='#000000')
    plt.plot([23,25],[63453.45*3.2,63453.45*3.2],linewidth=2,color='#000000')

    plt.plot([38,38],[63453.45*1.9,63453.45*4.3],linewidth=2,color='#000000')
    plt.scatter([38],[63453.45*2.8],s=50,color='#000000')
    plt.plot([37,39],[63453.45*1.9,63453.45*1.9],linewidth=2,color='#000000')
    plt.plot([37,39],[63453.45*4.3,63453.45*4.3],linewidth=2,color='#000000')

    plt.plot([67,67],[63453.45*2.8,63453.45*6.2],linewidth=2,color='#000000')
    plt.scatter([67],[63453.45*4.2],s=50,color='#000000')
    plt.plot([66,68],[63453.45*2.8,63453.45*2.8],linewidth=2,color='#000000')
    plt.plot([66,68],[63453.45*6.2,63453.45*6.2],linewidth=2,color='#000000')

    plt.plot([129,129],[63453.45*10.5,63453.45*16.2],linewidth=2,color='#000000')
    plt.scatter([129],[63453.45*13.3],s=50,color='#000000')
    plt.plot([128,130],[63453.45*10.5,63453.45*10.5],linewidth=2,color='#000000')
    plt.plot([128,130],[63453.45*16.2,63453.45*16.2],linewidth=2,color='#000000')

    Sero = np.array([63453.45*1.9,63453.45*2.8,63453.45*4.2,63453.45*13.3])
    SeroP = np.cumsum(ReportedP+UnreportedP)
    SeroPP = np.cumsum(ReportedPP+UnreportedPP)
    SeroP = np.array([SeroP[24],SeroP[38],SeroP[67],SeroP[129]])
    SeroPP = np.array([SeroPP[24],SeroPP[38],SeroPP[67],SeroPP[129]])

    TINFRMSE.append(np.sqrt(np.mean((SeroP-Sero)**2))/np.sqrt(np.mean((SeroPP-Sero)**2)))
    print (np.sqrt(np.mean((SeroP-Sero)**2)),np.sqrt(np.mean((SeroPP-Sero)**2)))

    ax.axvline(x = 113,color='#929591',linewidth=1,linestyle="dashdot")

    ax.set_xlabel('(d)', fontsize=18)
    
    ax.set_xticks(XNumber)
    ax.set_xticklabels(XDate)
    ax.xaxis.set_tick_params(labelsize=12)
    ax.set_yticks([0,1000000,2000000,3000000])
    ax.yaxis.set_tick_params(labelsize=12)
    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    ax.yaxis.set_major_formatter(mf)
    ax.yaxis.get_offset_text().set(size=12)
    ax.set_ylim(0,3000000)

    plt.tight_layout()


    plt.subplot(1,5,5)

    plt.bar([1,2,3,4],np.array(TINFRMSE),width=0.4,label=r'$\rho_{\mathrm{Tinf}}$',color='#33CC33')
    
    plt.xticks([1,2,3,4],['(a)','(b)','(c)','(d)'], fontsize=12)
    plt.yticks([0,1,2,3,4,5,6],fontsize=12)
    plt.ylim(0,6)

    mf = matplotlib.ticker.ScalarFormatter(useMathText=True)
    mf.set_powerlimits((-2,2))
    plt.gca().yaxis.set_major_formatter(mf)
    plt.gca().yaxis.get_offset_text().set(size=12)

    plt.axhline(y = 1,color='#929591',linewidth=1,linestyle="dashdot")
    
    plt.xlim(0,5)
    plt.xlabel('(e)', fontsize=18)
    plt.ylabel('\nPerformance '+r'$\rho_{\mathrm{Tinf}}$', fontsize=18)
    plt.title('Performance '+r'$\rho_{\mathrm{Tinf}}$'+' in different region', fontsize=13)
    plt.legend(fontsize=16, loc=2)

    plt.tight_layout()

    print (TINFRMSE)
    
    plt.savefig('Figure2.pdf')
    plt.show()
