import sys, os
import ConfigParser
import __init__
from util import BASE_SVM_RANK_DIR, SVM_RANK_ARGS, logging, TMP_DATA_DIR_PATH

class SVM_RANK :

    svm_rank_classify_command = BASE_SVM_RANK_DIR + 'svm_rank_classify'
    svm_rank_learn_command = BASE_SVM_RANK_DIR + 'svm_rank_learn'

    @staticmethod
    def svm_rank_classify(features, model, predictions):
        logging.info(('=='*10 + '%s' + '=='*10) % ( 'START SVM CLASSIFING'))
        svm_rank_classify_format = '%s %s %s %s'
        cmd_text = svm_rank_classify_format % (SVM_RANK.svm_rank_classify_command, features, model, predictions)
        logging.debug(cmd_text)
        os.system(cmd_text)

    @staticmethod
    def svm_rank_learn(features, output_model, args = '') :
        logging.info(('=='*10 + '%s' + '=='*10) % ( 'START SVM LEARNING'))
        svm_rank_learn_format = '%s %s %s %s'
        cmd_text = svm_rank_learn_format % (SVM_RANK.svm_rank_learn_command, args, features, output_model)
        logging.debug(cmd_text)
        os.system(cmd_text)

def workflow(adid) :
    model1 = TMP_DATA_DIR_PATH + 'model/bm25.model'
    model2 = TMP_DATA_DIR_PATH + 'model/bm25.model.transfer'
    model3 = TMP_DATA_DIR_PATH + 'model/bm25.model.transfer.relevance'

    features1 = TMP_DATA_DIR_PATH + 'feature/%s.bm25.ranking' % adid
    features2 = TMP_DATA_DIR_PATH + 'feature/%s.bm25.ranking.transfer' % adid
    features3 = TMP_DATA_DIR_PATH + 'feature/%s.bm25.ranking.transfer.relevance' % adid

    predictions1 = TMP_DATA_DIR_PATH + 'prediction/%s.bm25.prediction' % adid
    predictions2 = TMP_DATA_DIR_PATH + 'prediction/%s.bm25.prediction.transfer' % adid
    predictions3 = TMP_DATA_DIR_PATH + 'prediction/%s.bm25.prediction.transfer.relevance' % adid
    
    SVM_RANK.svm_rank_classify(features1, model1, predictions1)
    SVM_RANK.svm_rank_classify(features2, model2, predictions2)
    SVM_RANK.svm_rank_classify(features3, model3, predictions3)   
    

if __name__ == '__main__' :
    if len(sys.argv) < 2: 
        print 'Usages: python %s AdID' % sys.argv[0]
        sys.exit(-1)
    Adid = sys.argv[1]
    workflow(Adid)
