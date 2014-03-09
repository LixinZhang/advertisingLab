import __init__
import sys
from util import logging, TMP_DATA_DIR_PATH, DATA_TRAINING, DATA_DESCRIPTION, DATA_QUERY, DATA_TITLE, DATA_PROFILE, DATA_TRAINING_SAMPLE
from util.common import dumpDict2File
from topicLDA import LDA

def getUserFeatureSet() :
    logging.info('=========start getUserFeatureSet processing=========')
    query_set_fn = TMP_DATA_DIR_PATH + 'queryID.set'
    desc_set_fn = TMP_DATA_DIR_PATH + 'descID.set'
    title_set_fn = TMP_DATA_DIR_PATH + 'titleID.set'
    query_set = set([query.strip() for query in file(query_set_fn)])
    desc_set = set([desc.strip() for desc in file(desc_set_fn)])
    title_set = set([title.strip() for title in file(title_set_fn)])
    return query_set, desc_set, title_set

def expandFeatureId2Tokens(aggregateUserfile, expandId2TokensResultFile, query_set, desc_set, title_set) :
    logging.info('=========start expandFeatureId2Tokens processing=========')
    description_map = dict([(line.strip().split('\t')) for line in file(DATA_DESCRIPTION) if line.split('\t',1)[0] in desc_set])
    logging.debug('Read %s Done.' % DATA_DESCRIPTION)
    query_map = dict([(line.strip().split('\t')) for line in file(DATA_QUERY) if line.split('\t',1)[0] in query_set])
    logging.debug('Read %s Done.' % DATA_QUERY)
    title_map = dict([(line.strip().split('\t')) for line in file(DATA_TITLE) if line.split('\t',1)[0] in title_set])
    logging.debug('Read %s Done.' % DATA_TITLE)

    #profile_map = dict([(line.strip().split('\t', 1)) for line in file(DATA_PROFILE) if line.split('\t')])
    dump_format = '%s\x01%s\x01%s\x01%s\n'
    expandId2TokensResult = file(expandId2TokensResultFile, 'w') 
    logging.debug('start joining tokens')
    for line in file(aggregateUserfile) :
        userID, tmp_str = line.strip().split('\x01')
        queryIDlist, titleIDlist, descIDList = tmp_str.split('\x02')
        queryExpandTokensStr = '|'.join([query_map[queryId] for queryId in queryIDlist.split('\t') if queryId != ''])
        titleExpandTokensStr = '|'.join([title_map[titleId] for titleId in titleIDlist.split('\t') if titleId != ''])
        descExpandTokensStr = '|'.join([description_map[descId] for descId in descIDList.split('\t') if descId != ''])
        expandId2TokensResult.write( dump_format % \
               (userID, queryExpandTokensStr, titleExpandTokensStr, descExpandTokensStr))
    expandId2TokensResult.close()

def genStatus(click, imps) :
    if click > 0 : 
        return 1
    else :
        return 0 
    '''
    status = 0
    if click == 0 :
        if imps > 20 : status = 0
        elif imps > 13 : status = 1
        elif imps > 7 : status = 2
        elif imps > 3 : status = 3
        else : status = 4
    else :
        if click > 7 : status = 10
        elif click > 5 : status = 9
        elif click > 2: status = 8
        else : status = 7
    '''
    return status
    
def joinResult4SVMRanking(fn_trainFeature, fn_ad2userStatus, fn_out_SVMRanking, fn_userRawExpandTokens, fn_userid4SVMRanking, fn_ad2UsersGivenAdSet) :
    '''
    fn_trainFeature=TMP_DATA_DIR_PATH+'LDA_corpus.svmlight'
    fn_ad2userStatus=TMP_DATA_DIR_PATH+'ad2userStatus.dict'
    fn_userRawExpandTokens = TMP_DATA_DIR_PATH + 'userRawExpandTokens.dict'

    '''

    logging.info('=====joinResult4SVMRanking Start=====')
    userFeature = {}
    userlist = []
    #fn_userRawExpandTokens = TMP_DATA_DIR_PATH + 'userRawExpandTokens.dict'
    for line in file(fn_userRawExpandTokens) :
        userid, query, title, desc = line.strip().split('\x01')
        userlist.append(userid)

    trainFeature = file(fn_trainFeature)
    for userid in userlist :
        fields = trainFeature.readline().strip().split(' ',1)
        if len(fields) != 2 : continue
        tmp, feature_str = fields
        if len(feature_str.split()) <= 5 : continue
        userFeature[userid] = feature_str

    logging.debug('=====load raw training Feature Done.=====')
    logging.debug('=====loading status map.=====')
    
    statusMap = {}
    for line in file(fn_ad2userStatus) :
        adid, userid, click, impression = line.strip().split('\t')
        click = int(click)
        impression = int(impression)
        status = genStatus(click, impression)
        statusMap[(adid, userid)] = status

    logging.debug('=====join final data start=====')
    output = file(fn_out_SVMRanking, 'w')
    format = '%d qid:%d %s\n'
    adid2Idx = {}
    
    #line number of userid4SVMRanking equals to output4SVMRanking's
    #fn_userid4SVMRanking = TMP_DATA_DIR_PATH+'userid4SVMRanking.dat'
    userid_output = file(fn_userid4SVMRanking, 'w')

    #fn_ad2UsersGivenAdSet = TMP_DATA_DIR_PATH + 'ad2UsersGivenAdSet.dict'
    idx = 1
    for line in file(fn_ad2UsersGivenAdSet) :
        adid, user_str = line.strip().split('\x01')
        if adid not in adid2Idx :
            adid2Idx[adid] = idx
            idx += 1
        userids = user_str.split('\t')
        for userid in userids :
            if userid not in userFeature or (adid, userid) not in statusMap:
                continue
            userid_output.write('%s\n' % userid)
            output.write(format % (statusMap[(adid, userid)], adid2Idx[adid], userFeature[userid]))

    output.close()
    userid_output.close()
    dumpDict2File(adid2Idx, TMP_DATA_DIR_PATH+'adid2Idx.dict')


def filterUserRawTokensGivenUserSet(fn_userRawExpandTokens, fn_out_userQueryTokens, userSet=None) :
    tmp_file = file(fn_out_userQueryTokens, 'w')
    for line in file(fn_userRawExpandTokens) :
        userid, query, title, desc = line.strip().split('\x01')
        if userid not in userSet : continue
        tmp_file.write(query)
        tmp_file.write('\n')
    tmp_file.close()

def genBagOfWordsFromUserQueryTokens(fn_userQueryTokens, fn_out_BOW) :
    lda = LDA(fn_userQueryTokens)
    lda.serializeBOW(fn_bow=fn_out_BOW)

def getUserSetFromAd2UserStatus(fn_ad2userStatus = TMP_DATA_DIR_PATH + 'ad2userStatus.dict') :
    userSet = set()
    for line in file(fn_ad2userStatus) :
        adid, userid, click, impression = line.strip().split('\t')
        userSet.add(userid)
    return userSet
    

if __name__ == '__main__' :
    query_set, desc_set, title_set = getUserFeatureSet()
    aggregateUserfile = TMP_DATA_DIR_PATH + 'userRawFeature.dict'
    expandId2TokensResultFile = TMP_DATA_DIR_PATH + 'userRawExpandTokens.dict'
    #expandFeatureId2Tokens(aggregateUserfile, expandId2TokensResultFile, query_set, desc_set, title_set)
    joinResult4SVMRanking(fn_out_SVMRanking=TMP_DATA_DIR_PATH+'finalData4SVMRanking.dat')


