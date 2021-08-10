import cv2
import numpy as np
from PIL import Image
import pyocr
import re
from simstring.feature_extractor.character_ngram import CharacterNgramFeatureExtractor
from simstring.measure.cosine import CosineMeasure
from simstring.database.dict import DictDatabase
from simstring.searcher import Searcher

class umamusume:
	def __init__(self, name, status, shiba, dirt, tan, mile, chu, cho, nige, senkou, sashi, oikomi, skills):
		self.name = name
		self.status = status

# SimStringの詳しい使い方が分からないためおそらく冗長になっている
db = DictDatabase(CharacterNgramFeatureExtractor(2))
path = "db/skill.csv"
skills = []
with open(path, encoding='utf-8-sig') as f:
	lines = [s.strip() for s in f.readlines()]
	for words in lines:
		db.add(words.split(',')[0])
		skills.append(words.split(','))
searcher = Searcher(db, CosineMeasure())

db2 = DictDatabase(CharacterNgramFeatureExtractor(2))
db3 = DictDatabase(CharacterNgramFeatureExtractor(2))
path = "db/umamusume.csv"
names = []
with open(path, encoding='utf-8-sig') as f:
	lines = [s.strip() for s in f.readlines()]
	for words in lines:
		db2.add(words.split(',')[0])
		db3.add(words.split(',')[1])
		names.append(words.split(','))
searcher2 = Searcher(db2, CosineMeasure())
searcher3 = Searcher(db3, CosineMeasure())

# ocr準備
tools = pyocr.get_available_tools()
tool = tools[0]

# 画像読み込み&トリミング
frame = cv2.imread("cap11.png")
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

# ステータス読み取り
for i in range(5):
	cv2.imwrite("sp{}.png".format(i), frames[i])
	print(numres(Image.open("sp{}.png".format(i))))

# 適性読み取り
tekisei = []
for j in range(10):
	# img = cv2.cvtColor(tekiframes[j], cv2.COLOR_BGR2GRAY)
	# th = 140
	# img = cv2.threshold(img, th, 255, cv2.THRESH_BINARY)[1]
	cv2.imwrite("te{}.png".format(j), tekiframes[j])
	res = alphabetres(Image.open("te{}.png".format(j)))
	print(res)
	tekisei.append(res)

# 固有レベル読み取り
img = cv2.cvtColor(frame[930:970,505:525], cv2.COLOR_BGR2GRAY)
th = 140
img = cv2.threshold(img, th, 255, cv2.THRESH_BINARY)[1]
cv2.imwrite("lv.png", img)
print(numres(Image.open("lv.png")))

# スキル読み取り
skill = []
for i in range(len(skillframes)):
	img = cv2.cvtColor(skillframes[i], cv2.COLOR_BGR2GRAY)
	th = 140
	img = cv2.threshold(img, th, 255, cv2.THRESH_BINARY)[1]
	cv2.imwrite("sf{}.png".format(i), img)
	skistr = textres(Image.open("sf{}.png".format(i)))
	# print(skistr)
	threshold = 0.5
	count = 0
	preresults = ""
	while count < 50:
		results = searcher.search(skistr, threshold)
		if len(results) == 1:
			break
		elif len(results) == 0:
			threshold -= 0.01
		else:
			preresults = results
			threshold += 0.01
		count += 1
	# 以前候補があって無くなってしまった場合は候補を引き継ぐ
	if len(results) == 0 and len(preresults) > 0:
		results = preresults
	# 個別対応
	if len(re.findall('全',skistr)) == 2:
		results = ['全身全霊']
	if len(re.findall('機応',skistr)) > 0:
		results = ['臨機応変']
	# 〇と◎で両方ヒットした場合、〇とする
	if len(results) == 2 and results[0][:-1] == results[1][:-1]:
		results = [results[0][:-1]+'〇']
	# print(results)
	if results != []:
		skill.append(results[0])
print(skill)

# 名前読み取り
img = cv2.cvtColor(frame[200:300,550:1000], cv2.COLOR_BGR2GRAY)
th = 140
img = cv2.threshold(img, th, 255, cv2.THRESH_BINARY)[1]
cv2.imwrite("name.png", img)
umatext = textres(Image.open("name.png"))
# print(umatext)
sub,name = umatext.split("\n")
resultsub = searcher3.search(sub, 0.5)
resultname = searcher2.search(name, 0.5)
id = -1
for i in range(len(resultsub)):
	for j in range(len(resultname)):
		try:
			id = names.index([resultname[j],resultsub[i]])
		except Exception as e:
			pass
if id > -1:
	print(names[id])

# 査定計算
