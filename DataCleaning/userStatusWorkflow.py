import __init__
from dataUtil import *
from genTitleDesc import genTitleDesc

def getPreSet(input_file, refreshFile=False) :
    adSet = []
    for line in file(TMP_DATA_DIR_PATH + 'topAdClickCnt.dict') :
        cnt, adid = line.strip().split()
        adSet.append(adid)
    adSet = set(adSet)
    if refreshFile :
        ad2Users = generateAd2UsersGivenAdSet(input_file, adSet)
        dumpDict2File(ad2Users, TMP_DATA_DIR_PATH + 'ad2UsersGivenAdSet.dict')
    ad2Users = {}
    userSet = set()
    for line in file(TMP_DATA_DIR_PATH + 'ad2UsersGivenAdSet.dict') :
        adid, rest = line.strip().split('\x01')
        if adid not in adSet : continue
        ad2Users[adid] = set(rest.split())
        for user in ad2Users[adid] :
            userSet.add(user)

    return adSet, userSet

def joinStatus(input_file, adSet, userSet) :
    dumpAd2UserStatus(input_file, adSet, userSet, TMP_DATA_DIR_PATH + 'ad2userStatus.dict') 

    joinRes = dict((ad, {}) for ad in adSet)
    for line in file(TMP_DATA_DIR_PATH + 'ad2userStatus.dict') :
        fields = line.strip().split()
        adid = fields[0]
        if fields[1] not in joinRes[adid] :
            joinRes[adid][fields[1]] = [0,0]
        joinRes[adid][fields[1]][0] += int(fields[2])
        joinRes[adid][fields[1]][1] += int(fields[3])

    writers = dict((ad, file(TMP_DATA_DIR_PATH + 'status/%s.ad2userStatus.dat' % ad, 'w')) for ad in adSet)
    for adid in joinRes :
        for key in joinRes[adid] :
            writers[adid].write('%s\t%s\t%d\t%d\n' % (adid, key, joinRes[adid][key][0], joinRes[adid][key][1]))
    
    for adid in writers :
        writers[adid].close()

if __name__ == '__main__' :
    input_file = DATA_TRAINING
    adSet, userSet = getPreSet(input_file, refreshFile=True)
    joinStatus(input_file, adSet, userSet)
    #adSet = set(list(adSet)[15:])
    #genTitleDesc(input_file, adSet, userSet, fn_out='user_title_desc.dat')

