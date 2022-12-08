from docx import Document
from docx.shared import Inches
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT

document = Document()
# 表格基本属性
rows = 3        # 设置列数
cols = 4        # 设置行数
table = document.add_table(rows, cols, style='Table Grid')
# 设置宽度
for i in range(cols):
    table.cell(0, i).width = Inches(2)
# 设置高度
for i in range(rows):
    table.rows[i].height = Inches(1)
# 表格内文本居中
table.alignment = WD_TABLE_ALIGNMENT.CENTER     # 水平居中
# 文字居中
for i in range(rows):
    for j in range(cols):
        table.cell(i, j).vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
# 表格在word中居中
table.style.paragraph_format.alignment = WD_TABLE_ALIGNMENT.CENTER


# 表格第一行 ———— 第一种编辑方法
cells1 = table.rows[0].cells
run = cells1[0].text = '总分'
cells1[1].text = '0'

# 表格第二行 ———— 第二种编辑方法
table.cell(1, 0).text = 'final'
table.cell(2, 3).text = 'A'

# 添加元素并设置字体及加粗
run = table.cell(2, 2).paragraphs[0].add_run('smida')
run.font.name = '微软雅黑'
run.font.size = 140000
run.font.bold = True    # 加粗

# 合并单元格
cell_1 = table.cell(1, 0)
cell_2 = table.cell(2, 1)
cell_1.merge(cell_2)

document.save('table.docx')

