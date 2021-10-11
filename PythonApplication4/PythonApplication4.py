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
import serial
import winsound

import pygame
import pygame.midi

nextnote1 = 0  # 次の Note のインデックス(見本)
nextnote2 = 0  # 次の Note のインデックス（演奏）
starttime = time.time()  #現在時刻
t = 0
out=1          # 出力されたかどうか
breath_old=False  # 直前に息が吹き込まれていたか

ser = serial.Serial("COM3",115200,timeout = 1.0)

pygame.midi.init()
print("a")
player = pygame.midi.Output(0)
print(player)
player.set_instrument(72)
ch1=1  #今のチャンネル
ch2=0  #前のチャンネル
ve1=0  #今のベロシティー
ve2=50  #前のベロシティー
sa=0
while True:
    reply = ser.readline() #byte
    ser.reset_input_buffer()
    try:
        reply=reply.decode() #str
        reply=int(reply) #int 
    except:
        continue

    print(reply)
    
    t = time.time() - starttime # 演奏時間(現在時刻-演奏開始時刻)
    breath_now =  breath_detection(reply)
    #print(breath_now,breath_old)
    if breath_now == True and breath_old==False: 
        while t>notes[nextnote2].end:
            if nextnote2<len(notes)-1: #notesの範囲の一つ手前であればnextnoteを増やす
                nextnote2+=1
            else:
                break
        #print(nextnote2,notes[nextnote2].pitch)
        pi=notes[nextnote2].pitch
        print(pi)
        #ve1=1000-reply
        ve1=1.97*(1000-reply)-160.62
        if ve1>127:
            ve1=127    
        sa=ve1-ve2
        zouka=sa*0.1
        print("ve1",ve1,"sa",sa)
        salist=[]
        for a in range(10):
            salist.append(int(ve2+zouka))
            #salist.append(int(sa+zouka))
            ve2=int(ve2+zouka)
            #sa=sa+zouka 
        print(salist)
        for b in salist:
            print(b)
            ve1=b
            player.set_instrument(72,ch1%3)
            print("start",ch1%3,ve1)
            player.note_on(pi, ve1,ch1%3) 
            time.sleep(0.001)
            print("stop",ch2%3,ve2)
            player.note_off(pi,ve2,ch2%3)
            time.sleep(0.01)
            ch2=ch1
            ch1+=1
            ve2=ve1
           
        
    elif breath_now == False and breath_old==True:#音を止めて次の音に切り替える
        player.note_off(pi,ve2,ch2%3)
        ve2=0
        nextnote2+=1


    elif breath_now == True and breath_old==True:
        ve1=1000-reply     
        sa=ve1-ve2
        zouka=sa*0.1
        salist=[]
        for a in range(10):
            salist.append(int(ve2+zouka))
            #salist.append(int(sa+zouka))
            ve2=int(ve2+zouka)
            #sa=sa+zouka
        print(salist)
        for b in salist:
            print(b)
            ve1=b
            player.set_instrument(72,ch1%3)
            print("start",ch1%3,ve1)
            player.note_on(pi, ve1,ch1%3)
            time.sleep(0.001)
            print("stop",ch2%3,ve2)
            player.note_off(pi,ve2,ch2%3)
            time.sleep(0.01)
            ch2=ch1
            ch1+=1
            ve2=ve1
    breath_old = breath_now 
  


   #もし、ボタンで切替or息を吹き始めた際に、次の音の演奏時間内であるかを確認、範囲外(後)であれその次の音を確認する。
   #さらに過ぎていた場合これを繰り返す
   #もし、ボタンで切替or息を吹き始めた際に、次の音の演奏時間内であるかを確認、範囲外(前)であれば、そのまま演奏。


   #やること
   #・音が高くなる程流量増える



  
   
   
"""
# 仮想「息吹き込み検出関数」
# # "b"(吹く)が押されていれば 1.0（息の量） / "s"（止める）が押されていれば 0.0（息の量） を返す　
def get_breath_speed(current_speed): 
    breath_speed = current_speed
    if msvcrt.kbhit():
        ch = msvcrt.getch()
        print(ch)
        if ch==b'b': 
            breath_speed=1.0
        elif ch==b's': 
            breath_speed=0.0
        else:
            msvcrt.ungetch(ch) #push back
    return breath_speed
"""


"""
# 仮想「」
# # ボタンが押されていると、True / 押されていないと False を返す
def get_switch():
    is_pressed = False
    if msvcrt.kbhit():
        ch = msvcrt.getch()
        print(ch)
        if ch==b' ':            #スペースの場合True 
            is_pressed=True
        else:
            msvcrt.ungetch(ch)  #スペース以外の場合呼び出さなかったことにする
    return is_pressed

# msvcrt.getch() は「この関数呼び出しは読み出し可能な打鍵がない場合にはブロックします」なので、getch() を呼ぶ前に kbhit() が必要
# msvcrt.kbhit()読み出し待ちの打鍵イベントが存在する場合に True を返します。
"""

"""
while t < notes[-1].end  :
    t = time.time() - starttime # 演奏時間(現在時刻-演奏開始時刻)

    # キーが押されていたら次の音符を出す
   # if is_pressed == True:
    #    print(notes[nextnote2])
     #   nextnote2+=1
    # 見本
    if t>notes[nextnote1].start:
        if out==1:
            print("見本",notes[nextnote1].pitch) #音を鳴らす
            out=0
    if t>notes[nextnote1].end:
        nextnote1+=1
        out=1
   """
"""m=notes[nextnote2].pitch
   #print(m)
   fm = (2**((m-69)/12))*440
   #print(fm)
   winsound.Beep(int(fm),500)"""





