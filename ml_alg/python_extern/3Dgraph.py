#coding:utf-8
import random

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

from mpl_toolkits.mplot3d import Axes3D


#获取文件夹底下的所有文件
#os.chmod('log',0777)
#filedir=os.listdir('./log')
a = "./../log"
filedir = os.listdir(a)


for i in range(len(filedir)):
    filedir[i]=int(filedir[i].split('.')[0])
print filedir
mpl.rcParams['font.size'] = 10

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for z in filedir:
     xs = xrange(1,13)
     ys = 1000 * np.random.rand(12)

     color =plt.cm.Set2(random.choice(xrange(plt.cm.Set2.N)))
     ax.bar(xs, ys, zs=z, zdir='y', color=color, alpha=0.8)

ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(xs))
ax.yaxis.set_major_locator(mpl.ticker.FixedLocator(ys))

ax.set_xlabel('Month')
ax.set_ylabel('Year')
ax.set_zlabel('Sales Net [usd]')

plt.show()