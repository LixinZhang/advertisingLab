import __init__
import numpy
from util import logging, TMP_DATA_DIR_PATH
from util.common import dumpDict2File

def loadIdx2AdIdCache(fn_adId2Idx) :
    idx2adId = dict()
    for line in file(fn_adId2Idx) :
        adid, idx = line.strip().split('\x01')
        idx2adId[idx] = adid
    return idx2adId

def loadAd2userClickImpsCache(fn_ad2userStatus) :
    adUser2ClickImps = dict()
    for line in file(fn_ad2userStatus) :
        adid, userid, click, impression = line.strip().split()
        adUser2ClickImps[(adid, userid)] = (int(click), int(impression))
    return adUser2ClickImps

def ctrDistribution(fn_SVMRanking, fn_rankingResult, fn_userID4SVMRanking, fn_adId2Idx, fn_ad2userStatus, fn_out_ad2UserCTR) :
    idx2adId = loadIdx2AdIdCache(fn_adId2Idx)
    adUser2ClickImps = loadAd2userClickImpsCache(fn_ad2userStatus)

    ad2SortedUsers = dict()
    userIDList = file(fn_userID4SVMRanking)
    rankingResult = file(fn_rankingResult)
    linenum = 1
    for line in file(fn_SVMRanking) :
        rr = rankingResult.readline()
        raw_score, qid, rest = line.split(' ',2)
        adid = idx2adId[qid.split(':')[1]]
        userid = userIDList.readline().strip()
        if adid not in ad2SortedUsers :
            ad2SortedUsers[adid] = []
        #print fn_SVMRanking, rr, linenum
        linenum += 1
        prediction_score = float(rr)
        click, imps = adUser2ClickImps[(adid, userid)]
        ad2SortedUsers[adid].append((prediction_score, click, imps))

    mean_click = {}
    mean_impression = {}
    ad2userCTR = {}

    for adid in ad2SortedUsers :
        ad2SortedUsers[adid].sort(reverse=True)
        mean_click[adid] = numpy.mean([item[1] for item in ad2SortedUsers[adid]])
        mean_impression[adid] = numpy.mean([item[2] for item in ad2SortedUsers[adid]])
        ad2userCTR[adid] = []
     
    for adid in ad2SortedUsers :
        print mean_click[adid], mean_impression[adid]
        for raw_score, click, imps in ad2SortedUsers[adid] :
            ctr = (click + mean_click[adid]) * 1.0 / (imps + mean_impression[adid])
            #ctr = (click + 0.0657842032795) * 1.0 / (imps + 1.62795719114)
            #print mean_click[adid] * 1.0 / mean_impression[adid]
            #ctr = click * 1.0 / imps
            #print ctr
            ad2userCTR[adid].append(ctr)
        
    dumpDict2File(ad2userCTR, fn_out_ad2UserCTR)

if __name__ == '__main__' :
    pass
