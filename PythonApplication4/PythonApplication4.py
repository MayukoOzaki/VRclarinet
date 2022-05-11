import serial
import struct 
import matplotlib.pyplot as plt
from tkinter import filedialog
import msvcrt
import os

#00:00～00:42
#00:42～01:08
#01:08～01:21
#01:21～01:48
#01:48～02:26
#02:26～02:46


low=909
def breath_detection(reply):
    is_blowing = False
    if reply<low:  #1000未満だったら吹いている
         is_blowing=True
    else:
        is_blowing= False
    return is_blowing


#MiDI読み込み

import pretty_midi

typ = [('mid','*.mid'), ('すべてのファイル','*.*')]
dir = os.path.abspath(os.path.dirname(__file__))+'/../sound'
#fle = filedialog.askopenfilename(filetypes = typ, initialdir=dir)
fle=dir+'/prediction03.mid'


# MIDIファイルのロード
midi_data = pretty_midi.PrettyMIDI(fle)
# トラック別で取得
midi_tracks = midi_data.instruments
# トラック１のノートを取得
notes = midi_tracks[0].notes
#for note in notes:
    # ベロシティー、ノートナンバー、
    # ノートオンタイム、ノートオフタイム
    # の順でノート情報が渡される
    # Note(start=50.731117, end=51.406388, pitch=78, velocity=100)
    #print(note)


#リアルタイムで時間を図って音符を表示

# 「次の音符」の開始時刻を過ぎたら
#    「次の音符」のピッチを表示
# 「次の音符」の終了時刻が過ぎたら
#    「次の次の音符」を「次の音符」にする
# https://docs.python.org/ja/3/library/time.html


#今吹き込まれていて、直前が吹き込まれていなければ、次の音符を出し始め
# 直前が吹き込まれていて、今吹き込まれていなければ、音止める

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