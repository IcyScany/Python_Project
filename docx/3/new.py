import matplotlib.pyplot as plt
import numpy as np
import xlrd
from docx.shared import Inches
from docx import Document
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT


def table(content0, contentk):
    table_temp = document.add_table(len(contentk), cols=len(content0) + 1, style='Medium Grid 3 Accent 1')
    for k in range(len(table_temp.columns)):  # 设置宽度
        table_temp.cell(0, k).width = Inches(2)
    for k in range(len(table_temp.rows)):  # 设置高度
        table_temp.rows[k].height = Inches(0.25)
    for k in range(len(table_temp.rows)):  # 文字居中
        for c in range(len(table_temp.columns)):
            table_temp.cell(k, c).vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    table_temp.style.paragraph_format.alignment = WD_TABLE_ALIGNMENT.CENTER  # 表格在word中居中

    for k in range(len(contentk)):
        run_temp = table_temp.cell(k, 0).paragraphs[0].add_run(contentk[k])
        run_temp.font.name = '微软雅黑'
        run_temp.font.size = Pt(12)
        run_temp.font.color.rgb = RGBColor(255, 255, 255)
        run_temp.font.bold = True  # 加粗
    for k in range(0, len(content0)):
        run_temp = table_temp.cell(0, k + 1).paragraphs[0].add_run(content0[k])
        run_temp.font.name = '微软雅黑'
        run_temp.font.size = Pt(12)
        run_temp.font.color.rgb = RGBColor(255, 255, 255)
        run_temp.font.bold = True  # 加粗


def table1(content0, contentk):
    table_temp = document.add_table(rows=len(contentk), cols=len(content0) + 4, style='Medium Grid 3 Accent 1')
    for k in range(len(table_temp.columns)):  # 设置宽度
        table_temp.cell(0, k).width = Inches(2)
    for k in range(len(table_temp.rows)):  # 设置高度
        table_temp.rows[k].height = Inches(0.25)
    for k in range(len(table_temp.rows)):  # 文字居中
        for c in range(len(table_temp.columns)):
            table_temp.cell(k, c).vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    table_temp.style.paragraph_format.alignment = WD_TABLE_ALIGNMENT.CENTER  # 表格在word中居中
    table_temp.cell(1, 2).merge(table_temp.cell(len(table_temp.rows) - 1, 2))  # 合并单元格
    table_temp.cell(1, 3).merge(table_temp.cell(len(table_temp.rows) - 1, len(table_temp.columns) - 1))
    table_temp.cell(0, 3).merge(table_temp.cell(0, len(table_temp.columns) - 1))

    for k in range(len(contentk)):
        run_temp = table_temp.cell(k, 0).paragraphs[0].add_run(contentk[k])
        run_temp.font.name = '微软雅黑'
        run_temp.font.size = Pt(12)
        run_temp.font.color.rgb = RGBColor(255, 255, 255)
        run_temp.font.bold = True  # 加粗
    for k in range(0, len(content0)):
        run_temp = table_temp.cell(0, k + 1).paragraphs[0].add_run(content0[k])
        run_temp.font.name = '微软雅黑'
        run_temp.font.size = Pt(12)
        run_temp.font.color.rgb = RGBColor(255, 255, 255)
        run_temp.font.bold = True  # 加粗


def table2(content0):
    content1 = ('性别', '男', '女')
    content2 = ('age', '<30', '>70')
    content3 = ('teac_age', '5', '>25')
    document.add_paragraph('(2) 差异分析')
    document.add_paragraph('① 性别差异')
    table(content0, content1)
    document.add_paragraph('② 年龄差异')
    table(content0, content2)
    document.add_paragraph('③ 教龄差异')
    table(content0, content3)


def bar(x, y, title):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文
    plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号
    plt.figure()
    plt.title(title, fontsize=16, y=0.9, loc='center')
    p = plt.bar(x, y, 0.4, color='lightsteelblue', zorder=100)  # zorder图层顺序，隐藏网格
    plt.bar_label(p)
    plt.legend(("人数",), loc=(0.4, -0.14))
    plt.grid(axis="y", c='lightblue', alpha=0.5)  # aplha 透明度
    plt.savefig('figure.png')
    plt.close()
    document.add_picture('figure.png')


def pie(name, value):
    plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文显示
    plt.figure(figsize=(6, 6))  # 将画布设定为正方形，则绘制的饼图是正圆
    explode = [0.01 for k in range(len(name))]  # 设定各项距离圆心n个半径
    plt.pie(value, explode=explode, labels=name, autopct='%1.1f%%')  # 绘制饼图
    plt.title('职称', fontsize=18)  # 绘制标题
    plt.legend(loc=(0.5, -0.1))
    plt.savefig('figure.png')
    plt.close()
    document.add_picture('figure.png')


def box(data):
    plt.subplots()  # 得到画板、轴
    plt.boxplot(data, patch_artist=True)  # 描点上色
    plt.savefig('figure.png')
    plt.close()
    document.add_picture('figure.png')


def title1(n, a):
    p = document.add_paragraph()
    t = str(n) + '.' + a
    run = p.add_run(t)
    run.font.color.rgb = RGBColor(46, 116, 130)


def analyze(boxdata, content1, content0):
    # 箱线图
    document.add_paragraph(' (1) 总体情况')
    box(boxdata)
    # 柱状图
    table1(content1, content0)
    table2(content0)


