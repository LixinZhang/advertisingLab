import __init__
from util.miniPlotTool import MiniPlotTool

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

def displaySingleAd(fn_ad2userCTR, limit=6) :
    plotTool = MiniPlotTool(baseConfig)
    for line in file(fn_ad2userCTR) :
        limit -= 1
        if limit < 1 : break
        adid, ctrs = line.strip().split('\01')
        ctrs = [float(ctr) for ctr in ctrs.split('\t')]
        X = range(len(ctrs))
        plotTool.addline({'X':X, 'Y':ctrs})
    plotTool.plot()
    plotTool.show()
    
if __name__ == '__main__' :
    #fn_ad2userCTR = TMP_DATA_DIR_PATH+"ad2userCTR.dict"
    #displaySingleAd(fn_ad2userCTR)
    pass