#coding:utf-8
from numpy import  *
import csv
import pickle
dataDic={}
dataNumDic={}

def generateAverage():
    fileWrite=open('average.txt','w')
    with open(r'F:\BaiduYunDownload\papers\cup99test.txt') as f:
            reader=f.readlines()
            for row in reader:
                curdata=zeros(41)
                rowList=row.split(' ')
                curdata=array([float(i) for i in rowList[0:41]])
                #print dataDic.get(row[41],zeros(41)),'   ',curdata
                dataDic[rowList[41]]=dataDic.get(rowList[41],zeros(41))+curdata
                dataNumDic[rowList[41]]=dataNumDic.get(rowList[41],0)+1

            #dataDic[row[41]]=dataDic.get(row[41],zeros(41))/dataNumDic.get(row[41],0)
            #print dataDic
            for item in dataDic.keys():
                dataDic[item]=dataDic.get(item,zeros(41))/dataNumDic.get(item,0)
                for key in dataDic[item]:
                    #print key,
                    fileWrite.write(str(round(key,3))+' ')
                #print item

                fileWrite.write(item)
                fileWrite.write('\n')

    f.close()
    fileWrite.close()
def loadData(path):
    fileTest=open(path,'r')
    lines=fileTest.readlines()
    nData=len(lines)
    #print (lines[0].strip().split(' '))
    mdata=len(lines[0].strip().split(' '))-1
    dataArray=zeros((nData,mdata))
    labelList=[]
    index=0
    for line in lines:
        curLine=line.strip().split(' ')
        #print mdata,nData
        dataArray[index,:]=array(curLine[0:-1])
        labelList.append(curLine[-1])
        index+=1
    return dataArray,labelList
#余弦距离矩阵求解
def cosDisArray(vec1,vec2):
    if shape(vec1)!=shape(vec2):
        print "shape error",shape(vec1),shape(vec2)
    vecMulvec=(vec1*vec2).sum(axis=1)
    #print vecMulvec
    vec2add=(vec1*vec1).sum(axis=1)**0.5+(vec2*vec2).sum(axis=1)**0.5
    return vecMulvec/vec2add

#数据归一化
def autoNorm(dataSet):
    #0代表是按列计算
    minVals=dataSet.min(0)
    maxVals=dataSet.max(0)
    ranges=maxVals-minVals
    normDataSet=zeros(shape(dataSet))
    m=dataSet.shape[0]
    normDataSet=dataSet-tile(minVals,(m,1))
    normDataSet=normDataSet/tile(ranges,(m,1))
    return normDataSet,ranges,minVals

def crossValidation():
    dataArryTest,labelListTest=loadData(r'F:\BaiduYunDownload\papers\corrected.txt')
    from sklearn import preprocessing
    # normalize the data attributes
    dataArryTestNorm = preprocessing.normalize(dataArryTest)
    #dataArryTestNorm,dataArrayRanges,dataArryMinVals=autoNorm(dataArryTest)
    aveData,aveLabel=loadData('average.txt')
    aveDataNorm=preprocessing.normalize(aveData)
    numDataTest=shape(dataArryTest)[0]
    print numDataTest
    numDataAve=shape(aveData)[0]
    print shape(aveData),shape(dataArryTest)
    errorCount=0
    index=0
    for i in range(numDataTest):
        resultArrIndex=cosDisArray(tile(dataArryTestNorm[index,:],(numDataAve,1)),aveDataNorm).argsort()
        resultLabel=aveLabel[resultArrIndex[-1]]
        #print resultLabel,labelListTest[index]
        if labelListTest[index]!=resultLabel:
            errorCount+=1
        index+=1
    errorRate=errorCount/float(numDataTest)
    print 'errorCount is %d errorRaete is %f' %(errorCount,errorRate)

def kmeanCrossValidation(k):
    dataArrayTest,labelListTest=loadData(r'F:\BaiduYunDownload\papers\corrected.txt')
    dataArrayTrain,labelListTrain=load(r'F:\BaiduYunDownload\papers\cup99test.txt')
    from sklearn import preprocessing
    from sklearn.cluster   import KMeans
    dataArryTestNorm = preprocessing.normalize(dataArrayTest)
    clf=KMeans(init='k-means++', n_clusters=k, n_init=10)
    pre=clf.fit(dataArrayTrain)

    centroid=pre.cluster_centers_
    centroidWrite=open('centroid','w')
    pickle.dump(centroid,centroidWrite)

    labelCluster=pre.labels_
    labelClusterWrite=open('labelCluster','w')
    pickle.dump(labelCluster,labelClusterWrite)

    labelPre=clf.predict(dataArrayTest)
    labelClusterWrite=open('labelPre','w')
    pickle.dump(labelPre,labelClusterWrite)

    labelClusterDic={}
    for i in range(len(labelCluster)):
        labelClusterDic[labelCluster[i]]=labelClusterDic.get(labelCluster[i],[]).append(i)

    for item in labelClusterDic.keys():
        labelList=labelClusterDic[item]
        labelCount={}
        for labelitem in labelList:
























