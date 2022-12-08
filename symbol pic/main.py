from PIL import Image
img = Image.open("../字符图像/Scany.png")
out = img.convert("L")
width, height = out.size
out = out.resize((int(width * 5), int(height * 5)))
width, height = out.size
asciis = "#$%&()=+!*/^`. "
text = ""
for row in range(height):
    for col in range(width):
        gray = out.getpixel((col, row))          # 像素点灰度值
        text += asciis[int(gray / 255 * 14)]     # 根据灰度换成字符
    text += "\n"

with open("C:/Users/帅灿宇/Desktop/test.txt", "w") as file:
    file.write(text)
