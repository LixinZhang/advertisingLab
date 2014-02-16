import sys, os
import ConfigParser
import __init__
from __init__ import BASE_SVM_RANK_DIR, SVM_RANK_ARGS, logging

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

if __name__ == '__main__' :
    #test
    svm_rank = SVM_RANK()
    features = './corpus2learn.dat'
    model = 'output_model.tmp'
    svm_rank.svm_rank_learn(features, model)
    predictions = 'output_predictions.tmp'
    svm_rank.svm_rank_classify(features, model, predictions)
