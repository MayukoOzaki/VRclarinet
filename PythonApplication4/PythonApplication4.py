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

# 仮想「息吹き込み検出関数」
# "b"(吹く)が押されていれば 1.0（息の量） / "s"（止める）が押されていれば 0.0（息の量） を返す　
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

# 仮想「」
# ボタンが押されていると、True / 押されていないと False を返す
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

#MiDI読み込み

import pretty_midi

typ = [('mid','*.mid'), ('すべてのファイル','*.*')]
dir = os.path.abspath(os.path.dirname(__file__))+'/../sound'
fle = filedialog.askopenfilename(filetypes = typ, initialdir=dir)


# MIDIファイルのロード
midi_data = pretty_midi.PrettyMIDI(fle)
# トラック別で取得
midi_tracks = midi_data.instruments
# トラック１のノートを取得
notes = midi_tracks[0].notes
for note in notes:
    # ベロシティー、ノートナンバー、
    # ノートオンタイム、ノートオフタイム
    # の順でノート情報が渡される
    # Note(start=50.731117, end=51.406388, pitch=78, velocity=100)
    print(note)


#リアルタイムで時間を図って音符を表示

# 「次の音符」の開始時刻を過ぎたら
#    「次の音符」のピッチを表示
# 「次の音符」の終了時刻が過ぎたら
#    「次の次の音符」を「次の音符」にする
# https://docs.python.org/ja/3/library/time.html

import time

nextnote1 = 0  # 次の Note のインデックス(見本)
nextnote2 = 0  # 次の Note のインデックス（演奏）
starttime = time.time()  #現在時刻
t = 0
out=1          # 出力されたかどうか
breath_old = 0 # 直前に息が吹き込まれていたか

while t < notes[-1].end  :
    t = time.time() - starttime # 演奏時間(現在時刻-演奏開始時刻)

    # キーが押されていたら次の音符を出す
    if is_pressed == True:
        print(notes[nextnote2].pitch)
        nextnote2+=1

    # 見本
    if t>notes[nextnote1].start:
        if out==1:
            print(notes[nextnote1].pitch) #音を鳴らす
            out=0
    if t>notes[nextnote1].end:
        nextnote1+=1
        out=1
       






"""今吹き込まれていて、直前が吹き込まれていなければ、次の音符を出し始め
    # 直前が吹き込まれていて、今吹き込まれていなければ、音止める
    # # キーが押されていたら次の音符を出す
    breath_now = get_breath_speed(breath_old)
    if breath_now > 0:
        if breath_old == 0:
            print(notes[nextnote2].pitch)
        if breath_now == 0:
        if breath_old >0:
            print(0)
            nextnote2+=1
    breath_old = breath_now """


"""
やること
・採点（区分求積法）
・ブレス
息の
"""