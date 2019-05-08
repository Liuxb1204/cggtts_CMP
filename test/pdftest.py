import time
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.textlabels import Label
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table,Spacer,Image,PageBreak
pdfmetrics.registerFont(ttfonts.TTFont("simsun", "simsun.ttc"))
pdfmetrics.registerFont(ttfonts.TTFont('song', "STSONG.ttf"))
pdfmetrics.registerFont(ttfonts.TTFont('hei', "SIMHEI.TTF"))
pdfmetrics.registerFont(ttfonts.TTFont('fs', 'SIMFANG.TTF'))


# 画边框并添加文字
def autoLegender( title=''):
    width = 448
    height = 230
    d = Drawing(width,height)
    lab = Label()
    lab.x = 220  #x和y是文字的位置坐标
    lab.y = 210
    lab.setText(title)
    # lab.fontName = 'song' #增加对中文字体的支持
    lab.fontSize = 20
    d.add(lab)
    d.background = Rect(0,0,width,height,strokeWidth=1,strokeColor="#868686",fillColor=None) #边框颜色
    return d

ss = []

title = getSampleStyleSheet()['Title']    #字体的样式
title.fontName='hei'         #使用的字体
# bt.fontSize=18          #字号
# bt.alignment=1          # 居中
# bt.wordWrap = 'CJK'      # 换行

date = getSampleStyleSheet()['Title']    #字体的样式
date.fontName='song'

tuli = getSampleStyleSheet()['Normal']      #图例
tuli.fontName='fs'
tuli.fontSize=13
tuli.alignment=1

biaoz = getSampleStyleSheet()['Normal']     #标注
biaoz.fontName='fs'
biaoz.fontSize=12
biaoz.alignment=0
biaoz.leading = 20
biaoz.wordWrap = 'CJK'


title9 = Paragraph("图3、频率稳定度计算结果",tuli)

blank = Spacer(10,40)
blank2 = Spacer(10,20)
blank3 = Spacer(10,300)
blank4 = Spacer(10,138)


content6  = Paragraph('注：此处放置TDEV计算的阿伦方差数据和图形',biaoz)


ss.append(Paragraph('SEPY — SEPT 共视比对报告',title))
ss.append(blank)
ss.append(Paragraph('2018年3月19日',date))
ss.append(blank3)


bt2 = getSampleStyleSheet()['Heading2']    #字体的样式
bt2.fontName='song'    #使用的字体
# bt2.fontSize=15          #字号
# bt2.alignment=0          # 居左

ss.append(Paragraph('软件版本：CGGTTS CMP V1.1',bt2))
ss.append(Paragraph('时间范围：2017/02/01 — 2017/02/07',bt2))
ss.append(Paragraph('单位：北京卓越航导',bt2))
ss.append(Paragraph('地址：汤立路001号',bt2))
ss.append(Paragraph('联系人：孤独求败',bt2))
ss.append(Paragraph('电话：03311-899464656',bt2))

ss.append(PageBreak())          # 添加一页



bt3 = getSampleStyleSheet()['Normal']       #字体的样式
bt3.fontName='fs'          #使用的字体
bt3.fontSize=14                #字号
bt3.leading = 20               #设置行距
bt3.firstLineIndent = 32       #首行缩进


biaot = getSampleStyleSheet()['Heading2']     #标题
biaot.fontName='hei'
# biaot.fontSize=14
# biaot.alignment=0

num = 3

data = [['stat_name', 'file_name', 'start_mjd', 'end_mjd', 'data_type' ,"than_type" ,"compare_style"],
         ['SEPY', 'GZSEPY58.100\nGZSEPY58.101', '58100', '58101', 'L1C','REFSYS', 'CV'],

        ['SEPT', 'GZSEPT58.100\nGZSEPT58.101', '', '', '', '', ''],
        ]
t2 = Table(data,[60,80,50,50,50,50,70], [25,num*15,num*15],style=[
     ('GRID',(0,0),(-1,-1),0.5,colors.grey),
     # ('SPAN',(0,1),(0,4)),('SPAN',(0,5),(0,8)),
     # ('SPAN',(1,1),(1,4)),('SPAN',(1,5),(1,8)),
     ('SPAN',(2,1),(2,2)),
     ('SPAN',(3,1),(3,2)),
     ('SPAN',(4,1),(4,2)),
     ('SPAN',(5,1),(5,2)),
     ('SPAN',(6,1),(6,2)),
     ('ALIGN',(0,0),(-1,-1),'CENTER')
 ])
ss.append(Paragraph("一，用户数据",biaot))
ss.append(blank2)
ss.append(Paragraph('使用用户提供的CGGTTS数据进行比对，支持2.0、2E的格式版本。参与比对的数据源如下',bt3))
ss.append(blank2)
ss.append(t2)
ss.append(blank2)


sm = getSampleStyleSheet()['Normal']        #说明
sm.fontName='simsun'
sm.fontSize=12
sm.leading = 20

