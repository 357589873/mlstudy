#coding:utf-8
from numpy import *
def loadDataset(fileName):
    numFeat=len(open(fileName).readline().split('\t'))-1
    dataMat=[];labelMat=[]
    fr=open(fileName)
    for line in fr.readlines():
        lineArr=[]
        curLine=line.strip().split('\t')
        for i in range(numFeat):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return dataMat,labelMat

def standRegres(xArr,yArr):
    xMat=mat(xArr);yMat=mat(yArr).T
    xTx=xMat.T*xMat
    if linalg.det(xTx)==0.0:
        print "this matrix is singular,cannot do inverse"
        return
    ws=xTx.I*(xMat.T*yMat)
    return ws

def thisDraw(xArr,yArr,ws):
    xMat=mat(xArr)
    print xMat
    print xArr
    print array(xArr)
    yMat=mat(yArr)
    yHat=xMat*ws
    import matplotlib.pyplot as plt
    fig=plt.figure()
    ax=fig.add_subplot(111)
    #我就是看看这里到底是干什么，原来用了mat后必须这么做，要是arr就好了
    print array(xArr)[:,1]
    print xMat[:,1]
    print xMat[:,1].flatten()
    print xMat[:,1].flatten().A[0]
    ax.scatter(xMat[:,1].flatten().A[0],yMat.T[:,0]
               .flatten().A[0])
    xCopy=xMat.copy()
    xCopy.sort(0)
    yHat=xCopy*ws
    print xCopy[:,1],yHat
    #plot这个函数比较好，就算加了.flatten().A[0]变成arr一样可以。
    ax.plot(xCopy[:,1],yHat)
    plt.show()

#局部加权线性回归函数
#中心思想是来了数据再进行计算，不是事先求好回归方程
def lwlr(testPoint,xArr,yArr,k=1.0):
    xMat=mat(xArr);yMat=mat(yArr).T
    m=shape(xMat)[0]
    weights=mat(eye((m)))
    for j in range(m):
        diffMat=testPoint-xMat[j,:]
        weights[j,j]=exp(diffMat*diffMat.T/(-2.0*k**2))
    xTx=xMat.T*(weights*xMat)
    if linalg.det(xTx)==0.0:
        print 'this matrix is singular,change'
        return
    ws=xTx.I*(xMat.T*(weights*yMat))
    return testPoint*ws

def lwlrTest(testArr,xArr,yArr,k=1.0):
    m=shape(testArr)[0]
    yHat=zeros(m)
    for i in range(m):
        yHat[i]=lwlr(testArr[i],xArr,yArr,k)
    return yHat
#通过调节k的值来确定拟合的程度，0.3的时候就直线了。0.001过拟合
def thisDraw2(xArr,yArr,k=0.001):
    yHat=lwlrTest(xArr,xArr,yArr,k)
    xMat=mat(xArr)
    srtInd=xMat[:,1].argsort(0)
    xSort=xMat[srtInd][:,0,:]
    import matplotlib.pyplot as plt
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.plot(xSort[:,1],yHat[srtInd])
    ax.scatter(xMat[:,1].flatten().A[0],mat(yArr).T.flatten()
               .A[0],s=2,c='red')
    plt.show()

def ridgeRegres(xMat,yMat,lam=0.2):
    xTx=xMat.T*xMat
    denom=xTx+eye(shape(xMat)[1])*lam
    if linalg.det(denom)==0.0:
        print "this matrix is singular,can not inverse"
        return
    ws=denom.I*(xMat.T*yMat)
    return

def ridgeTest(xArr,yArr):
    xMat=mat(xArr);yMat=mat(yArr).T
    yMean=mean(yMat,0)
    yMat=yMat-yMean
    xMeans=mean(xMat,0)
    xVar=var(xMat,0)
    xMat=(xMat-xMeans)/xVar
    numTestPts=30
    wMat=zeros((numTestPts,shape(xMat)[1]))
    for i in range(numTestPts):
        ws=ridgeRegres(xMat,yMat,exp(i-10))
        wMat[i,:]=ws.T
    return wMat
