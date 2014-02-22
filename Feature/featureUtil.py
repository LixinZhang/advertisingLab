import __init__
import sys
from util import logging, TMP_DATA_DIR_PATH, DATA_TRAINING, DATA_DESCRIPTION, DATA_QUERY, DATA_TITLE, DATA_PROFILE, DATA_TRAINING_SAMPLE
from DataCleaning.dataUtil import dumpDict2File

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
    
def joinResult4SVMRanking(fn_trainFeature=TMP_DATA_DIR_PATH+'LDA_corpus.svmlight', 
    fn_ad2userStatus=TMP_DATA_DIR_PATH+'ad2userStatus.dict',
    fb_out_SVMRanking='') :
    logging.info('=====joinResult4SVMRanking Start=====')
    userFeature = {}
    userlist = []
    fn_userRawExpandTokens = TMP_DATA_DIR_PATH + 'userRawExpandTokens.dict'
    for line in file(fn_userRawExpandTokens) :
        userid, query, title, desc = line.strip().split('\x01')
        userlist.append(userid)

    trainFeature = file(fn_trainFeature)
    for userid in userlist :
        tmp, feature_str = trainFeature.readline().strip().split(' ',1)
        userFeature[userid] = feature_str

    logging.debug('=====load raw training Feature Done.=====')
    logging.debug('=====join final data start=====')
    output = file(fb_out_SVMRanking, 'w')

    adid2Idx = {}
    idx = 1
    format = '%d qid:%s %s\n'
    for line in file(fn_ad2userStatus) :
        adid, userid, click, impression = line.strip().split('\t')
        if adid not in adid2Idx :
            adid2Idx[adid] = idx
            idx += 1
        click = int(click)
        impression = int(impression)
        status = 1
        if click > 5 : status = 4
        elif click > 2 : status = 3
        elif click > 0 : status = 2

        if userid not in userFeature :
            logging.warn('%s not in userFeature' % userid)
            continue
        output.write(format % (status, adid2Idx[adid], userFeature[userid]))
    output.close()

    dumpDict2File(adid2Idx, TMP_DATA_DIR_PATH+'adid2Idx.dict')




if __name__ == '__main__' :
    query_set, desc_set, title_set = getUserFeatureSet()
    aggregateUserfile = TMP_DATA_DIR_PATH + 'userRawFeature.dict'
    expandId2TokensResultFile = TMP_DATA_DIR_PATH + 'userRawExpandTokens.dict'
    expandFeatureId2Tokens(aggregateUserfile, expandId2TokensResultFile, query_set, desc_set, title_set)
    joinResult4SVMRanking(fb_out_SVMRanking=TMP_DATA_DIR_PATH+'finalData4SVMRanking.dat')


