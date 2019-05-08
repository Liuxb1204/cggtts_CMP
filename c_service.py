import matplotlib.pyplot as plt
from collections import OrderedDict
import myutils.date as d
import datetime
import c_logg as lg
import math
import os, sys
import allantools.c_allantools as allan
import myutils.util as util
import myutils.creatPDF as pdf


arithmetic = "MDEV"     # 算法
versions = "1.1"        # 版本号
conf = util.readConf()  # 配置文件
tau = 960               # 我是谁？我在那？我叫啥？



def getFileHead(path,line_number,num):
    """
    读取文件头的几行参数信息
    :param : 文件路径,第几行，第几个字符到第几个字符之间
    :return: 文件头数据

    """
    f = open(path)
    a = num.split(",")[0]
    b = num.split(",")[1]
    line = f.readlines()[line_number-1]
    STR = line[int(a):int(b)].strip()
    f.close()
    return STR

# 卫星剔除
def removeByCV(mapmap1,mapmap2):
    """
    共视法 针对卫星剔除
    :param mapmap1: 站点一数据
    :param mapmap2: 站点二数据
    :return:
    """
    print("开始剔除单个卫星")
    lg.mylog("info", "开始剔除单个卫星")
    tichu = OrderedDict()  # 创建字典获取两个站点同一时间共同的卫星

    for k in mapmap1:
        k1 = mapmap1[k]
        list2 = [] #用于存放当前时间某一个站点拥有的卫星
        ss = 0 #两个站点共同卫星差值的和
        if k in mapmap2.keys():  # 判断站点一的时间是否存在于站点二
            y1 = mapmap2[k]
            for z in y1:
                list2.append(z.split(":")[0][-2:]) # 放入站点二的卫星
            gesu = 0 #共同卫星的个数
            sti1num = 0
            sti2num = 0
            y = 0 #下标位置
            strdif = []
            for i in range(len(k1)):    #遍历站点一的卫星
                kk1 = k1[i].split(":")[0]   #站点一的卫星编号
                sti1 = float(k1[i].split(":")[1])   #站点一的卫星数据
                # sti1num += sti1
                if kk1[-2:] in list2: #如果站点一当前的卫星也存在于另一个站点里  就是共同卫星
                    gesu += 1
                    for jj in list2: #获取当前卫星在另一个站点的卫星数组里的下标位置
                        if kk1[-2:] in jj:
                            y = list2.index(jj)
                            break
                    sti2 = float(y1[y].split(":")[1]) #通过下标位置获取站点二对应卫星的卫星数据
                    # sti2num += sti2
                    ss += (sti1 - sti2)
                    # y += 1
                    strdif.append(kk1[-2:]+":"+str(round(sti1-sti2,3)))
            # print(k,gesu)
            if gesu!=0:
                tichu[k+":"+str(round(ss/gesu,3))]=strdif
        else:
            continue


    # tichumap = OrderedDict()

    # 开始剔除卫星
    for t in tichu:
        t1 = tichu[t]
        if len(t1) > 3:
            suzu1 = []
            for i in t1:
                suzu1.append(float(i.split(":")[1]))
            bzc1 = util.getStanDeviation(suzu1)  # 原始标准差

            max = float(t1[0].split(":")[1]) #数组最大值
            min = float(t1[0].split(":")[1]) #数组最小值
            maxstr = t1[0]
            minstr = t1[0]
            for i in t1: #获取最大值和最小值
                if float(i.split(":")[1]) > max:
                    max = float(i.split(":")[1])
                    maxstr = i
                elif float(i.split(":")[1])<min:
                    min = float(i.split(":")[1])
                    minstr = i

            t1.remove(maxstr) #删除最大值
            suzu2 = []
            for i in t1:
                suzu2.append(float(i.split(":")[1]))
            bzc2 = util.getStanDeviation(suzu2)  # 剔除最大值标准差
            prnstr = "" # 要剔除的卫星
            if bzc1 > bzc2 * 6:
                prnstr = maxstr.split(":")[0]
                print(t.split(":")[0], "最大值剔除卫星", maxstr.split(":")[0])
                lg.mylog("info",t.split(":")[0]+" 最大值剔除卫星 "+maxstr.split(":")[0])
            if prnstr!="" and len(prnstr)>0:
                for y in mapmap1[t.split(":")[0]]:
                    if y.split(":")[0][-2:] == prnstr[-2:]:
                        mapmap1[t.split(":")[0]].remove(y)
                        break
                for y in mapmap2[t.split(":")[0]]:
                    if y.split(":")[0][-2:] == prnstr[-2:]:
                        mapmap2[t.split(":")[0]].remove(y)
                        break

            t1.append(maxstr) #添加最大值 恢复原数组
            t1.remove(minstr) #删除最小值
            suzu2 = []
            for i in t1:
                suzu2.append(float(i.split(":")[1]))
            bzc2 = util.getStanDeviation(suzu2)  # 剔除最小值标准差
            prnstr = ""  # 要剔除的卫星
            if bzc1 > bzc2 * 6:
                prnstr = minstr.split(":")[0]
                print(t.split(":")[0], "最小值剔除卫星", minstr.split(":")[0])
                lg.mylog("info",t.split(":")[0]+" 最小值剔除卫星 "+minstr.split(":")[0])
            if prnstr!="" and len(prnstr)>0:
                for y in mapmap1[t.split(":")[0]]:
                    if y.split(":")[0][-2:] == prnstr[-2:]:
                        mapmap1[t.split(":")[0]].remove(y)
                        break
                for y in mapmap2[t.split(":")[0]]:
                    if y.split(":")[0][-2:] == prnstr[-2:]:
                        mapmap2[t.split(":")[0]].remove(y)
                        break

