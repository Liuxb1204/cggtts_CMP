import matplotlib.pyplot as plt
import numpy as np
import time
import c_logg as lg
import datetime
from reportlab.graphics.shapes import Drawing, Rect
import os
import myutils.date as d
import myutils.util as util
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table,TableStyle,Spacer,Image,PageBreak
pathl = os.path.dirname(os.path.split(os.path.realpath(__file__))[0])
pdfmetrics.registerFont(ttfonts.TTFont("simsun", pathl+"/Fonts/simsun.ttc"))
pdfmetrics.registerFont(ttfonts.TTFont('song', pathl+"/Fonts/STSONG.ttf"))
pdfmetrics.registerFont(ttfonts.TTFont('hei', pathl+"/Fonts/SIMHEI.TTF"))
pdfmetrics.registerFont(ttfonts.TTFont('fs', pathl+'/Fonts/SIMFANG.TTF'))



def creatPDF(path,data1,data2):

    print("开始创建pdf文档")
    lg.mylog("info","开始创建pdf文档")
    ss = []
    map = util.readConf()

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

    blank = Spacer(10,40)
    blank2 = Spacer(10,20)
    blank3 = Spacer(10,300)

    view = " 共视" if map["view"]=="CV" else " 全视"

    ss.append(Paragraph(map["name1"]+' — '+map["name2"]+ view +'比对报告',title))
    ss.append(blank)

    now = datetime.datetime.now()
    ss.append(Paragraph(str(now.year)+'年'+str(now.month)+"月"+str(now.day)+"日",date))
    ss.append(blank3)


    bt2 = getSampleStyleSheet()['Heading2']    #字体的样式
    bt2.fontName='song'    #使用的字体
    # bt2.fontSize=15          #字号
    # bt2.alignment=0          # 居左

    ss.append(Paragraph('软件版本：CGGTTS CMP V1.1',bt2))

    smjd = d.mjdToTime(map["smjd"],"000000").split(" ")[0].replace("-","/")
    emjd = d.mjdToTime(map["emjd"],"000000").split(" ")[0].replace("-","/")

    ss.append(Paragraph('时间范围：'+smjd+' — '+emjd,bt2))
    ss.append(Paragraph('单位：北京卓越航导科技有限责任公司',bt2))
    ss.append(Paragraph('地址：北京市朝阳区汤立路220号',bt2))
    ss.append(Paragraph('联系人：张思德',bt2))
    ss.append(Paragraph('电话：86-10-56275513',bt2))
    ss.append(Paragraph('网址：www.navcompass.com', bt2))
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



    num = int(map["emjd"])-int(map["smjd"])+1
    sta1 = [map["name1"]]
    sta2 = [map["name2"]]
    str1 = ""
    str2 = ""
    for i in range(int(map["smjd"]),int(map["emjd"])+1):
        if i==int(map["emjd"]):
            str1 += map["filetype"] + map["name1"] + str(i)[0:2]+"."+str(i)[-3:]
            str2 += map["filetype"] + map["name2"] + str(i)[0:2]+"."+str(i)[-3:]
        else:
            str1 += map["filetype"] + map["name1"] + str(i)[0:2]+"."+str(i)[-3:] + "\n"
            str2 += map["filetype"] + map["name2"] + str(i)[0:2]+"."+str(i)[-3:] + "\n"

    sta1.append(str1)
    sta1.append(map["smjd"])
    sta1.append(map["emjd"])
    sta1.append(map["datatype"])
    sta1.append("refsys*" + str(map["sysnum"])  + "+\n" +
                  "mdtr*" + str(map["mdtrnum"]) + "+\n" +
                  "mdio*" + str(map["mdionum"]) + "+\n" +
                  "msio*" + str(map["msionum"]) + "  ")
    sta1.append(map["view"])
    sta2.append(str2)


    data = [['stat_name', 'file_name', 'start_mjd', 'end_mjd', 'data_type' ,"than_type" ,"compare_style"],sta1,sta2,]

    t2 = Table(data,[60,80,50,50,50,55,70], [25,num*15,num*15],style=[
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
    ss.append(Paragraph("一、用户数据",biaot))
    ss.append(blank2)
    ss.append(Paragraph('使用用户提供的CGGTTS数据进行比对，支持2.0、2E的格式版本。参与比对的数据源如下',bt3))
    ss.append(blank2)
    ss.append(t2)
    ss.append(blank2)


    sm = getSampleStyleSheet()['Normal']        #说明
    sm.fontName='simsun'
    sm.fontSize=12
    sm.leading = 20

    ss.append(Paragraph('1、data_type是指CGGTTS文件中的FRC列；',sm))
    ss.append(Paragraph('2、than_type是指CGGTTS中的哪些列参与了数据比对；',sm))
    ss.append(Paragraph('3、compare_style是指两站点比较所采用的共视法（CV）或全视法（AV）。',sm))
    ss.append(blank2)


    ss.append(Paragraph("二、比对说明",biaot))# 二 比对说明
    ss.append(blank2)
    ss.append(Paragraph('通过两个站点CGGTTS中的数据进行共视或全视比对，生成的比对结果包含站点1与站点2的时差比对结果、站点1相对于站点2的时间稳定度和频率稳定度。',bt3))
    ss.append(blank2)
    ss.append(Paragraph("三、比对结果",biaot))# 二 比对结果


    biaot2 = getSampleStyleSheet()['Heading3']    #副标题
    biaot2.fontName='hei'
    # biaot2.fontSize=13
    # biaot2.alignment=0

    ss.append(Paragraph("3.1、"+map["name1"]+"-"+map["name2"]+"时差比对",biaot2))

    ss.append(Paragraph('注：此处放置比较后三列数据形成的时差图，含均值、标准差、斜率(相对频率偏差)，如下图',biaoz))

    ss.append(PageBreak())          # 添加一页

    img3 = Table([[Image(path + "/diff.jpg", 550, 220)]], 550, 220, style=[
        ('GRID', (0, 0), (-1, -1), 0.1, colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER')
    ])
    ss.append(img3)
    img1 = Table([[Image(path+"/sta1.jpg",550,220)]],550,220,style=[
        ('GRID',(0,0),(-1,-1),0.1,colors.white),
        ('ALIGN',(0,0),(-1,-1),'CENTER')
    ])
    ss.append(img1)  # 图一
    img2 = Table([[Image(path+"/sta2.jpg",550,220)]],550,220,style=[
        ('GRID',(0,0),(-1,-1),0.1,colors.white),
        ('ALIGN',(0,0),(-1,-1),'CENTER')
    ])
    ss.append(img2)

    ss.append(Paragraph("图1、时差比对结果图",tuli))

    ss.append(PageBreak())          # 添加一页

    ss.append(Paragraph("3.2、"+map["name1"]+"-"+map["name2"]+"时间稳定度",biaot2))

    ss.append(Paragraph("注：此处放置TDEV计算的阿伦方差数据和图形",biaoz))
    ss.append(blank2)

    tdevdata = [["AF","TAU(s)","NUM(#)","Min_Sigma","Mod_Sigma","Max_Sigma"]]
    for i in data1.values():
        tdevdata.append([i[0],i[1],i[2],i[3],i[4],i[5]])



    table = Table(tdevdata,colWidths=[60,60,70,80,80,80],rowHeights=(len(data1)+1)*[25],style=[
        ('GRID',(0,0),(-1,-1),1,colors.grey),
        ('ALIGN',(0,0),(-1,-1),'CENTER')
    ])

    img4 = Table([[Image(path+"/tdevallan.jpg",520,320)]],530,330,style=[
        ('GRID',(0,0),(-1,-1),0.1,colors.white),
        ('ALIGN',(0,0),(-1,-1),'CENTER')
    ])

    ss.append(table)

    ss.append(img4)

    ss.append(Paragraph("图2、时间稳定度计算结果",tuli))

    ss.append(PageBreak())          # 添加一页

    mdevdata = [["AF", "TAU(s)", "NUM(#)", "Min_Sigma", "Mod_Sigma", "Max_Sigma"]]
    for i in data2.values():
        mdevdata.append([i[0], i[1], i[2], i[3], i[4], i[5]])

    table2 = Table(mdevdata, colWidths=[60, 60, 70, 80, 80, 80], rowHeights=(len(data2)+1) * [25], style=[
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER')
    ])

    ss.append(Paragraph("3.3、"+map["name1"]+"-"+map["name2"]+"频率稳定度",biaot2))
    ss.append(Paragraph("注：此处放置MDEV计算的阿伦方差数据和图形",biaoz))
    ss.append(blank2)
    ss.append(table2)

    img5 = Table([[Image(path+"/mdevallan.jpg",520,320)]],530,330,style=[
        ('GRID',(0,0),(-1,-1),0.1,colors.white),
        ('ALIGN',(0,0),(-1,-1),'CENTER')
    ])

    ss.append(img5)
    ss.append(Paragraph("图3、频率稳定度计算结果",tuli))

    pdf=SimpleDocTemplate(path+"/"+map["name1"]+"_"+map["name2"]+".pdf")


    pdf.build(ss)

    print("pdf文档创建完毕")
    lg.mylog("info","pdf文档创建完毕")

