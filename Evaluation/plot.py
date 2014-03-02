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

def displayGlobalResult(fn_ad2userCTR, chunks=100) :
    plotTool = MiniPlotTool(baseConfig)
    finalRes = [0 for i in range(chunks)]
    rates = [(i + 1) * 1.0 / chunks for i in range(chunks)]
    X = range(1,chunks+1)
    avaiableAdCnt = 0
    for line in file(fn_ad2userCTR) :
        adid, ctrs = line.strip().split('\01')
        ctrs = [float(ctr) for ctr in ctrs.split('\t')]
        if (len(ctrs) <= 50) : continue
        avaiableAdCnt += 1
        for i, rate in enumerate(rates) :
            finalRes[i] += numpy.mean(ctrs[:int(rate * len(ctrs))])

    finalRes = [res * 1.0 /avaiableAdCnt for res in finalRes]

    plotTool.addline({
        'X':X, 
        'Y':finalRes,
        'marker' : 'o',
        'color' : 'b',
        'label' : 'Top',
        'linewidth' : 2,})
    plotTool.plot()
    plotTool.show()
    
if __name__ == '__main__' :
    fn_ad2userCTR = TMP_DATA_DIR_PATH+"ad2userCTR.dict"
    #dumpCTRDistributionPlot(fn_ad2userCTR)
    displayGlobalResult(fn_ad2userCTR)
    pass
