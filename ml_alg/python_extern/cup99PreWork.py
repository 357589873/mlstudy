#coding:utf-8
from numpy import  *
import csv
def trainDataPrework():
    data2Dic={}
    data3Dic={}
    dataNumDic={}
    fileWrite=open('preWork.txt','w')
    data2num=0
    data3num=0
    fileNew=open(r'F:\BaiduYunDownload\papers\cup99test.txt','w')

    with open(r'F:\BaiduYunDownload\papers\cup99test.csv') as f:
            reader=csv.reader(f)
            for row in reader:
                #print type(row)
                if data2Dic.get(row[2])==None:
                    data2num+=1
                data2Dic[row[2]]=data2Dic.get(row[2],data2num)
                row[2]=data2Dic.get(row[2],data2num)
                if data3Dic.get(row[3])==None:
                    data3num+=1
                data3Dic[row[3]]=data3Dic.get(row[3],data3num)
                row[3]=data3Dic.get(row[3],data3num)
                for i in range(len(row)):
                    fileNew.write(str(row[i])+" ")
                fileNew.write('\n')
    #data2Dic=sorted(data2Dic.items(),key=lambda e:e[1],reverse=False)
    #data3Dic=sorted(data3Dic.items(),key=lambda e:e[1],reverse=False)
    for item in data2Dic.keys():
        fileWrite.write('2'+' '+item+' '+str(data2Dic[item]))
        fileWrite.write('\n')
    for item in data3Dic.keys():
        fileWrite.write('3'+' '+item+' '+str(data3Dic[item]))
        fileWrite.write('\n')
    fileWrite.close()
    fileNew.close()
    f.close()
def testDataPrework():
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

trainDataPrework()
testDataPrework()
