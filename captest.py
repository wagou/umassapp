import cv2
import numpy as np

# 画像読み込み&トリミング
frame = cv2.imread("cap22.png")
# height, width, channels = frame.shape[:3]
# if height > width * 16 / 9:
# 	frame = frame[(height//2-width*8//9):(height//2+width*8//9),:]
# frame = cv2.resize(frame,(1080,1920))
# cv2.imwrite("resized.png", frame)
# 座標特定
temp1 = cv2.imread("detail.png", 0)
temp2 = cv2.imread("close.png", 0)
#比較方法はcv2.TM_CCOEFF_NORMEDを選択
result1 = cv2.matchTemplate(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), temp1, cv2.TM_CCOEFF_NORMED)
result2 = cv2.matchTemplate(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), temp2, cv2.TM_CCOEFF_NORMED)
#類似度の設定(0~1)
threshold = 0.9
loc1 = ()
loc2 = ()
#検出結果から検出領域の位置を取得
loc1 += np.where(result1 >= threshold)
loc2 += np.where(result2 >= threshold)
for top_left in zip(*loc1[::-1]):
	print(top_left)
print(loc1[0][0],loc1[1][0])
print(loc2[0][0],loc2[1][0])
