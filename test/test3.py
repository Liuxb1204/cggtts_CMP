import myutils.date as date
import myutils.util as util
import matplotlib.pyplot as plt
import numpy as np
from pylab import *
# mpl.rcParams['Fonts.sans-serif'] = ['SimHei']    #支持中文
zhfont1 = matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\simsun.ttc')
mpl.rcParams['axes.unicode_minus'] = False


def aa(a,*list):
    print(a)
    for i in list:
        print("----",i)

#aa("sdsds",2,5,3)



def huatu(x1,y1):
    plt.plot(x1,y1,label='Frist line',linewidth=1,color='r',marker='.',)
    ax=plt.gca()
    plt.xticks(rotation=45) # 这里的rotation，当名称展示时候，一个倾斜的角度，当文案很长时候特别好用
    #ax.set_xticks(np.linspace(58138,58140,3))

    suzuy = []
    for i in ax.get_yticks():
        suzuy.append(i)
    print(suzuy)
    cha = suzuy[1]-suzuy[0]
    a = suzuy[0]
    b = suzuy[-1]

    if len(suzuy)>=2:
        suzuy.append(a - cha)
        suzuy.append(a - cha*2)
        suzuy.append(b + cha)
        suzuy.append(b + cha * 2)
    suzuy.sort()
    print(suzuy)

    c = ()
    ax.set_yticks(np.linspace(suzuy[0],suzuy[-1],len(suzuy)/2))
    for i in ax.get_yticks():
        a = (str(i),)
        c = c + a
    print(c)
    ax.set_yticklabels(c)

    plt.subplots_adjust(bottom=0.2) # 设置折线图和底部区域的距离
    plt.xlabel('时间戳',fontproperties=zhfont1)
    plt.ylabel('周',fontproperties=zhfont1)
    plt.title('TF14-TS02 (G10)\n 2018-12-04\n 标准差='+str(util.getStanDeviation(list2)),fontproperties=zhfont1)
    # plt.legend()
    plt.grid(True, linestyle = "-.")
    plt.show()



list1 = []
list2 = []

f = open("G:\\aaaaaa\\OZ_data.txt")             # 返回一个文件对象
line = f.readline()             # 调用文件的 readline()方法
while line:
   # print(line)

    list1.append(int(date.strToTime(line.split("G10:")[0].strip())))
    list2.append(float(line.split("G10:")[1].strip())*1e12/1575.42e6)
    line = f.readline()

f.close()
huatu(list1,list2)