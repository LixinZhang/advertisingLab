import logging
from gensim import corpora, models, similarities
import heapq
import numpy
import sys

def ctrCMP(itemA, itemB) :
    uid, click_a, pv_a = itemA
    uid, click_b, pv_b = itemB
    if click_a > click_b: return 1
    if click_a == click_b :
        if (click_a*1.0/pv_a) > (click_b*1.0/pv_b) : return 1
        if pv_a < pv_b : return 1
    return -1

class ExpandUsersHandler : 

    def __init__(self, corpusFile) :
        self.corpusFile = corpusFile
        self.prepareForUserModel()
        
    def iterFile(self, fn=None) :
        if fn == None : fn = self.corpusFile
        for line in open(fn) :
            yield self.tfidf[self.dictionary.doc2bow(line.strip().split('\x01')[1].split('|'))]
 
    def TODO(self, raw_corpus, fn_bow_out ) :
        corpora.SvmLightCorpus.serialize(fn_bow_out, self.iterFile(raw_corpus))
        
    def prepareForUserModel(self) :
        texts = []
        self.docID2UserID = {}
        docID = 0
        for line in open(self.corpusFile):
            fields = line.split('\x01')
            texts.append(fields[1].split('|'))
            self.docID2UserID[docID] = fields[0]
            docID += 1
        #return


        self.dictionary = corpora.Dictionary(texts)
        rare_tokens = [tokenid for tokenid, docfreq in self.dictionary.dfs.iteritems() if docfreq < 6]
        self.dictionary.filter_tokens(rare_tokens)
        self.dictionary.compactify()
        #self.dictionary.save('userModel.dict')
        self.corpus = [self.dictionary.doc2bow(text) for text in texts]
        #corpora.MmCorpus.serialize('userModel.mm', self.corpus)
        self.tfidf = models.TfidfModel(self.corpus, id2word=self.dictionary)
        self.index = similarities.MatrixSimilarity(self.tfidf[self.corpus])

    def SimilarityUsers(self, fn_seedUser) :
        #dictionary = corpora.Dictionary.load('userModel.dict')
        #corpus = corpora.MmCorpus('userModel.mm')
        for line in file(fn_seedUser) :
            user = line.strip().split('|')
            user = self.dictionary.doc2bow(user)
            sims = self.index[self.tfidf[user]]
            sims = sorted(enumerate(sims), key=lambda item: -item[1])
            print sims[:20]

    def RocchioAlgorithm(self, docs_relevant, docs_nonrelevant) :
        len_relevant = len(docs_relevant)
        len_nonrelevant = len(docs_nonrelevant)
        dict_relevant = dict()
        dict_nonrelevant = dict()
        for doc in docs_relevant :
            for key, val in dict(doc).items() :
                if key not in dict_relevant :
                    dict_relevant[key] = 0.0
                dict_relevant[key] += 2*val
        for key in dict_relevant :
            dict_relevant[key] = dict_relevant[key]/len_relevant

        for doc in docs_nonrelevant :
            for key, val in dict(doc).items() :
                if key not in dict_nonrelevant :
                    dict_nonrelevant[key] = 0.0
                dict_nonrelevant[key] += val
            dict_nonrelevant[key] = dict_nonrelevant[key]/len_nonrelevant

        all_Keys = list(set(dict_relevant.keys()).union(set(dict_nonrelevant.keys())))
        all_Keys.sort()
        res = []        
        for key in all_Keys :
            res.append((key, dict_relevant.get(key,0.0) - dict_nonrelevant.get(key,0.0)))
        return res

    def getSeedUsers(self, fn_raw_seed_user, wholeUsers=None) :

        if wholeUsers == None :
            wholeUsers = self.corpusFile

        #self.dictionary = corpora.Dictionary.load('userModel.dict')
        #self.corpus = corpora.MmCorpus('userModel.mm')
        #self.tfidf = models.TfidfModel(self.corpus, id2word=self.dictionary)
        #self.index = similarities.MatrixSimilarity(self.tfidf[self.corpus])

        seeduser = []
        userid2status = {}
        for line in file(fn_raw_seed_user) :
            adid, userid, click, pv = line.strip().split()
            if userid not in userid2status :
                userid2status[userid] = [0,0]
            userid2status[userid][0] += int(click)
            userid2status[userid][1] += int(pv)
        for userid in userid2status :
            click = userid2status[userid][0]
            pv = userid2status[userid][1]
            seeduser.append((userid, int(click), int(pv)))
        seeduser.sort(cmp=ctrCMP, reverse=True)
        relevantSeedUsersSet = set(item[0] for item in seeduser[:80])
        nonrelevantSeedUsersSet = set(item[0] for item in seeduser[-20:])
        selectedSeedUsersSet = relevantSeedUsersSet.union(nonrelevantSeedUsersSet)
        idx = 0

        relevantSeed = []
        nonrelevantSeed = []
        writer = file('similarityUsers.dat', 'w')
        
        BaseUserSet = set()
        
        for line in file(wholeUsers) :
            fields = line.strip().split('\x01')
            uid = fields[0]
            if uid not in selectedSeedUsersSet : continue
            query = fields[1].split('|')
            query_bow = self.dictionary.doc2bow(query)
            query_tfidf = self.tfidf[query_bow]

            if uid in relevantSeedUsersSet :
                relevantSeed.append(query_tfidf)
            if uid in nonrelevantSeedUsersSet :
                nonrelevantSeed.append(query_tfidf)

            sims = self.index[query_tfidf]
            sims = sorted(enumerate(sims), key=lambda item: -item[1])
            #print idx, query_tfidf
            for item in sims[:1000] :
                BaseUserSet.add(self.docID2UserID[item[0]])
                writer.write('%s\t%s\t%f\n' % (uid, self.docID2UserID[item[0]], item[1]))
            idx += 1
        writer.close()

        writer = file('uniformSimilarityUsers.dat', 'w')
        uniformQuery = self.RocchioAlgorithm(relevantSeed, nonrelevantSeed)
        sims = self.index[uniformQuery]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        for item in sims[:len(BaseUserSet) * 3] :
            writer.write('%s\t%s\t%f\n' % ('uid', self.docID2UserID[item[0]], item[1]))
        writer.close()

    def trannformUserDoc(self, fn, fn_out2rank) :
        writer = file(fn_out2rank, 'w')
        userset = set()
        for line in file(fn) :
            uid, userid, score = line.strip().split()
            userset.add(userid)
        for line in file(self.corpusFile) :
            fields = line.split('\x01')
            if fields[0] not in userset : continue
            writer.write('%s\x01%s\n' % (fields[0], fields[1]))
        writer.close()


