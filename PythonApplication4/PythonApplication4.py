import serial
import struct 
import matplotlib.pyplot as plt
import numpy as np
import time


starttime = time.time() #開始時刻
reply_l=[] #流量データ
t_l=[] #演奏時間


while True:
    import time
    ser = serial.Serial("COM4",115200,timeout = 1.0)
    reply = ser.readline() #byte
    t = time.time() - starttime# 演奏時間(現在時刻-演奏開始時刻
    reply=reply.decode() #str
    reply=int(reply) #int 
    print(reply)     
    ser.close()

    reply_l.append(reply) #reply_lに追加
    if len(reply_l)==11: #reply_lが11以上だったら1番目を消す
        del reply_l[1]
    
    t_l.append(t)#演奏時間をt_lに追加
    if len(t_l)==11: #t_lが11以上だったら1番目を消す
        del t_l[1]



    fig, ax = plt.subplots(1, 1) # 描画領域を取得
    line, = ax.plot(t_l[-1],reply_l[-1] , color='blue') #t_l,reply_lの最後尾を描写する
    plt.pause(0.01)
    line.remove()

   # plt.plot(t,reply,label="signal")
   # plt.show()










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
