#coding:utf-8
from numpy import *
import  operator
from os import listdir
#自己造一个简单的数据集
def createDataSet():
    group=array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels=['A','A','B','B']
    return  group,labels
'''main coding of classify,select top k of similarity
   intX代表要预测的输入向量，dataset是特征矩阵（array类型），labels是标签列表（list），k代表取前几个相似'''
def classify0(inX,dataSet,labels,k):
    dataSetsize=dataSet.shape[0]
    #比如tile(A,n)，功能是将数组A重复n次，构成一个新的数组，在这里是将向量intX列方向进行复制。
    diffMat=tile(inX,(dataSetsize,1))-dataSet
    sqDiffMat=diffMat**2
    #求每一行的残差和
    sqDistances=sqDiffMat.sum(axis=1)
    distances=sqDistances**0.5
    #求的索引的排序值。a=array([1,2,3,5,4,6])使用函数输出array([0, 1, 2, 4, 3, 5])
    sortedDistIndicies=distances.argsort()
    #字典的存储结果为  {类别：数量}
    classCount={}
    for i in range(k):
        voteIlabel=labels[sortedDistIndicies[i]]
        classCount[voteIlabel]=classCount.get(voteIlabel,0)+1
    sortedClassCount=sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]
#读文件，将文件读到array里。返回一个属性的array[m,n]和一个标签的list
def file2matrix(filename):
    fr=open(filename)
    arrayOLines=fr.readlines()
    numberOfLines=len(arrayOLines)
    returnMat=zeros((numberOfLines,3))
    classLabelVector=[]
    index=0
    for line in arrayOLines:
        line=line.strip()
        listFromLine=line.split('\t')
        returnMat[index,:]=listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index+=1
    return returnMat,classLabelVector
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
#算法的基本测试
def datingClassTest():
    #测试集的比例
    hoRatio=0.10
    datingDataMat,datingLabels=file2matrix('datingTestSet2.txt')
    normMat,ranges,minVals=autoNorm(datingDataMat)
    m=normMat.shape[0]
    errorCount=0.0
    numTestVecs=int(m*hoRatio)
    for i in range(numTestVecs):
        classifierResult=classify0(normMat[i,:],normMat[numTestVecs:m,:],\
                                   datingLabels[numTestVecs:m],10)
        print "the classifier came back with:%d,the real answer is :%d" %(classifierResult,datingLabels[i])
        if (classifierResult!=datingLabels[i]):errorCount+=1.0

    print "the total errorrate is %f" % (errorCount/float(numTestVecs))

def classifyPerson():
    resultList=['not at all','in small doses','in large doses']
    percentTats=float(raw_input("percentage of time spent playing video games?"))
    ffMiles=float(raw_input("frequent filer miles earned per year"))
    iceCream=float(raw_input("liters of ice cream consumed per year?"))
    datingDataMat,datingLabels=file2matrix('datingTestSet2.txt')
    normMat,ranges,minVals=autoNorm(datingDataMat);
    inArr=array([ffMiles,percentTats,iceCream])
    classifierResult=classify0((inArr-minVals)/ranges,normMat,datingLabels,3)
    print "you probably like this person :",resultList[classifierResult-1]


#handwriting recognization
#file is 32*32 but we create a array of 1*1024 to store these chars
def img2vector(filename):
    returnVect=zeros((1,1024))
    fr=open(filename)
    for i in range(32):
        lineBtr=fr.readline()
        for j in range(32):
            returnVect[0,32*i+j]=int(lineBtr[j])
    return returnVect

def handwritingClassTest():
    hwLabels=[]
    trainingFileList=listdir('trainingDigits')
    m=len(trainingFileList)
    trainingMat=zeros((m,1024))
    for i in range(m):
        fileNameStr=trainingFileList[i]
        fileStr=fileNameStr.split('.')[0]
        classNumStr=int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:]=img2vector('trainingDigits/%s' % fileNameStr)
    testFileList=listdir('testDigits')
    errorCount=0.0
    mTest=len(testFileList)
    for i in range(mTest):
        fileNameStr=testFileList[i]
        fileStr=fileNameStr.split('.')[0]
        classNumStr=int(fileStr.split('_')[0])
        vectorUnderTest=img2vector('testDigits/%s' % fileNameStr)
        classifierResult=classify0(vectorUnderTest,trainingMat,hwLabels,11)
        print "the classifier came back with:%d,the real answer is %d" % (classifierResult,classNumStr)
        if(classifierResult !=classNumStr):errorCount+=1.0
    print "\nthe total number of errors is:%d" % errorCount
    print "\nthe total error rate is: %f "% (errorCount/float(mTest))

def draw():
    import matplotlib
    import matplotlib.pyplot as plt
    datingDataMat,datingLabels=file2matrix('datingTestSet2.txt')
    fig=plt.figure()
    ax=fig.add_subplot(111)
    print len(datingDataMat[:,1]),len(datingDataMat[:,2]),len(datingLabels)
    ax.scatter(datingDataMat[:,1],datingDataMat[:,2],80.0*datingLabels,1.0*array(datingLabels))
    plt.show()