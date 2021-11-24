import subprocess
import cv2
import numpy as np



#画面録画
#fps = 30
# 録画する動画のフレームサイズ（webカメラと同じにする）
#size = (1920, 1080)
# 出力する動画ファイルの設定
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#video = cv2.VideoWriter('output.avi', fourcc, fps, size)


#mat = cv2.imread(r"C:\Users\mayuk\Documents\stolip.png")
#cv2.imshow("image", mat)
#cv2.waitKey()

#print("a")


cap = cv2.VideoCapture(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 646) # カメラ画像の横幅を1280に設定
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 484) # カメラ画像の縦幅を720に設定

avg=None

# 閾値の設定
#threshold = 100


p = 312664  # 2073600


while(True):
    
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    data1 = gray.copy().astype("float")
    data1 = np.asarray(data1)
    #print(data1)
    data1 = data1.flatten()  # 元データ
    #print(data1)

    # コントラストストレッチ
    #gray1 = cv2.equalizeHist(gray)

    # 二値化(閾値100を超えた画素を255にする。)
    #ret, gray2 = cv2頂点頂点hreshold(gray1, threshold, 255, cv2.THRESH_BINARY)
    # 細線化 THINNING_ZHANGSUEN
    #skeleton1 = cv2.ximgproc.thinning(gray2, thinningType=cv2.ximgproc.THINNING_GUOHALL )
    #skeleton1 = cv2.dilate(gray2, None, iterations=5)
    #skeleton1 = cv2.ximgproc.thinning(skeleton1, thinningType=cv2.ximgproc.THINNING_GUOHALL )

    # 前フレームを保存
  

    if avg is None:

        #print("b")
        avg = gray.copy().astype("float")
        base = np.asarray(avg)
        #print(base)
        base=base.flatten()#元データ
        #print(base)
        
        
        basedata=[]#移動平均
        basetop=[]#頂点位置
        x=[0,0,0,0,0]
        num=-2
        b=0
        for a in range(p+2):
            num+=1
            iti=b%5
            if num == p-2 or num == p-1:  # 最後の２つ
                x[iti]=0
            else:  # 通常
                x[iti] = base[a] #通常
            
            if num==0 or num==1:#始めの二つ
                d=sum(x)/(iti+1)
                basedata.append(d)
            elif num == p-2 :#最後の２つ
                #print(iti)
                d=sum(x)/4
                basedata.append(d)
            elif num == p-1:
                d = sum(x)/3
                basedata.append(d)
            elif num>1: #通常
                d=sum(x)/5
                basedata.append(d)
            b+=1
        
        count=1
        start=0
        before=-999999
        trend=0 #上がっていたら１下がっていたら０

        for e in range(p):
            now = basedata[e]

            if before==now:
                count+=1
            elif before>now:
                if trend==1:
                    if count>1:
                        if (start+e-1)/2 >= 3 and (start+e-1)/2<=(p-1)-3:
                            basetop.append((start+e-1)/2)
                    else:
                        if e-1 >= 3 and e-1 <= (p-1)-3:
                            basetop.append(e-1)
                trend = 0
                count = 1
                start = 0
            elif before < now:
                trend = 1
                count = 1
                start = e

                        
            before=now 
        """    
        ql=[]
        qi=[]
        for q in range(len(basetop)-1):
            qq=basetop[q+1]-basetop[q]
            if qq==18:
                qi.append(q)
            ql.append(qq)
        #print(qi)
        print(set(ql))

        rl=[]
        for r in range(len(qi)-1):
            rr = qi[r+1]-qi[r]     
            rl.append(rr)
        print(set(rl))
         """

        #print(basedata[0:101])
        print(basetop)   
        continue


    #print(basedata)
    #print(basetop)

    cv2.imshow("image2", avg)

    

    x = [0, 1, 2, 3, 4, 5, 6]
    toplist = []

    for top in basetop:
        top=int(top)
        if top<=3:
            y=data1[:7]
        elif top>=(p-1)-3:
            y=data1[(p-1)-6:]
        else:
            y=data1[top-3:top+4]
        z = np.polyfit(x, y, 2)
        d = (-z[1]) / (2 * z[0])
    
        if top <= 3:
            toplist.append(d)
        elif top >= (p-1)-3:
            toplist.append(d+(p-1)-6)
        else:
            toplist.append(d+top-3)

    #print(toplist)

    key = cv2.waitKey(1)
    if key == 27:
        break

    # 現在のフレームと移動平均との間の差を計算する
    # accumulateWeighted関数の第三引数は「どれくらいの早さで以前の画像を忘れるか」。小さければ小さいほど「最新の画像」を重視する。
    # http://opencv.jp/opencv-2svn/cpp/imgproc_motion_analysis_and_object_tracking.html
    # 小さくしないと前のフレームの残像が残る
    # 重みは蓄積し続ける。
    
    #cv2.imshow("image2",  cv2.convertScaleAbs(avg))#前

    #frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))#差
    #frameDelta_diff = cv2.absdiff(skeleton1, cv2.convertScaleAbs(avg))  # 差

    #alpha = 1000  # コントラスト項目
    #beta = 0    # 明るさ項目
    #frameDelta1 = cv2.convertScaleAbs(frameDelta, alpha=alpha, beta=beta)
    #cv2.accumulateWeighted(gray, avg, 0.9999)



    #cv2.imshow("image1", frameDelta1)#差
    #cv2.imshow("image2", avg)

    #cv2.imshow("now", gray)#今
    #cv2.imshow("Contrast_Stretch", gray1)#コントラストストレッチ
    #cv2.imshow("binarization", gray2)#2値化
    #cv2.imshow("fibrillation", skeleton1)# 細線化
    #cv2.imshow("diff", frameDelta_diff)#差
    
    #video.write(gray)  # 画面録画
    #key = cv2.waitKey(1)
    #if key == 27:
    #    break


#cap.release()
#video.release()
#cv2.destroyAllWindows()



#print(moving_average(data, 4))