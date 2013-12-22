#!/usr/bin/python
import math
import sys

class IBCF :
    def __init__(self) :
        self.itemMat = {}
        self.similarityMat = {}
        self.similarityTop = {}
        self.below = {}
        self.user2item = {}

    def ItemSimilarity(self, item1, item2, item_id1,item_id2) :
        upon = 0.0
        for u_id in item1 :
            if u_id in item2 :
                upon += item1[u_id] * item2[u_id]
        below1 = self.below[item_id1]
        below2 = self.below[item_id2]
        if upon == 0.0 or below1 == 0.0 or below2 == 0.0 : return 0.0
        return upon * 1.0 / (below1 * below2)
    
    def prepareFromFile(self, trainfile) :
        datafile = file(trainfile, 'r')
        for line in datafile :
            item_id, user_id_list_str = line.split('\x01')
            user_id_list = user_id_list_str.split('\x02')
            for user_id in user_id_list :
                if item_id not in self.itemMat :
                    self.itemMat[item_id] = {}
                    self.similarityMat[item_id] = {}
                if user_id not in self.itemMat[item_id] :
                    self.itemMat[item_id][user_id] = 1.0
                
        for item_id in self.itemMat :
            tmp = 0.0
            for u_id in self.itemMat[item_id] :
                tmp += self.itemMat[item_id][u_id] ** 2
            self.below[item_id] = math.sqrt(tmp)

    def generateSimilarityMat(self) :
        item_ids = self.itemMat.keys()
        print 'len : ', len(item_ids)
        idx = 1
        for id1 in range(len(item_ids)) :
            print idx
            idx += 1
            for id2 in range(id1, len(item_ids)) :
                item_id1 = item_ids[id1]
                item_id2 = item_ids[id2]
                sim = self.ItemSimilarity(self.itemMat[item_id1], self.itemMat[item_id2], item_id1, item_id2)
                self.similarityMat[item_id1][item_id2] = sim
                self.similarityMat[item_id2][item_id1] = sim
        self.__generateTopSimilarity()

    def dumpRes2File(self, dumpFile, Top = 10) :
        dumpF = file(dumpFile, 'w')
        line_format = '%s\x01%s\x01%d\x01%f\x01\n'
        for item_id1 in self.itemMat :
            arr = [ (self.similarityMat[item_id1][item_id2], item_id2) for item_id2 in self.similarityMat[item_id1] ]
            arr.sort(reverse = True)
            idx = 1
            for t in range(min(Top, len(arr))) :
                dumpF.write(line_format % (item_id1, arr[t][1], idx,  arr[t][0]))
                idx += 1 
        dumpF.close()

    def __generateTopSimilarity(self, Top = 10) :
        for item_id1 in self.itemMat :
            arr = [ (self.similarityMat[item_id1][item_id2], item_id2) for item_id2 in self.similarityMat[item_id1] ]
            arr.sort(reverse = True)
            self.similarityTop[item_id1] = set()
            top = Top
            for rating, item_id in arr :
                top -= 1
                self.similarityTop[item_id1].add(item_id)
                if top == 0 : break

    def pred(self, user_id, item_id, isTop = True) :
        item_ids = self.user2item[user_id]
        upon = 0.0
        below = 0.0
        for item_id_cmp in item_ids :
            if isTop and (item_id_cmp not in self.similarityTop[item_id]) :
                continue
            print self.similarityMat[item_id][item_id_cmp], self.itemMat[item_id_cmp][user_id]
            upon += self.similarityMat[item_id][item_id_cmp] * self.itemMat[item_id_cmp][user_id]
            below += self.similarityMat[item_id][item_id_cmp]
        if upon == 0.0 : return 0.0
        return upon * 1.0 /  below
    
if __name__ == '__main__' :
    if len(sys.argv) != 3 :
        print 'python IBCF.py trainfile outputfile'
        exit(0)
    trainfile = sys.argv[1]
    outputfile = sys.argv[2]
    ib = IBCF()
    ib.prepareFromFile(trainfile)
    ib.generateSimilarityMat()
    ib.dumpRes2File(outputfile)
