import random
import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Spacer, SimpleDocTemplate,Table,Paragraph,Image
import pandas as pd
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.shapes import Circle
from reportlab.lib.styles import ParagraphStyle
from reportlab.graphics.shapes import Image as DrawingImage
from func_get_app_information import  get_app_information
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from androguard.core.bytecodes.apk import APK
from reportlab.lib.colors import HexColor
from func_get_app_information import get_app_information,get_permissions_report

ANDROID_PERMISSION_PATH = r"D:\学习资料\反炸APP分析\Data\permissions.csv"

# 注册字体
msyh = "msyh"
msyhbd = "msyhbd"
song = "simsun"
pdfmetrics.registerFont(TTFont(song, "simsun.ttc"))
pdfmetrics.registerFont(TTFont(msyh, "msyh.ttc"))
pdfmetrics.registerFont(TTFont(msyhbd, "msyhbd.ttc"))

#页面大小
PAGE_HEIGHT = A4[1]
PAGE_WIDTH = A4[0]

apk_path = r"D:\学习资料\反炸APP分析\apk\data\ウマ娘.apk"
target_path = r"D:\学习资料\反炸APP分析\apk\data"

#获取apk中属于AOSP的权限及描述
apk_permissions = get_permissions_report(APK(apk_path).get_details_permissions())
android_permissions = pd.read_csv(ANDROID_PERMISSION_PATH, encoding='gbk')
permissions_df = android_permissions[android_permissions['权限标识'].isin(apk_permissions['Name'])]
permissions_data = [permissions_df.columns.tolist()] + permissions_df.values.tolist()

#获取APP信息
information_path =get_app_information(apk_path = apk_path,target_path=target_path)#r"D:\学习资料\反炸APP分析\apk\data\20240609144057.csv"
info = pd.read_csv(information_path, encoding="gbk")
columns = info.columns
icon_path = info['icon'][0]
info_data = []
#处理信息文本
for column in columns:
    attribute_name = column
    attribute_name = attribute_name.replace('_', ' ')
    attribute_name = attribute_name[0].upper() + attribute_name[1:] + ':'
    temp = str(info[column][0])
    if temp.count(',') >= 1:
        info_data.append([attribute_name, temp.count(',')])
    else:
        info_data.append([attribute_name, info[column][0]])


# 绘制用户信息表
def drawTable(c: Canvas, x, y):
    data = [["File name: ", info['file_name'][0]],
            ['Package name: ',info['package_name'][0]],
            ['Scan date: ',info['scan_time'][0]],
            ['Label: ','?'],
            ['Grade: ', '?']
            ]
    t = Table(data,colWidths=130,rowHeights=20, style={
        ("FONT", (0, 0), (-1, -1), msyhbd, 8),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
        ('ALIGN', (1, 0), (1, -1), 'LEFT')#对齐方式 LEFT CENTER
    })
    t.wrapOn(c, 0, 0)
    t.drawOn(c, x, y)

def drawScorePie(canvas: Canvas, x, y, score,label : str = '?'):
    """绘制评分饼图"""
    d = Drawing(100, 100)
    # 画大饼图
    pc = Pie()
    pc.width = 100
    pc.height = 100
    # 设置数据
    pc.data = [score, 100 - score]
    pc.slices.strokeWidth = 0.1
    # 设置颜色
    color = colors.seagreen
    if (score < 60):
        color = colors.orangered
    elif (score < 85):
        color = colors.orange
    pc.slices.strokeColor = colors.transparent
    pc.slices[0].fillColor = color
    pc.slices[1].fillColor = colors.transparent
    d.add(pc)
    # 画内圈
    circle = Circle(50, 50, 40)
    circle.fillColor = colors.white
    circle.strokeColor = colors.transparent
    d.add(circle)
    # 把饼图画到Canvas上
    d.drawOn(canvas, x, y)
    # 写字
    canvas.setFont(msyh, 30)
    canvas.setFillColor(color)
    canvas.drawCentredString(x + 50, y + 40, label)

