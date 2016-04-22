#coding:utf-8
import socket
import sys
import  binascii
import struct
import wxversion
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
wxversion.select('3.0')
selectedMac=[]

key='\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
iv='\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
#import wx
def strconvert(s):
    s=str(s).strip().split(' ')
    my=r'\x'
    fin=''
    for i in range(len(s)):
        fin=fin+struct.pack('B',int(s[i],16))
    return fin
def ipToBroadcast(ip):
    ipList=ip.split('.')
    retstr=''
    ipList[3]='255'
    for i in range(3):
        retstr+=ipList[i]
        retstr+='.'
    return retstr+ipList[3]

def md5(str):
    import hashlib
    m = hashlib.md5()
    m.update(str)
    return m.digest()
def encode_AES128(text):
    mode=AES.MODE_CBC
    cryptor = AES.new(key,mode,iv)
    #这里密钥key 长度必须为16（AES-128）,
    #24（AES-192）,或者32 （AES-256）Bytes 长度
    #目前AES-128 足够目前使用
    length = 16
    count = len(text)
    print count,len(text)
    if count < length:
        add = (length-count)
        #\0 backspace
        text = text + ('\x00' * add)
    elif count > length:
        add = (length-(count % length))
        text = text + ('\x00' * add)
    #print add,len(text)
    print b2a_hex(text)
    ciphertext = cryptor.encrypt(text)
    #因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
    #所以这里统一把加密后的字符串转化为16进制字符串
    print b2a_hex(ciphertext)
    return ciphertext
socketList=[]
data_send='03 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'
def broadCast():
    localIP = socket.gethostbyname(socket.gethostname())#这个得到本地ip
    print localIP
    myname = socket.getfqdn(socket.gethostname(  ))
    #获取本机ip
    myaddr = socket.gethostbyname(myname)
    broadCastAddr=ipToBroadcast(localIP)
    print broadCastAddr
    dest=(broadCastAddr,20131)
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    #s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
    s.bind(('',0))

    import  time
    try:
        print strconvert(data_send)
        s.sendto(strconvert(data_send),dest)
    except socket.error,e:
        print e

    dataDisplay=[]
    while 1:
        s.settimeout(5)
        try:
            data,addr= s.recvfrom(2048)
        except:
            print 'error'
            break
        info={}
        print "data is"
        curList=''
        for i in range(14,20):
            curList+=binascii.b2a_hex(data[i])
        info['mac']=curList
        info['addr']=addr
        dataDisplay.append(curList)
        socketList.append([info])

    for i in range(len(socketList)):
        print [socketList[i][0]['mac']]
        frame.m_listCtrl1.Append([socketList[i][0]['mac']])

def toggleSocket():
    print 'mac is'
    selectedMac=frame.selectedMac
    togglgData='09'+'01'+'01'+'00'*11+selectedMac[0]['mac']
    togglgDataSplit=' '.join(togglgData[i]+togglgData[i+1] for i in range(0,len(togglgData),2))
    head=togglgDataSplit
    str=md5(strconvert(togglgDataSplit))
    dataSendToSocket=strconvert(head)+encode_AES128(str+'\x01')
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.sendto(dataSendToSocket,selectedMac[0]['addr'])
    data,addr= sock.recvfrom(1024)
    sock.close()







###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.dataview

###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1 ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 800,400 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

		gSizer1 = wx.GridSizer( 2, 1, 0, 0 )

		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gSizer2 = wx.GridSizer( 1, 2, 0, 0 )

		self.m_panel4 = wx.Panel( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.refresh = wx.Button( self.m_panel4, wx.ID_ANY, u"refresh", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.refresh, 0, wx.ALL, 5 )

		self.stop = wx.Button( self.m_panel4, wx.ID_ANY, u"stop", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.stop, 0, wx.ALL, 5 )

		self.m_listCtrl1 = wx.ListCtrl( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.Size(100,200), wx.LC_ICON )

		fgSizer1.Add( self.m_listCtrl1, 0, wx.ALL, 5 )

		self.ok = wx.Button( self.m_panel4, wx.ID_ANY, u"ok", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.ok, 0, wx.ALL, 5 )

		self.m_dataViewCtrl2 = wx.dataview.DataViewCtrl( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_dataViewCtrl2, 0, wx.ALL, 5 )


		self.m_panel4.SetSizer( fgSizer1 )
		self.m_panel4.Layout()
		fgSizer1.Fit( self.m_panel4 )
		gSizer2.Add( self.m_panel4, 1, wx.EXPAND |wx.ALL, 5 )

		fgSizer2 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.toggle = wx.Button( self.m_panel1, wx.ID_ANY, u"on/off", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.toggle, 0, wx.ALL, 5 )

		self.m_button12 = wx.Button( self.m_panel1, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.m_button12, 0, wx.ALL, 5 )

		self.m_button13 = wx.Button( self.m_panel1, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.m_button13, 0, wx.ALL, 5 )

		self.m_button14 = wx.Button( self.m_panel1, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.m_button14, 0, wx.ALL, 5 )


		gSizer2.Add( fgSizer2, 1, wx.EXPAND, 5 )


		self.m_panel1.SetSizer( gSizer2 )
		self.m_panel1.Layout()
		gSizer2.Fit( self.m_panel1 )
		gSizer1.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 5 )

		self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		self.m_notebook1 = wx.Notebook( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		bSizer2.Add( self.m_notebook1, 1, wx.EXPAND |wx.ALL, 5 )


		self.m_panel2.SetSizer( bSizer2 )
		self.m_panel2.Layout()
		bSizer2.Fit( self.m_panel2 )
		gSizer1.Add( self.m_panel2, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( gSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.refresh.Bind( wx.EVT_BUTTON, self.refreshOnButtonClick )
		self.stop.Bind( wx.EVT_BUTTON, self.stopOnButtonClick )
		self.ok.Bind( wx.EVT_BUTTON, self.okOnButtonClick )
		self.toggle.Bind( wx.EVT_BUTTON, self.toggleOnButtonClick )


	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def refreshOnButtonClick( self, event ):
         broadCast()
         event.Skip()

	def stopOnButtonClick( self, event ):
		event.Skip()

	def okOnButtonClick( self, event ):
         selectedIndex=self.m_listCtrl1.GetFirstSelected()
         self.selectedMac=socketList[self.m_listCtrl1.GetFirstSelected()]
         print self.selectedMac[0]['addr']
         event.Skip()

	def toggleOnButtonClick( self, event ):
         toggleSocket()
         event.Skip()

app = wx.App(False)
frame = MyFrame1(None)
frame.Show(True)
#start the applications
app.MainLoop()


