import featureUtil
from featureUtil import filterUserRawTokensGivenUserSet, genBagOfWordsFromUserQueryTokens, getUserSetFromAd2UserStatus, TMP_DATA_DIR_PATH, logging
import sys

if __name__ == '__main__' :
    fn_userRawExpandTokens = TMP_DATA_DIR_PATH + 'userRawExpandTokens.dict'
    fn_userQueryTokens = TMP_DATA_DIR_PATH + 'userRawExpandTokensGivenUserSet.dict'
    fn_ad2userStatus = TMP_DATA_DIR_PATH + 'ad2userStatus.dict'
    userSet = getUserSetFromAd2UserStatus(fn_ad2userStatus)
    
    logging.info('Total User Count to be filter : %d ' % len(userSet))

    filterUserRawTokensGivenUserSet(fn_userRawExpandTokens, fn_userQueryTokens, userSet=userSet)

    fn_out_BOW = TMP_DATA_DIR_PATH + 'corpusGivenUserSet.svmlight'
    genBagOfWordsFromUserQueryTokens(fn_userQueryTokens, fn_out_BOW)