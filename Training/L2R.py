import __init__
from util import TMP_DATA_DIR_PATH
from classify import SVM_RANK

#SVM_RANK.svm_rank_learn(TMP_DATA_DIR_PATH+'ranking/bm25.ranking', TMP_DATA_DIR_PATH+'model/bm25.model.new',' -c 10 ')
SVM_RANK.svm_rank_learn(TMP_DATA_DIR_PATH+'ranking/bm25.ranking.transfer', TMP_DATA_DIR_PATH+'model/bm25.model.transfer.new',' -c 10 ')
#SVM_RANK.svm_rank_learn(TMP_DATA_DIR_PATH+'ranking/bm25.ranking.transfer.relevance', TMP_DATA_DIR_PATH+'model/bm25.model.transfer.relevance.new',' -c 10 ')
