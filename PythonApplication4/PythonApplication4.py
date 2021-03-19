import wave
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog

import os



#00:00～00:42
#00:42～01:08
#01:08～01:21
#01:21～01:48
#01:48～02:26
#02:26～02:46


#MiDI

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

nextnote = 0    # 次の Note のインデックス
starttime = time.time()  #現在時刻
t = 0
m=1
while t < notes[-1].end:
    t = time.time() - starttime
    if t>notes[nextnote].start:
        if m==1:
            print(notes[nextnote].pitch)
            m=0
    if t>notes[nextnote].end:
        nextnote+=1
        m=1

#音の出方は息に合わせる

タイミングがずれた場合は
