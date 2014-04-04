import __init__
from util import logging, TMP_DATA_DIR_PATH
from ctrDistribution import ctrDistribution
from plot import displayGlobalResult
import sys

def testEvaluation() :
    #fn_rankingResult = TMP_DATA_DIR_PATH + 'SVMRanking_test.prediction'
    fn_rankingResult = '/Users/zhanglixin/research/tools/gensim/data4Evaluate/bm25.ranking.5k.prediction'
    fn_rankingResult_cmp = '/Users/zhanglixin/research/tools/gensim/data4Evaluate/bm25.ranking.5k.prediction.cmp'
    fn_rankingResult_relevant = '/Users/zhanglixin/research/tools/gensim/data4Evaluate/bm25.ranking.5k.prediction.relevant_trans'
    
    #fn_userID4SVMRanking = TMP_DATA_DIR_PATH + 'userid4SVMRanking_test.dat'
    fn_userID4SVMRanking = '/Users/zhanglixin/research/tools/gensim/data4Evaluate/userID4SVMRanking.dat.full'
    #fn_adId2Idx = TMP_DATA_DIR_PATH + 'adid2Idx_test.dict'
    fn_adId2Idx = '/Users/zhanglixin/research/tools/gensim/data4Evaluate/20192676_idx.txt'
    #fn_ad2userStatus = TMP_DATA_DIR_PATH + 'ad2userStatus_test.dict'
    fn_ad2userStatus = '/Users/zhanglixin/research/tools/gensim/data4Evaluate/20192676.userStatus.old'

    #fn_out_ad2userCTR = TMP_DATA_DIR_PATH + "ad2userCTR_test.dict"
    fn_out_ad2userCTR = '/Users/zhanglixin/research/tools/gensim/data4Evaluate/ad2userCTR.dat'
    fn_out_ad2userCTR_cmp = '/Users/zhanglixin/research/tools/gensim/data4Evaluate/ad2userCTR_cmp.dat'
    fn_out_ad2userCTR_relevant = '/Users/zhanglixin/research/tools/gensim/data4Evaluate/ad2userCTR_relevant.dat'
    #fn_SVMRanking=TMP_DATA_DIR_PATH+'finalData4SVMRanking_test.dat'
    fn_SVMRanking = '/Users/zhanglixin/research/tools/gensim/data4Evaluate/bm25.ranking.full'

    #calculate ctr distribution
    ctrDistribution(fn_SVMRanking, fn_rankingResult, fn_userID4SVMRanking, fn_adId2Idx, fn_ad2userStatus, fn_out_ad2userCTR)
    ctrDistribution(fn_SVMRanking, fn_rankingResult_cmp, fn_userID4SVMRanking, fn_adId2Idx, fn_ad2userStatus, fn_out_ad2userCTR_cmp)
    ctrDistribution(fn_SVMRanking, fn_rankingResult_relevant, fn_userID4SVMRanking, fn_adId2Idx, fn_ad2userStatus, fn_out_ad2userCTR_relevant)
    #plot single ad's users' ctr distribution
    displayGlobalResult(fn_out_ad2userCTR, fn_out_ad2userCTR_cmp, fn_out_ad2userCTR_relevant, 5)

def evaluate(adid, chunks=20, reCal=True, testing=False) :
    predictions1 = TMP_DATA_DIR_PATH + 'prediction/%s.bm25.prediction' % adid
    predictions2 = TMP_DATA_DIR_PATH + 'prediction/%s.bm25.prediction.transfer' % adid
    predictions3 = TMP_DATA_DIR_PATH + 'prediction/%s.bm25.prediction.transfer.relevance' % adid
    if testing :
        predictions1 += '.new'
        predictions2 += '.new'
        predictions3 += ''
    fn_userID4SVMRanking = TMP_DATA_DIR_PATH + 'feature/%s.userID4SVMRanking.dat' % adid
    fn_adId2Idx = TMP_DATA_DIR_PATH + 'feature/%s.idx' % adid
    fn_ad2userStatus = TMP_DATA_DIR_PATH + 'status/%s.ad2userStatus.dat' % adid
    fn_out_ad2userCTR = TMP_DATA_DIR_PATH + 'evaluation/%s.ad2userCTR' % adid
    fn_out_ad2userCTR_transfer = TMP_DATA_DIR_PATH + 'evaluation/%s.ad2userCTR.transfer' % adid
    fn_out_ad2userCTR_relevance = TMP_DATA_DIR_PATH + 'evaluation/%s.ad2userCTR.transfer.relevance' % adid

    fn_SVMRanking = TMP_DATA_DIR_PATH + 'feature/%s.bm25.ranking' % adid
   
    if reCal == True :
        #calculate ctr distribution
        ctrDistribution(fn_SVMRanking, predictions1, fn_userID4SVMRanking, fn_adId2Idx, fn_ad2userStatus, fn_out_ad2userCTR)
        ctrDistribution(fn_SVMRanking, predictions2, fn_userID4SVMRanking, fn_adId2Idx, fn_ad2userStatus, fn_out_ad2userCTR_transfer)
        ctrDistribution(fn_SVMRanking, predictions3, fn_userID4SVMRanking, fn_adId2Idx, fn_ad2userStatus, fn_out_ad2userCTR_relevance)
        
    finalres = displayGlobalResult(fn_out_ad2userCTR, fn_out_ad2userCTR_transfer, fn_out_ad2userCTR_relevance, chunks, False)
    top = finalres[0]
    total = finalres[-1]
    for item in finalres :
        print item
    return [(topCtr - totalCtr)/totalCtr for topCtr, totalCtr in zip(top, total)], finalres

if __name__ == '__main__' :
    if len(sys.argv) < 2:
        print 'Usages: python %s AdID' % sys.argv[0]
        sys.exit(-1)
    adid = sys.argv[1]
    #print evaluate(adid)
    print evaluate(adid, 20 ,True, True)
