from trainSet_util import TrainingSet_util

titleid_tokensid = ''
dataset = {}
dataset['training'] = 'user.filter'


class object_model :

    def __init__(self) :
       self.trainsetUtil = TrainingSet_util() 

    def prepareData(self) :
        for line in open(filename) :
            fields = line.strip().split('\t')

    def splitFilesByHashUser(self, hashbase = 1) :
        hashfiles = [file(str(hashval) + '.dat', 'w') for hashval in range(hashbase)]
        line_cnt = 0
        for line in file('user.filter') :
            line_cnt += 1
            terms = self.trainsetUtil._parse_training_log_file(line) 
            if terms == None : continue
            Click, Impression, Display_url,\
                AdID, AdvertiserID, Depth, \
                Position, QueryID, KeywordID,\
                TitleID, DescriptionID, UserID = terms
            if UserID == '0' : continue

            hashfiles[int(UserID) % hashbase].write(line)

        for hashfile in hashfiles : hashfile.close()


if __name__ == '__main__' :
    handler = object_model()
    handler.splitFilesByHashUser()



        