#     for t in tichu:
#         t1 = tichu[t]
#         if len(t1)>3:
#             num = 0
#             prnstr = []
#             for i in t1:
#                 num += round(util.getSquare(float(i.split(":")[1]) - float(t.split(":")[1])),3)
#             biaozc = round(math.sqrt(num/len(t1)),3) # 标准差
#             for y in t1:
#                 aa = round(float(y.split(":")[1]) - float(t.split(":")[1]),3)
#                 if aa >= biaozc * 3:  #大于等于三倍的标准差
#                     print(t.split(":")[0]+":"+y.split(":")[0]+"号卫星已剔除")
#                     prnstr.append(y.split(":")[0])
#                     tichumap[t.split(":")[0]]=prnstr


    # for t in tichu:
    #     t1 = tichu[t]
    #     if len(t1)>3:
    #         max = float(t1[0].split(":")[1])
    #         maxstr = t1[0]
    #         for i in t1:
    #             if float(i.split(":")[1]) > max:
    #                 max = float(i.split(":")[1])
    #                 maxstr = i
    #         t1.remove(maxstr)
    #         suzu = []
    #         for i in t1:
    #             suzu.append(float(i.split(":")[1]))
    #         bzc = util.getStanDeviation(suzu)  # 标准差
    #         avg = util.getAvg(suzu)  # 平均值
    #         prnstr = []
    #         if max - avg >= bzc * 3:
    #             print(t.split(":")[0], "剔除卫星", maxstr.split(":")[0])
    #             prnstr.append(maxstr.split(":")[0])
    #         if len(prnstr) > 0:
    #             tichumap[t.split(":")[0]] = prnstr

    lg.mylog("info","卫星剔除完毕...")
    print("卫星剔除完毕")
    return mapmap1,mapmap2


