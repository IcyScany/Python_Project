from captcha.image import ImageCaptcha

image = ImageCaptcha(fonts=['data/SIMYOU.TTF', 'data/STSONG.TTF'])  # 设置字体
image.write('Scany', 'captcha.png')

