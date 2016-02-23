#coding:utf-8
from numpy import *
#from math import *
def loadDataSet(filename):
    dataMat=[];labelMat=[]
    fr=open(filename)
    for line in fr.readlines():
        lineArr=line.strip().split('\t')
        dataMat.append([float(lineArr[0]),float(lineArr[1])])
        labelMat.append(float(lineArr[2]))
    return dataMat,labelMat

def selectJrand(i,m):
    j=i
    while(j==i):
        j=int(random.uniform(0,m))
    return j

def clipAlpha(aj,H,L):
    if aj>H:
        aj=H
    if L>aj:
        aj=L
    return aj

def smosimple(dataMatIn,classLabels,C,toler,maxIter):
    dataMatrix=mat(dataMatIn);labelMat=mat(classLabels).transpose()
    b=0;m,n=shape(dataMatrix)
    alphas=mat(zeros((m,1)))
    iter=0
    while(iter<maxIter):
        alphaPairsChanged=0
        for i in range(m):
            #求出来xi对应的y
            fxi=float(multiply(alphas,labelMat).T*\
                      (dataMatrix*dataMatrix[i,:].T))+b
            #求一下残差。至于为啥，还没搞懂
            Ei=fxi-float(labelMat[i])
            #如果没有被优化（还没搞懂）
            if((labelMat[i]*Ei<-toler)and(alphas[i]<C))\
                or ((labelMat[i]*Ei>toler) and(alphas[i]*Ei>0)):
                j=selectJrand(i,m)
                #求xj对应的y
                fxj=float(multiply(alphas,labelMat).T*\
                          (dataMatrix*dataMatrix[j,:].T))+b
                #求残差
                Ej=fxj-float(labelMat[j])
                #先把原先的保存一下
                alphaIold=alphas[i].copy()
                alphaJold=alphas[j].copy()
                #加入约束，保证符合约束
                if(labelMat[i]!=labelMat[j]):
                    L=max(0,alphas[j]-alphas[i])
                    H=min(C,C+alphas[j]-alphas[i])
                else:
                    L=max(0,alphas[j]+alphas[i]-C)
                    H=min(C,alphas[j]+alphas[i])
                if L==H:print "L==H";continue
                #eta代表相似度，其实是为了求alpha[j]
                eta=2.0*dataMatrix[i,:]*dataMatrix[j,:].T-dataMatrix[i,:]*dataMatrix[i,:].T\
                -dataMatrix[j,:]*dataMatrix[j,:].T
                if eta>=0:print "eta >=0";continue
                #求得alpha[j]
                alphas[j]-=labelMat[j]*(Ei-Ej)/eta
                alphas[j]=clipAlpha(alphas[j],H,L)
                if(abs(alphas[j]-alphaJold)<0.00001):print "j not moving enough";continue
                #求alpha[i]
                alphas[i]+=labelMat[j]*labelMat[i]*(alphaJold-alphas[j])
                #求b
                b1=b-Ei-labelMat[i]*(alphas[i]-alphaIold)*dataMatrix[i,:]*dataMatrix[i,:].T\
                -labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[i,:]*dataMatrix[j,:].T
                b2=b-Ej-labelMat[i]*(alphas[i]-alphaIold)*dataMatrix[i,:]*dataMatrix[j,:].T\
                -labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[j,:]*dataMatrix[j,:].T
                if(0<alphas[i])and(C>alphas[i]):b=b1
                elif(0<alphas[j])and(C>alphas[j]):b=b2
                else:b=(b1+b2)/2.0
                #代表了没有改变的次数
                alphaPairsChanged+=1
                print "iter:%d i:%d,pairs changed %d" %(iter,i,alphaPairsChanged)
        if(alphaPairsChanged==0):iter+=1
        else:iter=0
        print "iteration number: %d" % iter
    return  b,alphas
'''
class optStruct:
    def __init__(self,dataMatIn,classLabels,C,toler):
        self.X=dataMatIn
        self.labelMat=classLabels
        self.C=C
        self.tol=toler
        self.m=shape(dataMatIn)[0]
        self.alphas=mat(zeros((self.m,1)))
        self.b=0
        self.eCache=mat(zeros((self.m,2)))'''
def kernelTrans(X,A,kTup):
    m,n=shape(X)
    K=mat(zeros((m,1)))
    #第一个参数是描述类型的
    if kTup[0]=='lin':K=X*A.T
    elif kTup[0]=='rbf':
        for j in range(m):
            deltaRow=X[j,:]-A
            K[j]=deltaRow*deltaRow.T
        #print K/(-1*kTup[1]**2)
        #for i in range(len(K)):
        #   print i,exp(K[i]/(-1*kTup[1]**2)) ,
        K = exp(K/(-1*kTup[1]**2))
    else:raise NameError('not recognized this kernel')
    return K

