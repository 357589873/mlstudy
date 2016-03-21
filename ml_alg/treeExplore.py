#coding:utf-8
#use Tkinter
from numpy import *
from Tkinter import *
import regTrees
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
def reDraw(tolS,tolN):
    reDraw.f.clf()
    reDraw.a=reDraw.f.add_subplot(111)
    if chkBtnVar.get():
        if tolN<2:tolN=2
        myTree=regTrees.createtree(reDraw.rawDat,regTrees.modelLeaf,\
                                   regTrees.modelErr,(tolS,tolN))
        yHat=regTrees.createForeCast(myTree,reDraw.testDat,\
                                     regTrees.modelTreeEval)
    else:
        myTree=regTrees.createtree(reDraw.rawDat,ops=(tolS,tolN))
        yHat=regTrees.createForeCast(myTree,reDraw.testDat)
    #画点
    reDraw.a.scatter(reDraw.rawDat[:,0],reDraw.rawDat[:,1],s=5)
    #画线
    reDraw.a.plot(reDraw.testDat,yHat,lineWidth=2.0)
    reDraw.canvas.show()
#取值
def getInputs():
    try:tolN=int(tolNentry.get())
    except:
        tolN=10
        print "enter Integer for tolN"
        tolNentry.delete(0,END)
        tolNentry.insert(0,'10')
    try:tolS=float(tolSentry.get())
    except:
        tolS=1.0
        print "enter float for tols"
        tolSentry.delete(0,END)
        tolSentry.insert(0,'1.0')
    return tolN,tolS

def drawNewtree():
    tolN,tolS=getInputs()
    reDraw(tolS,tolN)

root=Tk()
#新建画布
#Label(root,text="plot place holder").grid(row=0,columnspan=4)
reDraw.f=Figure(figsize=(5,4),dpi=100)
reDraw.canvas=FigureCanvasTkAgg(reDraw.f,master=root)
reDraw.canvas.show()
reDraw.canvas.get_tk_widget().grid(row=0,columnspan=3)

Label(root,text="tolN").grid(row=1,column=0)
tolNentry=Entry(root)
tolNentry.grid(row=1,column=1)
tolNentry.insert(0,'10')
Label(root,text="tolS").grid(row=2,column=0)
tolSentry=Entry(root)
tolSentry.grid(row=2,column=1)
tolSentry.insert(0,'1.0')
Button(root,text="ReDraw",command=drawNewtree).\
    grid(row=1,column=2,rowspan=3)
chkBtnVar=IntVar()
chkBtn=Checkbutton(root,text="model tree",variable=chkBtnVar)
chkBtn.grid(row=3,column=0,columnspan=2)
reDraw.rawDat=mat(regTrees.loadDataSet('sine.txt'))
reDraw.testDat=arange(min(reDraw.rawDat[:,0]),
                   max(reDraw.rawDat[:,0]),0.01)
#reDraw(1.0,10)
root.mainloop()