'''
Training Data
Each line consists of fields delimited by the TAB character
* Click : the number of times, among the above impressions, the user (UserID) clicked the ad (AdID)
* Impression : the number of search sessions in which the ad (AdID) was impressed by the user (UserID) who issued the query (Query).
* Display URL :a property of the ad
    
    The URL is shown together with the title and description of an ad. It is usually the shortened landing page URL of the ad, but not always. In the data file,  this URL is hashed for anonymity. 
* AdID :
* AdvertiserID : a property of the ad
* Depth : The number of ads impressed in a session is known as the 'depth'
* Position : The order of an ad in the impression list is known as the 'position' of that ad.
* QueryID : id of the queryid_tokensid. It is the key of the data file 'queryid_tokensid.txt'
* KeywordID : a property of ads 

	This is the key of  'purchasedkeyword_tokensid.txt'. 
* TitleID : a property of ads
	
	This is the key of 'titleid_tokensid.txt'. 
* DescriptionID : a property of ads. 

	This is the key of 'descriptionid_tokensid.txt'.
* UserID : 
 
 	This is the key of 'userid_profile.txt'.  When we cannot identify the user, this field has a special value of 0. 
'''

import sys

_dataset = {}
_dataset['training'] = '../dataset/training.txt'


class TrainingSet_util :
    def __init__ (self, dataset = _dataset) :
        self.training_log_file = dataset.get('training', None)
        if self.training_log_file == None :
            return
        self.acookie_set = set()
        self.ad_set = set()
        self.ad2user_map = {}
        self.advertiser_map = {}

    def _parse_training_log_file (self, line) :
        terms = line.strip().split('\t')
        if len(terms) != 12 : return None
        Click, Impression, Display_url,\
                AdID, AdvertiserID, Depth, \
                Position, QueryID, KeywordID,\
                TitleID, DescriptionID, UserID = terms
        return  int(Click), int(Impression), Display_url,\
                AdID, AdvertiserID, int(Depth), \
                int(Position), QueryID, KeywordID,\
                TitleID, DescriptionID, UserID


    def splitFilesByHashUser(self, hashbase = 1) :
       hashfiles = [file(str(hashval) + '.dat', 'w') for hashval in range(hashbase)]
       line_cnt = 0
       for line in file('user.filter') :
           line_cnt += 1
           terms = self._parse_training_log_file(line) 
           if terms == None : continue
           Click, Impression, Display_url,\
               AdID, AdvertiserID, Depth, \
               Position, QueryID, KeywordID,\
               TitleID, DescriptionID, UserID = terms
           if UserID == '0' : continue

           hashfiles[int(UserID) % hashbase].write(line)

       for hashfile in hashfiles : hashfile.close()

    def aggregateUser(self, userfilter = 'user.filter', aggregateUserResultFile = 'user.aggr') :
        userDict = dict()
        queryIDset = set()
        titleIDset = set()
        descIDset = set()

        for line in file(userfilter) :
            terms = self._parse_training_log_file(line) 
            if terms == None : continue
            Click, Impression, Display_url,\
                AdID, AdvertiserID, Depth, \
                Position, QueryID, KeywordID,\
                TitleID, DescriptionID, UserID = terms
            if UserID not in userDict :
                userDict[UserID] = {'queryIDlist' : [], 'titleIDlist' : [], 'descIDList': []}
           
            queryIDset.add(QueryID)
            titleIDset.add(TitleID)
            descIDset.add(DescriptionID)

            userDict[UserID]['queryIDlist'].append(QueryID)
            #only track clicked ads' infomation
            if Click > 0 :
                userDict[UserID]['titleIDlist'].append(TitleID)
                userDict[UserID]['descIDList'].append(DescriptionID)

        #dump aggregation result to file
        dump_format = '%s%s%s%s\n'
        aggregateUserResult = file(aggregateUserResultFile, 'w')
        for user in userDict :
            #if len(userDict[user]['queryIDlist']) < 3 : continue
            aggregateUserResult.write(dump_format % \
                    (user,
                        ','.join(userDict[user]['queryIDlist']),
                        ','.join(userDict[user]['titleIDlist']),
                        ','.join(userDict[user]['descIDList'])))
        aggregateUserResult.close()

        #dump all ID set to files which would be used to filter additional data.
        dumpFilesName = {'queryID.set' : queryIDset, 'titleID.set' : titleIDset, 'descID.set' : descIDset}
        for filename, s in dumpFilesName.items() :
            dumpfile = file(filename, 'w')
            for item in s :
                dumpfile.write('%s\n' % (item))
            dumpfile.close()


    def expandId2Tokens(self, aggregateUserfile = 'user.aggr', expandId2TokensResultFile = 'user.expand2Tokens', isFiltered = True) :
        if isFiltered :
            filterstr = '.filter'
        else :
            filterstr = ''
        description_map = dict([(line.strip().split('\t')) for line in file(dataset['description'] + filterstr)])
        query_map = dict([(line.strip().split('\t')) for line in file(dataset['query'] + filterstr)])
        title_map = dict([(line.strip().split('\t')) for line in file(dataset['title'] + filterstr)])
        profile_map = dict([(line.strip().split('\t', 1)) for line in file(dataset['profile'] + filterstr)])

        dump_format = '%s%s%s%s%s\n'
        expandId2TokensResult = file(expandId2TokensResultFile, 'w') 
        for line in file(aggregateUserfile) :
            userID, queryIDlist, titleIDlist, descIDList = line.strip().split('')
            queryExpandTokensStr = '|'.join([query_map[queryId] for queryId in queryIDlist.split(',') if queryId != ''])
            titleExpandTokensStr = '|'.join([title_map[titleId] for titleId in titleIDlist.split(',') if titleId != ''])
            descExpandTokensStr = '|'.join([description_map[descId] for descId in descIDList.split(',') if descId != ''])
            profileExpandTokensStr = '|'.join(profile_map.get(userID, "'0'\t'0'").split('\t'))
            expandId2TokensResult.write( dump_format % \
                   (userID, profileExpandTokensStr, queryExpandTokensStr, titleExpandTokensStr, descExpandTokensStr))

        expandId2TokensResult.close()

    def filterUsers(self, usersetFile = '', filterResultFile = '') :
        userset = set()
        for line in file(usersetFile) :
            userset.add(line.strip())

        filterResult = file(filterResultFile, 'w')

        line_cnt = 0
        for line in file(self.training_log_file) :
            line_cnt += 1
            terms = self._parse_training_log_file(line) 
            if terms == None : continue
            Click, Impression, Display_url,\
                AdID, AdvertiserID, Depth, \
                Position, QueryID, KeywordID,\
                TitleID, DescriptionID, UserID = terms
            if UserID in userset :
                filterResult.write(line)
            if line_cnt % 100000 == 0 :
                print line_cnt

    def filterAdditionalData(self, usersetFile = 'user.dat', querysetFile = 'queryID.set', titlesetFile = 'titleID.set', descsetFile = 'descID.set') :
        userset = set()
        queryIDset = set()
        titleIDset = set()
        descIDset = set()

        for line in file(usersetFile) :
            userset.add(line.strip())
        for line in file(querysetFile) :
            queryIDset.add(line.strip())
        for line in file(titlesetFile) :
            titleIDset.add(line.strip())
        for line in file(descsetFile) :
            descIDset.add(line.strip())
        
        filter_data = [('description', descIDset), ('query', queryIDset), ('title', titleIDset), ('profile',userset)]
        for dataname, checkset in filter_data :
            filter_result = file(dataset[dataname] + '.filter', 'w')
            for line in file(dataset[dataname]) :
                if line.strip().split('\t')[0] in checkset :
                    filter_result.write(line)
            filter_result.close()

    def prepare(self) :
        self.click_cnt = 0
        self.impression_cnt = 0
        line_cnt = 0
        for line in file(self.training_log_file) :
            line_cnt += 1
            terms = self._parse_training_log_file(line) 
            if terms == None : continue
            Click, Impression, Display_url,\
                AdID, AdvertiserID, Depth, \
                Position, QueryID, KeywordID,\
                TitleID, DescriptionID, UserID = terms
            if Click > 0 :
                self.click_cnt += Click
            if Impression > 0 :
                self.impression_cnt += Impression
            
            
            self.acookie_set.add(UserID)
            self.ad_set.add(AdID)
            if AdvertiserID not in self.advertiser_map:
                self.advertiser_map[AdvertiserID] = set()
            self.advertiser_map[AdvertiserID].add(AdID)
            
            if AdID not in self.ad2user_map :
                self.ad2user_map[AdID] = set()
            self.ad2user_map[AdID].add(UserID)
            
            if line_cnt % 100000 == 0 : print line_cnt
        
    def printStatus(self) :
        output_format = '%s25%s'
        print 'Total Impression :', self.impression_cnt
        print 'Total Average CTR :', self.click_cnt * 1.0 / self.impression_cnt
        print 'Total User Cnt :', len(self.acookie_set)
        print 'Total Ad Cnt :', len(self.ad_set)

        ad2user_tmpfile = file('ad2user_tmpfile', 'w')
        ad2user_outputformat = '%s%s\n'
        for ad in self.ad2user_map :
            if len(self.ad2user_map[ad]) < 1 : continue
            ad2user_tmpfile.write(ad2user_outputformat % (ad, ''.join(self.ad2user_map[ad])))
        ad2user_tmpfile.close()

        acookie_file = file('user.dat', 'w')
        ad_file = file('adID.dat', 'w')
        advertiser_file = file('advertiser2ad.dat', 'w')

        for acookie in self.acookie_set :
            acookie_file.write(acookie + '\n')

        for ad_id in self.ad_set :
            ad_file.write(ad_id + '\n')

        for adver in self.advertiser_map :
            advertiser_file.write(adver + '\t'.join(self.advertiser_map[adver]) + '\n')




if __name__ == '__main__' :
    dataset = {}
    dataset['training'] = '../dataset/training.txt'
    dataset['description'] = '../dataset/descriptionid_tokensid.txt'
    dataset['query'] = '../dataset/queryid_tokensid.txt'
    dataset['title'] = '../dataset/titleid_tokensid.txt'
    dataset['profile'] = '../dataset/userid_profile.txt'

    #dataset['training'] = sys.argv[1]
#    dataset['training'] = '../dataset/training.txt'
    ts_util = TrainingSet_util(dataset)
#    ts_util.prepare()
#    ts_util.printStatus()
#    ts_util.aggregateUser()
#    ts_util.filterAdditionalData('user.dat')
    ts_util.expandId2Tokens()
