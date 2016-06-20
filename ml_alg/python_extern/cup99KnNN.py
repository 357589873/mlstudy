#coding:utf-8
from numpy import  *
import csv
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
                    fileWrite.write(str(round(key,3))+'\t')
                #print item

                fileWrite.write(item)
                fileWrite.write('\n')

    f.close()
    fileWrite.close()
writecorrect=open(r'F:\BaiduYunDownload\papers\corrected.txt','w')
writePreword=open('preWork.txt','r')
prework={}
lines=writePreword.readlines()
for line in lines:
    curline=line.strip().split(' ')

    prework[curline[0]]=prework.get(curline[0],{})
    prework[curline[0]][curline[1]]=curline[2]
#print prework

with open(r'F:\BaiduYunDownload\papers\corrected.csv') as fcorr:
    reader=csv.reader(fcorr)
    curline=[]
    for row in reader:
        curline=row
        allAttibute=[]
        for item in prework.keys():
            for itemj in prework[item].keys():
                allAttibute.append(itemj)
        if curline[int(item)] not in allAttibute:
            continue
        for item in prework.keys():
            print curline[int(item)]
            curline[int(item)]=prework[item][curline[int(item)]]
        for i in range(len(curline)):
            writecorrect.write(curline[i]+' ')
        writecorrect.write('\n')
fcorr.close()
writecorrect.close()
writePreword.close()



