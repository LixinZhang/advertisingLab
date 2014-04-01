import __init__
from dataUtil import *
import userStatusWorkflow
from genTitleDesc import genTitleDesc
from genQueryToken import genQueryToken

if __name__ == '__main__' :
    input_file = DATA_TRAINING
    adSet, userSet = userStatusWorkflow.getPreSet(input_file)
    #userStatusWorkflow.joinStatus(input_file, adSet, userSet)
    '''
    # avoid memory overflow error
    for i in range(0,len(adSet),5) :
        adset = set(list(adSet)[i:i+5])
        print adset
        genTitleDesc(input_file, adset, userSet)
    '''
    for adid in adSet :
        genQueryToken(input_file, adid)


