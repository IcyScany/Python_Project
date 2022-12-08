import requests
from lxml import etree
import time
import os
import warnings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains


warnings.simplefilter("ignore", DeprecationWarning)

import json

# config file
with open("config/config.json", "r") as f:
    CONFIG = json.loads(f.read())


class QiCC(object):
    def __init__(self, config):
        self.config = config

    def login(self, url, pwlogin=True):

        LOGIN_XPATH = "/html/body/div[1]/div[1]/div/div/nav[2]/ul/li[last()]/a/span"

        # selenium 初始化
        chrome_options = webdriver.ChromeOptions()

        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
        )
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="chromedriver.exe")

        # 访问链接
        driver.get(url)

        # 点击登录按钮
        # driver.find_element_by_xpath(LOGIN_XPATH).click()
        driver.find_element(by=By.XPATH, value=LOGIN_XPATH).click()


        # 密码登录或者验证码登录
        time.sleep(2)
        if pwlogin:
            self.login_with_password(driver)
        else:
            self.login_with_captcha(driver)

        print("login in success")

        return driver

    def login_with_password(self, driver):
        #driver.find_element(by=By.XPATH,
        #                     value="/html/body/div[1]/div[2]/div[2]/div/div[3]/img").click()  # 点击密码登录
        driver.find_element(by=By.XPATH,
                            value="/html/body/div[2]/div/div/div/div[2]/div[1]/div[2]/a").click()  # 点击密码登录


        account_input = driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div[2]/div[3]/form/div[1]/input")
        account_input.send_keys(self.config.get("ACCOUNT"))
        pass_input = driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div[2]/div[3]/form/div[2]/input")
        pass_input.send_keys(self.config.get("PASSWORD"))
        time.sleep(1)
        driver.find_element_by_xpath(
            "/html/body/div[2]/div/div/div/div[2]/div[3]/form/div[4]/button").click()  # 点击登录

        button = driver.find_element_by_xpath(
            '/html/body/div[1]/div[3]/div/div[2]/div[3]/form/div[3]/div/div/div[1]/span')
        # 滑动滑块//*[@id="nc_1__scale_text"]/span//*[@id="nc_1__scale_text"]
        ActionChains(driver).click_and_hold(button).perform()



