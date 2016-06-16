#coding:utf-8
from numpy import  *
import csv
dataDic={}
with open(r'C:\Users\Administrator\Desktop\cainiao\item_feature1.csv') as f:
        reader=csv.reader(f)
        for row in reader:
            curdata=[]
            for i in range(41):
                curdata=curdata.append(row[i])
            dataDic.get(row[41],[0]*42)+curdata
