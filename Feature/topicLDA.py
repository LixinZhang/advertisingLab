import __init__
from gensim import corpora, models, similarities
from util import logging, TMP_DATA_DIR_PATH
import os

class LDA(object) :
    def __init__(self, corpusFile = None) :
        if corpusFile == None :
            return
        self.corpusFile = corpusFile
        
    def generateDict(self) :
        self.dictionary = corpora.Dictionary(line.lower().split('|') for line in open(self.corpusFile))
        rare_tokens = [tokenid for tokenid, docfreq in self.dictionary.dfs.iteritems() if docfreq < 5]
        logging.debug('=====The number of tokens to be removed is %d =====' % len(rare_tokens))
        self.dictionary.filter_tokens(rare_tokens)
        logging.debug('=====Total %d tokens=====' % len(self.dictionary.dfs) )
        self.dictionary.compactify()

    def __iter__(self) :
        for line in open(self.corpusFile) :
            yield self.dictionary.doc2bow(line.lower().split('|'))

    def run(self, num_topics=200, fn_bow='corpus.svmlight', fn_out_topic='LDA_corpus.svmlight') :
        self.generateDict()
        logging.debug('=====start generateDict=====')
        corpora.SvmLightCorpus.serialize(fn_bow, lda)
        bow_corpus = corpora.SvmLightCorpus(fn_bow) 
        logging.debug('=====Topic Processing=====')
        lda_model = models.ldamodel.LdaModel(bow_corpus, id2word=lda.dictionary, num_topics=num_topics)
        corpus_lda = lda_model[bow_corpus]
        corpora.SvmLightCorpus.serialize(fn_out_topic, corpus_lda) 

if __name__ == '__main__' :
    userlist = []
    tmp_file = file(TMP_DATA_DIR_PATH + 'tmp', 'w')
    fn_userRawExpandTokens = TMP_DATA_DIR_PATH + 'userRawExpandTokens.dict'
    for line in file(fn_userRawExpandTokens) :
        userid, query, title, desc = line.strip().split('\x01')
        userlist.append(userid)
        tmp_file.write(query)
        tmp_file.write('\n')
    tmp_file.close()

    #lda = LDA('/Users/zhanglixin/research/kdd_cup/kddcup_lab/src/utils/corpus.dat')
    lda = LDA(TMP_DATA_DIR_PATH + 'tmp')
    lda.run(num_topics=200, fn_bow=TMP_DATA_DIR_PATH+'corpus.svmlight', fn_out_topic=TMP_DATA_DIR_PATH+'LDA_corpus.svmlight')
    os.system('rm' + TMP_DATA_DIR_PATH + 'tmp')



