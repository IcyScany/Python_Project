# -*- coding: utf-8 -*-
# python 3.7.0
#
import re
import requests
import pytesseract
from selenium import webdriver
from PIL import Image, ImageEnhance
import time
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()
driver.maximize_window()
driver.get("http://zlxx.gzgs.gov.cn/pubsearch/portal/uilogin-forwardLogin.shtml")
driver.implicitly_wait(30)
# 用户名和密码
driver.find_element(by=By.NAME, value='j_username').send_keys('scany_')
driver.find_element(by=By.ID, value='j_password_show').send_keys('Scany0605!!!')

# 识别验证码
pic = driver.find_element(by=By.ID, value="j_validation_code")
# 清空验证码输入框
driver.find_element(by=By.ID, value="j_validation_code").clear()
# 截图或验证码图片保存地址
screenImg = r"E:\Pic.png"
# 浏览器页面截屏
driver.get_screenshot_as_file(screenImg)
# 定位验证码位置及大小
location = driver.find_element(by=By.ID, value='codePic').location
size = driver.find_element(by=By.ID, value='codePic').size
print(location, size)
# 根据截图修改截图位置
left = location['x']+230
top = location['y']+80
right = location['x'] + size['width']+300
bottom = location['y'] + size['height']+100
# 从文件读取截图，截取验证码位置
print(left, top, right, bottom)
img = Image.open(screenImg).crop((left, top, right, bottom))
# 对图片做一些处理
img = img.convert('RGBA')  # 转换模式：L | RGB
img = img.convert('L')  # 转换模式：L | RGB
img = ImageEnhance.Contrast(img)  # 增强对比度
img = img.enhance(2.0)  # 增加饱和度
img.save(screenImg)
# 再次读取识别验证码
img = Image.open(screenImg)
code = pytesseract.image_to_string(img)

# 识别出来验证码去特殊符号
b = ''
for i in code.strip():
    pattern = re.compile(r'[a-zA-Z0-9]')
    m = pattern.search(i)
    if m != None:
        b += i

# 把b的值输入验证码输入框
driver.find_element(by=By.ID, value="j_validation_code").send_keys(b)
# 点击登录按钮
driver.find_element(by=By.XPATH, value='//*[@id="loginForm"]/div[5]/a').click()
# 定时等待1秒
time.sleep(1)
# 获取cookie，并把cookie转化为字符串格式
cookie1 = str(driver.get_cookies())
print(cookie1)
# 第二次用正则表达式，代码实现的功能就是看cookie里是否有tokenId这个词，如果有说明登录成功，跳出循环
matchObj = re.search(r'tokenId', cookie1, re.M | re.I)
print('登录成功')

driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[2]/ul/li[2]/a').click()
time.sleep(1)
driver.find_element(by=By.XPATH, value='//*[@id="radioTypeCongregatePAVIEW"]').click()
driver.find_element(by=By.ID, value='search_input').send_keys('huawei')
driver.find_element(by=By.XPATH, value='//*[@id="btn_generalSearch"]').click()

time.sleep(100)
