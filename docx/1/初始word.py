from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt #磅数
from docx.oxml.ns import qn #中文格式

import time
price = input('请输入今日价格：')
company_list = ['客户1','客户2','客户3','客户4','客户5','客户6']
today1 = time.strftime("%Y-%m-%d",time.localtime())
today2 = time.strftime("%Y/%m/%d",time.localtime())
today = time.strftime("%Y{y}%m{m}%d{d}",time.localtime()).format(y='年',m='月',d='日')

for i in company_list:
    document = Document()
    #设置文档的基础字体中文
    document.styles['Normal'].font.name = u'宋体'
    #设置文档的基础字体西文
    document.styles['Normal'].element.rPr.rFonts.set(qn('w:eastAsia'),u'宋体')

    # 初始化建立第一个自然段
    pl = document.add_paragraph()
    #对齐方式为居中，没有这句话默认左对齐
    pl.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run1 = pl.add_run('关于下达%s产品价格的通知'%(today))
    run1.font.name = '微软雅黑'
    run1.element.rPr.rFonts.set(qn('w:eastAsia'),u'微软雅黑')
    run1.font.size = Pt(21)
    #是否加粗
    run1.font.bold = True
    #前后距离5磅
    pl.space_before = Pt(5)
    pl.space_after = Pt(5)

    # 初始化建立第二个自然段
    p2 = document.add_paragraph()
    run2 = p2.add_run(i+":")
    #对客户的称呼
    run2.font.name = '仿宋_GB2312'
    run2.element.rPr.rFonts.set(qn('w:eastAsia'), u'仿宋_GB2312')
    run2.font.size = Pt(16)
    # 是否加粗
    run2.font.bold = True

    # 初始化建立第三个自然段
    p3 = document.add_paragraph()
    run3 = p3.add_run("  根据公司安排,为提供优质客户服务,我单位拟定了今日黄金价格为%s元,特此通知."%price)
    # 对客户的称呼
    run3.font.name = '仿宋_GB2312'
    run3.element.rPr.rFonts.set(qn('w:eastAsia'), u'仿宋_GB2312')
    run3.font.size = Pt(16)
    # 是否加粗
    run3.font.bold = True

    # 初始化建立第四个自然段
    p4 = document.add_paragraph()
    # 对齐方式为居中，没有这句话默认左对齐
    p4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run4 = p4.add_run("(      联系人:小杨  电话:18888888888)")
    # 对客户的称呼
    run4.font.name = '仿宋_GB2312'
    run4.element.rPr.rFonts.set(qn('w:eastAsia'), u'仿宋_GB2312')
    run4.font.size = Pt(16)
    # 是否加粗
    run4.font.bold = True
    document.save('%s-价格通知.docx'% i)