def outputByCV(mapmap1,mapmap2,name1,name2,datatype,sysnum,mdtrnum,mdionum,msionum,path1,path2):
    """
    计算两个站点差值并输出文件
    :param mapmap1: 字典一
    :param mapmap2: 字典二
    :param name1: 站点名称
    :param name2:
    :param datatype: 数据类型
    :param sysnum:
    :param mdtrnum:
    :param mdionum:
    :param msionum:
    :param path1: 站点一路径
    :param path2: 站点二路径
    :return:
    """
    print("开始比对站点数据，并写出文件")
    lg.mylog("info", "开始比对站点数据，并写出文件")
    now_time = str(datetime.datetime.now()).split(".")[0]

    # 创建目录（文件夹）
    path = conf["outpath"]+"/RESULT_"+conf["name1"]+"_"+conf["name2"]\
           +"_"+conf["datatype"]+"_"+conf["view"]+"_"\
           +now_time.replace("-","").replace(" ","").replace(":","")[2:14]
    util.mkDir(path)

    # 写出文件
    file1path = path +"/TIMEDIFF_"+conf["name1"]+"_"+conf["name2"]+".txt"
    file1 = open(file1path, "w")
    print("开始写入文件"+file1path)
    lg.mylog("info","开始写入文件"+file1path)
    file1.write("/****************************************************\n")
    file1.write(" *CGGTTS DATA COMPARE FORMAT VERSION: " + versions + "\n") #软件版本号
    file1.write(" *Creator:      "+"Navcompass"+"\n")
    file1.write(" *CreateTime:   "+now_time+"\n")

    file1.write(" *Base1 Info: \n" +
                "    Name:       " + name1 + "\n" +
                "    CGG Ver:    " + getFileHead(path1+"/"+os.listdir(path1)[0],1,"41,43") + "\n" +
                "    RCVR:       " + getFileHead(path1+"/"+os.listdir(path1)[0],3,"7,46") + "\n" +
                "    X/Y/Z:      " + getFileHead(path1+"/"+os.listdir(path1)[0],7,"4,16")+"/"
                                   + getFileHead(path1+"/"+os.listdir(path1)[0],8,"4,16")+"/"
                                   + getFileHead(path1+"/"+os.listdir(path1)[0],9,"4,16")+ "\n" +
                "    INT DLY:    " + getFileHead(path1+"/"+os.listdir(path1)[0],12,"10,67") + "\n" +
                "    CAB DLY:    " + getFileHead(path1+"/"+os.listdir(path1)[0],13,"10,17") + "\n" +
                "    REF DLY:    " + getFileHead(path1+"/"+os.listdir(path1)[0],14,"10,17") + "\n" +
                "    REF Name:   " + getFileHead(path1+"/"+os.listdir(path1)[0],15,"6,15") + "\n" +
                "    TIME AVG:   " + "----------" + "ns\n" +
                "    SD:         " + "----------" + "ns\n" +
                "    SLOPE:      " + "----------" + "\n")

    file1.write(" *Base2 Info: \n" +
                "    Name:       " + name2 + "\n" +
                "    CGG Ver:    " + getFileHead(path2 + "/" + os.listdir(path2)[0], 1, "41,43") + "\n" +
                "    RCVR:       " + getFileHead(path2 + "/" + os.listdir(path2)[0], 3, "7,46") + "\n" +
                "    X/Y/Z:      " + getFileHead(path2 + "/" + os.listdir(path2)[0], 7, "4,16") + "/"
                                   + getFileHead(path2 + "/" + os.listdir(path2)[0], 8, "4,16") + "/"
                                   + getFileHead(path2 + "/" + os.listdir(path2)[0], 9, "4,16") + "\n" +
                "    INT DLY:    " + getFileHead(path2 + "/" + os.listdir(path2)[0], 12, "10,67") + "\n" +
                "    CAB DLY:    " + getFileHead(path2 + "/" + os.listdir(path2)[0], 13, "10,17") + "\n" +
                "    REF DLY:    " + getFileHead(path2 + "/" + os.listdir(path2)[0], 14, "10,17") + "\n" +
                "    REF Name:   " + getFileHead(path2 + "/" + os.listdir(path2)[0], 15, "6,15") + "\n" +
                "    TIME AVG:   " + "----------" + "ns\n" +
                "    SD:         " + "----------" + "ns\n" +
                "    SLOPE:      " + "----------" + "\n")

    file1.write(" *Style:        "+"Common View"+"\n")
    file1.write(" *Data Type:    "+datatype+"\n")
    file1.write(" *Comp Mode:    "+"REFSYS*"+str(sysnum)+" + MDTR*"+str(mdtrnum)+" + MDIO*" +str(mdionum)+" + MSIO*"+str(msionum) + "\n")
    file1.write(" *Difference Result:"+"\n"+
                "    TIME AVG:   " + "----------" + "ns\n" +
                "    SD:         " + "----------" + "ns\n" +
                "    SLOPE:      " + "----------" + "\n")
    file1.write("****************************************************/\n\n\n")
    file1.write(("%20s" % "YYYY-MM-DD HH:mm:SS")+("%15s" % "MJD")+("%18s" % "Base1_Data")+("%18s" % "Base2_Data")+
                ("%18s" % "Difference")+("%5s" % "     ")+("%-45s" % "Base1_Satellite")+("%-45s" % "Base2_Satellite")+("%-45s" % "Common_Satellite")+"\n\n")

    datelist = [] #mjd日期数组
    sumlist1 = [] #站点一数据
    sumlist2 = [] #沾点二数据
    diflist = [] # 差值 ns
    diflist2 = [] # 差值 s
    filelist = []
    for k in mapmap1:
        commonstrweixing = ""
        sta1weixing = ""
        sta2weixing = ""
        k1 = mapmap1[k]
       # print(k+"------")
        datek = d.mjdToTime(k.split(",")[0],k.split(",")[1])
        list2 = []
        ss = 0
        if k in mapmap2.keys():#判断key是否存在
            y1 = mapmap2[k]

            for z in y1:
                list2.append(z.split(":")[0][-2:])
                sta2weixing+=z.split(":")[0]

            gesu = 0
            sti1num = 0
            sti2num = 0

            y = 0
            for i in range(len(k1)):
                kk1 = k1[i].split(":")[0]
                sta1weixing+=kk1
                sti1 = float(k1[i].split(":")[1])
                if kk1[-2:] in list2:
                    sti1num += sti1
                    gesu+=1
                    for jj in list2:
                        if kk1[-2:] in jj:
                            y =list2.index(jj)
                            break
                    sti2 = float(y1[y].split(":")[1])
                    sti2num += sti2
                    ss += (sti1 - sti2)
                    commonstrweixing += kk1
                    y += 1

            if gesu==0:
               # file1.write("   -------------除数不能为0------------"+"\n")
                continue

            str1 = ""
            # file1.write("%20s" % datek)
            str1+="%20s" % datek
            # file1.write("%15s" % d.timeToMJD(k.split(",")[0],k.split(",")[1]))
            str1+="%15s" % d.timeToMJD(k.split(",")[0],k.split(",")[1])
            datelist.append(float(d.timeToMJD(k.split(",")[0],k.split(",")[1]))) #mjd日期数组添加元素
            # file1.write("%18.3f" % (sti1num/gesu))
            str1+="%18.3f" % (sti1num/gesu)
            sumlist1.append(sti1num/gesu) # 站点一数据数组

            # file1.write("%18.3f" % (sti2num/gesu))
            str1+="%18.3f" % (sti2num/gesu)
            sumlist2.append(sti2num / gesu) # 站点二数据数组

            # file1.write("%18.3f" % (ss/gesu))
            str1+="%18.3f" % (ss/gesu)
            diflist.append((ss/gesu/1e9))
            diflist2.append(ss/gesu)

            # file1.write("%5s" % "     ")
            str1+="%5s" % "     "
            # file1.write("%-45s" % sta1weixing)
            str1+="%-45s" % sta1weixing
            # file1.write("%-45s" % sta2weixing)
            str1+="%-45s" % sta2weixing
            # file1.write("%-45s" % commonstrweixing+"\n")
            str1+="%-45s" % commonstrweixing
            filelist.append(str1)
        else:
            continue

    # 拉伊达法则剔除
    if conf["tichu2"] == "1":
        x3 = util.getCurveFitting(x=datelist, y=diflist2)
        for i in x3:
            datelist.pop(i)
            sumlist1.pop(i)
            sumlist2.pop(i)
            diflist2.pop(i)
            diflist.pop(i)
            filelist.pop(i)

    for i in filelist:
        file1.write(i+"\n")
    lg.mylog("info", "文件写入完毕" + file1path)
    print("文件写入完毕：" + file1path)
    file1.close()



    list1num = 0
    for i in sumlist1:
        list1num += i # 求和
    util.fileReplace(file1path,14,str(round(list1num/len(sumlist1),2)))
    util.fileReplace(file1path, 15,str(round(util.getStanDeviation(sumlist1),2)))
    util.fileReplace(file1path, 16, str(format(util.getSlope(datelist,sumlist1),'.3e')))
    util.creatTDChart(datelist, sumlist1, path + "/sta1.jpg", str(round(list1num / len(sumlist1), 2)),
        str(round(util.getStanDeviation(sumlist1), 2)),str(format(util.getSlope(datelist, sumlist1), '.3e')),'g','S1')

    list1num = 0
    for i in sumlist2:
        list1num += i  #  求和
    util.fileReplace(file1path, 26, str(round(list1num / len(sumlist2), 2)))
    util.fileReplace(file1path, 27, str(round(util.getStanDeviation(sumlist2), 2)))
    util.fileReplace(file1path, 28, str(format(util.getSlope(datelist, sumlist2), '.3e')))
    util.creatTDChart(datelist, sumlist2, path + "/sta2.jpg", str(round(list1num / len(sumlist2), 2)),
        str(round(util.getStanDeviation(sumlist2), 2)),str(format(util.getSlope(datelist, sumlist2), '.3e')),'b','S2')

    list1num = 0
    for i in diflist2:
        list1num += i  # 求和
    util.fileReplace(file1path, 33, str(round(list1num / len(diflist2), 2)))
    util.fileReplace(file1path, 34, str(round(util.getStanDeviation(diflist2), 2)))
    util.fileReplace(file1path, 35, str(format(util.getSlope(datelist, diflist2), '.3e')))
    util.creatTDChart(datelist, diflist2, path + "/diff.jpg", str(round(list1num / len(diflist2), 2)),
        str(round(util.getStanDeviation(diflist2), 2)),str(format(util.getSlope(datelist, diflist2), '.3e')),'r','Di')



    # 获取一下当前时间
    now_time = str(datetime.datetime.now()).split(".")[0]
    now_time = now_time.replace("-", "").replace(" ", "").replace(":", "")


    diflist2.sort()
    a = 0
    for i in diflist2:
        a +=i
    # 写出文件
    file2path = path+"/ALLAN_MDEV_"+conf["name1"]+"_"+conf["name2"]+".txt"
    file2 = open(file2path, "w")
    file2.write("/****************************************************\n")
    file2.write(" *CGGTTS DATA COMPARE FORMAT VERSION: " + versions + "\n")  # 软件版本号
    file2.write(" *Creator:       " + "Navcompass" + "\n")
    file2.write(" *Sigma Type:    " + "Modified Allan Deviation" + "\n")
    file2.write(" *Base1 Name:    " + conf["name1"] + "\n")
    file2.write(" *Base2 Name:    " + conf["name2"] + "\n")
    file2.write(" *CreateTime:    " + str(datetime.datetime.now()).split(".")[0] + "\n")
    file2.write(" *Diff Max Data: " + str(round(diflist2[len(diflist2)-1],2)) + " ns\n")
    file2.write(" *Diff Min Data: " + str(round(diflist2[0],2)) + " ns\n")
    file2.write(" *Diff Avg Data: " + str(round(a/len(diflist2),2)) + " ns\n")
    file2.write(" *Conf Factor:   " + "0.683" + "\n")
    file2.write("****************************************************/\n\n")
    file2.write(
        ("%10s" % "AF") + ("%15s" % "TAU") + ("%15s" % "#") + ("%20s" % "Min_Sigma") +
        ("%20s" % "Mod_Sigma") + ("%20s" % "Max_Sigma")+"\n\n")

    data1 = OrderedDict()  # 创建有序字典
    rate1 = 1 / float(tau)  # 1 PPS measurements, data interval is 1 s
    (taus, devs, errs, ns) = allan.mdev(diflist, rate=rate1, data_type="phase", taus="octave")
    min = []
    max = []
    for i in range(len(taus)):
        dev = devs[i]
        list1 = []  # 创建列表
        try:
            (lo2, hi2) = allan.confidence_interval_noiseID(diflist, dev, af=int(taus[i]*rate1), dev_type="mdev", data_type="phase")
           # print("tau:",taus[i],"num:",ns[i],"Min_Sigma:",lo2,"Mod_Sigma",devs[i],"Max_Sigma:",hi2)
            min.append(lo2)
            max.append(hi2)
            file2.write("%10s" % str(int(taus[i])/tau))
            file2.write("%15s" % taus[i])
            file2.write("%15s" % ns[i])
            file2.write("%20s" % format(lo2,".3e"))
            file2.write("%20s" % format(devs[i],'.3e'))
            file2.write("%20s" % format(hi2,'.3e'))
            file2.write("\n")

            list1.append(str(int(taus[i]) / tau))
            list1.append(taus[i])
            list1.append(ns[i])
            list1.append(format(lo2, '.3e'))
            list1.append(format(devs[i], '.3e'))
            list1.append(format(hi2, '.3e'))
        except NotImplementedError:
            print("无法计算：",taus[i])
            min.append(0)
            max.append(0)
            file2.write("%10s" % str(int(taus[i]) / tau))
            file2.write("%15s" % taus[i])
            file2.write("%15s" % ns[i])
            file2.write("%20s" % "      -     ")
            file2.write("%20s" % format(devs[i],'.3e'))
            file2.write("%20s" % "      -     ")
            file2.write("\n")

            list1.append(str(int(taus[i]) / tau))
            list1.append(taus[i])
            list1.append(ns[i])
            list1.append("  -  ")
            list1.append(format(devs[i], '.3e'))
            list1.append("  -  ")
        except:
            print("未知错误，无法计算：", taus[i])
            min.append(0)
            max.append(0)
            file2.write("%10s" % str(int(taus[i]) / tau))
            file2.write("%15s" % taus[i])
            file2.write("%15s" % ns[i])
            file2.write("%20s" % "      -     ")
            file2.write("%20s" % format(devs[i], '.3e'))
            file2.write("%20s" % "      -     ")
            file2.write("\n")

            list1.append(str(int(taus[i]) / tau))
            list1.append(taus[i])
            list1.append(ns[i])
            list1.append("  -  ")
            list1.append(format(devs[i], '.3e'))
            list1.append("  -  ")
        data1[str(int(taus[i]) / tau)] = list1
    file2.close()
    print("文件写入完毕"+file2path)
    lg.mylog("info", "文件写入完毕" + file2path)
    # ALLAN画图
    util.creatALChart(path + "/mdevallan.jpg", taus, devs, max, min, lable="MDEV")


    # 写出文件
    file3path = path + "/ALLAN_TDEV_" + conf["name1"] + "_" + conf["name2"] + ".txt"
    file3 = open(file3path, "w")
    file3.write("/****************************************************\n")
    file3.write(" *CGGTTS DATA COMPARE FORMAT VERSION: " + versions + "\n")  # 软件版本号
    file3.write(" *Creator:       " + "Navcompass" + "\n")
    file3.write(" *Sigma Type:    " + "Time Deviation" + "\n")
    file3.write(" *Base1 Name:    " + conf["name1"] + "\n")
    file3.write(" *Base2 Name:    " + conf["name2"] + "\n")
    file3.write(" *CreateTime:    " + str(datetime.datetime.now()).split(".")[0] + "\n")
    file3.write(" *Diff Max Data: " + str(round(diflist2[len(diflist2) - 1], 2)) + " ns\n")
    file3.write(" *Diff Min Data: " + str(round(diflist2[0], 2)) + " ns\n")
    file3.write(" *Diff Avg Data: " + str(round(a / len(diflist2), 2)) + " ns\n")
    file3.write(" *Conf Factor:   " + "0.683" + "\n")
    file3.write("****************************************************/\n\n")
    file3.write(
        ("%10s" % "AF") + ("%15s" % "TAU") + ("%15s" % "#") + ("%20s" % "Min_Sigma") +
        ("%20s" % "Mod_Sigma") + ("%20s" % "Max_Sigma") + "\n\n")
    data2 = OrderedDict()  # 创建有序字典
    (taus2, devs2, errs, ns) = allan.tdev(diflist, rate=rate1, data_type="phase", taus="octave")
    min = []
    max = []
    for i in range(len(taus2)):
        dev = devs2[i]
        list1 = []  # 创建列表
        try:
            (lo2, hi2) = allan.confidence_interval_noiseID(diflist, dev, af=int(taus2[i] * rate1), dev_type="tdev",
                                                           data_type="phase")
            # print("tau:",taus[i],"num:",ns[i],"Min_Sigma:",lo2,"Mod_Sigma",devs[i],"Max_Sigma:",hi2)
            min.append(lo2)
            max.append(hi2)
            file3.write("%10s" % str(int(taus2[i]) / tau))
            file3.write("%15s" % taus2[i])
            file3.write("%15s" % ns[i])
            file3.write("%20s" % format(lo2, ".3e"))
            file3.write("%20s" % format(devs2[i], '.3e'))
            file3.write("%20s" % format(hi2, '.3e'))
            file3.write("\n")
            list1.append(str(int(taus2[i]) / tau))
            list1.append(taus2[i])
            list1.append(ns[i])
            list1.append(format(lo2, '.3e'))
            list1.append(format(devs2[i], '.3e'))
            list1.append(format(hi2, '.3e'))
        except NotImplementedError:
            min.append(0)
            max.append(0)
            file3.write("%10s" % str(int(taus2[i]) / tau))
            file3.write("%15s" % taus2[i])
            file3.write("%15s" % ns[i])
            file3.write("%20s" % "      -     ")
            file3.write("%20s" % format(devs2[i], '.3e'))
            file3.write("%20s" % "      -     ")
            file3.write("\n")
            list1.append(str(int(taus2[i]) / tau))
            list1.append(taus2[i])
            list1.append(ns[i])
            list1.append("  -  ")
            list1.append(format(devs2[i], '.3e'))
            list1.append("  -  ")
        except:
            min.append(0)
            max.append(0)
            file3.write("%10s" % str(int(taus2[i]) / tau))
            file3.write("%15s" % taus2[i])
            file3.write("%15s" % ns[i])
            file3.write("%20s" % "      -     ")
            file3.write("%20s" % format(devs2[i], '.3e'))
            file3.write("%20s" % "      -     ")
            file3.write("\n")
            list1.append(str(int(taus2[i]) / tau))
            list1.append(taus2[i])
            list1.append(ns[i])
            list1.append("  -  ")
            list1.append(format(devs2[i], '.3e'))
            list1.append("  -  ")
        data2[str(int(taus2[i]) / tau)] = list1
    file3.close()
    print("文件写入完毕" + file3path)
    lg.mylog("info", "文件写入完毕" + file3path)
    util.creatALChart(path + "/tdevallan.jpg", taus2, devs2, max, min, lable="TDEV")

    # 生成pdf文档
    if conf["generatepdf"]=="1":
        pdf.creatPDF(path, data2, data1)

    # 善后
    util.deletFile(path + "/sta1.jpg")
    util.deletFile(path + "/sta2.jpg")
    util.deletFile(path + "/diff.jpg")
    util.deletFile(path + "/tdevallan.jpg")
    util.deletFile(path + "/mdevallan.jpg")


