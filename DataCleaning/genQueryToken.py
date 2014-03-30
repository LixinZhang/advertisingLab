from dataUtil import *
from dataParser import dataParser
import sys
from userStatusWorkflow import getPreSet

def genQueryToken (ADID) :
    preFilterUserSet = set(line.split()[1] for line in file(TMP_DATA_DIR_PATH + 'status/%s.ad2userStatus.dat' % ADID ))
    user_query = {}
    num = 1
    for line in file(input_file) :
        if num % 100000 == 0 : print ADID, num
        num += 1
        fields = dataParser.parseTrainData(line)
        Click, Impression, Display_url, AdID, AdvertiserID, Depth, Position, QueryID, KeywordID, TitleID, DescriptionID, UserID = fields
        if UserID not in preFilterUserSet : continue
        if UserID not in user_query :
            user_query[UserID] = []
        user_query[UserID].append(QueryID)

    writer = file(TMP_DATA_DIR_PATH + 'userQuery/%s.user.query' % ADID, 'w')
    for user in user_query :
        writer.write('%s%s\n' % (user, '\t'.join(user_query[user])))
    writer.close() 

    writer = file(TMP_DATA_DIR_PATH + 'userQuery/%s.user.queryTokens' % ADID, 'w')
    querySet = set()

    for line in file(TMP_DATA_DIR_PATH + 'userQuery/%s.user.query' % ADID) :
        for q in line.strip().split('')[1].split() :
            querySet.add(q)

    queryMap = dict(line.strip().split() for line in file(DATA_QUERY) if line.strip().split()[0] in querySet)

    for line in file(TMP_DATA_DIR_PATH + 'userQuery/%s.user.query' % ADID) :
        user, query = line.strip().split('')
        query = query.split()
        writer.write('%s%s\n' % (user, '|'.join(queryMap[q] for q in query)))
    
    userQuery = None
    querySet = None
    queryMap = None

if __name__ == '__main__' :
    input_file = DATA_TRAINING
    adset, userset = getPreSet(input_file)
    for adid in adset :
        genQueryToken(adid)
    