class optStruct:
    def __init__(self,dataMatIn,classLabels,C,toler,kTup):
        self.X=dataMatIn
        self.labelMat=classLabels
        self.C=C
        self.tol=toler
        self.m=shape(dataMatIn)[0]
        self.alphas=mat(zeros((self.m,1)))
        self.b=0
        self.eCache=mat(zeros((self.m,2)))
        self.K=mat(zeros((self.m,self.m)))
        for i in range(self.m):
            self.K[:,i]=kernelTrans(self.X,self.X[i,:],kTup)

def calcEk(oS,k):
    a=multiply(oS.alphas,oS.labelMat).T*oS.K[:,k]
    #print 'a is\n',a
    fxk=float(a)+oS.b
    Ek=fxk-float(oS.labelMat[k])
    return Ek

def selectJ(i,oS,Ei):
    maxK=-1;maxDeltaE=0;Ej=0
    oS.eCache[i]=[1,Ei]
    #nonzero是求这个结构里的非零位置。结果是两个array。其中一个
    #代表了横坐标，另外一个代表纵坐标
    validEcacheList=nonzero(oS.eCache[:,0].A)[0]
    if(len(validEcacheList))>1:
        for k in validEcacheList:
            if k==i:continue
            Ek=calcEk(oS,k)
            deltaE=abs(Ei-Ek)
            if(deltaE>maxDeltaE):
                maxK=k;maxDeltaE=deltaE;Ej=Ek
        return maxK,Ej
    else:
        j=selectJrand(i,oS.m)
        Ej=calcEk(oS,j)
    return j,Ej

def updateEk(oS,k):
    Ek=calcEk(oS,k)
    oS.eCache[k]=[1,Ek]

def innerL(i,oS):
    Ei=calcEk(oS,i)
    if((oS.labelMat[i]*Ei<-oS.tol)and (oS.alphas[i]<oS.C)) or\
            ((oS.labelMat[i]*Ei>oS.tol)and (oS.alphas[i]>0)):
        j,Ej=selectJ(i,oS,Ei)
        alphaIold=oS.alphas[i].copy();alphaJold=oS.alphas[j].copy()
        if(oS.labelMat[i]!=oS.labelMat[j]):
            L=max(0,oS.alphas[j]-oS.alphas[i])
            H=min(oS.C,oS.C+oS.alphas[j]-oS.alphas[i])
        else:
            L=max(0,oS.alphas[j]+oS.alphas[i]-oS.C)
            H=min(oS.C,oS.alphas[j]+oS.alphas[i])
        if L==H :print "L==H";return 0
        eta=2.0*oS.K[i,j]-oS.K[i,i]-oS.K[j,j]
        if eta>=0:print "eta>=0";return 0
        oS.alphas[j]-=oS.labelMat[j]*(Ei-Ej)/eta
        oS.alphas[j]=clipAlpha(oS.alphas[j],H,L)
        updateEk(oS,j)
        if(abs(oS.alphas[j]-alphaJold)<0.00001):
            print "j not moving enough";return  0
        oS.alphas[i]+=oS.labelMat[j]*oS.labelMat[i]*(alphaJold-oS.alphas[j])
        updateEk(oS,i)
        b1=oS.b-Ei-oS.labelMat[i]*(oS.alphas[i]-alphaIold)*\
        oS.K[i,i]-oS.labelMat[j]*(oS.alphas[j]-alphaJold)*\
        oS.K[i,j]
        b2=oS.b-Ej-oS.labelMat[i]*(oS.alphas[i]-alphaIold)*\
        oS.K[i,j]-oS.labelMat[j]*(oS.alphas[j]-alphaJold)*\
        oS.K[j,j]
        if(0<oS.alphas[i])and(oS.C>oS.alphas[i]):oS.b=b1
        elif (0<oS.alphas[j])and(oS.C>oS.alphas[j]):oS.b=b2
        else:oS.b=(b1+b2)/2.0
        return 1
    else:return 0

def smoP(dataMatIn,classLabels,C,toler,maxIter,kTup=('lin',0)):
    oS=optStruct(mat(dataMatIn),mat(classLabels).transpose(),C,toler,kTup)
    iter=0
    entireSet=True;alphaPairsChanged=0
    while(iter<maxIter)and((alphaPairsChanged>0)or(entireSet)):
        alphaPairsChanged=0
        if entireSet:
            for  i in range(oS.m):
                alphaPairsChanged+=innerL(i,oS)
            print "fullset,iter %d i:%d,pairs changed %d" %\
                  (iter,i,alphaPairsChanged)
            iter+=1
        else:
            nonBoundIs=nonzero((oS.alphas.A>0)*(oS.alphas.A<C))[0]
            for i in nonBoundIs:
                alphaPairsChanged+=innerL(i,oS)
            print "non-bound,iter:%d i:%d,pairs changed %d"%\
                      (iter,i,alphaPairsChanged)
            iter+=1
        if entireSet:entireSet=False
        elif (alphaPairsChanged==0):entireSet=True
        print "iteration number:%d" % iter
    return oS.b,oS.alphas

