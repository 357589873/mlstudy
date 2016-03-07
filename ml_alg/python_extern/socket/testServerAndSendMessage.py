#coding:utf-8
#监测服务器，如果服务器挂掉，就发送短信。
import socket
import sys
import  binascii
import struct
import urllib2, urllib
HOST='182.92.79.42'
PORT=6666
numberErr=0
data = {'account':'cf_shsqxx','password':'shsqxx@123','mobile':'18910107026','content':"您的验证码是：服务器挂了。请不要把验证码泄露给其他人。"}

BUFFER=1024
test_str='00 00 00 00 00 00 00 00 00 00 00 00 00 00 1a fe 34 f7 5f 3f'
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
        sock.sendto(strconvert(test_str),(HOST,PORT))
    except socket.error,e:
        #Send failed
        print 'Send failed'
        print e,sys.exc_info()[0],sys.exc_info()[1]
        #sys.exit()
    try:
        print "recvfrom"
        data,addr= sock.recvfrom(BUFFER)
        print "afterecv"
        print int(binascii.b2a_hex(data[8]),16),'月',int(binascii.b2a_hex(data[9]),16),"日 星期",int(binascii.b2a_hex(data[10]),16),\
            int(binascii.b2a_hex(data[11]),16),'点',int(binascii.b2a_hex(data[12]),16)
        numberErr=0
    except socket.error,e:
        print "timedelay....numnerErr =" ,numberErr
        numberErr+=1

        if numberErr==10:
            f=urllib2.urlopen(url="http://106.veesing.com/webservice/sms.php?method=Submit",data=urllib.urlencode(data))
            print f.read()
            sys.exit()
    time.sleep(3)
    print "again"
sock.close()