def outputByAV(mapmap1,mapmap2,name1,name2,datatype,path,path1,path2):
    """
    计算两个站点差值并输出文件
    :param mapmap1: 字典一
    :param mapmap2: 字典二
    :param name1: 站点名称
    :param name2:
    :param datatype: 数据类型
    :param path: 输出路径
    :param path1: 站点一路径
    :param path2: 站点二路径
    :return:
    """
    # 获取当前时间
    now_time = str(datetime.datetime.now()).split(".")[0]

    # 创建目录（文件夹）
    path = conf["outpath"] + "/RESULT_" + conf["name1"] + "_" + conf["name2"] \
           + "_" + conf["datatype"] + "_" + conf["view"] + "_" \
           + now_time.replace("-", "").replace(" ", "").replace(":", "")[2:14]
    util.mkDir(path)

    # 写出文件
    file1path = path + "/TIMEDIFF_" + conf["name1"] + "_" + conf["name2"] + ".txt"
    file1 = open(file1path, "w")
    lg.mylog("info", "创建文件成功开始写出文件")
    file1.write("/****************************************************\n")
    file1.write(" *CGGTTS DATA COMPARE FORMAT VERSION: " + versions + "\n")  # 软件版本号
    file1.write(" *Creator:      " + "Navcompass" + "\n")
    file1.write(" *CreateTime:   " + now_time + "\n")

    file1.write(" *Base1 Info: \n" +
                "    Name:       " + name1 + "\n" +
                "    CGG Ver:    " + getFileHead(path1 + "/" + os.listdir(path1)[0], 1, "41,43") + "\n" +
                "    RCVR:       " + getFileHead(path1 + "/" + os.listdir(path1)[0], 3, "7,46") + "\n" +
                "    X/Y/Z:      " + getFileHead(path1 + "/" + os.listdir(path1)[0], 7, "4,16") + "/"
                + getFileHead(path1 + "/" + os.listdir(path1)[0], 8, "4,16") + "/"
                + getFileHead(path1 + "/" + os.listdir(path1)[0], 9, "4,16") + "\n" +
                "    INT DLY:    " + getFileHead(path1 + "/" + os.listdir(path1)[0], 12, "10,67") + "\n" +
                "    CAB DLY:    " + getFileHead(path1 + "/" + os.listdir(path1)[0], 13, "10,17") + "\n" +
                "    REF DLY:    " + getFileHead(path1 + "/" + os.listdir(path1)[0], 14, "10,17") + "\n" +
                "    REF Name:   " + getFileHead(path1 + "/" + os.listdir(path1)[0], 15, "6,15") + "\n" +
                "    TIME AVG:   " + "----------" + "ns\n" +
                "    SD:         " + "----------" + "ns\n" +
                "    SLOPE:      " + "----------" + "\n")

    file1.write(" *Base2 Info: \n" +
                "    Name:       " + name2 + "\n" +
                "    CGG Ver:    " + getFileHead(path2 + "/" + os.listdir(path2)[0], 1, "41,43") + "\n" +
                "    RCVR:       " + getFileHead(path2 + "/" + os.listdir(path2)[0], 3, "7,46") + "\n" +
                "    X/Y/Z:      " + getFileHead(path2 + "/" + os.listdir(path2)[0], 7, "4,16") + "/"
                + getFileHead(path2 + "/" + os.listdir(path2)[0], 8, "4,16") + "/"
                + getFileHead(path2 + "/" + os.listdir(path2)[0], 9, "4,16") + "\n" +
                "    INT DLY:    " + getFileHead(path2 + "/" + os.listdir(path2)[0], 12, "10,67") + "\n" +
                "    CAB DLY:    " + getFileHead(path2 + "/" + os.listdir(path2)[0], 13, "10,17") + "\n" +
                "    REF DLY:    " + getFileHead(path2 + "/" + os.listdir(path2)[0], 14, "10,17") + "\n" +
                "    REF Name:   " + getFileHead(path2 + "/" + os.listdir(path2)[0], 15, "6,15") + "\n" +
                "    TIME AVG:   " + "----------" + "ns\n" +
                "    SD:         " + "----------" + "ns\n" +
                "    SLOPE:      " + "----------" + "\n")

    file1.write(" *Style:        " + "All View" + "\n")
    file1.write(" *Data Type:    " + datatype + "\n")
    file1.write(" *Difference Result:" + "\n" +
                "    TIME AVG:   " + "----------" + "ns\n" +
                "    SD:         " + "----------" + "ns\n" +
                "    SLOPE:      " + "----------" + "\n")
    file1.write("****************************************************/\n\n\n")
    file1.write(("%20s" % "YYYY-MM-DD HH:mm:SS") + ("%15s" % "MJD") + ("%13s" % "Base1_Data") + ("%13s" % "Base2_Data")
                + ("%13s" % "Difference")+("%5s" % "     ")+("%-45s" % "Base1_Satellite")+("%-45s" % "Base2_Satellite") + "\n\n")

    datelist = []  # mjd日期数组
    sumlist1 = []  # 站点一数据
    sumlist2 = []  # 沾点二数据
    diflist = []   # 差值  ns
    diflist2 = []  # 差值  s
    filelist = []
    for k in mapmap1:
        ss1 = 0.0
        ss2 = 0.0
        sta1weixing = ""
        sta2weixing = ""
        k1 = mapmap1[k]

        datek = d.mjdToTime(k.split(",")[0], k.split(",")[1])
    #    print(k + "------")

        for i in range(len(k1)):
            kk1 = k1[i].split(":")[1]
            ss1 +=float(kk1)
            sta1weixing+=k1[i].split(":")[0]
        if len(k1)!=0:
            ss1 = ss1/len(k1)
        else:
            ss1=0
            lg.mylog("error","-----------站点一 "+k+"收到卫星个数为零")

        str1 = ""
        if k in mapmap2.keys():
            k2 = mapmap2[k]
            # file1.write("%20s" % datek)
            str1+="%20s" % datek
            for y in range(len(k2)):
                kk2 = k2[y].split(":")[1]
                ss2 +=float(kk2)
                sta2weixing += k2[y].split(":")[0]
            if len(k1) != 0:
                ss2 = ss2 / len(k2)
            else:
                ss2 = 0
                lg.mylog("error","-----------站点二 "+k+" 收到卫星个数为零")


            # file1.write("%15s" % d.timeToMJD(k.split(",")[0],k.split(",")[1]))
            str1+="%15s" % d.timeToMJD(k.split(",")[0],k.split(",")[1])
            datelist.append(float(d.timeToMJD(k.split(",")[0], k.split(",")[1])))  # mjd日期数组添加元素
            # file1.write("%13.3f" % ss1)
            str1+="%13.3f" % ss1
            sumlist1.append(ss1)

            # file1.write("%13.3f" % ss2)
            str1+="%13.3f" % ss2
            sumlist2.append(ss2)

            # file1.write("%13.3f" %(ss1-ss2))
            str1+="%13.3f" %(ss1-ss2)
            diflist.append(ss1-ss2)
            diflist2.append((ss1-ss2)/1e9)

            # file1.write("%5s" % "     ")
            str1+="%5s" % "     "
            # file1.write("%-45s" % sta1weixing)
            str1+="%-45s" % sta1weixing
            # file1.write("%-45s" % sta2weixing + "\n")
            str1+="%-45s" % sta2weixing
            filelist.append(str1)
        else:
            lg.mylog("error", "--------------站点二没有 "+k+" 时间的数据")
            continue

    # 拉伊达法则剔除
    if conf["tichu2"] == "1":
        x3 = util.getCurveFitting(x=datelist, y=diflist)
        for i in x3:
            datelist.pop(i)
            sumlist1.pop(i)
            sumlist2.pop(i)
            diflist2.pop(i)
            diflist.pop(i)
            filelist.pop(i)
    for i in filelist:
        file1.write(i + "\n")
    lg.mylog("info", "文件写出完毕路径为：" + file1path)
    print("文件输出完毕路径为：" + file1path)
    file1.close()

    list1num = 0
    for i in sumlist1:
        list1num += i  # 求和
    util.fileReplace(file1path, 14, str(round(list1num / len(sumlist1), 2)))
    util.fileReplace(file1path, 15, str(round(util.getStanDeviation(sumlist1), 2)))
    util.fileReplace(file1path, 16, str(format(util.getSlope(datelist, sumlist1), '.3e')))
    util.creatTDChart(datelist, sumlist1, path + "/sta1.jpg",str(round(list1num / len(sumlist1), 2)),
        str(round(util.getStanDeviation(sumlist1), 2)),str(format(util.getSlope(datelist, sumlist1), '.3e')),'g','S1')

    list1num = 0
    for i in sumlist2:
        list1num += i  # 求和
    util.fileReplace(file1path, 26, str(round(list1num / len(sumlist2), 2)))
    util.fileReplace(file1path, 27, str(round(util.getStanDeviation(sumlist2), 2)))
    util.fileReplace(file1path, 28, str(format(util.getSlope(datelist, sumlist2), '.3e')))
    util.creatTDChart(datelist, sumlist2, path + "/sta2.jpg",str(round(list1num / len(sumlist2), 2)),
        str(round(util.getStanDeviation(sumlist2), 2)),str(format(util.getSlope(datelist, sumlist2), '.3e')),'b','S2')

    list1num = 0
    for i in diflist:
        list1num += i  # 求和
    util.fileReplace(file1path, 32, str(round(list1num / len(diflist), 2)))
    util.fileReplace(file1path, 33, str(round(util.getStanDeviation(diflist), 2)))
    util.fileReplace(file1path, 34, str(format(util.getSlope(datelist, diflist), '.3e')))
    util.creatTDChart(datelist, diflist, path + "/diff.jpg",str(round(list1num / len(diflist), 2)),
        str(round(util.getStanDeviation(diflist), 2)),str(format(util.getSlope(datelist, diflist), '.3e')),'r','Di')

    diflist.sort()
    a = 0
    for i in diflist:
        a += i

    # 写出文件
    file2path = path + "/ALLAN_MDEV_" + conf["name1"] + "_" + conf["name2"] + ".txt"
    file2 = open(file2path, "w")
    file2.write("/****************************************************\n")
    file2.write(" *CGGTTS DATA COMPARE FORMAT VERSION: " + versions + "\n")  # 软件版本号
    file2.write(" *Creator:       " + "Navcompass" + "\n")
    file2.write(" *Sigma Type:    " + "Time Deviation" + "\n")
    file2.write(" *Base1 Name:    " + conf["name1"] + "\n")
    file2.write(" *Base2 Name:    " + conf["name2"] + "\n")
    file2.write(" *CreateTime:    " + str(datetime.datetime.now()).split(".")[0] + "\n")
    file2.write(" *Diff Max Data: " + str(round(diflist[len(diflist) - 1], 2)) + " ns\n")
    file2.write(" *Diff Min Data: " + str(round(diflist[0], 2)) + " ns\n")
    file2.write(" *Diff Avg Data: " + str(round(a / len(diflist), 2)) + " ns\n")
    file2.write(" *Conf Factor:   " + "0.683" + "\n")
    file2.write("****************************************************/\n\n")
    file2.write(
        ("%10s" % "AF") + ("%15s" % "TAU") + ("%15s" % "#") + ("%20s" % "Min_Sigma") +
        ("%20s" % "Mod_Sigma") + ("%20s" % "Max_Sigma") + "\n\n")

    rate1 = 1 / float(tau)  # 1 PPS measurements, data interval is 1 s

    data1 = OrderedDict()  # 创建有序字典
    (taus, devs, errs, ns) = allan.mdev(diflist2, rate=rate1, data_type="phase", taus="octave")
    min = []
    max = []
    for i in range(len(taus)):
        dev = devs[i]
        list1 = []  # 创建列表
        try:
            (lo2, hi2) = allan.confidence_interval_noiseID(diflist2, dev, af=int(taus[i] * rate1), dev_type="mdev",data_type="phase")
            min.append(lo2)
            max.append(hi2)
            # print("tau:",taus[i],"num:",ns[i],"Min_Sigma:",lo2,"Mod_Sigma",devs[i],"Max_Sigma:",hi2)
            file2.write("%10s" % str(int(taus[i]) / tau))
            file2.write("%15s" % taus[i])
            file2.write("%15s" % ns[i])
            file2.write("%20s" % format(lo2,'.3e'))
            file2.write("%20s" % format(devs[i],'.3e'))
            file2.write("%20s" % format(hi2,'.3e'))
            file2.write("\n")

            list1.append(str(int(taus[i]) / tau))
            list1.append(taus[i])
            list1.append(ns[i])
            list1.append(format(lo2,'.3e'))
            list1.append(format(devs[i],'.3e'))
            list1.append(format(hi2,'.3e'))
        except NotImplementedError:
            print("无法计算：", taus[i])
            min.append(0)
            max.append(0)
            file2.write("%10s" % str(int(taus[i]) / tau))
            file2.write("%15s" % taus[i])
            file2.write("%15s" % ns[i])
            file2.write("%20s" % "      -     ")
            file2.write("%20s" % format(devs[i],'.3e'))
            file2.write("%20s" % "      -     ")
            file2.write("\n")

            list1.append(str(int(taus[i]) / tau))
            list1.append(taus[i])
            list1.append(ns[i])
            list1.append("  -  ")
            list1.append(format(devs[i], '.3e'))
            list1.append("  -  ")
        except:
            print("未知错误，无法计算：", taus[i])
            min.append(0)
            max.append(0)
            file2.write("%10s" % str(int(taus[i]) / tau))
            file2.write("%15s" % taus[i])
            file2.write("%15s" % ns[i])
            file2.write("%20s" % "      -     ")
            file2.write("%20s" % format(devs[i], '.3e'))
            file2.write("%20s" % "      -     ")
            file2.write("\n")
            list1.append(str(int(taus[i]) / tau))
            list1.append(taus[i])
            list1.append(ns[i])
            list1.append("  -  ")
            list1.append(format(devs[i], '.3e'))
            list1.append("  -  ")
        data1[str(int(taus[i]) / tau)]=list1
    file2.close()
    # ALLAN画图
    util.creatALChart(path+"/mdevallan.jpg",taus, devs,max,min,lable="MDEV")



    # 写出文件
    file3path = path + "/ALLAN_TDEV_" + conf["name1"] + "_" + conf["name2"] + ".txt"
    file3 = open(file3path, "w")
    file3.write("/****************************************************\n")
    file3.write(" *CGGTTS DATA COMPARE FORMAT VERSION: " + versions + "\n")  # 软件版本号
    file3.write(" *Creator:       " + "Navcompass" + "\n")
    file3.write(" *Sigma Type:    " + "Time Deviation" + "\n")
    file3.write(" *Base1 Name:    " + conf["name1"] + "\n")
    file3.write(" *Base2 Name:    " + conf["name2"] + "\n")
    file3.write(" *CreateTime:    " + str(datetime.datetime.now()).split(".")[0] + "\n")
    file3.write(" *Diff Max Data: " + str(round(diflist[len(diflist) - 1], 2)) + " ns\n")
    file3.write(" *Diff Min Data: " + str(round(diflist[0], 2)) + " ns\n")
    file3.write(" *Diff Avg Data: " + str(round(a / len(diflist), 2)) + " ns\n")
    file3.write(" *Conf Factor:   " + "0.683" + "\n")
    file3.write("****************************************************/\n\n")
    file3.write(
        ("%10s" % "AF") + ("%15s" % "TAU") + ("%15s" % "#") + ("%20s" % "Min_Sigma") +
        ("%20s" % "Mod_Sigma") + ("%20s" % "Max_Sigma") + "\n\n")

    data2 = OrderedDict()  # 创建有序字典
    (taus2, devs2, errs, ns) = allan.tdev(diflist2, rate=rate1, data_type="phase", taus="octave")
    min = []
    max = []
    for i in range(len(taus2)):
        dev2 = devs2[i]
        list2 = []
        try:
            (lo2, hi2) = allan.confidence_interval_noiseID(diflist2, dev2, af=int(taus2[i] * rate1), dev_type="tdev",                                             data_type="phase")
            min.append(lo2)
            max.append(hi2)
            file3.write("%10s" % str(int(taus2[i]) / tau))
            file3.write("%15s" % taus2[i])
            file3.write("%15s" % ns[i])
            file3.write("%20s" % format(lo2, '.3e'))
            file3.write("%20s" % format(devs2[i], '.3e'))
            file3.write("%20s" % format(hi2, '.3e'))
            file3.write("\n")

            list2.append(str(int(taus2[i]) / tau))
            list2.append(taus2[i])
            list2.append(ns[i])
            list2.append(format(lo2, '.3e'))
            list2.append(format(devs2[i], '.3e'))
            list2.append(format(hi2, '.3e'))
        except NotImplementedError:
            # print("无法计算：", taus2[i])
            min.append(0)
            max.append(0)
            file3.write("%10s" % str(int(taus2[i]) / tau))
            file3.write("%15s" % taus2[i])
            file3.write("%15s" % ns[i])
            file3.write("%20s" % "      -     ")
            file3.write("%20s" % format(devs2[i], '.3e'))
            file3.write("%20s" % "      -     ")
            file3.write("\n")
            list2.append(str(int(taus2[i]) / tau))
            list2.append(taus2[i])
            list2.append(ns[i])
            list2.append("  -  ")
            list2.append(format(devs2[i], '.3e'))
            list2.append("  -  ")
        except:
            # print("未知错误，无法计算：", taus2[i])
            min.append(0)
            max.append(0)
            file3.write("%10s" % str(int(taus2[i]) / tau))
            file3.write("%15s" % taus2[i])
            file3.write("%15s" % ns[i])
            file3.write("%20s" % "      -     ")
            file3.write("%20s" % format(devs2[i], '.3e'))
            file3.write("%20s" % "      -     ")
            file3.write("\n")
            list2.append(str(int(taus2[i]) / tau))
            list2.append(taus2[i])
            list2.append(ns[i])
            list2.append("  -  ")
            list2.append(format(devs2[i], '.3e'))
            list2.append("  -  ")
        data2[str(int(taus2[i]) / tau)]=list2
    util.creatALChart(path + "/tdevallan.jpg", taus2, devs2, max, min, lable="TDEV")

    # 生成pdf文档
    if conf["generatepdf"]=="1":
        pdf.creatPDF(path, data2, data1)



    # 善后
    util.deletFile(path+"/sta1.jpg")
    util.deletFile(path + "/sta2.jpg")
    util.deletFile(path + "/diff.jpg")
    util.deletFile(path + "/tdevallan.jpg")
    util.deletFile(path + "/mdevallan.jpg")


