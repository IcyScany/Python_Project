from PIL import Image
import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from captcha1 import get_result
import cv2


options = webdriver.ChromeOptions()
options.add_argument("--disable-extensions")
options.add_argument('ignore-certificate-errors')
options.add_argument("--disable-gpu")
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                     '(KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
driver = webdriver.Chrome(executable_path=r'C:\Program Files\Google\Chrome\Application\chromedriver', options=options)
driver.execute_cdp_cmd("Network.enable", {})
driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": """
           Object.defineProperty(navigator, 'webdriver', {
               get: () => undefined
           })
       """
})

driver.maximize_window()
driver.get("http://pss-system.cnipa.gov.cn/sipopublicsearch/portal/uilogin-forwardLogin.shtml")
driver.implicitly_wait(30)
driver.refresh()
# 用户名和密码
time.sleep(3)
driver.find_element(by=By.NAME, value='j_username').send_keys('scany_')
driver.find_element(by=By.ID, value='j_password_show').send_keys('Scany0605!!!')

# 识别验证码
pic = driver.find_element(by=By.ID, value="j_validation_code")
# 清空验证码输入框
driver.find_element(by=By.ID, value="j_validation_code").clear()
# 验证码图片保存地址
screenImg = r"ScreenShoot.png"
# 浏览器页面截屏
driver.get_screenshot_as_file(screenImg)
# 定位验证码位置及大小
location = driver.find_element(by=By.ID, value='codePic').location
size = driver.find_element(by=By.ID, value='codePic').size
# 根据截图修改截图位置
left = location['x']+290
top = location['y']+101
right = location['x'] + size['width']+272
bottom = location['y'] + size['height']+98
# 截取验证码位置
img = Image.open(screenImg).crop((left, top, right, bottom))
img.save('get_captcha.png')

# 处理验证码
img = cv2.imread('get_captcha.png', cv2.IMREAD_GRAYSCALE)
ans = get_result(img)


# 把ans输入验证码输入框
driver.find_element(by=By.ID, value="j_validation_code").send_keys(ans)
time.sleep(3)
# 点击登录按钮
driver.find_element(by=By.XPATH, value='//*[@id="loginForm"]/div[6]/a').click()
time.sleep(3)
# 获取cookie，并把cookie转化为字符串格式
cookie1 = str(driver.get_cookies())
print(cookie1)
# 第二次用正则表达式，代码实现的功能就是看cookie里是否有tokenId这个词，如果有说明登录成功，跳出循环
# matchObj = re.search(r'tokenId', cookie1, re.M | re.I)
# print('登录成功')

driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[2]/ul/li[2]/a').click()
time.sleep(1)
driver.find_element(by=By.XPATH, value='//*[@id="radioTypeCongregatePAVIEW"]').click()
driver.find_element(by=By.ID, value='search_input').send_keys('huawei')
driver.find_element(by=By.XPATH, value='//*[@id="btn_generalSearch"]').click()

time.sleep(100)
