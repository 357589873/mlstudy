#coding:utf-8
#约瑟夫环，本来想删除元素，后来觉得直接讲元素改成0
from numpy import *

nums=0
numLeft=45
peop=list(linspace(1,45,45))
while(numLeft>0):
    for i in range(len(peop)):
        nums+=1
        if peop[nums]==0:continue
        if nums==13:
            print peop[i]
            len(peop)
            peop[i]==0
            #print peop
            nums=0
            numLeft-=1
