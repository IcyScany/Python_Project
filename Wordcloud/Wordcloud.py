from wordcloud import WordCloud
import numpy as np
from PIL import Image
import jieba    # 自然语言处理库

file = open(r"zwx.txt", encoding='utf-8')
text = file.read()
ss = " ".join(jieba.lcut(text))    # 将文本中的词语提取,’" ".join‘是将分开的词语之间用空格隔开
stopwords = ()      # 黑名单词汇

# 设置词云参数，字体，背景颜色，黑名单词汇等
mask = np.array(Image.open('alice_mask.png'))   # 设置词云轮廓
wc = WordCloud(font_path=r'SIMYOU.TTF', background_color=None,
               repeat=True, max_words=500, stopwords=stopwords, colormap='Greens',
               mask=mask,   # contour_color='Reds', contour_width=8,     # 轮廓参数
               mode="RGBA")     # 设置透明背景，此设置时不能使用contour设置轮廓
print(dir(wc))      # 查看词云的参数

wc.generate(ss)       # 生成词云
image = wc.to_image()
image.show()
wc.to_file('zwx.png')     # 保存图片

