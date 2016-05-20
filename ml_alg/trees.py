#coding: UTF-8
from math import log

import operator

def calcShannnEnt(dataSet):
    numEntries=len(dataSet)
    labelCounts={}
    for featVec in dataSet:
        #根据label来分类别，-1代表取label，即最后一个。
        currentLabel=featVec[-1]
        labelCounts[currentLabel]=labelCounts.get(currentLabel,0)+1
    shannonEnt=0.0
    for key in labelCounts:
        prob=float(labelCounts[key])/numEntries
        shannonEnt-=prob*log(prob,2)
    return shannonEnt

def createDataSet():
    dataSet=[[1,1,'yes'],[1,1,'yes'],[1,0,'no'],[0,1,'no'],[0,1,'no']]
    lables=['no surfacing','flippers']
    return dataSet,lables
#把dataset中，axis属性为value的数据集取出，去掉此属性后返回。
def splitDataSet(dataSet,axis,value):
    retDataSet=[]
    for featVec in dataSet:
        if featVec[axis]==value:
            #单纯的讲数据中axis属性的值给剔除掉，剩下的重新拼接
            reducedFeatVec=featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

def chooseBestFeatureToSplit(dataSet):
    #特征数目
    numFeatures=len(dataSet[0])-1
    #基准熵
    baseEntropy=calcShannnEnt(dataSet)
    bestInfoGain=0.0;bestFeature=-1
    #对每个特征进行测试，找到最佳属性来进行分割
    for i in range(numFeatures):
        featList=[example[i] for example in dataSet]
        #元素去重
        uniqueVals=set(featList)
        newEntropy=0.0
        for value in uniqueVals:
            subDataSet=splitDataSet(dataSet,i,value)
            prob=len(subDataSet)/float(len(dataSet))
            newEntropy+=prob*calcShannnEnt(subDataSet)
        infoGain=baseEntropy-newEntropy
        if(infoGain>bestInfoGain):
            bestInfoGain=infoGain
            bestFeature=i
    return bestFeature
#
def majorityCnt(classList):
    classCount={}
    for vote in classList:
        if vote not in classCount.keys():classCount[vote]=0
        classCount[vote]+=1
    sortedClassCount=sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

def createTree(dataSet,labels):
    classList=[example[-1] for example in dataSet]
    #如果标签里面所有值都一样，直接返回
    if classList.count(classList[0])==len(classList):
        return classList[0]
    #如果特征只剩一个，那么就调用此函数开始多数表决来决定哪个分类
    if len(dataSet[0])==1:
        return majorityCnt(classList)
    bestFeat=chooseBestFeatureToSplit(dataSet)
    bestFeatLabel=labels[bestFeat]
    myTree={bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues=[example[bestFeat] for example in dataSet]
    uniqueVals=set(featValues)
    for value in uniqueVals:
        subLabels=labels[:]
        myTree[bestFeatLabel][value]=createTree(splitDataSet(dataSet,bestFeat,value),subLabels)
    return myTree

def classify(inputTree,featLabels,testVec):
    firstStr=inputTree.keys()[0]
    secondDict=inputTree[firstStr]
    featIndex=featLabels.index(firstStr)  #查找这个特征的索引值，也就是在数组的第几个
    #print featIndex
    #print secondDict
    for key in secondDict.keys():
        #print key
        if testVec[featIndex]==key:
           # print 'its ok'
            if type(secondDict[key]).__name__=='dict':
               # print 'this is dict'
                classLabel=classify(secondDict[key],featLabels,testVec)
            else:
               # print 'this is not dict'
                classLabel=secondDict[key]
       # print 'not ok'
    return classLabel

'''
#使用决策树执行分类
def classify(inputTree, featLabels, testVec):
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)   #index方法查找当前列表中第一个匹配firstStr变量的元素的索引
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key], featLabels, testVec)
            else: classLabel = secondDict[key]
    return classLabel
'''

def storeTree(inputTree,filename):
    import pickle
    fw=open(filename,'w')
    pickle.dump(inputTree,fw)
    fw.close()

def grabTree(filename):
    import pickle
    fr=open(filename)
    return pickle.load(fr)

def lensesclass():
    fr=open('lenses.txt')
    lenses=[inst.strip().split('\t') for inst in fr.readlines()]
    lensesLabels=['age','prescript','astigmatic','tearRate']
    lensesTree=createTree(lenses,lensesLabels)
    print lensesTree
    import treePlotter
    treePlotter.createPlot(lensesTree)