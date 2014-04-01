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
            print finalRes[i]

    finalRes = [res * 1.0 /avaiableAdCnt for res in finalRes]
    return X, finalRes



def displayGlobalResult(fn_ad2userCTR, fn_ad2userCTR_cmp, fn_ad2userCTR_relevant, chunks=50, plot=True) :
    X1, finalRes1 = prepareData(fn_ad2userCTR, chunks)
    X2, finalRes2 = prepareData(fn_ad2userCTR_cmp, chunks)
    X3, finalRes3 = prepareData(fn_ad2userCTR_relevant, chunks)
    
    if plot == False : return zip(finalRes1, finalRes2, finalRes3)

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
    
if __name__ == '__main__' :
    fn_ad2userCTR = TMP_DATA_DIR_PATH+"ad2userCTR.dict"
    #dumpCTRDistributionPlot(fn_ad2userCTR)
    displayGlobalResult(fn_ad2userCTR)
    pass