def ctrGivenUserSet(userSet, fn_status) :
    totalClick = 0
    totalPv = 0
    totalClickGivenUserSet = 0
    totalPvGivenUserSet = 0
    cnt = 0
    ctr = {}
    totalCtr = {}
    for line in file(fn_status) :
        adid, userid, click, pv = line.strip().split()
        if userid == '0' : continue
        cnt += 1
        click = int(click)
        pv = int(pv)
        if userid in userSet :
            totalPvGivenUserSet += pv
            totalClickGivenUserSet += click
            ctr[userid] = (click, pv)
        totalCtr[userid] = (click, pv)
        totalClick += click
        totalPv += pv
    avg_click = totalClick*1.0/cnt
    avg_pv = totalPv*1.0/cnt

    #print avg_click, avg_pv

    print numpy.mean([(totalCtr[userid][0]+avg_click)*1.0 / (totalCtr[userid][1]+avg_pv) for userid in totalCtr])
    print numpy.mean([(ctr[userid][0]+avg_click)*1.0 / (ctr[userid][1]+avg_pv) for userid in ctr])

def getExpandUserSet(fn_expandUserSet) :
    uidset = set()
    idx = 0
    for line in file(fn_expandUserSet) :
        uid, recUid, score = line.strip().split()
        uidset.add(recUid)
        idx+=1
        #if idx == 1536 : break
    return uidset

def joinFinalDat4SvmRanking(fn_trans, fn_toRank, fn_status, fn_result) :
    status = {}
    for line in file(fn_status) :
        adid, userid, click, pv = line.strip().split()
        if int(click) >= 1 :
            status[userid] = 1
        else :
            status[userid] = 0
    reader = file(fn_trans)
    writer = file(fn_result, 'w')
    for line in file(fn_toRank) :
        tmp, rest = line.strip().split(' ',1)
        uid = reader.readline().strip().split('\x01')[0]
        writer.write('%d qid:1 %s\n' % (status[uid], rest))
    writer.close()

if __name__ == '__main__' :
    seedUsers = '/Users/zhanglixin/research/kdd_cup/advertisingLab/data/tmp_data/seed.users'
    #rawUsers = '/Users/zhanglixin/research/kdd_cup/advertisingLab/data/tmp_data/userRawExpandTokens.dict'
    #rawUsers = '/Users/zhanglixin/research/kdd_cup/advertisingLab/data/tmp_data/userRawExpandTokens.dict.20192676'
    rawUsers = './userRawExpandTokens.dict.20192676.filter'
    fn_status = '20192676.userStatus.old'
    fn_expandUserSet = 'similarityUsers.dat'
    fn_uniform = 'uniformSimilarityUsers.dat'

    joinFinalDat4SvmRanking('fn_uniform.trans', 'fn_uniform.toRank', fn_status, 'fn_result4Ranking.dat')



    sys.exit(0)

    #rawUsers = '/Users/zhanglixin/research/kdd_cup/advertisingLab/data/tmp_data/seed.users'
    euh = ExpandUsersHandler(rawUsers)
    #euh.SimilarityUsers(seedUsers)
    euh.getSeedUsers(fn_status)
    
    euh.trannformUserDoc(fn_uniform, 'fn_uniform.trans')
    euh.TODO('fn_uniform.trans', 'fn_uniform.toRank')

    userSet = getExpandUserSet(fn_expandUserSet)
    userSet2 = getExpandUserSet(fn_uniform)
    print len(userSet)
    ctrGivenUserSet(userSet, fn_status)
    print '*' * 20
    print len(userSet2)
    ctrGivenUserSet(userSet2, fn_status)



