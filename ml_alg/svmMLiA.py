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
                      (dataMatrix*dataMatrix[i,:]))+b
            #求一下残差。至于为啥，还没搞懂
            Ei=fxi-float(labelMat[i])
            #如果没有被优化（还没搞懂）
            if((labelMat[i]*Ei<-toler)and(alphas[i]<C))\
                or ((labelMat[i]*Ei>toler) and(alphas[i]*Ei>0)):
                j=selectJrand(i,m)
                #求xj对应的y
                fxj=float(multiply(alphas,labelMat).T*\
                          (dataMatrix*dataMatrix[j,:]))+b
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
