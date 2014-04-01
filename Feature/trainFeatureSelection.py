import __init__
from util import TMP_DATA_DIR_PATH, logging
from SimilarityQueries import ctrCMP 

def getSeedUserSet(fn_status, keepAdID=None, keepPositive=2000, keepNegative=4000) :
    seeduser = []
    userid2status = {}
    for line in file(fn_status) :
        adid, userid, click, pv = line.strip().split()
        if adid != keepAdID : continue
        if userid not in userid2status :
            userid2status[userid] = [0,0]
        userid2status[userid][0] += int(click)
        userid2status[userid][1] += int(pv)
    for userid in userid2status :
        click = userid2status[userid][0]
        pv = userid2status[userid][1]
        seeduser.append((userid, int(click), int(pv)))
    seeduser.sort(cmp=ctrCMP, reverse=True)
    relevantSeedUsersSet = set(item[0] for item in seeduser[:keepPositive])
    nonrelevantSeedUsersSet = set(item[0] for item in seeduser[(-1) * keepNegative:])
    return relevantSeedUsersSet, nonrelevantSeedUsersSet

def dumpSelectedFeature(adset, seeduserDict, feature_tpl, writer) :
    fn_status_tpl = TMP_DATA_DIR_PATH + 'status/%s.ad2userStatus.dat'
    for i, adid in enumerate(adset) :
        fn_status = fn_status_tpl % adid
        fn_feature = feature_tpl % adid
        logging.info('Handling %s \n %s' % (fn_status, fn_feature))
        allset = seeduserDict[adid]
        status = {}
        for line in file(fn_status) :
            adid, userid, click, pv = line.strip().split()
            if userid not in allset : continue
            if int(click) >= 1 :
                status[userid] = 1
            else :
                status[userid] = 0
        for featureLine in file(fn_feature) :
            userid, rest = featureLine.strip().split('\t',1)
            if userid not in status : continue
            features = rest.split()
            writer.write('%d qid:%d ' % (status[userid], i+1))
            writer.write(' '.join(['%d:%s' % (j+1,item) for j, item in enumerate(features)]))
            writer.write('\n')
    writer.close()
 
def rankingFeatureSelection () :
    adset = set([line.strip().split()[1] for line in file(TMP_DATA_DIR_PATH+'topAdClickCnt.dict.final')])
    #adset = set(list(adset)[:2])
    blacklist = set(['20174985','3834142','3373964','4344041','8350700','2878230','3803920','20174982','4341158','6434934', '3219148','20035409'])
    adset = adset - blacklist
    feature = TMP_DATA_DIR_PATH + 'feature/%s.bm25.feature'
    featureTransfer = TMP_DATA_DIR_PATH + 'feature/%s.bm25.feature.transfer'
    featureTransferRelevance = TMP_DATA_DIR_PATH + 'feature/%s.bm25.feature.transfer.relevance'

    fn_status_tpl = TMP_DATA_DIR_PATH + 'status/%s.ad2userStatus.dat'
    selectionFeature = file(TMP_DATA_DIR_PATH + 'ranking/bm25.ranking', 'w')
    selectionFeatureTransfer = file(TMP_DATA_DIR_PATH + 'ranking/bm25.ranking.transfer', 'w')
    selectionFeatureTransferRelevance = file(TMP_DATA_DIR_PATH + 'ranking/bm25.ranking.transfer.relevance', 'w')
   
    logging.info('Dumping adid2idx')
    seeduserDict = {}
    writer = file(TMP_DATA_DIR_PATH + 'ranking/adid2idx.txt', 'w')
    for i, adid in enumerate(adset) :
        writer.write('%s\t%d\n' % (adid, i+1))
        fn_status = fn_status_tpl % adid 
        rset, nrset = getSeedUserSet(fn_status, adid)
        seeduserDict[adid] = rset.union(nrset)
    writer.close()

    dumpSelectedFeature(adset, seeduserDict, feature, selectionFeature) 
    dumpSelectedFeature(adset, seeduserDict, featureTransfer, selectionFeatureTransfer) 
    dumpSelectedFeature(adset, seeduserDict, featureTransferRelevance, selectionFeatureTransferRelevance)
 
if __name__ == '__main__' :
    rankingFeatureSelection()

     
