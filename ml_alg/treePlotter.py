#coding:utf-8
import matplotlib.pyplot as plt


decisionNode=dict(boxstyle="sawtooth",fc="0.8")
leafNode=dict(boxstyle="round4",fc="0.8")
arrow_args=dict(arrowstyle="<-")

def plotNode(nodeTxt,centerPt,parentPt,nodeType):
    #xy要注释的点，xytext另外的一个点，xycoords是点的类型，默认也可。va和ha代表文本框的格式，这里选择居中
    createPlot.ax1.annotate(nodeTxt,xy=parentPt,xycoords='axes fraction',\
                            xytext=centerPt,textcoords='axes fraction',\
                            va="center",ha="center",bbox=nodeType,arrowprops=arrow_args)

def createPlot():
    #第一个参数1代表num,第二个参数代表整个背景的颜色，默认是灰色
    fig=plt.figure(1,facecolor="white")
    #清除当前的图形
    fig.clf()
    # ax1 是函数 createPlot 的一个属性，这个可以在函数里面定义也可以在函数定义后加入也可以
    createPlot.ax1=fig.add_subplot(111,frameon=False)
    plotNode('a decision node',(0.5,0.1),(0.1,0.5),decisionNode)
    plotNode('a leaf node',(0.8,0.1),(0.3,0.8),leafNode)
    plt.show()

def getNumLeafs(myTree):
    numleafs=0
    firstStr=myTree.keys()[0]
    secondDict=myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            numleafs+=getNumLeafs(secondDict[key])
        else:numleafs+=1
    return  numleafs

def getTreeDepth(myTree):
    maxDepth=0
    firstStr=myTree.keys()[0]
    secondDict=myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            thisDepth=1+getTreeDepth(secondDict[key])
        else:thisDepth=1
        if thisDepth>maxDepth:maxDepth=thisDepth
    return  maxDepth

def retrieveTree(i):
    listOfTrees=[{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},\
                 {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head':{0:'no', 1:\
                     'yes'}},1:'no'}}}}]
    return  listOfTrees[i]

def plotMidText(cntrPt,parentPt,txtString):
    xmid=(parentPt[0]-cntrPt[0])/2.0+cntrPt[0]
    ymid=(parentPt[1]-cntrPt[1])/2.0+cntrPt[1]
    createPlot.ax1.text(xmid,ymid,txtString)

def plotTree(myTree,parentPt,nodeTxt):
    numleafs=getNumLeafs(myTree)
    depth=getTreeDepth(myTree)
    firstStr=myTree.keys()[0]
    cntrPt=(plotTree.xoff+(1.0+float(numleafs))/2.0/plotTree.totalW,plotTree.yoff)
    #画箭头中间的文字部分
    plotMidText(cntrPt,parentPt,nodeTxt)
    #画箭头
    plotNode(firstStr,cntrPt,parentPt,decisionNode)
    print cntrPt,parentPt
    secondDict=myTree[firstStr]
    plotTree.yoff=plotTree.yoff-1.0/plotTree.totalD
    for key in secondDict.keys():
        print key
        if type(secondDict[key]).__name__=='dict':
            plotTree(secondDict[key],cntrPt,str(key))
        else:
            plotTree.xoff=plotTree.xoff+1.0/plotTree.totalW
            plotNode(secondDict[key],(plotTree.yoff,plotTree.yoff),cntrPt,leafNode)
            plotMidText((plotTree.xoff,plotTree.yoff),cntrPt,str(key))
    plotTree.yoff=plotTree.yoff+1.0/plotTree.totalD

def createPlot(inTree):
    fig=plt.figure(1,facecolor='white')
    fig.clf()
    axprops=dict(xticks=[],yticks=[])
    createPlot.ax1=plt.subplot(111,frameon=False,**axprops)
    plotTree.totalW=float(getNumLeafs(inTree))
    plotTree.totalD=float(getTreeDepth(inTree))
    plotTree.xoff=-0.5/plotTree.totalW;plotTree.yoff=1.0
    plotTree(inTree,(0.5,1.0),'')
    plt.show()