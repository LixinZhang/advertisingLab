import __init__
from util import logging
from BM25 import BM25
import os, sys
from SimilarityQueries import ctrCMP
from util import logging, TMP_DATA_DIR_PATH

def relevantSeed(fn_status, fn_docdata, keepAdID=None) :
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
    relevantSeedUsersSet = set(item[0] for item in seeduser[:100])
    nonrelevantSeedUsersSet = set(item[0] for item in seeduser[-200:])

    relevantQuery = {}
    nonrelevantQuery = {}
    for line in file(fn_docdata) :
        fields = line.strip().split('\x01')
        userid = fields[0]
        user_query = fields[1]
        if userid in relevantSeedUsersSet :
            tokens = user_query.split('|')
            for token in tokens :
                if token not in relevantQuery :
                    relevantQuery[token] = 0
                relevantQuery[token] += 1
        if userid in nonrelevantSeedUsersSet :
            tokens = user_query.split('|')
            for token in tokens :
                if token not in nonrelevantQuery :
                    nonrelevantQuery[token] = 0
                nonrelevantQuery[token] += 1
    relevantfreqToken = [(freq, token)for token, freq in relevantQuery.items()]
    relevantfreqToken.sort(reverse=True)
    nonrelevantfreqToken = [(freq, token) for token, freq in nonrelevantQuery.items()]
    nonrelevantfreqToken.sort(reverse=True)
    print len(relevantfreqToken)
    print len(nonrelevantfreqToken)
    relevantfreqToken = set([token for freq, token in relevantfreqToken[:70]])
    nonrelevantfreqToken = set([token for freq, token in nonrelevantfreqToken[:70]])
    commonTokens = relevantfreqToken & nonrelevantfreqToken
    for token in commonTokens :
        relevantfreqToken.remove(token)
        nonrelevantfreqToken.remove(token)
    return relevantfreqToken, nonrelevantfreqToken

class FeatureExtracter :
    def __init__(self, fn_querydata, fn_docdata, fn_transfer='./transfer.dict', fn_status='', keepAdID = '', isTransfer=False, isRelevanted=False) :
        self.Query = {}
        self.UserID2DocID = {}
        self.isRelevanted = isRelevanted
        self.keepAdID = keepAdID
        self.isTransfer = isTransfer
        
        if isRelevanted :
            relevantfreqToken, nonrelevantfreqToken = relevantSeed(fn_status, fn_docdata, keepAdID)
            relevantfreqToken = '|'.join(relevantfreqToken)
            nonrelevantfreqToken = '|'.join(nonrelevantfreqToken)

        for line in file(fn_querydata) :
            adid, userid, title, click_title, nonclick_title, desc, click_desc, nonclick_desc = line.strip().split('\x01')
            if self.isRelevanted :
                self.Query[userid] = [title, click_title, nonclick_title, desc, click_desc, nonclick_desc, relevantfreqToken, nonrelevantfreqToken]
            else :
                self.Query[userid] = [title, click_title, nonclick_title, desc, click_desc, nonclick_desc]
            
        tmpfile = file('tmp', 'w')
        docID = 0
        for line in file(fn_docdata) :
            fields = line.strip().split('\x01')
            userid = fields[0]
            tmpfile.write(fields[1])
            tmpfile.write('\n')
            self.UserID2DocID[userid] = docID
            docID += 1
        tmpfile.close()
        self.bm25 = BM25(fn_docs='tmp', delimiter='|', fn_transfer=fn_transfer)

    def dumpFeature(self, fn_out) :
        writer = file(fn_out, 'w')
        self.user2BM25 = dict()
        for userid in self.Query :
            querys = self.Query[userid]
            docid = self.UserID2DocID[userid]
            writer.write(userid)
            writer.write('\t')
            _transferAdID = self.keepAdID
            if self.isTransfer == False :
                _transferAdID = None
            writer.write('\t'.join([str(self.bm25.BM25Score(Query=query.split('|'), DocID=docid, transferAdID=_transferAdID)) for query in querys]))
            writer.write('\n')
        writer.close()

    def cleanup(self) :
        if os.path.exists('tmp') : os.system('rm tmp')

def pvClickFilter(pv, click) :
    # return True if pv and click satisfies threshold, False otherwise. 
    return True
    if int(pv) <= 3 and int(click) == 0  : return False
    if int(pv) <= 2 and int(click) == 1  : return False
    if int(pv) >= 50 : return False
    return True

def generate4Ranking(fn_status, fn_feature, fn_out) :
    status = {}
    for line in file(fn_status) :
        adid, userid, click, pv = line.strip().split()
        if pvClickFilter(pv, click) == False : continue
        if int(click) >= 1 :
            status[userid] = 1
        else :
            status[userid] = 0
    writer = file(fn_out, 'w')
    linenum = 1
    for line in file(fn_feature) :
        userid, rest = line.strip().split('\t',1)
        if userid not in status : continue
        features = rest.split()
        writer.write('%d qid:1 ' % status[userid])
        writer.write(' '.join(['%d:%s' % (i+1,item) for i, item in enumerate(features)]))
        writer.write('\n')
    writer.close()

def workflow(adID, isTransfer=False, isRelevanted=False) :
    fn_user_title_desc = TMP_DATA_DIR_PATH + 'user_title_desc/%s.user_title_desc.dat' % adID
    fn_queryTokens = TMP_DATA_DIR_PATH + 'userQuery/%s.user.queryTokens' % adID
    fn_transfer = '../data/tmp_data/transfer.dict'
    fn_status = TMP_DATA_DIR_PATH + 'status/%s.ad2userStatus.dat' % adID
    fn_out_userID4SVMRanking = TMP_DATA_DIR_PATH + 'feature/%s.userID4SVMRanking.dat' % adID

    transfer_tag, relevant_tag = '', ''
    if isTransfer == True : transfer_tag = '.transfer'
    if isRelevanted == True : relevant_tag = '.relevance'

    fn_out_feature = TMP_DATA_DIR_PATH + 'feature/%s.bm25.feature%s%s' % (adID, transfer_tag, relevant_tag)
    fn_out_ranking = TMP_DATA_DIR_PATH + 'feature/%s.bm25.ranking%s%s' % (adID, transfer_tag, relevant_tag)

    fe = FeatureExtracter(fn_user_title_desc, fn_queryTokens, fn_transfer, fn_status, adID, isTransfer, isRelevanted)
    fe.dumpFeature(fn_out_feature)
    generate4Ranking(fn_status, fn_out_feature, fn_out_ranking)

    writer = file(fn_out_userID4SVMRanking, 'w')
    for line in file(fn_out_feature) :
        writer.write(line.strip().split()[0])
        writer.write('\n')
    writer.close()
    
    writer = file(TMP_DATA_DIR_PATH + 'feature/%s.idx' % adID, 'w')
    writer.write('%s%d\n' % (adid, 1))
    writer.close()


if __name__ == '__main__' :
    if len(sys.argv) < 2 :
        logging.warn('Usages python %s ADID' % sys.argv[0])
        sys.exit(-1)
    ADID = sys.argv[1]
    workflow(ADID, False, False)
    #workflow(ADID, True, True)
    #workflow(ADID, True, True)