def DrawPageInfo(c: Canvas, date=datetime.date.today):
    """绘制页脚"""
    # 设置边框颜色
    c.setStrokeColor(colors.dimgrey)
    # 绘制线条
    c.line(30, PAGE_HEIGHT - 790, 570, PAGE_HEIGHT - 790)
    # 绘制页脚文字
    c.setFont(song, 8)
    c.setFillColor(colors.black)
    c.drawString(30, PAGE_HEIGHT - 810, f"生成日期：{date}")

def myFirstPage(c: Canvas, doc):
    c.saveState()
    # 设置填充色
    c.setFillColor(colors.orange)
    # 设置字体大小
    c.setFont(msyhbd, 30)
    # 绘制居中标题文本
    #c.setFont('simsun',40)
    c.drawCentredString(300, PAGE_HEIGHT-40, "分析报告")
    drawTable(c,1*inch,PAGE_HEIGHT-4*inch)#x,y
    drawScorePie(c,PAGE_WIDTH - 2*inch,PAGE_HEIGHT-2*inch,random.randint(1,100))
    # 绘制页脚
    #DrawPageInfo(c)
    c.restoreState()

def myLaterPages(c: Canvas, doc):
    c.saveState()
    # 绘制页脚
    #DrawPageInfo(c)
    c.restoreState()

# 设置段落格式
titleStyle = ParagraphStyle(
    name="titleStyle",
    alignment=1,#CENTER
    fontName=msyhbd,
    fontSize=10,
    textColor=colors.black,
    backColor=HexColor(0xF2EEE9),
    borderPadding=(5, 5),
    #leftIndent = -100,
    #rightIndent = -100,
)

app_name_style = ParagraphStyle(
    name="titleStyle",
    alignment=1,#CENTER
    fontName=msyhbd,
    fontSize=10,
    textColor=colors.black,
    borderPadding=(5, 5),
)

# 定义表格样式
permissions_style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.white),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                ('FONTNAME', (0, 0), (-1, -1), "simsun"),
                                ('FONTSIZE', (0, 0), (-1, -1), 6),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                                ('GRID', (0, 0), (-1, -1), 1, colors.black)])


def BUILD():
    # 创建文档
    doc = SimpleDocTemplate(r"D:\学习资料\反炸APP分析\apk\data\output.pdf")
    Story = [Spacer(1, -0.1 * inch)]

    # 绘制app图标
    Story.append(Image(icon_path, 0.5 * inch, 0.5 * inch))
    Story.append(Paragraph('——', app_name_style))
    Story.append(Paragraph(info['name'][0], app_name_style))
    Story.append(Spacer(1, 4 * inch))

    #添加APK INFORMATION部分
    Story.append(Paragraph("APP INFORMATION", titleStyle))
    Story.append(Spacer(1, 0.2 * inch))
    t = Table(info_data,colWidths=100,rowHeights=15,
              style={
        ("FONT", (0, 0), (-1, -1), msyhbd, 7),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),#对齐方式 LEFT CENTER
        ("LEFTPADDING", (0, 0), (-1, -1), -100),  # 左边距
    })
    Story.append(t)
    Story.append(Spacer(1, 1 * inch))

    #添加APK PERMISSIONS部分
    Story.append(Paragraph("APK PERMISSIONS", titleStyle))
    Story.append(Spacer(1, 0.2 * inch))

    # 根据单元格文本设置特定单元格的样式
    for row in range(1, len(permissions_data)):
        for col in range(len(permissions_data[row])):
            if 'dangerous' in permissions_data[row][col]:
                permissions_style.add('TEXTCOLOR', (col, row), (col, row), colors.red)
            if 'normal' in permissions_data[row][col]:
                permissions_style.add('TEXTCOLOR', (col, row), (col, row), colors.green)
    # 创建表格对象，并应用样式
    # 设置每列的宽度 #font_size = 6
    col_widths = [170, 80,260,50]
    # 创建表格
    table = Table(permissions_data, colWidths=col_widths)
    table.setStyle(permissions_style)
    # 添加表格到文档，使用 KeepTogether 来确保表格跨页时整体显示在一页上
    Story.append(table)

    # 保存文档
    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)

BUILD()

'''
# 绘制两个横向排布的图像
d = Drawing()
d.add(DrawingImage(0, 0, 200, 200, icon_path))
d.add(DrawingImage(200, 0, 200, 200, icon_path))
Story.append(d)'''

