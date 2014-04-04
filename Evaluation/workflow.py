import __init__
from util import TMP_DATA_DIR_PATH 
from evaluate import evaluate
from DataCleaning.userStatusWorkflow import getPreSet 
import numpy
from plot import plotTopDistribution

blacklist = set(['7955184','3373964','20393504', '3137471', '4341158'])

def workflow() :
    metric = []
    adset = set([line.strip().split()[1] for line in file(TMP_DATA_DIR_PATH+'topAdClickCnt.dict.final')])
    adidlist = []
    wholeResult = None
    total_advertisments = 0
    for adid in adset :
        if adid in blacklist : continue 
        adidlist.append(adid)
        res, finalres = evaluate(adid, 20, reCal=False, testing=True)
        if wholeResult == None :
            if finalres[-1][0] < 0.2 :
                wholeResult = numpy.array(finalres)
                total_advertisments += 1
        else :
            if finalres[-1][0] < 0.2 :
                wholeResult += numpy.array(finalres)
                total_advertisments += 1
        metric.append(res)
    linenum = 1
    for adid, res in zip(adidlist, metric) :
        print '|'.join([str(linenum), adid, str(res[0]), str(res[1])])
        linenum += 1
    wholeResult = wholeResult / total_advertisments
    print total_advertisments
    print wholeResult
    print numpy.mean(metric, axis=0)
    plotTopDistribution(wholeResult)

if __name__ == '__main__' :
    workflow()

