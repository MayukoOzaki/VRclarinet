import serial
import struct 

ser = serial.Serial("COM4",115200,timeout = 0.1)
b_reply = ser.read(23) 
#b_reply = ser.read_all()

print(b_reply)
#reply =struct.unpack('23B',b_reply)
reply=b_reply.decode()
print(reply)
ser.close()
#reply=list(reply)
reply=reply.split("\r\n")
print(reply)
replyli=list(reply)


import time

starttime = time.time()  #現在時刻
t = time.time() - starttime # 演奏時間(現在時刻-演奏開始時刻)
for a in range(0,10):
    bre_ele=replylist[0(+a*5)-4:4+(5*a)] #5個ずつ取り出す0-4 5-9 10-14
    bre_ave=sum(bre_ele)/len(bre_ele) #平均をとる




plt.plot(t, label='signal')
plt.show()

       

    
    



