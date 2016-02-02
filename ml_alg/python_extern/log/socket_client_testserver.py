#coding:utf-8
import socket
import sys
import  binascii
import struct
HOST='182.92.79.42'
PORT=7777
BUFFER=1024
test_str='00 00 00 00 00 00 00 00 00 00 00 00 00 00 1a fe 34 f7 5f 3f'
message_heart_5f3f='\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1a\xfe\x34\xf7\x5f\x3f'
message='\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02'
message_open='\x09\x01\xa5\x13\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1a\xfe\x34\xf7\x5f\x3f\x02\x6c\x12\x67\x01\xec\x65\x6e\x15\xc6\x7e\x68\x18\x5a\xec\x4d\xc3\x55\x49\xed\xae\xca\xf0\xed\xd2\xfe\x38\xce\x12\xc9\x94\x7f'
message_close=''
message_queryinfo='\x19\x01\xa5\x13\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1a\xfe\x34\xf7\x5f\x3f\xd9\x0d\x62\xb8\xac\x20\xa7\xc9\xfe\x34\xab\xf8\x3d\xa6\xa9\x66'
message_queryinfo1='\x1b\x01\xa5\x13\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1a\xfe\x34\xf7\x5f\x3f\x3b\x1a\xc7\x31\x0d\xef\xdb\x18\x46\x50\xc2\xfd\x1d\x39\xec\xff'
def strconvert(s):
    s=str(s).strip().split(' ')
    my=r'\x'
    fin=''
    for i in range(len(s)):
        fin=fin+struct.pack('B',int(s[i],16))
    return fin
sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#sock.connect((HOST,PORT))
import time
while(1):
    try :
        #Set the whole string
        print strconvert(test_str)
        sock.sendto(strconvert(test_str),(HOST,PORT))
    except socket.error,e:
        #Send failed
        print 'Send failed'
        print e,sys.exc_info()[0],sys.exc_info()[1]
        sys.exit()
    data,addr= sock.recvfrom(BUFFER)
    print int(binascii.b2a_hex(data[8]),16),'月',int(binascii.b2a_hex(data[9]),16),"日 星期",int(binascii.b2a_hex(data[10]),16),\
    int(binascii.b2a_hex(data[11]),16),'点',int(binascii.b2a_hex(data[12]),16)
    time.sleep(3)
'''
    while(1):
        data,addr= sock.recvfrom(BUFFER)
        for i in range(len(data)):
            print binascii.b2a_hex(data[i]),
        print
    print int(binascii.b2a_hex(data[8]),16),'月',int(binascii.b2a_hex(data[9]),16),"日 星期",int(binascii.b2a_hex(data[10]),16),\
    int(binascii.b2a_hex(data[11]),16),'点',int(binascii.b2a_hex(data[12]),16)
    #print int(data[7:13],2),addr
    #time.sleep(3)'''
sock.close()