import __init__
from util import logging, TMP_DATA_DIR_PATH, DATA_TRAINING, DATA_QUERY, DATA_TRAINING_SAMPLE
from DataCleaning.dataParser import dataParser

def query_Filter(topAdSet, fn_rawData) :
    logging.debug('generate Query Filter')
    queryIdSet = set()
    for line in file(fn_rawData) :
        Click, Impression, Display_url, AdID, AdvertiserID, Depth, \
        Position, QueryID, KeywordID, TitleID, DescriptionID, UserID = dataParser.parseTrainData(line)
        if AdID not in topAdSet : continue
        queryIdSet.add(QueryID)
    return queryIdSet

def generateTransferAdQueryTokenPair(topAdSet, fn_rawData, fn_rawQuery, fn_out, query_filter) :
    logging.debug('Loading Query Map')
    #query_filter = set(line.strip() for line in file(TMP_DATA_DIR_PATH+'queryID.set'))
    query_map = dict([(line.strip().split('\t')) for line in file(fn_rawQuery) if line.strip().split('\t')[0] in query_filter])
    Ad_QueryToken_map = {}
    token_map = {}
    logging.debug('Generating Ad_QueryToken_map')
    for line in file(fn_rawData) :
        Click, Impression, Display_url, AdID, AdvertiserID, Depth, \
        Position, QueryID, KeywordID, TitleID, DescriptionID, UserID = dataParser.parseTrainData(line)
        if AdID not in topAdSet : continue
        if AdID not in Ad_QueryToken_map :
            Ad_QueryToken_map[AdID] = {}
        tokens = query_map[QueryID].split('|')
        for token in tokens :
            if token not in token_map :
                token_map[token] = 0
            token_map[token] += 1
            if token not in Ad_QueryToken_map[AdID] :
                Ad_QueryToken_map[AdID][token] = 0
            Ad_QueryToken_map[AdID][token] += 1
    logging.debug('Dumping Transfer info to file')
    writer = file(fn_out, 'w')
    for Ad in Ad_QueryToken_map :
        for token in Ad_QueryToken_map[Ad]:
            #print token, Ad_QueryToken_map[Ad][token],token_map[token]
            writer.write('%s\t%s\t%f\n' % (Ad, token, Ad_QueryToken_map[Ad][token] * 1.0 / token_map[token]))
    writer.close()

if __name__ == '__main__' :

    fn_topAd = TMP_DATA_DIR_PATH + 'topAdClickCnt.dict'
    hotad = [line.strip().split()[1] for line in file(fn_topAd)]
    topAdSet = set(hotad[:100])
    fn_rawData = DATA_TRAINING
    fn_rawQuery = DATA_QUERY
    fn_out = TMP_DATA_DIR_PATH + 'transfer.dict'
    query_filter = query_Filter(topAdSet, fn_rawData)
    generateTransferAdQueryTokenPair(topAdSet, fn_rawData, fn_rawQuery, fn_out, query_filter)
