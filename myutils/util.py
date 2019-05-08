import configparser
import c_logg as lg
import ftplib
import os, sys
import math
from collections import OrderedDict
import myutils.date as d
import matplotlib.pyplot as plt
from scipy.optimize import leastsq  # 引入最小二乘函数
from pylab import *
# mpl.rcParams['Fonts.sans-serif'] = ['SimHei']    #支持中文
pathl = os.path.dirname(os.path.split(os.path.realpath(__file__))[0])
zhfont1 = matplotlib.font_manager.FontProperties(fname=pathl+'/Fonts/simsun.ttc')
mpl.rcParams['axes.unicode_minus'] = False      #解决保存图像是负号'-'显示为方块的问题
import numpy as np


def readConf(path = pathl+"/cggtts.ini"):
    """
    读取配置文件
    :param path: 配置文件路径
    :return: 配置文件字典
    """
    map = {}
    myfile1 = open(path, "r")
    config = configparser.ConfigParser()
    config.read(path)
    # 读取参数信息
    map["view"]= config.get("data", "compare_style")
    map["filetype"] = config.get("data", "file_type")
    map["smjd"]  = config.get("data", "start_mjd")
    map["emjd"] = config.get("data", "end_mjd")
    map["datatype"]  = config.get("data", "code_type")
    map["sysnum"] = int(config.get("data", "refsys_ratio"))
    map["mdtrnum"] = int(config.get("data", "mdtr_ratio"))
    map["mdionum"]  = int(config.get("data", "mdio_ratio"))
    map["msionum"] = int(config.get("data", "msio_ratio"))
    map["tichu"]  = config.get("data", "state_eliminate")
    map["tichu2"] = config.get("data", "pauta_rule")
    map["outpath"] = config.get("data", "outpath")
    map["generatepdf"] = config.get("data", "generatepdf")

    # 读取站点一的信息
    map["name1"]  = config.get("station1", "name")
    map["datasource1"]  = config.get("station1", "data_source")  # 获取方式（本地或者ftp）
    map["localpath1"]  = config.get("station1", "local_path").replace("\t", "\\t")\
        .replace("\r", "\\r").replace("\n","\\n")  # 路径
    map["ip1"] = config.get("station1", "ftp_ip")
    map["port1"] = config.get("station1", "ftp_port")
    map["username1"] = config.get("station1", "ftp_username")
    map["password1"] = config.get("station1", "ftp_password")
    map["ftppath1"] = config.get("station1", "ftp_path").replace("\t", "\\t") \
        .replace("\r", "\\r").replace("\n", "\\n")  # ftp路径

    # 读取站点二的信息
    map["name2"] = config.get("station2", "name")
    map["datasource2"]  = config.get("station2", "data_source")  # 获取方式（本地或者ftp）
    map["localpath2"]  = config.get("station2", "local_path").replace("\t", "\\t")\
        .replace("\r", "\\r").replace("\n","\\n")  # 路径
    map["ip2"] = config.get("station2", "ftp_ip")
    map["port2"] = config.get("station2", "ftp_port")
    map["username2"] = config.get("station2", "ftp_username")
    map["password2"] = config.get("station2", "ftp_password")
    map["ftppath2"] = config.get("station2", "ftp_path").replace("\t", "\\t") \
        .replace("\r", "\\r").replace("\n", "\\n")  # ftp路径

    myfile1.close()
    return map


def mkDir(path):
    """
    创建目录文件夹
    :param path: 完整的路径及文件名
    :return:
    """
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)

        print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False


def fileReplace(path,row,str):
    """
    替换文本文件中指定行某一个唯一的字符串
    :param path: 文件路径名称
    :param aa: 第几行
    :param str: 替换的文本
    :return:
    """
    f = open(path,'r+')
    for i in range(len(str),10):
        str += " "

    num = 16+row-1
    for i in range(row-1):
        num +=len(f.readline())

    f.seek(num,0)
    f.write(str)
    f.close()


