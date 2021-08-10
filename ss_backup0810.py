import cv2
import numpy as np
from PIL import Image
import pyocr
import re

tools = pyocr.get_available_tools()
tool = tools[0]

frame = cv2.imread("cap6.png")
frames = [frame[520:555,120:210],frame[520:555,320:410],frame[520:555,520:610],frame[520:555,720:810],frame[520:555,920:1010]]
tekiframes = [frame[600:645,365:400],frame[600:645,560:600],frame[660:705,365:400],frame[660:705,560:600],frame[660:705,760:800],frame[660:705,960:995]
	,frame[720:765,365:400],frame[720:765,560:600],frame[720:765,760:800],frame[720:765,960:995]]
skillframe = frame[930:970,110:460]
skillframe2 = frame[930:970,610:960]

Wlist = [110,610]
Hlist = [930,1050,1160,1270,1380,1490,1600]

skillframes = []
for i in range(len(Hlist)):
	for j in range(len(Wlist)):
		skillframes.append(frame[Hlist[i]:Hlist[i]+40,Wlist[j]:Wlist[j]+350])

# cv2.imwrite("sp1.png", frames[0])
# cv2.imwrite("sp2.png", frame2)
# img = cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY)
# th = 140
# img = cv2.threshold(img, th, 255, cv2.THRESH_BINARY)[1]
# cv2.imwrite("target.png",img)

# cap5 = Image.open("cap5.png")
# cap_sp = cap5.crop((114, 520, 210, 555))
# cap_sp2 = cap5.crop((36, 500, 235, 580))
# cap_sp.save('spp.png')
# cap_sp2.save('spp2.png')
# test = Image.open("sp2.png")
# 数字を読み取る
def numres(test):
	res = tool.image_to_string(test,lang="eng",builder=pyocr.builders.TextBuilder(tesseract_layout=6))
	return res
# アルファベット1文字を読み取る
def alphabetres(test):
	res = tool.image_to_string(test,lang="eng",builder=pyocr.builders.TextBuilder(tesseract_layout=6))
	if 'EF' in res:
		res = 'F'
	letter = re.search('[SABCDEFG]',res)
	if letter:
		res = letter.group()
	if '(' in res:
		res = 'C'
	return res
# 文字列を読み取る
def textres(test):
	res = tool.image_to_string(test,lang="jpn",builder=pyocr.builders.TextBuilder(tesseract_layout=6))
	return res
for i in range(5):
	cv2.imwrite("sp{}.png".format(i), frames[i])
	print(numres(Image.open("sp{}.png".format(i))))
for j in range(10):
	# img = cv2.cvtColor(tekiframes[j], cv2.COLOR_BGR2GRAY)
	# th = 140
	# img = cv2.threshold(img, th, 255, cv2.THRESH_BINARY)[1]
	cv2.imwrite("te{}.png".format(j), tekiframes[j])
	res = alphabetres(Image.open("te{}.png".format(j)))
	print(res)
# img = cv2.cvtColor(skillframe, cv2.COLOR_BGR2GRAY)
# th = 140
# img = cv2.threshold(img, th, 255, cv2.THRESH_BINARY)[1]
# cv2.imwrite("sf.png", img)
# print(textres(Image.open("sf.png")))
img = cv2.cvtColor(frame[930:970,505:525], cv2.COLOR_BGR2GRAY)
th = 140
img = cv2.threshold(img, th, 255, cv2.THRESH_BINARY)[1]
cv2.imwrite("lv.png", img)
print(numres(Image.open("lv.png")))
for i in range(len(skillframes)):
	img = cv2.cvtColor(skillframes[i], cv2.COLOR_BGR2GRAY)
	th = 140
	img = cv2.threshold(img, th, 255, cv2.THRESH_BINARY)[1]
	cv2.imwrite("sf{}.png".format(i), img)
	print(textres(Image.open("sf{}.png".format(i))))