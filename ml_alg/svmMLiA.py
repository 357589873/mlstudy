#coding:utf-8
from numpy import *
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

class optStruct:
    def __init__(self,dataMatIn,classLabels,C,toler):
        self.X=dataMatIn
        self.labelMat=classLabels
        self.C=C
        self.tol=toler
        self.m=shape(dataMatIn)[0]
        self.alphas=mat(zeros((self.m,1)))
        self.b=0
        self.eCache=mat(zeros((self.m,2)))

def calcEk(oS,k):
    fxk=float(multiply(oS.alphas,oS.labelMat).T*(oS.X*oS.X[k,:].T))+oS.b
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
            H=min(oS.C,oS.C+oS)
