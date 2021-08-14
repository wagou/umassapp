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
frame = cv2.imread("20210813-001246umamusume.png")
height, width, channels = frame.shape[:3]
if height > width * 16 / 9:
	frame = frame[(height//2-width*8//9):(height//2+width*8//9),:]
frame = cv2.resize(frame,(1080,1920))
cv2.imwrite("resized.png", frame)
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
dis = loc1[0][0] - 70

def dist(dis,point):
	return int(dis * (1920-point) / 1920)

frames = [frame[520+dist(dis,520):555+dist(dis,520),a:a+90] for a in [120,320,520,720,920]]
# frames = [frame[520:555,120:210],frame[520:555,320:410],frame[520:555,520:610],frame[520:555,720:810],frame[520:555,920:1010]]
# frames2 = [frame[550:585,a:a+90] for a in [120,320,520,720,920]]
# frames2 = [frame[550:585,120:210],frame[550:585,320:410],frame[550:585,520:610],frame[550:585,720:810],frame[550:585,920:1010]]
tekiframes = [frame[600+dist(dis,600):645+dist(dis,600),365:400],frame[600+dist(dis,600):645+dist(dis,600),565:600],frame[660+dist(dis,660):705+dist(dis,660),365:400],frame[660+dist(dis,660):705+dist(dis,660),560:600],frame[660+dist(dis,660):705+dist(dis,660),760:800],frame[660+dist(dis,660):705+dist(dis,660),955:995]
	,frame[720+dist(dis,720):765+dist(dis,720),365:400],frame[720+dist(dis,720):765+dist(dis,720),560:600],frame[720+dist(dis,720):765+dist(dis,720),760:800],frame[720+dist(dis,720):765+dist(dis,720),960:995]]
# tekiframes = [frame[600:645,365:400],frame[600:645,560:600],frame[660:705,365:400],frame[660:705,560:600],frame[660:705,760:800],frame[660:705,960:995]
# 	,frame[720:765,365:400],frame[720:765,560:600],frame[720:765,760:800],frame[720:765,960:995]]
skillframe = frame[930+dist(dis,930):970+dist(dis,930),110:460]
skillframe2 = frame[930+dist(dis,930):970+dist(dis,930),610:960]

Wlist = [110,610]
Hlist = [930+dist(dis,930),1050+dist(dis,1050),1160+dist(dis,1160),1270+dist(dis,1270),1380+dist(dis,1380),1490+dist(dis,1490),1600+dist(dis,1600)]

skillframes = []
for i in range(len(Hlist)):
	for j in range(len(Wlist)):
		skillframes.append(frame[Hlist[i]:Hlist[i]+40,Wlist[j]:Wlist[j]+350])

# 数字を読み取る
def numres(test):
	res = tool.image_to_string(test,lang="eng",builder=pyocr.builders.TextBuilder(tesseract_layout=6))
	return re.sub(r"\D","",res)
# アルファベット1文字を読み取る
def alphabetres(test):
	res = tool.image_to_string(test,lang="eng",builder=pyocr.builders.TextBuilder(tesseract_layout=6))
	if 'EF' in res:
		res = 'F'
	letter = re.search('[SABCDEFG]',res)
	if letter:
		res = letter.group()
	if '(' in res or '€' in res:
		res = 'C'
	return res
# 文字列を読み取る
def textres(test):
	res = tool.image_to_string(test,lang="jpn",builder=pyocr.builders.TextBuilder(tesseract_layout=6))
	return res

# ステータス読み取り
status = []
for i in range(5):
	img = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)
	th = 140
	img = cv2.threshold(img, th, 255, cv2.THRESH_BINARY)[1]
	cv2.imwrite("sp{}.png".format(i), img)
	# cv2.imwrite("sp{}.png".format(i), frames[i])
	num = int(numres(Image.open("sp{}.png".format(i))))
	# if num == '':
	# 	img = cv2.cvtColor(frames2[i], cv2.COLOR_BGR2GRAY)
	# 	th = 140
	# 	img = cv2.threshold(img, th, 255, cv2.THRESH_BINARY)[1]
	# 	cv2.imwrite("sp{}.png".format(i), img)
	# 	num = numres(Image.open("sp{}.png".format(i)))
	if num > 1200:
		num = 1200
	status.append(int(num))
	# print(num)
print(status)

# 適性読み取り
def Match(image,alphabet):
	temp = cv2.imread("db/{}.png".format(alphabet))
	#比較方法はcv2.TM_CCOEFF_NORMEDを選択
	result = cv2.matchTemplate(image, temp, cv2.TM_CCOEFF_NORMED)
	#類似度の設定(0~1)
	threshold = 0.9
	loc = ()
	#検出結果から検出領域の位置を取得
	loc += np.where(result >= threshold)
	if len(loc[0]) > 0:
		return True
	return False
tekisei = []
for j in range(10):
	# img = cv2.cvtColor(tekiframes[j], cv2.COLOR_BGR2GRAY)
	# th = 150
	# img = cv2.threshold(img, th, 255, cv2.THRESH_BINARY)[1]
	# cv2.imwrite("te{}.png".format(j), img)
	cv2.imwrite("te{}.png".format(j), tekiframes[j])
	res = alphabetres(Image.open("te{}.png".format(j)))
	# print(res)
	if res == '' or res not in 'SABCDEFG':
		img = cv2.imread("te{}.png".format(j))
		for p in "SABCDEFG":
			match = Match(img,p)
			if match:
				res = p
	if res == '':
		print("not found at",j)
		res = 'A'
	tekisei.append(res)

# 固有レベル読み取り
img = cv2.cvtColor(frame[930+dist(dis,930):970+dist(dis,930),505:525], cv2.COLOR_BGR2GRAY)
th = 140
img = cv2.threshold(img, th, 255, cv2.THRESH_BINARY)[1]
cv2.imwrite("lv.png", img)
lv = int(numres(Image.open("lv.png")))
print(lv)

# スキル読み取り
skill = []
for i in range(len(skillframes)):
	img = cv2.cvtColor(skillframes[i], cv2.COLOR_BGR2GRAY)
	th = 140
	img = cv2.threshold(img, th, 255, cv2.THRESH_BINARY)[1]
	cv2.imwrite("sf{}.png".format(i), img)
	skistr = textres(Image.open("sf{}.png".format(i)))
	print(skistr)
	# 個別対応(検索前処理)
	if len(skistr) > 0 and skistr[-1] == 'カ':
		skistr = skistr.replace('カ','力')
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
	# results.append('')
	if results != []:
		skill.append(results[0])
	# skill.append(results[0])
print(skill)

# 名前読み取り
img = cv2.cvtColor(frame[200+dist(dis,200):300+dist(dis,200),550:1000], cv2.COLOR_BGR2GRAY)
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
point = 0
# ステータス
path = "db/status.csv"
statustable = []
with open(path, encoding='utf-8-sig') as f:
	lines = [s.strip() for s in f.readlines()]
	for statusline in lines:
		statustable.append(statusline.split(','))
def calculate(status):
	return int(statustable[status-1][1].replace('点',''))

for num in status:
	point += calculate(num)

print(point)
print(tekisei)
# スキル
tekiseis = ['短距離','マイル','中距離','長距離','逃げ','先行','差し','追込']
skillnames = [sks[0] for sks in skills]
for i in range(len(skill)):
	ind = skillnames.index(skill[i])
	print(skill[i],skills[ind][1])
	sklpoint = int(skills[ind][1])
	if i == 0 and sklpoint == -1:
		point += 120 * lv
	elif i == 0 and sklpoint == -2:
		point += 170 * lv
	elif sklpoint == -2:
		point += 180
	elif skills[ind][3] == '':
		point += sklpoint
	else:
		tind = tekiseis.index(skills[ind][3])
		print(tind,tekisei[tind+2])
		if tekisei[tind+2] == 'B' or tekisei[tind+2] == 'C':
			point += int(sklpoint / 1.1 * 0.9)
		elif tekisei[tind+2] == 'D' or tekisei[tind+2] == 'E' or tekisei[tind+2] == 'F':
			point += int(sklpoint / 1.1 * 0.8)
		elif tekisei[tind+2] == 'G':
			point += int(sklpoint / 1.1 * 0.7)
		else:
			point += sklpoint
while len(skill) < 14:
	skill.append('')
print(point)

def Calc_rank(point):
	if point >= 17000:
		rank = 'S+'
	elif point >= 14500:
		rank = 'S'
	elif point >= 12100:
		rank = 'A+'
	elif point >= 10000:
		rank = 'A'
	elif point >= 8200:
		rank = 'B+'
	elif point >= 7000:
		rank = 'B'
	else:
		rank = '-B'
	return rank
umaid = 0
rank = Calc_rank(point)
outstr = "{0},{1[0]},{1[1]},{2},{3},{4[0]},{4[1]},{4[2]},{4[3]},{4[4]},{5[0]},{5[1]},{5[2]},{5[3]},{5[4]},{5[5]},{5[6]},{5[7]},{5[8]},{5[9]},{6[0]},{7},{6[1]},{6[2]},{6[3]},{6[4]},{6[5]},{6[6]},{6[7]},{6[8]},{6[9]},{6[10]},{6[11]},{6[12]},{6[13]}".format(umaid,names[id],point,rank,status,tekisei,skill,lv)
print(outstr)