def getSlope(suzu1,suzu2):
    """
    计算斜率
    :param suzu1:数组1 mjd
    :param suzu2:数组2
    :return: 斜率
    """
    mx = 0
    my = 0
    mdx2 = 0
    mdxdy = 0

    for i in range(0,len(suzu1)):
        mx += (suzu1[i] * 86400 * 1000000000 - mx) / (i + 1.0)
        my +=(suzu2[i]-my)/(i+1.0)


    for i in range(0,len(suzu1)):
        dx = suzu1[i] * 86400 * 1000000000 - mx
        dy = suzu2[i] - my
        mdx2 += (dx * dx - mdx2) / (i + 1.0)
        mdxdy += (dx * dy - mdxdy) / (i + 1.0)

    # number = format(mdxdy/mdx2,'.3e')
    return mdxdy/mdx2


def getStanDeviation(suzu):
    """
    计算标准差
    心法口诀:一组数据中的每个数分别减去这组数据的平均数的差的平方相加起来除以这组数据的个数，就是该组数据的方差，方差再开平方即为标准差
    :param suzu: 数组
    :return: 标准差
    """
    num = 0
    avg = getAvg(suzu)
    for i in suzu:
        num +=(i-avg)*(i-avg)
    return math.sqrt(num/len(suzu))


def getAvg(suzu):
    """
    一个平均数，还要我多说什么
    :param suzu: 数组
    :return: 本数组的平均数
    """
    num = 0
    for i in suzu:
        num +=i
    return num/len(suzu)


def getSquare(x):
    """
    获取一个数值的平方
    :param x: 数值
    :return: 数值的平方
    """
    return x*x


def createDictionary(localpath1,name1,filetype,smjd,emjd):
    """
    根据路径 站点名 文件类型 开始结束时间 创建一个组合起来的字典
    :param localpath1: 文件路径
    :param name1: 站点名称
    :param filetype: 文件类型
    :param smjd: 开始时间
    :param emjd: 结束时间
    :return: 字典
    """
    dirs = os.listdir(localpath1)
    map3 = OrderedDict()
    for i in range(int(smjd),int(emjd)+1):
        for file in dirs:
            if filetype + name1 + str(i) == file.replace(".", ""):
                pathname = localpath1 + "/" + file
                pathname = pathname.replace("\t","\\t").replace("\r","\\r").replace("\n","\\n")
                # map1 = fileToDictionary(pathname) # 弃用旧版的文件转字典  较慢
                map1 = fileToDIC(pathname)  # 启用新版的文件转字典 较快
                lg.mylog("info",pathname+"  字典转换成功长度为："+str(len(map1)))
                print(pathname+"    字典转换成功长度为："+str(len(map1)))
                map3.update(map1)
    print("字典合并成功总长度为："+str(len(map3)))
    lg.mylog("info","字典合并成功总长度为："+str(len(map3)))
    return map3


def readFile(line_number,path):
    """
    解析文本文件（弃用）
    :param line_number: 第几行，行数
    :param path: 文件路径
    :return: 返回这一行的数据特定信息

    """

    f = open(path)
    line = f.readlines()[line_number-1]
    SAT = line[0:3].strip()
    MJD = line[7:12].strip()
    STTIME = line[13:19].strip()
    REFSYS = line[53:64].strip()
    MDTR = line[81:85].strip()
    MDIO = line[91:95].strip()
    MSIO = line[101:105].strip()
    FRC = line[121:124].strip()
    f.close()

    if len(SAT)==2:
        SAT = " "+SAT
    elif len(SAT)==1:
        SAT = " 0"+SAT

    return SAT+"++"+MJD+"++"+STTIME+"++"+REFSYS+"++"+MDTR+"++"+MDIO+"++"+MSIO+"++"+FRC


