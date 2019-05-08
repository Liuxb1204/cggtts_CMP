import matplotlib.pyplot as plt
import numpy as np
from pylab import *
# mpl.rcParams['Fonts.sans-serif'] = ['SimHei']    #支持中文
zhfont1 = matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\simsun.ttc')
mpl.rcParams['axes.unicode_minus'] = False
y1=[4542047,4542100,4542200,4542210,4542120,4542325,4542277,4542640,4542555]
x1=[58138.00,58138.25,58138.50,58138.75,58139.00,58139.25,58139.50,58139.75,58140.00]


def aa(x1,y1):
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
    plt.xlabel('时间(MJD)',fontproperties=zhfont1)
    plt.ylabel('纳秒(ns)',fontproperties=zhfont1)
    plt.title('(公视法)SEPY站与TS02站L1C差值\n均值=123,标准差=55.0，相对频率偏差=12e-15',fontproperties=zhfont1)
    # plt.legend()
    plt.grid(True, linestyle = "-.")
    plt.show()
    #plt.savefig("C://Users//dancer//Desktop//123.jpg")
aa(x1,y1)