def screeByCV(map,datatype,sysnum,mdtrnum,mdionum,msionum):

    """
     共视视算法通过参数过滤字典
    :param map: 数据字典
    :param datatype: 数据类型
    :param sysnum,mdtrnum,mdionum,msionum: 四个系数
    :return: 满足条件的新字典
             key: 时间
             value: 卫星编号+系数计算结果值（list）
    """
    print("开始筛选字典 添加系数 计算，数据类型为："+datatype)
    lg.mylog("info", "开始筛选字典 添加系数 计算，数据类型为："+datatype)
    data = OrderedDict() #创建数据字典
    # startime = int(startime)
    # endtime = int(endtime)
    for k in map:
        # k1 = d.date(k.split(",")[0],k.split(",")[1])
        # if k1 >= startime and k1 <= endtime:
            list = map[k]
            listdata = []
            for i in list:
                a = 0
                frc = i.split(",")[6] #数据类型
                if frc ==datatype or frc =="XXX" :
                    sat = i.split(",")[0] #卫星编号
                    sys = int(i.split(",")[2])
                    mdtr = int(i.split(",")[3])
                    mdio = int(i.split(",")[4])
                    msio = int(i.split(",")[5])
                    a += sys*sysnum*0.1+mdtr*mdtrnum*0.1+mdio*mdionum*0.1+msio*msionum*0.1
                    listdata.append(sat+":"+str(a))
                else:
                    print("没有此数据类型："+datatype)
                    lg.mylog("error","没有此数据类型："+datatype)
            data[k]=listdata
    #print(data)
    print("字典筛选完毕长度为："+str(len(data)))
    lg.mylog("info", "字典筛选完毕长度为：" + str(len(data)))
    return data