def fileToDIC(path):
    """
    文件直接转字典
    :param path:
    :return: 字典
    """
    f = open(path)
    i = 0
    list = []
    for line in f:
        i = i + 1
        if i >= 20:
            SAT = line[0:3].strip()
            MJD = line[7:12].strip()
            STTIME = line[13:19].strip()
            REFSYS = line[53:64].strip()
            MDTR = line[81:85].strip()
            MDIO = line[91:95].strip()
            MSIO = line[101:105].strip()
            FRC = line[121:124].strip()
            if FRC =='':
                FRC = "XXX"
            if len(SAT) == 2:
                SAT = " " + SAT
            elif len(SAT) == 1:
                SAT = " 0" + SAT
            str1 = SAT + "++" + MJD + "++" + STTIME + "++" + REFSYS + "++" + MDTR + "++" + MDIO + "++" + MSIO + "++" + FRC
            list.append(str1)
    f.close()

    data1 = OrderedDict()  # 创建有序字典

    list2 = []
    time = ""
    for i in list:
        sat = i.split("++")[0]
        mjd = i.split("++")[1]
        time1 = mjd + "," + i.split("++")[2]
        if time == "":
            time = time1
        sys = i.split("++")[3]
        mdtr = i.split("++")[4]
        mdio = i.split("++")[5]
        msio = i.split("++")[6]
        frc = i.split("++")[7]
        str = ""

        if time != time1:
            data1[time] = list2
            list2 = []
            time = time1
            str += sat + "," + time1.split(",")[1] + "," + sys + "," + mdtr + "," + mdio + "," + msio + "," + frc
            list2.append(str)
        else:
            str += sat + "," + time1.split(",")[1] + "," + sys + "," + mdtr + "," + mdio + "," + msio + "," + frc
            list2.append(str)
            time = time1
    data1[time] = list2
    return data1


def fileToDictionary(path):
    """
    把文本文件转换成字典 （弃用）
    :param path: 文件路径
    :return: 文件字典
    """

    #  data1 = {}  # 创建无序字典
    data1 = OrderedDict()  # 创建有序字典
    list = []  # 创建列表

    file = open(path)
    i = 20
    time = ""

    try:
        while True:
            lin = file.readline()
            if not lin:
                break
            else:
                strs = readFile(i, path)
                sat = strs.split("++")[0]
                mjd = strs.split("++")[1]
                time1 = mjd+","+strs.split("++")[2]
                sys = strs.split("++")[3]
                mdtr = strs.split("++")[4]
                mdio = strs.split("++")[5]
                msio = strs.split("++")[6]
                frc = strs.split("++")[7]

                if time == "":
                    time = time1
                    str = ""
                    str += sat + ","
                    str += time1.split(",")[1] + ","
                    str += sys + ","
                    str += mdtr + ","
                    str += mdio + ","
                    str += msio + ","
                    str += frc
                    list.append(str)

                    #  print(sat + "---" + time1 + "--" + sys)

                elif time1 == time:

                    str = ""
                    str += sat + ","
                    str += time1.split(",")[1] + ","
                    str += sys + ","
                    str += mdtr + ","
                    str += mdio + ","
                    str += msio + ","
                    str += frc
                    list.append(str)

                    # print(sat + "---" + time1 + "--" + sys)

                else:
                    data1[time] = list
                    time = time1
                    list = []

                    str = ""
                    str += sat + ","
                    str += time1.split(",")[1] + ","
                    str += sys + ","
                    str += mdtr + ","
                    str += mdio + ","
                    str += msio + ","
                    str += frc
                    list.append(str)
            i += 1
    except:
        data1[time] = list
    file.close()
    #print(data1)
    return data1


def myFormat(val): # 失效 已被内置函数取代
    """
    返回科学计数法表示形式并保留3位小数
    :param val: 数值
    :return:
    """

    val = ("%20e" % val).split("e")
    val1 = ("%.3f" % float(val[0]))
    return str(val1)+"e"+val[1]


