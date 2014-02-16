import __init__
from util import logging, TMP_DATA_DIR_PATH, DATA_TRAINING, DATA_DESCRIPTION, DATA_QUERY, DATA_TITLE, DATA_PROFILE, DATA_TRAINING_SAMPLE
from dataParser import dataParser
import heapq

def generateTopAdsUsersByClick(data_training, top = 200) :
    AdClickCnt = dict()
    for line in file(data_training) :
        fields = dataParser.parseTrainData(line)
        if fields == None or len(fields) == 0 : return
        Click, Impression, Display_url, AdID, AdvertiserID, Depth, \
        Position, QueryID, KeywordID, TitleID, DescriptionID, UserID = fields
        if AdID not in AdClickCnt :
            AdClickCnt[AdID] = 0
        AdClickCnt[AdID] += Click

    adClickCntList = [(clickCnt, adid) for adid, clickCnt in AdClickCnt.items()]
    return heapq.nlargest(top, adClickCntList)

def generateAd2UsersGivenAdSet(data_training, adSet) :
    ad2Users = dict([(adid, set())for adid in adSet])
    for line in file(data_training) :
        fields = dataParser.parseTrainData(line)
        if fields == None or len(fields) == 0 : return
        Click, Impression, Display_url, AdID, AdvertiserID, Depth, \
        Position, QueryID, KeywordID, TitleID, DescriptionID, UserID = fields
        if UserID == '0' or AdID not in adSet : continue
        ad2Users[AdID].add(UserID)
    return ad2Users

def dumpUserRawFeatureGivenUserSet(data_training, userSet, fn) :
    userDict = dict([(userid, {'queryIDlist' : [], 'titleIDlist' : [], 'descIDList': []}) for userid in userSet])
    queryIDset = set()
    titleIDset = set()
    descIDset = set()

    for line in file(data_training) :
        fields = dataParser.parseTrainData(line)
        if fields == None or len(fields) == 0 : return
        Click, Impression, Display_url, AdID, AdvertiserID, Depth, \
        Position, QueryID, KeywordID, TitleID, DescriptionID, UserID = fields

        if UserID == '0' or UserID not in userSet : continue
       
        queryIDset.add(QueryID)
        titleIDset.add(TitleID)
        descIDset.add(DescriptionID)

        userDict[UserID]['queryIDlist'].append(QueryID)
        #only track clicked ads' infomation
        if Click > 0 :
            userDict[UserID]['titleIDlist'].append(TitleID)
            userDict[UserID]['descIDList'].append(DescriptionID)

    #dump aggregation result to file
    dump_format = '%s\x01%s\x02%s\x02%s\n'
    aggregateUserResult = file(fn, 'w')
    for user in userDict :
        aggregateUserResult.write(dump_format % \
                (user,
                    '\t'.join(userDict[user]['queryIDlist']),
                    '\t'.join(userDict[user]['titleIDlist']),
                    '\t'.join(userDict[user]['descIDList'])))
    aggregateUserResult.close()

    #dump all ID set to files which would be used to filter additional data.
    dumpFilesName = {TMP_DATA_DIR_PATH + 'queryID.set' : queryIDset, TMP_DATA_DIR_PATH + 'titleID.set' : titleIDset, TMP_DATA_DIR_PATH + 'descID.set' : descIDset}
    for filename, s in dumpFilesName.items() :
        dumpfile = file(filename, 'w')
        for item in s :
            dumpfile.write('%s\n' % (item))
        dumpfile.close()

def dumpList2File(listObj, fn) :
    output = file(fn, 'w')
    for item in listObj :
        if hasattr(item, '__iter__') :
            output.write('\t'.join([str(subitem) for subitem in item]) + '\n')
        else :
            output.write(item + '\n')
    output.close()

def dumpDict2File(dictObj, fn) :
    output = file(fn, 'w')
    format = '%s\x01%s\n'
    for key in dictObj :
        value = dictObj[key]
        if hasattr(value, '__iter__') :
            output.write(format % (key, '\t'.join([str(subitem) for subitem in value])))
        else :
            output.write(format % (key, value))
    output.close()

if __name__ == '__main__' :

    input_file = DATA_TRAINING_SAMPLE

    adClickCntList = generateTopAdsUsersByClick(input_file)
    dumpList2File(adClickCntList, TMP_DATA_DIR_PATH + 'topAdClickCnt.dict')
    
    adSet = set()
    for line in file(TMP_DATA_DIR_PATH + 'topAdClickCnt.dict') :
        cnt, adid = line.strip().split()
        adSet.add(adid)

    ad2Users = generateAd2UsersGivenAdSet(input_file, adSet)
    dumpDict2File(ad2Users, TMP_DATA_DIR_PATH + 'ad2UsersGivenAdSet.dict')

    userSet = set()
    for line in file(TMP_DATA_DIR_PATH + 'ad2UsersGivenAdSet.dict') :
        adid, users = line.strip().split('\x01')
        for user in users.split('\t') :
            userSet.add(user)
    
    dumpUserRawFeatureGivenUserSet(input_file, userSet, TMP_DATA_DIR_PATH + 'userRawFeature.dict')


