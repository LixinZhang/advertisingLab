import __init__
from util import logging, TMP_DATA_DIR_PATH
from ctrDistribution import ctrDistribution
from plot import displaySingleAd

if __name__ == '__main__' :

    fn_rankingResult = TMP_DATA_DIR_PATH + 'SVMRanking.prediction'
    fn_userID4SVMRanking = TMP_DATA_DIR_PATH + 'userid4SVMRanking.dat'
    fn_adId2Idx = TMP_DATA_DIR_PATH + 'adid2Idx.dict'
    fn_ad2userStatus = TMP_DATA_DIR_PATH + 'ad2userStatus.dict'

    fn_out_ad2userCTR = TMP_DATA_DIR_PATH + "ad2userCTR.dict"
    fn_SVMRanking=TMP_DATA_DIR_PATH+'finalData4SVMRanking.dat'

    #calculate ctr distribution
    ctrDistribution(fn_SVMRanking, fn_rankingResult, fn_userID4SVMRanking, fn_adId2Idx, fn_ad2userStatus, fn_out_ad2userCTR)
    #plot single ad's users' ctr distribution
    displaySingleAd(fn_out_ad2userCTR)