def screeByAV(map,datatype,sysnum,mdtrnum,mdionum,msionum):

    """
     全视算法通过参数过滤字典
    :param map: 数据字典
    :param datatype: 数据类型
    :param sysnum,mdtrnum,mdionum,msionum: 四个系数
    :return: 满足条件的新字典
             key: 时间
             value: 卫星编号+系数计算结果值（list）
    """
    print("开始筛选字典 添加系数 计算，数据类型为：" + datatype)
    lg.mylog("info", "开始筛选字典 添加系数 计算，数据类型为：" + datatype)
    data = OrderedDict() #创建数据字典
    # startime = int(startime)
    # endtime = int(endtime)
    for k in map:
        # k1 = d.date(k.split(",")[0],k.split(",")[1])
        # if k1 >= startime and k1 <= endtime:
            list = map[k]
            listdata = []
            for i in list:
                a = 0
                frc = i.split(",")[6] #数据类型
                if frc ==datatype:
                    sat = i.split(",")[0] #卫星编号
                    sys = float(i.split(",")[2])
                    mdtr = int(i.split(",")[3])
                    mdio = int(i.split(",")[4])
                    msio = int(i.split(",")[5])
                    if mdtrnum!="" and mdionum!="" and msionum!="" and sysnum!="":
                        a += sys*sysnum*0.1+mdtr*mdtrnum*0.1+mdio*mdionum*0.1+msio*msionum*0.1
                    else:
                        a += sys*0.1
                    listdata.append(sat+":"+str(a))
                else:
                    print("没有此数据类型：" + datatype)
                    lg.mylog("error", "没有此数据类型：" + datatype)
            data[k]=listdata
    #print(data)
    print("字典筛选完毕长度为：" + str(len(data)))
    lg.mylog("info", "字典筛选完毕长度为：" + str(len(data)))
    return data





