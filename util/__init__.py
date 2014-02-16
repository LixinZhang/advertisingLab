from ConfigParser import ConfigParser
import logging

cp = ConfigParser()
cp.read('../conf/config.conf')
LOG_LEVEL_MAP = {'DEBUG':logging.DEBUG, 'INFO':logging.INFO}

#Read Configuration Options from conf file
BASE_SVM_RANK_DIR = cp.get('SVM_RANK', 'BASE_SVM_RANK_DIR')
SVM_RANK_ARGS = cp.get('SVM_RANK', 'BASE_SVM_RANK_DIR') 

LOG_LEVEL = cp.get('PROJECT', 'LOG_LEVEL')

TMP_DATA_DIR_PATH = cp.get('DATA', 'TMP_DATA_DIR_PATH')
DATA_TRAINING = cp.get('DATA', 'DATA_TRAINING')
DATA_DESCRIPTION = cp.get('DATA', 'DATA_DESCRIPTION')
DATA_QUERY = cp.get('DATA', 'DATA_QUERY')
DATA_TITLE = cp.get('DATA', 'DATA_TITLE')
DATA_PROFILE = cp.get('DATA', 'DATA_PROFILE')
DATA_TRAINING_SAMPLE = cp.get('DATA', 'DATA_TRAINING_SAMPLE')

#Init global variables
logging.basicConfig(level=LOG_LEVEL_MAP[LOG_LEVEL])