def creatALChart(outpath,x,y,max_y,min_y,lable="MDEV",xlable="Averaging Time (s)",ytable="mod allan"):
    """
    生成allan图片
    :param outpath: 输出路径
    :param x: x轴数据 type:数组
    :param y: y轴数据 type:数组
    :param max_y:  最大值数据 type:数组
    :param min_y:  最小值数据 type:数组
    :param lable:  图例名称
    :param xlable: x轴名称
    :param ytable: y轴名称
    :return:
    """
    # yerr = []
    # for i in range(len(y)):
    #     if min_y[i]==0:
    #         yerr.append(0)
    #     else:
    #         y1 = max_y[i]-y[i]
    #         yerr.append(y1)

    yavl4 = []
    yerr = []
    for i in range(len(y)):
        a = (max_y[i] + min_y[i]) / 2
        yavl4.append(a)
        yerr.append(a - min_y[i])

    ax = plt.subplot(111, xscale="log", yscale="log")

    plt.errorbar(x, yavl4, yerr=yerr, zorder=3, fmt="r.", markersize=2, alpha=0.5)

    plt.errorbar(x, y, fmt='-ro',mfc="w" , alpha=0.5,label=lable,elinewidth=0.5,linewidth=1,markersize=4)

    plt.errorbar(x, min_y,  zorder=3, fmt="r_")

    plt.errorbar(x, max_y,  zorder=3, fmt="r_")

    plt.xlabel(xlable)


    if lable=="MDEV":
        plt.title("FREQUENCY STABILITY")
        plt.ylabel("Modified Allan Deviation(s)")
    else:
        plt.title("TIME STABILITY")
        plt.ylabel("Time Deviation(s)")


    #设置刻度
    max = max_y
    min = min_y
    max.extend(min)
    max.extend(y)
    max.sort()
    # print(max)
    minnum = 0
    maxnum = max[len(max) - 1]
    for i in max:
        if i != 0:
            minnum = i
            break
    # print(minnum, maxnum)
    s = str("%e" % minnum).split("e")
    minnum = pow(10, int(s[1]))
    s = str("%e" % maxnum).split("e")
    maxnum = pow(10, int(s[1]) + 1)
    plt.ylim(ymin=minnum, ymax=maxnum)

    plt.legend(framealpha=0.5)
    # plt.grid(True, linestyle = "-.")
    ax.xaxis.grid(True, which='both', linestyle="--")  # x坐标轴的网格使用主刻度
    ax.yaxis.grid(True, which='both', linestyle="--")  # y坐标轴的网格使用次刻度
    plt.savefig(outpath)
    plt.clf()  # 清除图形


def creatTDChart(x1,y1,outpath,avg,sd,slope,color,type):
    """
    生成时差图
    :param x1: x轴时间
    :param y1: y轴数据
    :param outpath: 输出图片路径
    :param avg: 平均值
    :param sd:  标准差
    :param slope: 相对频率偏差
    :param color: 线条颜色
    :param type:
        S1 站点一
        S2 站点二
        Di 差值
    :return:
    """
    plt.plot(x1, y1, label='Frist line', linewidth=1, color=color, marker='.')

    a = int(x1[0])
    b = int(x1[-1])+1
    # print("时间范围：",a,b)

    ax = plt.gca()
    ax.set_xticks(np.linspace(a, b, b-a+1))
    c = ()
    for i in range(a,b+1):
        y = (str(i),)
        c = c+y
    print("开始生成图片时间范围："+str(c))
    lg.mylog("info","开始生成图片时间范围："+str(c))
    ax.set_xticklabels(c)

    suzuy = []
    for i in ax.get_yticks():
        suzuy.append(i)

    cha = suzuy[1] - suzuy[0]
    a = suzuy[0]
    b = suzuy[-1]

    if len(suzuy) >= 2:
        suzuy.append(a - cha)
        suzuy.append(a - cha * 2)
        suzuy.append(b + cha)
        suzuy.append(b + cha * 2)
    suzuy.sort()

    c = ()
    ax.set_yticks(np.linspace(suzuy[0], suzuy[-1], len(suzuy) / 2))
    for i in ax.get_yticks():
        a = (str(round(i,1)),)
        c = c + a
    ax.set_yticklabels(c)


    map = readConf()
    view = "共视" if map["view"] == "CV" else "全视"

    plt.xticks(rotation=45)  # 这里的rotation，当名称展示时候，一个倾斜的角度，当文案很长时候特别好用
    plt.xlabel('时间(MJD)',fontproperties=zhfont1)
    plt.ylabel('纳秒(ns)',fontproperties=zhfont1)
    if type=="Di":
        plt.title('(' + view + ')' + map["name1"] + '站与' + map["name2"] + '站' + map["datatype"] +
                  '差值\n均值=' + avg + '(ns),标准差=' + sd + '(ns)，相对频率偏差=' + slope, fontproperties=zhfont1)
    elif type=="S1":
        plt.title('(' + view + ')' + map["name1"] + '站点'+ map["datatype"] +'原始数据'+
                  '\n均值=' + avg + '(ns),标准差=' + sd + '(ns)，相对频率偏差=' + slope, fontproperties=zhfont1)
    else:
        plt.title('(' + view + ')' + map["name2"] + '站点'+ map["datatype"] +'原始数据'+
                  '\n均值=' + avg + '(ns),标准差=' + sd + '(ns)，相对频率偏差=' + slope, fontproperties=zhfont1)

    # plt.legend()
    plt.grid(True, linestyle = "-.")
    #plt.show()
    plt.subplots_adjust(bottom=0.2)  # 设置折线图和底部区域的距离
    plt.savefig(outpath)
    plt.clf()  # 清除图形


