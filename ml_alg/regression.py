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

def rssError(yArr,yHatArr):
    return ((yArr-yHatArr)**2).sum()

#岭回归
def ridgeRegres(xMat,yMat,lam=0.2):
    xTx=xMat.T*xMat
    denom=xTx+eye(shape(xMat)[1])*lam
    if linalg.det(denom)==0.0:
        print "this matrix is singular,can not inverse"
        return
    ws=denom.I*(xMat.T*yMat)
    #print ws
    #ws是一个1*m的矩阵
    return ws

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
        break
    return wMat
#數據標準化
def regularize(xMat):
    xMeans=mean(xMat,0)
    xVar=var(xMat,0)
    xMat=(xMat-xMeans)/xVar
    return xMat
#前向逐步线性回归
def stageWise(xArr,yArr,eps=0.01,numIt=100):
    xMat=mat(xArr);yMat=mat(yArr).T
    yMean=mean(yMat,0)
    yMat=yMat-yMean
    xMat=regularize(xMat)
    m,n=shape(xMat)
    returnMat=zeros((numIt,n))
    ws=zeros((n,1));wsTest=ws.copy();wsMax=ws.copy()
    for i in range(numIt):
        print ws.T
        lowestError=inf
        for j in range(n):
            for sign in [-1,1]:
                wsTest=ws.copy()
                wsTest[j]+=eps*sign
                yTest=xMat*wsTest
                rssE=rssError(yMat.A,yTest.A)
                if rssE<lowestError:
                    lowestError=rssE
                    wsMax=wsTest
        ws=wsMax.copy()
        returnMat[i,:]=ws.T
    return  returnMat

#预测乐高的价格
from time import sleep
import  json
import  urllib2
def searchForTest(retX,retY,setNum,yr,numPce,origPrc):
    sleep(10)
    myAPIstr='AIzaSyD2cR2KFyx12hXu6PFU-wrWot3NXvko8vY'
    searchURL='https://www.googleapis.com/shopping/search/v1/public/' \
              'products?key=%s&country=US&q=lego+%d%alt=json' % (myAPIstr,setNum)
    pg=urllib2.urlopen(searchURL)
    retDict=json.loads(pg.read())
    for i in range(len(retDict['items'])):
        try:
            currItem=retDict['items'][i]
            if currItem['product']['condition']=='new':
                newFlag=1
            else:newFlag=0
            listOfInv=currItem['product']['inventories']
            for item in listOfInv:
                sellingPrice=item['price']
                if sellingPrice>origPrc*0.5:
                    print "%d\t%d\t%d\t%f\t%f" %\
                          (yr,numPce,newFlag,origPrc,sellingPrice)
                    retX.append([yr,numPce,newFlag,origPrc,sellingPrice])
                    retY.append(sellingPrice)
        except:print 'problem with item %d' % i

def setDataCollect(retX,retY):
    searchForTest(retX,retY,8288,2006,800,49.99)
    searchForTest(retX,retY,10030,2002,3096,269.99)
    searchForTest(retX,retY,10179,2007,5195,499.99)
    searchForTest(retX,retY,10181,2007,3428,199.99)
    searchForTest(retX,retY,10189,2008,5922,299.99)
    searchForTest(retX,retY,10196,2009,3263,249.99)

def scrapePage(inFile,outFile,yr,numPce,origPrc):
    from BeautifulSoup import BeautifulSoup
    fr = open(inFile); fw=open(outFile,'a') #a is append mode writing
    soup = BeautifulSoup(fr.read())
    i=1
    currentRow = soup.findAll('table', r="%d" % i)
    while(len(currentRow)!=0):
        currentRow = soup.findAll('table', r="%d" % i)
        title = currentRow[0].findAll('a')[1].text
        lwrTitle = title.lower()
        if (lwrTitle.find('new') > -1) or (lwrTitle.find('nisb') > -1):
            newFlag = 1.0
        else:
            newFlag = 0.0
        soldUnicde = currentRow[0].findAll('td')[3].findAll('span')
        if len(soldUnicde)==0:
            print "item #%d did not sell" % i
        else:
            soldPrice = currentRow[0].findAll('td')[4]
            priceStr = soldPrice.text
            priceStr = priceStr.replace('$','') #strips out $
            priceStr = priceStr.replace(',','') #strips out ,
            if len(soldPrice)>1:
                priceStr = priceStr.replace('Free shipping', '') #strips out Free Shipping
            print "%s\t%d\t%s" % (priceStr,newFlag,title)
            fw.write("%d\t%d\t%d\t%f\t%s\n" % (yr,numPce,newFlag,origPrc,priceStr))
        i += 1
        currentRow = soup.findAll('table', r="%d" % i)
    fw.close()

def setDataCollect():
    scrapePage('setHtml/lego8288.html','out.txt', 2006, 800, 49.99)
    scrapePage('setHtml/lego10030.html','out.txt', 2002, 3096, 269.99)
    scrapePage('setHtml/lego10179.html','out.txt', 2007, 5195, 499.99)
    scrapePage('setHtml/lego10181.html','out.txt', 2007, 3428, 199.99)
    scrapePage('setHtml/lego10189.html','out.txt', 2008, 5922, 299.99)
    scrapePage('setHtml/lego10196.html','out.txt', 2009, 3263, 249.99)