class QiCCRequester(QiCC):
    def request(self):
        # 1. 登录网站
        ###################
        # url = self.config["main_url"]
        # header = {'User-Agent':
        #               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
        # res = requests.get(url, headers=header)
        # self.driver = self.login(res)
        ###################
        self.driver = self.login(self.config["main_url"])

        # 2. 在配置文件配置要爬取的公司的url
        for com_url in self.config.get("company_url"):
            try:
                self.request_company(com_url)
            except Exception as err:
                print(f"something went wrong! detail: {err}")
                continue

    def request_company(self, url):
        print(f"正在爬取公司的专利文件中，url为: {url}")

        self.driver.get(url)
        time.sleep(2)

        whole_urls = []
        # 点击专利信息
        # button0 = self.driver.find_element(by=By.XPATH,
        #                                    value='/html/body/div/div[2]/div[4]/div/div/div[1]/a[6]/h2')
        # self.driver.execute_script("$(arguments[0]).click()", button0)

        button = self.driver.find_element(by=By.XPATH,
                            value="/html/body/div/div[2]/div[5]/div[6]/div/div[1]/a[3]")
        self.driver.execute_script("$(arguments[0]).click()", button)

        selector = etree.HTML(self.driver.page_source)
        company_name = selector.xpath("//*[@class='title']/div/span/h1[@class='copy-value']/text()")[0]
        page_num = selector.xpath("//*[@id='zhuanlilist']/div/div/nav/ul/li")
        ########################
        button2 = self.driver.find_element(by=By.XPATH,
                                          value="/html/body/div/div[2]/div[5]/div[6]/div/div[2]/section[1]/div[3]/div[1]/div/span[5]/span/span")
        self.driver.execute_script("$(arguments[0]).click()", button2)
        #######################
        if not page_num:
            raise Exception("没有专利信息!")

        # page_list = []
        # for num in page_num:
        #     page_list.append(num.xpath("a/text()")[0])
        # max_page = QiCCRequester.int_and_max(page_list)
        # patent_urls = selector.xpath("//*[@id='zhuanlilist']/div/div/table/tr/td[10]/span/a/@href")
        # patent_urls = [self.config.get("main_url") + url for url in patent_urls if "http" not in url]
        # whole_urls.extend(patent_urls)
        # for page in range(1, max_page):
        #     try:
        #         if max_page <= 6:
        #             self.driver.find_element_by_xpath(f"//*[@id='zhuanlilist']/div/div[2]/nav/ul/li[last()]/a").click()
        #             #######
        #             # button = self.driver.find_element(by=By.XPATH,
        #             #                                   value="/html/body/div[1]/div[2]/div[5]/div[6]/div/div[1]/a[3]")
        #             self.driver.execute_script("$(arguments[0]).click()", button)
        #         if max_page == 7:
        #             self.driver.find_element_by_xpath(
        #                 f"//*[@id='zhuanlilist']/div/div[2]/nav/ul/li[last()-1]/a").click()
        #         if max_page >= 8:
        #             if (max_page - page) <= 3:
        #                 self.driver.find_element_by_xpath(
        #                     f"//*[@id='zhuanlilist']/div/div[2]/nav/ul/li[last()-1]/a").click()
        #             else:
        #                 self.driver.find_element_by_xpath(
        #                     f"//*[@id='zhuanlilist']/div/div[2]/nav/ul/li[last()-2]/a").click()
        #         time.sleep(2)
        #         selector = etree.HTML(self.driver.page_source)
        #         patent_urls = selector.xpath("//*[@id='zhuanlilist']/div/div/table/tr/td[10]/span/a/@href")
        #         patent_urls = [self.config.get("main_url") + url for url in patent_urls if "http" not in url]
        #         print(f"location page {page} now")
        #         whole_urls.extend(patent_urls)
        #     except Exception as err:
        #         print(f"no next page already, detail:{err}")
        #         continue
        # print(f"专利数量: {len(whole_urls)}")
        # print(">>>>start save patent files!<<<<")
        for patent_url in whole_urls:
            self.request_patent(patent_url, company_name)

    def request_patent(self, url, company_name):
        self.driver.get(url)
        # time.sleep(2)
        # selector = etree.HTML(self.driver.page_source)
        # pdf_url = selector.xpath("/html/body/div[1]/div[2]/section/a/@href")
        # if len(pdf_url) > 0:
        #     pdf_url = pdf_url[0]
        #     name = selector.xpath("/html/body/div[1]/div[2]/section/div[1]/text()")[0]
        #     print(f"current pdf url:{pdf_url}")
        #     res = requests.get(pdf_url)
        #     pdf_back = pdf_url[pdf_url.rfind("/") + 1:]
        #     pdf_name = name + pdf_back
        #     pdf_name = pdf_name.replace("/", "-")
        #     print(f"save pdf file: {pdf_name}")
        #     if not os.path.exists(f"./patent_pdf/{company_name}"):
        #         os.mkdir(f"./patent_pdf/{company_name}")
        #     with open(f"./patent_pdf/{company_name}/" + pdf_name, "wb") as pdf:
        #         pdf.write(res.content)

    @staticmethod
    def int_and_max(data: list):
        result = []
        compare = 0
        for i in data:
            try:
                i = i.replace(".", "")
                result.append(int(i))
            except:
                continue
        for num in result:
            if num > compare:
                compare = num
        return compare


class QiCCParser(QiCC):
    def parse(self):
        pass


if __name__ == '__main__':
    # 初始化QiCC类
    qicc_request_obj = QiCCRequester(CONFIG)
    qicc_request_obj.request()





