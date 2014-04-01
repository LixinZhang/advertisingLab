import __init__
from util import TMP_DATA_DIR_PATH 
from evaluate import evaluate
from DataCleaning.userStatusWorkflow import getPreSet 
import numpy

blacklist = set(['20174985','3834142','3373964','4344041','8350700','2878230','3803920','20174982','4341158','6434934', '3219148','20035409'])

def workflow() :
    metric = []
    adset = set([line.strip().split()[1] for line in file(TMP_DATA_DIR_PATH+'topAdClickCnt.dict.final')])
    adidlist = []
    for adid in adset :
        if adid in blacklist : continue 
        adidlist.append(adid)
        res = evaluate(adid, reCal=False)
        metric.append(res)
    for adid, res in zip(adidlist, metric) :
        print adid, res
    print numpy.mean(metric, axis=0)

if __name__ == '__main__' :
    workflow()

