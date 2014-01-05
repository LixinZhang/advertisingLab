import sys
from trainSet_util import TrainingSet_util

class Learning2rank4BT :
    def __init__(self, dataset = {}) :
        self.util = TrainingSet_util(dataset)
        self.training_log_file = dataset['training', None)
        if self.training_log_file == None :
            return

    def generateTraingData(self) :
        for line in file(self.training_log_file) :
            terms = self.util._parse_training_log_file(line)
            Click, Impression, Display_url,\
                AdID, AdvertiserID, Depth, \
                Position, QueryID, KeywordID,\ = terms

            print AdID,
            if Click == 0 :

