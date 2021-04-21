import serial
import struct 
import matplotlib.pyplot as plt

ser = serial.Serial("COM4",115200,timeout = 1.0)
reply = ser.readline()
#print(reply)
#print(type(reply)) byte
reply=reply.decode()
#print(type(reply)) str
print(reply)
ser.close()

import time

plt.plot(t,reply,label="signal")
plt.show()










#bre_ave=sum(replyli)/len(replyli)
#bre.append(bre_ave)

"""bre=[]
for a in range(0,10):
   bre_ele=replylist[0+(23*a)-4:4+(23*a)] #23個ずつ取り出す0.1秒
   bre_ave=sum(bre_ele)/len(bre_ele) #平均をとる
   bre.append(bre_ave)
t=[ 0.1*i for i in range(len(bre)]
plt.plot(t,bre,label="signal")
plt.show()
"""



# starttime = time.time()  #現在時刻
#  t = time.time() - starttime # 演奏時間(現在時刻-演奏開始時刻)
#  for a in range(0,10):
#  bre_ele=replylist[0+(5*a):4+(5*a)] #5個ずつ取り出す0-4 5-9 10-14
#  bre_ave=sum(bre_ele)/len(bre_ele) #平均をとる
#  bre.append(bre_ave)
