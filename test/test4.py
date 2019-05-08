import matplotlib.pyplot as plt
import time
from pylab import *
import math
import matplotlib.pyplot as plt

from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from matplotlib.ticker import MultipleLocator, FormatStrFormatter , LogitLocator
#mpl.rcParams['Fonts.sans-serif'] = ['SimHei']    #支持中文
zhfont1 = matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\simsun.ttc')
mpl.rcParams['axes.unicode_minus'] = False

colors = ["b","g","c","m","y","k","r","g","c","m","y","k",
          "b","g","c","m","y","k","r","g","c","m","y","k"]

xlabels = ['A','B','8','14']

yval = [9889900, 4677700, 2952000, 1990300,6907600,2999400]

yval2 = [9593900, 4537700, 2832000, 1530300,6837600,2839400]

yval3 = [9382000, 4431700, 2732080, 1420300,6706600,2639400]

yavl4 = []
erro = []
for i in range(len(yval2)):
    a = (yval[i]+yval3[i])/2
    yavl4.append(a)
    erro.append(a-yval3[i])
print(erro)
print("-------------------")

# yval = [1.0226540669769422e-12, 4.6110807323865393e-13, 1.0914682393676012e-13, 8.2676155349718636e-14,2.5105850614411865e-13,5.1462598911472179e-13]

xval = [9600, 19200, 38400, 76800,153600,307200]


max = []
# max = [1.0226540669769422e-12, 5.1462598911472179e-13, 2.5105850614411865e-13, 1.3600434145961426e-13, 8.2676155349718636e-14, 0, 0]
# min = [9.3020230172230144e-13, 4.6110807323865393e-13, 2.1803887589158178e-13, 1.0914682393676012e-13, 6.2177782086273768e-14, 0, 0]
# max = [9489900, 4477700, 2152000, 1390300]
# min = [6707600,2599400]

max.extend(yval)
max.extend(yval2)
max.extend(yval3)
max.sort()

print(max)

minnum = 0
maxnum = max[len(max)-1]
for i in max:
    if i!=0:
        minnum =i
        break
print(minnum,maxnum)
s =  str("%e" % minnum).split("e")
minnum = 1*pow(10,int(s[1]))
s =  str("%e" % maxnum).split("e")
maxnum = 1*pow(10,int(s[1])+1)

print(minnum,maxnum)

ax = plt.subplot(111, xscale="log", yscale="log")



# ymajorLocator = LogitLocator(10)
plt.errorbar(xval, yval3,  zorder=3,fmt="m_",label='min')
plt.errorbar(xval, yval,  zorder=3,fmt="m_",label='max')
plt.errorbar(xval, yavl4, yerr=erro, zorder=1,fmt="m.",markersize=2,alpha=0.5)
plt.errorbar(xval, yval2,label='MDEV',fmt='-mo',mfc="w",alpha=0.5,linewidth=1,markersize=3)

plt.xlabel('测试中文 (s)',fontproperties=zhfont1)
plt.ylabel('MOD-ALLAN')
plt.ylim(minnum,maxnum)



plt.legend(framealpha=0.5)

ax.xaxis.grid(True, which='both',linestyle = "--") #x坐标轴的网格使用主刻度
ax.yaxis.grid(True, which='both',linestyle = "--") #y坐标轴的网格使用次刻度


plt.show()


def creatPaint(outpath,x,y,min_y,max_y,lable="MDEV",xlable="tau",ytable="mod allan"):
    """
    生成allan图片
    :param outpath: 输出路径
    :param x: x轴数据 type:数组
    :param y: y轴数据 type:数组
    :param min_y:  最小值数据 type:数组
    :param max_y:  最大值数据 type:数组
    :param lable:  图例名称
    :param xlable: x轴名称
    :param ytable: y轴名称
    :return:
    """
    yerr = []
    for i in range(len(y)):
        if min_y[i]==0:
            yerr.append(0)
        else:
            y1 = y[i]-min_y[i]
            yerr.append(y1)

    plt.subplot(111, xscale="log", yscale="log")

    plt.errorbar(x, y, yerr=yerr, fmt="-D", label=xlable,elinewidth=3)

    plt.errorbar(x, min_y,  zorder=3, fmt="s", label='mix_sigma')

    plt.errorbar(x, max_y,  zorder=3, fmt="o", label='max_sigma')

    plt.xlabel(xlable)
    plt.ylabel(ytable)

    plt.legend(framealpha=0.5)
    plt.grid()
    plt.savefig(outpath)

path = "C://Users//dancer//Desktop//s.jpg"
creatPaint(path,xval,yval,yval2,yval3)
# axis = ax.xaxis
# plt.xscale("log")
# plt.yscale("log")
# plt.xticks([0,0.5,1,2,4,6,8])

# ymajorLocator = MultipleLocator(0.5) #将y轴主刻度标签设置为0.5的倍数
# ymajorLocator = LogitLocator(10,[1])
# ax.yaxis.set_minor_locator(ymajorLocator)
# ax.xaxis.set_major_locator(ymajorLocator)


#xerr = [0.5, 0.4, 0.6, 0.9]

# yerr = [100, 100, 100, 100]
# yerr2 = [0, 0, 0, 0]

# plt.loglog(xval,yval)
# plt.xlim(1.0, 9.0)

# plt.grid()
#plt.savefig("scatter_error.png")