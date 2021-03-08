
import wave
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog

typ = [('すべてのファイル','*.*')] 
dir = 'C:\\pg'
fle = filedialog.askopenfilename(filetypes = typ, initialdir = dir) 

#wavファイルの読み込みとnumpy化
wave_file = wave.open(fle,"rb") 
x = wave_file.readframes(wave_file.getnframes()) 
x = np.frombuffer(x, dtype= "int16") #int16:16ビットの符号付整数

print(x[0])
print(len(x))

#dbに変換する関数(デシベルに変換)
def to_db(x, N):
    pad = np.zeros(N//2) #0で埋められた配列
    pad_data = np.concatenate([pad, x, pad])    #配列を結合
    rms = np.array([np.sqrt((1/N) * (np.sum(pad_data[i:i+N]))**2) for i in range(0,len(x),N)]) #二乗平均平方根 Root Mean Square 実効値
    return 20 * np.log10(rms)


N = 882  # 44100*2 samples / sec. 882 サンプルは 0.01[s] の平均音圧レベルに相当 #1024サンプル
db = to_db(x[int(44100*80):int(44100*180)], N)
#1サンプル(1/44100)[s] 
#約0.02秒の幅で音量を算出 1024/44100
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
    for i in range(0, input.shape[0], window*2):
        if i < window:
            output.append(np.average(input[:i+window+1])) 
        elif i > input.shape[0] - 1 - window:
            output.append(np.average(input[i:]))
        else:
            output.append(np.average(input[i-window:i+window+1]))
            # 対象データの前４個、後５個をとることで、全部で１０個
    return np.array(output)

smoothed_db = smoothing(db, 4) # 10 サンプルの中央値をとることで、0.1[s] ごとの平滑化されたデータにする
t = [ 0.1*i for i in range(len(smoothed_db)) ]


plt.plot(t, smoothed_db, label='signal')
plt.show()



#00:00～00:42
#00:42～01:08
#01:08～