import matplotlib.pyplot as plt
import xlrd
from docx import Document
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

# 读取文件
data = xlrd.open_workbook('data3.xlsx')
sheet1 = data.sheet_by_name('Sheet1')
sheet2 = data.sheet_by_name('Sheet2')

for k in range(112):
    # 写文件
    name = sheet1.cell(k+1, 6).value      # name
    tele = int(sheet1.cell(k+1, 10).value)      # telephone
    ID = str(sheet1.cell(k+1, 9).value)       # ID
    sex = sheet1.cell(k+1, 7).value       # sex
    age = int(sheet1.cell(k+1, 8).value)      # age
    document = Document()

    # title
    paragraph = document.add_paragraph()
    paragraph_format = paragraph.paragraph_format  # 获取段落的格式属性
    paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER  # 水平对齐设为居中
    title = paragraph.add_run('【症状自评量表】金盾安保人员适应性量表测评结果报告')
    font = title.font
    font.name = 'Calibri'
    font.size = Pt(17)

    # 正文字体
    document.styles['Normal'].font.name = u'宋体'
    document.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
    document.styles['Normal'].font.size = Pt(12)
    document.styles['Normal'].font.color.rgb = RGBColor(0, 0, 0)

    p1 = document.add_paragraph('\n测试者姓名: ')
    p1.add_run(name)
    p2 = document.add_paragraph('性别: ')
    p2.add_run(sex)
    p3 = document.add_paragraph('年龄: ')
    p3.add_run(str(age))
    p4 = document.add_paragraph('身份证号：')
    p4.add_run(str(ID))
    p5 = document.add_paragraph('电话号码：')
    p5.add_run(str(tele))

    # 画柱状图
    plt.rcParams['font.sans-serif'] = ['SimHei']    # 正常显示中文
    plt.rcParams['axes.unicode_minus'] = False      # 正常显示负号
    typ = ('躯体化', '强迫', '人际关系\n敏感', '抑郁', '焦虑', '敌对', '恐怖', '偏执', '精神病性')
    result = list()
    color = list()
    for i in range(9):
        grade = float(sheet2.cell(k+1, 3*i+1).value)
        if grade < 2:
            color.append('steelblue')
        else:
            color.append('firebrick')
        result.append(int(sheet2.cell(k+1, 3*i).value))

    p = plt.bar(typ, result)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.bar(
        x=typ,  # Matplotlib自动将非数值变量转化为x轴坐标
        height=result,  # 柱子高度，y轴坐标
        width=0.6,  # 柱子宽度，默认0.8，两根柱子中心的距离默认为1.0
        align="center",  # 柱子的对齐方式，'center' or 'edge'
        color=color,  # 柱子颜色
    )

    ax.set_title("因子分柱状图", fontsize=15)
    plt.bar_label(p, label_type='edge')
    plt.grid(True, linestyle='--')
    plt.savefig('picture.png')
    plt.close()
    document.add_picture('picture.png')

    # analyse
    # document.add_page_break()
    # document.add_paragraph('\n')
    document.add_paragraph('【结果解释】')
    table = document.add_table(rows=10, cols=2, style='Medium Grid 1 Accent 1')
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = '总分'
    score = int(sheet1.cell(k+1, 101).value)
    if score <= 160:
        hdr_cells[1].text = '总分:' + str(score) + '这个测验主要测量的是您近期有无不健康的心理状态。' \
                                                 '您在该测验中的总分处于正常范围，也就是说，您的总体心理健康水平正常'
        # hdr_cells[1].text = '这个测验主要测量的是[' + name + ']近期有无不健康的心理状态。[' \
        #                     + name + ']在该测验中的总分处于正常范围，也就是说，[' \
        #                     + name + ']的总体心理健康水平正常。'
    else:
        hdr_cells[1].text = '总分=' + str(score) + '这个测验主要测量的是您近期有无不健康的心理状态。' \
                                                 '您在该测验中的总分较高，也就是说，您的心理健康水平可能有一定问题。'
        # hdr_cells[1].text = '这个测验主要测量的是[' + name + ']近期有无不健康的心理状态。[' \
        #                     + name + ']在该测验中的总分处于正常范围，也就是说，[' \
        #                     + name + ']心理健康水平可能有一定问题。'
    for i in range(9):
        hdr_cells = table.rows[i+1].cells
        hdr_cells[0].text = sheet2.cell(0, 3*i).value
        hdr_cells[1].text = sheet2.cell(k+1, 3*i+2).value

    document.save(str(name)+'_'+str(ID)+'.docx')
