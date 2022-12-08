import openpyxl
import requests  # 模拟请求
import pandas as pd  # 清洗数据
from bs4 import BeautifulSoup

# 打开目标execl，这里注意openpyxl能读取的execl后缀名是'.xlsx'文件
workbook1 = openpyxl.load_workbook('wshp.xlsx')
# 选定目标sheet
worksheet1 = workbook1.active
# 请求头**
headers = {
    "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/101.0.4951.67 Safari/537.36',
    "referer": "ttps://www4.bing.com/",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "cookie": "qcc_did=977c374d-feca-40c8-ab1c-5381bc5ddeb7; "
              "acw_tc=24930b2216537460342267489e1ed7d9e6b0cf03a09583f97fa01dbdc0; QCCSESSID=03cc2c10eb4f22ad9a38f72284",
}


# headers = {
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
#                   "100.0.4896.60 Safari/537.36",
#     "referer": "https://www.qcc.com/",
#     "sec-fetch-mode": "navigate",
#     "sec-fetch-site": "same-origin",
#     "cookie": "acw_tc=b73da88b16527954159736782e2b88537475ce76f08573d5693125223b;"
#               "QCCSESSID=16865cb659e719b9d63b92b6e5;qcc_did=8b3cf7bd-a934-407d-b7e9-c6e5fea2390b; "
#               "UM_distinctid=180d248a1b43bb-09b976678a448-1f343371-e1000-180d248a1b59d1;"
#               " CNZZDATA1254842228=316623179-1652791304-https%253A%252F%252Fwww.google.com.hk%252F%7C1652791304",
# }

ko = []
# 循环获取 数据 列**
for cell in worksheet1['N']:
    # 路径
    if cell.value != None:
        url = 'https://www.qcc.com/web/search?key=' + cell.value
        # 模拟请求网页
        html_text = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html_text, 'html.parser')
        # 循环获取div
        for ks in soup.find_all('div', {'class': 'maininfo'}):
            # print(ks.span.text)
            # 追加到ko数组 中
            ko.append([ks.span.text, ks.a['href']])
            # print(ks.a['href'])
            break
    else:
        break
print(ko)
# 保存的标题
title = ['公司名称', '公司链接']
# 保存的数据
table = pd.DataFrame(ko, columns=title)
# 保存路径
table.to_excel('url2.xlsx', sheet_name='sheet1')



