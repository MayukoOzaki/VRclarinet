import serial
import struct 
import matplotlib.pyplot as plt
import numpy as np
import time
ser = serial.Serial("COM4",115200,timeout = 1.0)
fig, ax = plt.subplots(1, 1) # 描画領域を取得

starttime = time.time() #開始時刻
reply_l=[] #流量データ
t_l=[] #演奏時間


while True:
    reply = ser.readline() #byte
    ser.reset_input_buffer()
    t = time.time() - starttime# 演奏時間(現在時刻-演奏開始時刻)
    try:
        reply=reply.decode() #str
        reply=int(reply) #int 
    except:
        continue 
   # print(reply)
    if 909<reply:
        reply=0
    else:
        reply=(-43/46)*reply
    reply_l.append(reply) #reply_lに追加
    if len(reply_l)==101: #reply_lが11以上だったら1番目を消す
        del reply_l[0]
    
    t_l.append(t)#演奏時間をt_lに追加
    if len(t_l)==101: #t_lが11以上だったら1番目を消す
        del t_l[0]
    
    ax.set_xlim(t_l[0], t_l[-1])#横軸の範囲指定
    line,= ax.plot(t_l,reply_l, color='blue')#描写する

    plt.pause(0.001)#待ち時間
    line.remove()#消去