ss.append(Paragraph('1、数据类型是指CGGTTS文件中的FRC列；',sm))
ss.append(Paragraph('2、比对类型是指CGGTTS中的哪些列参与了数据比对；',sm))
ss.append(Paragraph('3、共视模式是指两站点比较所采用的共视法（CV）或全视法（AV）。',sm))
ss.append(blank2)





ss.append(Paragraph("二，比对说明",biaot))# 二 比对说明
ss.append(blank2)
ss.append(Paragraph('通过两个站点CGGTTS中的数据进行共视或全视比对，生成的比对结果包含站点1与站点2的时差比对结果、站点1相对于站点2的时间稳定度和频率稳定度。',bt3))
ss.append(blank2)
ss.append(Paragraph("三，比对结果",biaot))# 二 比对结果


biaot2 = getSampleStyleSheet()['Heading3']    #副标题
biaot2.fontName='hei'
# biaot2.fontSize=13
# biaot2.alignment=0

ss.append(Paragraph("3.1、SEPY-SEPT时差比对",biaot2))

ss.append(Paragraph('注：此处放置比较后三列数据形成的时差图，含均值、标准差、斜率(相对频率偏差)，如下图',biaoz))

ss.append(PageBreak())          # 添加一页

img1 = Table([[Image("C://Users//dancer//Desktop//aaa.jpg",420,220)]],430,220,style=[
    ('GRID',(0,0),(-1,-1),0.1,colors.white),
    ('ALIGN',(0,0),(-1,-1),'CENTER')
])
ss.append(img1)  # 图一
img2 = Table([[Image("C://Users//dancer//Desktop//bbb.jpg",420,220)]],430,220,style=[
    ('GRID',(0,0),(-1,-1),0.1,colors.white),
    ('ALIGN',(0,0),(-1,-1),'CENTER')
])
ss.append(img2)
img3 = Table([[Image("C://Users//dancer//Desktop//ss.jpg",420,220)]],430,220,style=[
    ('GRID',(0,0),(-1,-1),0.1,colors.white),
    ('ALIGN',(0,0),(-1,-1),'CENTER')
])
ss.append(img3)
ss.append(Paragraph("图1、时差比对结果图",tuli))

ss.append(PageBreak())          # 添加一页

ss.append(Paragraph("3.2、SEPY-SEPT时间稳定度",biaot2))

ss.append(Paragraph("注：此处放置TDEV计算的阿伦方差数据和图形",biaoz))
ss.append(blank2)

tdevdata = [["AF","TAU(s)","NUM(#)","Min_Sigma","Mod_Sigma","Max_Sigma"],
            ["1"," "," "," ", " "," "],
            ["2", " ", " ", " ", " ", " "],
            ["4", " ", " ", " ", " ", " "],
            ["8", " ", " ", " ", " ", " "],
            ["16", " ", " ", " ", " ", " "],
            ["32", " ", " ", " ", " ", " "],]

mdevdata = [["AF","TAU(s)","NUM(#)","Min_Sigma","Mod_Sigma","Max_Sigma"],
            ["1"," "," "," ", " "," "],
            ["2", " ", " ", " ", " ", " "],
            ["4", " ", " ", " ", " ", " "],
            ["8", " ", " ", " ", " ", " "],
            ["16", " ", " ", " ", " ", " "],
            ["32", " ", " ", " ", " ", " "],]

table = Table(tdevdata,colWidths=[60,60,70,80,80,80],rowHeights=7*[25],style=[
    ('GRID',(0,0),(-1,-1),1,colors.grey),
    ('ALIGN',(0,0),(-1,-1),'CENTER')
])


img4 = Table([[Image("C://Users//dancer//Desktop//ss.jpg",420,220)]],430,300,style=[
    ('GRID',(0,0),(-1,-1),0.1,colors.white),
    ('ALIGN',(0,0),(-1,-1),'CENTER')
])

ss.append(table)

ss.append(img4)
ss.append(blank2)

ss.append(Paragraph("图2、时间稳定度计算结果",tuli))

ss.append(PageBreak())          # 添加一页



ss.append(Paragraph("3.3、SEPY-SEPT频率稳定度",biaot2))
ss.append(Paragraph("注：此处放置MDEV计算的阿伦方差数据和图形",biaoz))
ss.append(blank2)
ss.append(table)



tab2 = Table([[Image("C://Users//dancer//Desktop//1803251155.jpg",520,320)]],530,330,style=[
    ('GRID',(0,0),(-1,-1),0.1,colors.white),
    ('ALIGN',(0,0),(-1,-1),'CENTER')
])

ss.append(tab2)
ss.append(blank2)
ss.append(Paragraph("图3、频率稳定度计算结果",tuli))

pdf=SimpleDocTemplate("C://Users//dancer//Desktop//"+str(time.time())+".pdf")

pdf.build(ss)


