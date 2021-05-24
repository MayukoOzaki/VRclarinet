import wave
import numpy as np
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
    #ベロシティー、ノートナンバー、ノートオンタイム、ノートオフタイムの順でノート情報が渡される
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
import serial
import winsound


ser = serial.Serial("COM4",115200,timeout = 1.0)
replylist=[]
while True:
    reply = ser.readline() #byte
    ser.reset_input_buffer()
    try:
        reply=reply.decode() #str
        reply=int(reply) #int 
    except:
        continue
    print(reply)    
    replylist.append(reply)
    if len(replylist)>=1000:
        break
Quantity=len(replylist)
average=sum(replylist)/Quantity #平均
print(average)
deviationlist=[] #偏差
for a in replylist:
    deviation=a-average
    deviationlist.append(deviation)
c=0
for b in deviationlist:
    c+=b**2
SS=c/Quantity #分散
S=SS**0.5 #標準偏差

print("S",S,"SS",SS)
       



   #やること
   #・音が高くなる程流量増える



