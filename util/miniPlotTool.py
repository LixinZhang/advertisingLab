# -*- coding: utf-8 -*-
import pylab
import random
import sys
import numpy

class MiniPlotTool :
    '''
    A mini tool to draw lines using pylab
    '''
    basecolors = ['red','green','blue','black','cyan','magenta']

    def __init__(self, baseConfig) :
        self.figsize = baseConfig.get('figsize',None)
        self.axis = baseConfig.get('axis',None)
        self.title = unicode(baseConfig.get('title','NoName'), 'utf-8')
        self.ylabel = unicode(baseConfig.get('ylabel','NoName'), 'utf-8')
        self.grid = baseConfig.get('grid',False)
        self.xaxis_locator = baseConfig.get('xaxis_locator',None)
        self.yaxis_locator = baseConfig.get('yaxis_locator',None)
        self.legend_loc = baseConfig.get('legend_loc',0)

        if 'xticks' in baseConfig :
            xticks_conf = baseConfig.get('xticks')
            _rotation = int(xticks_conf.get('ticks_rotation', 0))
            x_idx = xticks_conf.get('x_idx',[])
            x_lable = xticks_conf.get('x_lable', [])
            if len(x_idx) > 0 and len(x_idx) == len(x_lable) :
                pylab.xticks(x_idx, x_lable, rotation=_rotation)
        
        if self.figsize != None :
            pylab.figure(figsize = self.figsize)
        if self.axis != None :
            pylab.axis(self.axis)
        
        pylab.title(self.title)
        pylab.ylabel(self.ylabel)
        ax = pylab.gca()
        pylab.grid(self.grid)
        if self.xaxis_locator != None :
            ax.xaxis.set_major_locator( pylab.MultipleLocator(self.xaxis_locator) )
        if self.yaxis_locator != None :
            ax.yaxis.set_major_locator( pylab.MultipleLocator(self.yaxis_locator) )
        self.lineList = []
        self.id = 1

    def addline(self, lineConf) :
        lineConf['color'] =  lineConf.get('color', MiniPlotTool.basecolors[self.id % len(MiniPlotTool.basecolors)])

        self.lineList.append((self.id, lineConf))
        self.id += 1
        return {'id' : self.id - 1}

    def removeline(self, lineId) :
        for i in range(len(self.lineList)) :
            id, conf = self.lineList[i]
            if id == lineId :
                del self.lineList[i]
                break
        else :
            return {'status' : -1}
        print len(self.lineList)
        return {'status' : 0}

    def __parselineConf(self, lineConf) :
        X = lineConf['X']
        Y = lineConf['Y']
        marker = lineConf.get('marker',None)
        #color = lineConf.get('color', random.choice(MiniPlotTool.basecolors))
        color = lineConf.get('color', MiniPlotTool.basecolors[self.id % len(MiniPlotTool.basecolors)])
        markerfacecolor = lineConf.get('markerfacecolor',color)
        label = lineConf.get('label','NoName')
        linewidth = lineConf.get('linewidth',1)
        linestyle = lineConf.get('linestyle','-')
        return X, Y, marker, color, markerfacecolor, label, linewidth, linestyle

    def plotSingleLine(self, lineConf):
        X, Y, marker, color, markerfacecolor, label, linewidth, linestyle = self.__parselineConf(lineConf)
        pylab.plot(X, Y, marker = marker, color = color, markerfacecolor = markerfacecolor, label=label, linewidth = linewidth, linestyle = linestyle)
        pylab.legend(loc = self.legend_loc)

    def plot(self) :
        colors = [MiniPlotTool.basecolors[i % len(MiniPlotTool.basecolors)] for i in range(len(self.lineList))]
        for i in range(len(self.lineList)) :
            id, conf = self.lineList[i]
            if conf.get('color',None) :
                conf['color'] = colors[i]
            X, Y, marker, color, markerfacecolor, label, linewidth, linestyle = self.__parselineConf(conf)
            pylab.plot(X, Y, marker = marker, color = color, markerfacecolor = markerfacecolor, label=label, linewidth = linewidth, linestyle = linestyle)
        pylab.legend(loc = self.legend_loc)

    def show(self) :
        #pylab.savefig('test.png')
        pylab.show()

    def save(self, fn) :
        pylab.savefig(fn)

        
if __name__ == '__main__' :
    #test
    X = [ i for i in range(10)]
    Y = [random.randint(1,10) for i in range(10)]
    Y2 = [random.randint(1,10) for i in range(10)]

    baseConfig = {
        #'figsize' : (6,8),
        #'axis': [0,line_Num,0,10 * m],
        'title' : 'MiniPlotTool 画图小工具',
        'ylabel' : 'Y value',
        'grid' : True,
        #'xaxis_locator' : 0.5,
        #'yaxis_locator' : 1,
        #'legend_loc' : 'upper right',
        'xticks' : {'ticks_rotation':10, 'x_idx':[0,1,2,3,4,5,6,7,8,9], 'x_lable':['zero','one','two','three','four','five','six','seven','eight','nine']}
    }
    tool = MiniPlotTool(baseConfig)

    lineConf = {
        'X' : X,
        'Y' : Y,
        'marker' : 'x',
        #'color' : 'b',
        #'markerfacecolor' : 'r',
        'label' : 'label1',
        'linewidth' : 2,
        #'linestyle' : '--'
    }
    lineConf2 = {
        'X' : X,
        'Y' : Y2,
        'marker' : 'o',
        'color' : 'b',
        'markerfacecolor' : 'b',
        'label' : 'lable2',
        'linewidth' : 2,
        'linestyle' : '--'
    }
    #tool.plotSingleLine(lineConf)
    print tool.addline(lineConf)
    print tool.addline(lineConf2)

    #print tool.removeline(1)
    tool.plot()
    tool.show()
    #tool.save('test.png')




