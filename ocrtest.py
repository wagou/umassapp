from PIL import Image
import pyocr
import os
from ss import umainfo

tools = pyocr.get_available_tools()
tool = tools[0]


test = Image.open("te7.png")
res = tool.image_to_string(test,lang="eng",builder=pyocr.builders.TextBuilder(tesseract_layout=6))
print(res)
str1 = 'A'
print(str1 in 'SABCDEFG')
for char in str1:
	print(char in 'SABCDEFG')

lists = os.listdir('test')

for aa in lists:
	path = "test/"+aa
	print(path)
	umainfo(path)
