import __init__
from util.miniPlotTool import MiniPlotTool
from util import TMP_DATA_DIR_PATH, logging
import numpy

import pylab as pl

baseConfig = {
        #'figsize' : (6,8),
        #'axis': [0,line_Num,0,10 * m],
        'title' : 'CTR Distribution',
        'ylabel' : 'Y value',
        'grid' : True,
        #'xaxis_locator' : 0.5,
        #'yaxis_locator' : 1,
        #'legend_loc' : 'upper right',
        #'xticks' : {'ticks_rotation':10, 'x_idx':[0,1,2,3,4,5,6,7,8,9], 'x_lable':['zero','one','two','three','four','five','six','seven','eight','nine']}
    }

def dumpCTRDistributionPlot(fn_ad2userCTR, output_dir = '/Users/zhanglixin/research/kdd_cup/advertisingLab/data/tmp_data/plot_out/') :
    for line in file(fn_ad2userCTR) :
        plotTool = MiniPlotTool(baseConfig)
        adid, ctrs = line.strip().split('\01')
        logging.debug(adid)
        ctrs = [float(ctr) for ctr in ctrs.split('\t')]
        plotTool.addline({'X':range(len(ctrs)), 'Y':ctrs})
        plotTool.plot()
        plotTool.save(output_dir + adid + '.png')


def prepareData(fn_ad2userCTR, chunks=50) :
    print fn_ad2userCTR
    finalRes = [0 for i in range(chunks)]
    rates = [(i + 1) * 1.0 / chunks for i in range(chunks)]
    X = range(1,chunks+1)
    avaiableAdCnt = 0
    for line in file(fn_ad2userCTR) :
        adid, ctrs = line.strip().split('\01')
        ctrs = [float(ctr) for ctr in ctrs.split('\t')]
        #ctrs = ctrs[:5000]
        if (len(ctrs) <= 50) : continue
        avaiableAdCnt += 1
        for i, rate in enumerate(rates) :
            right = int(rate * len(ctrs))
            if i == 0 : left = 0
            else :left = int((rates[i-1]) * len(ctrs))
            left = 0
            finalRes[i] += numpy.mean(ctrs[left:right])
            #finalRes[i] = numpy.mean(ctrs[left:right])
            #print finalRes[i]

    finalRes = [res * 1.0 /avaiableAdCnt for res in finalRes]
    return X, finalRes



def displayGlobalResult(fn_ad2userCTR, fn_ad2userCTR_cmp, fn_ad2userCTR_relevant, chunks=50, plot=True) :
    X1, finalRes1 = prepareData(fn_ad2userCTR, chunks)
    X2, finalRes2 = prepareData(fn_ad2userCTR_cmp, chunks)
    X3, finalRes3 = prepareData(fn_ad2userCTR_relevant, chunks)
    
    if plot == False : return zip(finalRes1, finalRes2)

    plotTool = MiniPlotTool(baseConfig)
    plotTool.addline({
        'X':X1, 
        'Y':finalRes1,
        #'marker' : 'o',
        'color' : 'b',
        'label' : 'ORI',
        'linewidth' : 2,})
    
    plotTool.addline({
        'X':X2, 
        'Y':finalRes2,
        #'marker' : 'o',
        'color' : 'b',
        'label' : 'CMP',
        'linewidth' : 2,})

    plotTool.addline({
        'X':X3, 
        'Y':finalRes3,
        #'marker' : 'o',
        'color' : 'b',
        'label' : 'relevant',
        'linewidth' : 2,})

 
    plotTool.plot()
    plotTool.show()
    return zip(finalRes1, finalRes2, finalRes3)


def plotTopDistribution(data) :

    Y1 = [item[0] for item in data]
    Y2 = [item[1] for item in data]
    X_axis_length = len(Y1)
    X = range(X_axis_length)
    x_lable = ['CTR@%d%%' % ((i+1) * 100/X_axis_length) for i in X]
    xticks = {'ticks_rotation':10, 'x_idx':range(X_axis_length), 'x_lable':x_lable}
    baseConfig = {
        #'figsize' : (6,8),
        #'axis': [0,line_Num,0,10 * m],
        'title' : 'TransferBM25 Comparison with ClassicalBM25',
        'ylabel' : 'Impr@N%',
        'grid' : True,
        #'xaxis_locator' : 0.5,
        'yaxis_locator' : 0.015,
        #'legend_loc' : 'upper right',
        'xticks' : xticks
    }
    tool = MiniPlotTool(baseConfig)

    lineConf = {
        'X' : X,
        'Y' : Y1,
        'marker' : 'o',
        #'color' : 'b',
        #'markerfacecolor' : 'r',
        'label' : 'Classical BM25',
        'linewidth' : 3,
        #'linestyle' : '--'
    }
    lineConf2 = {
        'X' : X,
        'Y' : Y2,
        'marker' : 'o',
        'color' : 'b',
        #'markerfacecolor' : 'b',
        'label' : 'Transfer BM25',
        'linewidth' : 3,
        'linestyle' : '--'
    }
    #tool.plotSingleLine(lineConf)
    print tool.addline(lineConf)
    print tool.addline(lineConf2)
    
    tool.plot()
    tool.show()


    
if __name__ == '__main__' :
    #fn_ad2userCTR = TMP_DATA_DIR_PATH+"ad2userCTR.dict"
    #dumpCTRDistributionPlot(fn_ad2userCTR)
    #displayGlobalResult(fn_ad2userCTR)
    data_10 = [(0.22757682,0.24243649),
            (0.1858024,0.19079852),
            (0.15344257,0.15584889),
            (0.13176402,0.13330674),
            (0.11790079,0.11821518),
            (0.10616274,0.10622164),
            (0.09741966,0.09745177),
            (0.09101447,0.09094719),
            (0.08613917,0.08602828),
            (0.08221415,0.08221415)]
    
    data_20 = [[ 0.23130471,0.25412292],
         [ 0.22757682,0.24243649],
         [ 0.20728206,0.21615155],
         [ 0.1858024,0.19079852],
         [ 0.16778339,0.17147597],
         [ 0.15344257,0.15584889],
         [ 0.14140055,0.14346368],
         [ 0.13176402,0.13330674],
         [ 0.12391467,0.12516454],
         [ 0.11790079,0.11821518],
         [ 0.11168482,0.1116685 ],
         [ 0.10616274,0.10622164],
         [ 0.10148065,0.10148795],
         [ 0.09741966,0.09745177],
         [ 0.09395642,0.09395174],
         [ 0.09101447,0.09094719],
         [ 0.08840643,0.08833176],
         [ 0.08613917,0.08602828],
         [ 0.08406119,0.08399539],
         [ 0.08221415,0.08221415]]
    plotTopDistribution(data_20)
    pass