def calcWs(alphas,dataArr,classLabels):
    X=mat(dataArr);labelMat=mat(classLabels).transpose()
    m,n=shape(X)
    w=zeros((n,1))
    for i in range(m):
        w+=multiply(alphas[i]*labelMat[i],X[i,:].T)
    return w




def testRbf(k1=1.3):
    dataArr,labelArr=loadDataSet('testSetRBF.txt')
    b,alphas=smoP(dataArr,labelArr,200,0.0001,10000,('rbf',k1))
    datMat=mat(dataArr);labelMat=mat(labelArr).transpose()
    svInd=nonzero(alphas.A>0)[0]
    sVs=datMat[svInd]
    labelSV=labelMat[svInd]
    print "there are %d support vectors " %shape(sVs)[0]
    m,n=shape(datMat)
    errorCount=0
    for i in range(m):
        kernelEval=kernelTrans(sVs,datMat[i,:],('rbf',k1))
        predict=kernelEval.T*multiply(labelSV,alphas[svInd])+b
        if sign(predict)!=sign(labelArr[i]):errorCount+=1
    print "the training error rate is %f" %(float(errorCount/m))
    dataArr,labelArr=loadDataSet('testSetRBF.txt')
    errorCount=0
    dataMat=mat(dataArr);labelMat=mat(labelArr).transpose()
    m,n=shape(datMat)
    for i in range(m):
        kernelEval=kernelTrans(sVs,datMat[i,:],('rbf',k1))
        predict=kernelEval.T*multiply(labelSV,alphas[svInd]+b)
        if sign(predict)!=sign(labelArr[i]):errorCount+=1
    print "the test error rate is %f" %(float(errorCount/m))

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

def loadImages(dirName):
    from os import listdir
    hwLabels=[]
    trainingFilelist=listdir(dirName)
    m=len(trainingFilelist)
    trainingMat=zeros((m,1024))
    for i in range(m):
        fileNameStr=trainingFilelist[i]
        fileStr=fileNameStr.split('.')[0]
        classNumStr=int(fileStr.split('_')[0])
        if classNumStr==9:hwLabels.append(-1)
        else:hwLabels.append(1)
        trainingMat[i,:]=img2vector('%s/%s' % (dirName,fileNameStr))
    return trainingMat,hwLabels

def testDigits(kTup=('rbf',10)):
    dataArr,labelArr=loadImages('trainingDigits')
    b,alphas=smoP(dataArr,labelArr,200,0.0001,10000,kTup)
    datMat=mat(dataArr);labelMat=mat(labelArr).transpose()
    #返回两个维度，代表了x,y的值。合并起来代表一个坐标数组。
    #.A是代表array()
    #其实呢就是想把alpha中的等于1的索引找出来。也就是支持向量的索引
    '''>>> x
    array([[ 1.,  0.,  0.],
           [ 1.,  1.,  1.],
           [ 0.,  0.,  1.]])
       >>> np.nonzero(x)
    (array([0, 1, 1, 1, 2]), array([0, 0, 1, 2, 2]))

    '''
    svInd=nonzero(alphas.A>0)[0]
    #一下子把索引对应的行数抽出来组成一个矩阵。
    sVs=datMat[svInd]
    labelSV=labelMat[svInd]
    print "there are %d Support Vectors" % shape(sVs)[0]
    m,n=shape(datMat)
    errorCount=0
    for i in range(m):
        kernelEval=kernelTrans(sVs,datMat[i,:],kTup)
        predict=kernelEval.T*multiply(labelSV,alphas[svInd])+b
        if sign(predict)!=sign(labelArr[i]):errorCount+=1
    print "the training error rate is :%f" %(float(errorCount)/m)
    dataArr,labelArr=loadImages('testDigits')
    errorCount=0
    datMat=mat(dataArr);labelMat=mat(labelArr).transpose()
    m,n=shape(datMat)
    for i in range(m):
        kernelEval=kernelTrans(sVs,datMat[i,:],kTup)
        predict=kernelEval.T*multiply(labelSV,alphas[svInd])+b
        if sign(predict)!=sign(labelArr[i]):errorCount+=1
    print "the test error rate is %f" % (float(errorCount)/m)
