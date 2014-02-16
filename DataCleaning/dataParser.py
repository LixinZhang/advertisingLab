import __init__
import sys
sys.path.append('../')
from util import logging

class dataParser :

    @staticmethod
    def parseTrainData(line) :
        fields = line.strip().split('\t')
        if len(fields) != 12 : return None
        Click, Impression, Display_url, AdID, AdvertiserID, Depth, \
                Position, QueryID, KeywordID, TitleID, DescriptionID, UserID = fields
        return  int(Click), int(Impression), Display_url,\
                AdID, AdvertiserID, int(Depth), \
                int(Position), QueryID, KeywordID,\
                TitleID, DescriptionID, UserID

if __name__ == '__main__' :
    example_row = '0\t1\t4298118681424644510\t7686695\t385\t3\t3\t1601\t5521\t7709\t576\t490234'
    logging.debug(dataParser.parseTrainData(example_row))