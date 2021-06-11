import wave
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog


import os

typ = [('wav','*.wav'), ('すべてのファイル','*.*')]
dir = os.path.abspath(os.path.dirname(__file__))+'/../sound'
fle = filedialog.askopenfilename(filetypes = typ, initialdir=dir)

#wavファイルの読み込みとnumpy化
wave_file = wave.open(fle,"rb") 
x = wave_file.readframes(wave_file.getnframes()) 
x = np.frombuffer(x, dtype= "int16") #int16:16ビットの符号付整数
x = x[::2] #ステレオ

#print(x[0])
#print(len(x))

#dbに変換する関数(デシベルに変換)
def to_db(x, N):
    pad = np.zeros(N//2) #0で埋められた配列
    pad_data = np.concatenate([pad, x, pad])    #配列を結合
    rms = np.array([np.sqrt((1/N) * np.sum(np.square(pad_data[i:i+N]))) for i in range(0,len(x),N)]) #二乗平均平方根 Root Mean Square 実効値
    return 20 * np.log10(rms)

N = 1024     #1024サンプル
#N = 1764     #1764サンプル
#N = 2205     #2205サンプル
#N = 3528     #3528サンプル
#N = 4410     #4410サンプル


db = to_db(x[int(44100*0):int(44100*197)], N)      #2分
#db = to_db(x[int(44100*47):int(44100*80)], N)　　#4分
#db = to_db(x[int(44100*80):int(44100*95)], N)　　#8分
#db = to_db(x[int(44100*95):int(44100*128)], N)　 #16分
#db = to_db(x[int(44100*128):int(44100*175)], N)  #4分、8分、付点4分、2分
#db = to_db(x[int(44100*175):int(44100*197)], N)　#4分、2分


#1サンプル(1/44100)[s] 
#1024=0.02s　
#1764=0.04s
#2205=0.05s
#3528=0.08s
#4410=0.1s
#7056=0.16s　　
#サンプルレート:時間軸で見た音の解像度のこと。
#https://masatsumu-dtm.com/word_36-sample_rate/

sr = 44100
t = np.arange(0, db.shape[0]/sr, 1/sr) 
#等差数列　np.arange(初、終、差)
#db.shape:dbの配列の形状を確認できる。


#plt.plot(t, db, label='signal')
#plt.show()

def smoothing(input, window):
    output = []
    for i in range(0, input.shape[0], window*2+2):
        if i < window:
            output.append(np.average(input[:i+window+1])) 
        elif i > input.shape[0] - 1 - window:
            output.append(np.average(input[i:]))
        else:
            output.append(np.average(input[i-window:i+window+1]))
            # 対象データの前４個、後５個をとることで、全部で１０個
    return np.array(output)
print(min(db))
print(max(db))
smoothed_db = smoothing(db, 4) #平均値 10 個

#print(len(smoothed_db))

t = [ 0.233*i for i in range(len(smoothed_db)) ]

print(max(smoothed_db))
print(min(smoothed_db))
plt.plot(t, smoothed_db, label='signal')
plt.show()



#00:00～00:47
#00:47～01:20
#01:20～01:35
#01:35～02:08
#02:08～02:55
#02:55～03:17
