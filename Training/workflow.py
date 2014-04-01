import classify
import __init__
from util import TMP_DATA_DIR_PATH
from DataCleaning import userStatusWorkflow

if __name__ == '__main__' :
    adset, userset = userStatusWorkflow.getPreSet('')
    blacklist = set(['20174985','3834142','3373964','4344041','8350700','2878230','3803920','20174982','4341158','6434934', '3219148','20035409'])
    adset = set([line.strip().split()[1] for line in file(TMP_DATA_DIR_PATH+'topAdClickCnt.dict.final')])
    for adid in adset :
        if adid in blacklist : continue
        print adid
        classify.workflow(adid ,testing=True)

