import __init__
from util import logging,DATA_TRAINING
from DataCleaning import userStatusWorkflow
import featureExtracter

def run() :
    Adset, UserSet = userStatusWorkflow.getPreSet(DATA_TRAINING)
    for adid in Adset :
        logging.info('Now handling AD:' + adid)
        featureExtracter.workflow(adid, False, False)
        featureExtracter.workflow(adid, True, False)
        featureExtracter.workflow(adid, True, True)

if __name__ == '__main__' :
    run()