def deletFile(path):
    """
    删除文件
    :param path:
    :return:
    """
    if os.path.exists(path):
        # 删除文件，可使用以下两种方法。
        os.remove(path)
        # os.unlink(my_file)

    else:
        print("文件删除失败")
# print(myFormat(505.95400000000003))

def fit_func(p, x):
    # 多项式函数
    f = np.poly1d(p)
    return f(x)
def residuals_func(p, y, x):
    # 残差函数
    ret = fit_func(p, x) - y
    return ret
def getCurveFitting(x,y,n=3):
    """
    最小二乘法曲线拟合
    :param x: x轴数据
    :param y: y轴数据
    :param n: 多项式次数
    :return: 需要剔除的下标
    """
    print("开始 拉伊达法则剔除数据")
    lg.mylog("info","开始 拉伊达法则剔除数据")
    p_init = np.random.randn(n)  # 随机初始化多项式参数

    bzc = getStanDeviation(y) # 标准差 0.9515194755243933

    plsq = leastsq(residuals_func, p_init, args=(y, x))[0]
    x1 = [] # 剔除的下标
    # y1 = [] # 剔除数据
    for i in range(len(x)):
        a = plsq[0]*pow(x[i],n-1)+plsq[1]*pow(x[i],n-2)+plsq[2]*pow(x[i],n-3)-y[i]
        if abs(a)>=bzc*3:
            print(i,"--",x[i],"剔除",y[i])
            lg.mylog("info", "["+str(i)+"]  "+str(x[i])+" 剔除 "+str(y[i]))
            x1.append(i)
            # y1.append(i)
    # for i in x1:
    #     x.remove(i)
    # for i in y1:
    #     y.remove(i)
    print("剔除完毕")
    lg.mylog("info","剔除完毕")
    return (x1)


def ftpDownload(ip,port,name,pwd,ftpPath,localPath,statname):
    """
    ftp 文件下载
    :param ip: ip地址
    :param port: 端口号
    :param name: 用户名
    :param pwd: 密码
    :param ftpPath: ftp路径
    :param localPath: 本地路径
    :param statname: 站点名称
    :return: null
    """
    Path = ""
    map = readConf()
    type = map["filetype"]
    sjd = int(map["smjd"])
    ejd = int(map["emjd"])

    try:
        f = ftplib.FTP()  # 实例化FTP对象
        f.connect(ip, port)
        f.login(name, pwd)  # 登录
        f.cwd(ftpPath) #设置ftp当前路径
        bufsize = 1024  # 设置缓冲器大小

        # print(f.nlst())
        for i in f.nlst():
            for y in range(sjd,ejd+1):
                if type+statname+str(y) == i.replace(".", ""):
                    Path = ftpPath+"/"+i
                    fp = open(localPath + "/" + i, 'wb')
                    f.retrbinary('RETR %s' % Path, fp.write, bufsize)
                    print(Path, "下载成功")
                    fp.close()
        f.quit()
    except:
        print(Path,"下载失败")
        sys.exit()


def remFile(path):
    """
    清空文件夹
    :param path:
    :return:
    """
    for i in os.listdir(path):
        path_file = os.path.join(path, i) # 取文件绝对路径
        if os.path.isfile(path_file):
            os.remove(path_file)
        else:
            remFile(path_file)



