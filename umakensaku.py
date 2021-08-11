import cv2
import numpy as np
from time import sleep

# frame = cv2.imread("template.png", 0)[194:894,328:428]
# frame2 = cv2.imread("template.png", 0)[194:894,1228:1328]
# frame = cv2.imread("cap7.png", 0)
# for i in range(10):
#     temp = cv2.imread("{}.png".format(i), 0)
#     #比較方法はcv2.TM_CCOEFF_NORMEDを選択
#     result = cv2.matchTemplate(frame, temp, cv2.TM_CCOEFF_NORMED)
#     #類似度の設定(0~1)
#     threshold = 0.9
#     loc = ()
#     #検出結果から検出領域の位置を取得
#     loc += np.where(result >= threshold)
#     print(loc)
#     #検出領域を四角で囲んで保存
#     result = cv2.imread("cap4.png")
#     w, h = temp.shape[::-1]
#     for top_left in zip(*loc[::-1]):
#         # top_left = (top_left[0] + 328, top_left[1] + 194)
#         bottom_right = (top_left[0] + w, top_left[1] + h)
#         cv2.rectangle(result,top_left, bottom_right, (255, 0, 0), 2)
#     cv2.imwrite("result{}.png".format(i), result)
frame = cv2.imread("cap7.png", 0)[70:120,420:670]
cv2.imwrite("detail.png",frame)
frame = cv2.imread("cap22.png", 0)
temp = cv2.imread("db/A.png", 0)
#比較方法はcv2.TM_CCOEFF_NORMEDを選択
result = cv2.matchTemplate(frame, temp, cv2.TM_CCOEFF_NORMED)
#類似度の設定(0~1)
threshold = 0.9
loc = ()
#検出結果から検出領域の位置を取得
loc += np.where(result >= threshold)
print(loc[0][0],loc[1][0])
#検出領域を四角で囲んで保存
result = cv2.imread("cap22.png")
w, h = temp.shape[::-1]
for top_left in zip(*loc[::-1]):
    # top_left = (top_left[0] + 328, top_left[1] + 194)
    bottom_right = (top_left[0] + w, top_left[1] + h)
    print(top_left)
    cv2.rectangle(result,top_left, bottom_right, (255, 0, 0), 2)
cv2.imwrite("result.png", result)