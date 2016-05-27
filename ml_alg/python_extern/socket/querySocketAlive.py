#coding:utf-8
#第三方发送控制命令到服务器。
import socket
import sys
import  binascii
import struct
import urllib2, urllib
HOST='182.92.79.42'
PORT=7777
numberErr=0

BUFFER=1024
test_str_on='62 11 22 33 44 55 66 77 88 00 00 00 00 00 20 59 a0 78 82 14 03 1a fe 34 f7 55 25 1a fe 34 f7 55 24 1a fe 34 f7 55 2f'
normalStr='6C 11 22 33 44 55 66 77 88 00 00 00 00 00 20 59 a0 78 82 14 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'
def strconvert(s):
    s=str(s).strip().split(' ')
    my=r'\x'
    fin=''
    for i in range(len(s)):
        fin=fin+struct.pack('B',int(s[i],16))
    return fin
sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
import time
while(1):
    try :
        #Set the whole string
        sock.sendto(strconvert(test_str_on),(HOST,PORT))
    except socket.error,e:
        #Send failed
        print 'Send failed'
        print e,sys.exc_info()[0],sys.exc_info()[1]
        #sys.exit()
    try:
        print "recvfrom"
        data,addr= sock.recvfrom(BUFFER)
        print "afterecv"
        for i in range(len(data)):
            print binascii.b2a_hex(data[i]),
        print
        numberErr=0
    except socket.error,e:
        print "timedelay....numnerErr =" ,numberErr
        numberErr+=1

        if numberErr==10:
            sys.exit()
    time.sleep(30)
    print "again"
sock.close()