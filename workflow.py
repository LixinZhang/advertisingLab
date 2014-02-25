from util import logging, TMP_DATA_DIR_PATH, DATA_TRAINING, DATA_DESCRIPTION, DATA_QUERY, DATA_TITLE, DATA_PROFILE, DATA_TRAINING_SAMPLE
from DataCleaning.dataUtil import generateTopAdsUsersByClick, generateAd2UsersGivenAdSet, generateUser2AdGivenAd2User, dumpAd2UserStatus, dumpUserRawFeatureGivenUserSet

from Feature import topicLDA
from Feature.featureUtil import expandFeatureId2Tokens, getUserFeatureSet, joinResult4SVMRanking
from util import SVM_RANK
from util.common import dumpList2File, dumpDict2File

from Evaluation.ctrDistribution import ctrDistribution
from Evaluation.plot import displaySingleAd

def dataCleaning() :
    logging.info('===Data Cleaning Processing===')
    input_file = DATA_TRAINING_SAMPLE
    adClickCntList = generateTopAdsUsersByClick(input_file)
    dumpList2File(adClickCntList, TMP_DATA_DIR_PATH + 'topAdClickCnt.dict')

    adSet = set()
    for line in file(TMP_DATA_DIR_PATH + 'topAdClickCnt.dict') :
        cnt, adid = line.strip().split()
        adSet.add(adid)
    ad2Users = generateAd2UsersGivenAdSet(input_file, adSet)
    dumpDict2File(ad2Users, TMP_DATA_DIR_PATH + 'ad2UsersGivenAdSet.dict')
    userDict = generateUser2AdGivenAd2User(TMP_DATA_DIR_PATH + 'ad2UsersGivenAdSet.dict', adViewThreshold = 10)
    dumpDict2File(userDict, TMP_DATA_DIR_PATH + 'user2AdGivenAd2User.dict')
    userSet = set()
    for line in file(TMP_DATA_DIR_PATH + 'user2AdGivenAd2User.dict') :
        user, ads = line.strip().split('\x01')
        userSet.add(user)
    
    dumpUserRawFeatureGivenUserSet(input_file, userSet, TMP_DATA_DIR_PATH + 'userRawFeature.dict')

def featureEngineering() :
    logging.info('===Feature Engineering Processing===')
    query_set, desc_set, title_set = getUserFeatureSet()
    aggregateUserfile = TMP_DATA_DIR_PATH + 'userRawFeature.dict'
    expandId2TokensResultFile = TMP_DATA_DIR_PATH + 'userRawExpandTokens.dict'
    expandFeatureId2Tokens(aggregateUserfile, expandId2TokensResultFile, query_set, desc_set, title_set)
    
    tmp_file = file(TMP_DATA_DIR_PATH + 'tmp', 'w')
    fn_userRawExpandTokens = expandId2TokensResultFile
    for line in file(fn_userRawExpandTokens) :
        userid, query, title, desc = line.strip().split('\x01')
        tmp_file.write(query)
        tmp_file.write('\n')
    tmp_file.close()

    lda = topicLDA.LDA(TMP_DATA_DIR_PATH + 'tmp')
    lda.run(num_topics=200, fn_bow=TMP_DATA_DIR_PATH+'corpus.svmlight', fn_out_topic=TMP_DATA_DIR_PATH+'LDA_corpus.svmlight')
    os.system('rm ' + TMP_DATA_DIR_PATH + 'tmp')

    joinResult4SVMRanking(fn_trainFeature=TMP_DATA_DIR_PATH+'LDA_corpus.svmlight', 
    fn_ad2userStatus=TMP_DATA_DIR_PATH+'ad2userStatus.dict', fn_out_SVMRanking=TMP_DATA_DIR_PATH+'finalData4SVMRanking.dat')

def Training():
    logging.info('===Trainng Processing===')
    features = TMP_DATA_DIR_PATH + 'finalData4SVMRanking.dat'
    model = TMP_DATA_DIR_PATH + 'SVMRanking.model'
    SVM_RANK.svm_rank_learn(features, model, args=' -c 10 ')

def Prediction() :
    logging.info('===Prediction Processing===')
    predictions = TMP_DATA_DIR_PATH + 'SVMRanking.prediction'
    SVM_RANK.svm_rank_classify(features, model, predictions)

def Evaluation() :
    logging.info('===Evaluation Processing===')
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

if __name__ == '__main__' :
    # Let us just play it !
    dataCleaning()
    featureEngineering()
    Training()
    Prediction()
    Evaluation()