def begin():
    pl = document.add_paragraph()  # 初始化建立第一个自然段
    pl.alignment = WD_ALIGN_PARAGRAPH.CENTER  # 对齐方式为居中，没有这句话默认左对齐
    run1 = pl.add_run('西南大学教师职业能力测评团体报告')
    run1.font.size = Pt(22)
    run1.font.bold = False  # 是否加粗
    p1 = document.add_paragraph('单位：')
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER  # 对齐方式为居中，没有这句话默认左对齐
    p2 = document.add_paragraph('人数：')
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER  # 对齐方式为居中，没有这句话默认左对齐
    document.add_paragraph()
    # *************************************1111111*********************************************
    p3 = document.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER  # 对齐方式为居中，没有这句话默认左对齐
    r3 = p3.add_run('基本情况')
    r3.font.size = Pt(18)
    r3.font.color.rgb = RGBColor(46, 116, 181)
    r3.font.bold = True


if __name__ == '__main__':
    # 读取文件
    excel = xlrd.open_workbook('data.xlsx')
    data = excel.sheet_by_name('Sheet1')
    final = dict()

    for k in range(1, data.nrows):
        type_temp = data.cell(k, 10).value
        sex_temp = data.cell(k, 8).value
        if type_temp not in final:
            final[type_temp] = {'男': 0, '女': 0}
        if sex_temp == '男':
            final[type_temp]['男'] += 1
        if sex_temp == '女':
            final[type_temp]['女'] += 1
    print(final)

    document = Document()
    document.styles['Normal'].font.size = Pt(14)
    document.styles['Normal'].font.name = u'宋体'  # 设置文档的基础字体中文
    document.styles['Normal'].element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')  # 设置文档的基础字体西文

    begin()
    # **************************************柱状图**************************************
    document.add_paragraph('1.性别')
    sex = ('男', '女')
    data1 = [10, 20]
    bar(sex, data1, '性别')

    document.add_paragraph('2.年龄')
    age = ('<30', '30-40', '40-50', '50-60', '60-70', '>70')
    data2 = [10, 20, 1, 1, 1, 1]
    bar(age, data2, '年龄')

    document.add_paragraph('2.教龄')
    teachage = ('<5', '5-10', '10-15', '15-20', '20-25', '>25')
    data3 = [10, 20, 1, 1, 1, 1]
    bar(teachage, data3, '教龄')

    document.add_paragraph('4.学历')
    ex = ('研究生', '本科', '大专', '高职', '高中', '初中', '小学')
    data4 = [10, 20, 1, 1, 1, 1, 1]
    bar(ex, data4, '学历')

    # ***************************************饼状图*************************************
    document.add_paragraph('5.职称')
    name1 = ['第一', '第二', '第三']  # 定义饼图的标签，标签是列表
    values1 = [1, 2, 3]
    pie(name1, values1)

    document.add_paragraph('6.岗位分布')
    name2 = ['第一', '第二', '第三']  # 定义饼图的标签，标签是列表
    values2 = [1, 2, 3]
    pie(name2, values2)

    # *************************************222222*********************************************
    p9 = document.add_paragraph()
    p9.alignment = WD_ALIGN_PARAGRAPH.CENTER  # 对齐方式为居中，没有这句话默认左对齐
    r9 = p9.add_run('测评结果')
    r9.font.size = Pt(18)
    r9.font.color.rgb = RGBColor(46, 116, 181)
    r9.font.bold = True

    # *************************************工作疲劳*********************************************
    title1(1, '工作疲劳')
    data1 = [np.random.normal(0, std, 100) for std in range(1, 4)]
    content1_0 = (' ', '各维度平均分', '情绪衰竭', '成就感低落', '玩世不恭')
    content1_1 = ('平均得分', '水平', '解释')
    analyze(data1, content1_0, content1_1)

    # *************************************幸福感*********************************************
    title1(2, '幸福感')
    data2 = [np.random.normal(0, std, 100) for std in range(1, 4)]
    content2_0 = (' ', '总分', '对健康的担心', '精力', '对生活的满足和兴趣',
                  '忧郁或愉快的心境', '对情感和行为的控制', '松弛与紧张')
    content2_1 = ('平均得分', '水平', '解释')
    analyze(data2, content2_1, content2_0)

    # *************************************压力情况*********************************************
    title1(3, '压力情况')
    data3 = [np.random.normal(0, std, 100) for std in range(1, 4)]
    content3_0 = (' ', '总分', '紧张感', '失控感')
    content3_1 = ('平均得分', '水平', '解释')
    analyze(data3, content3_1, content3_0)

    # *************************************心理状况*********************************************
    title1(4, '心理状况')
    data4 = [np.random.normal(0, std, 100) for std in range(1, 4)]
    content4_0 = (' ', '总分', '躯体化', '强迫', '人际关系敏感', '抑郁',
                  '焦虑', '敌对', '恐怖', '偏执', '精神病性')
    content4_1 = ('平均得分', '水平', '解释')
    analyze(data4, content4_1, content4_0)

    p45 = document.add_paragraph('-------------------------报告结束-------------------------')
    p45.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p45.paragraph_format.space_before = Pt(50)
    document.save('new.docx')
