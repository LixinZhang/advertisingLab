import sys
import __init__
from util import logging, TMP_DATA_DIR_PATH, DATA_TRAINING, DATA_DESCRIPTION, DATA_QUERY, DATA_TITLE, DATA_PROFILE, DATA_TRAINING_SAMPLE

def genTitleDesc(inputFile, adSet, userset=None, fn_out='user_title_desc.dat') :
    logging.info('Generating Click and Unclick Title Description For Per User')

    ad2Profile = {}
    titleSet = set()
    descSet = set()

    for line in file(inputFile) :
        fields = line.strip().split()
        adid = fields[3]
        userid = fields[-1]
        if userid == '0' or adid not in adSet : continue
        if userid not in userset : continue
        if adid not in ad2Profile :
            ad2Profile[adid] = {'profile':{}, 'nonClick_profile':{}, 'click_profile':{}}
        profile = ad2Profile[adid]['profile']
        nonClick_profile = ad2Profile[adid]['nonClick_profile']
        click_profile = ad2Profile[adid]['click_profile']
        title = fields[-3]
        desc = fields[-2]
        titleSet.add(title)
        descSet.add(desc)
        if userid not in profile :
            profile[userid] = {'desc':set(), 'title':set()}
            nonClick_profile[userid] = {'desc':set(), 'title':set()}
            click_profile[userid] = {'desc':set(), 'title':set()}

        if title not in profile[userid]['title']:
            profile[userid]['title'].add(title)
            if int(fields[0]) > 0 : 
                click_profile[userid]['title'].add(title)
            else :
                nonClick_profile[userid]['title'].add(title)

        if desc not in profile[userid]['desc'] :
            profile[userid]['desc'].add(desc)
            if int(fields[0]) > 0 : 
                click_profile[userid]['desc'].add(desc)
            else :
                nonClick_profile[userid]['desc'].add(desc)

    fn_DESC = DATA_DESCRIPTION
    fn_TITLE = DATA_TITLE

    expandDesc = dict()
    expandTitle = dict()

    for line in file(fn_DESC) :
        tid, rest = line.strip().split()
        if tid not in descSet : continue
        expandDesc[tid] = rest

    for line in file(fn_TITLE) :
        tid, rest = line.strip().split()
        if tid not in titleSet : continue
        expandTitle[tid] = rest

    writers = dict((ad, file(TMP_DATA_DIR_PATH + 'user_title_desc/%s.user_title_desc.dat' % ad, 'w')) for ad in adSet)

    for adid in ad2Profile :
        profile = ad2Profile[adid]['profile']
        nonClick_profile = ad2Profile[adid]['nonClick_profile']
        click_profile = ad2Profile[adid]['click_profile']
        for userid in profile :
            click_title = '|'.join(expandTitle[key] for key in click_profile[userid]['title'])
            title = '|'.join(expandTitle[key] for key in profile[userid]['title'])
            nonclick_title = '|'.join(expandTitle[key] for key in nonClick_profile[userid]['title'])
            
            click_desc = '|'.join(expandDesc[key] for key in click_profile[userid]['desc'])
            desc = '|'.join(expandDesc[key] for key in profile[userid]['desc'])
            nonclick_desc = '|'.join(expandDesc[key] for key in nonClick_profile[userid]['desc'])
            writers[adid].write('\x01'.join([adid, userid, title, click_title, nonclick_title, desc, click_desc, nonclick_desc]))
            writers[adid].write('\n')

    for ad in writers:
        writers[ad].close()

if __name__ == '__main__' :
    pass
