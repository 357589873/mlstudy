#coding:gbk
import math
import copy
import numpy as np
import matplotlib.pyplot as plt
def init_data(sigma,mu1,mu2,k,n):
    global x
    x=np.zeros((1,n))
    global mu
    mu=np.random.random(2)
    global exception
    exception=np.zeros((n,k))
    for i in range(n):
        if np.random.random(1)>0.5:
            x[0,i]=np.random.normal()*sigma+mu1
        else:
            x[0,i]=np.random.normal()*sigma+mu2

def e_step(n,k,sigma):
    global x
    global exception
    global mu
    for i in range(n):
        fenmu=0
        for j in range(k):
            fenmu+=math.exp((-1/(float(2*(sigma**2))))*(float(x[0,i]-mu[j])))**2
        for j in range(k):
            fenzi=math.exp((-1/(float(2*(sigma**2))))*(float(x[0,i]-mu[j])))**2
            exception[i,j]=fenzi/fenmu


def m_step(k,n):
    for i in range(k):
        fenzi=0
        fenmu=0
        for j in range(n):
            fenzi+=exception[j,i]*x[0,j]
            fenmu+=exception[j,i]
        mu[i]=fenzi/fenmu


def run(sigma,mu1,mu2,k,n,iter_num,jingdu):
    init_data(sigma,mu1,mu2,k,n)
    for i in range(iter_num):
        old_mu=copy.deepcopy(mu)
        e_step(n,k,sigma)
        m_step(k,n)
        if sum(abs(mu-old_mu))<jingdu:
            break


if __name__ == '__main__':
    run(6,20,40,2,1000,1000,0.0001)
    plt.hist(x[0,:],20)
    plt.show()