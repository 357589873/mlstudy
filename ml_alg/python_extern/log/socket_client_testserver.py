#coding:utf-8
import socket
import sys
import  binascii
HOST='182.92.79.42'
PORT=6666
BUFFER=1024
message='\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02'
sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#sock.connect((HOST,PORT))
import time
while(1):
    try :
        #Set the whole string
        sock.sendto(message,(HOST,PORT))
    except socket.error,e:
        #Send failed
        print 'Send failed'
        print e,sys.exc_info()[0],sys.exc_info()[1]
        sys.exit()
    data,addr= sock.recvfrom(BUFFER)
    print int(binascii.b2a_hex(data[8]),16),'月',int(binascii.b2a_hex(data[9]),16),"日 星期",int(binascii.b2a_hex(data[10]),16),\
    int(binascii.b2a_hex(data[11]),16),'点',int(binascii.b2a_hex(data[12]),16)
    #print int(data[7:13],2),addr
    time.sleep(30)
sock.close()