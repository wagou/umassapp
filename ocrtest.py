from PIL import Image
import pyocr

tools = pyocr.get_available_tools()
tool = tools[0]


test = Image.open("sf6.png")
res = tool.image_to_string(test,lang="jpn",builder=pyocr.builders.TextBuilder(tesseract_layout=6))
print(res)