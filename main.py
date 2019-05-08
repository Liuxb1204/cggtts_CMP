import c_service as ser
import c_logg as lg
import datetime
import myutils.util as util
import os

def commonView(path1,name1,path2,name2,filetype,datatype,smjd,emjd,sysnum,mdtrnum,mdionum,msionum):
    """
    启用共视算法
    :param path1: 路径1
    :param name1: 站点名
    :param path2: 路径2
    :param name2: 站点名2
    :param filetype: 文件类型
    :param datatype: 数据类型
    :param smjd: 开始时间 （儒略日）
    :param emjd: 结束时间
    :param sysnum: 基数（refsys_ratio）
    :param mdtrnum:
    :param mdionum:
    :param msionum:
    :return:
    """
    # 数据文件生成数据字典
    print("开始创建字典")
    lg.mylog("info","开始创建字典")

    map1 = util.createDictionary(path1, name1, filetype, smjd, emjd)
    map2 = util.createDictionary(path2, name2, filetype, smjd, emjd)

    # 通过条件筛选字典
    mapmap1 = ser.screeByCV(map1, datatype, sysnum, mdtrnum, mdionum, msionum)
    mapmap2 = ser.screeByCV(map2, datatype, sysnum, mdtrnum, mdionum, msionum)


    if tichu == "1":
        # 剔除数据
        mapmap1, mapmap2 = ser.removeByCV(mapmap1,mapmap2)

    # 比对两个文件并生成文件写出
    ser.outputByCV(mapmap1,mapmap2,name1,name2,datatype,sysnum,mdtrnum,mdionum,msionum,path1,path2)


def allView(path1,name1,path2,name2,filetype,datatype,smjd,emjd,sysnum,mdtrnum,mdionum,msionum,outpath):
    """
    启用全视算法
    :param path1: 路径1
    :param name1: 站点名
    :param path2: 路径2
    :param name2: 站点名2
    :param filetype: 文件类型
    :param datatype: 数据类型
    :param smjd: 开始时间 （儒略日）
    :param emjd: 结束时间
    :param sysnum: 基数（refsys_ratio）
    :param mdtrnum:
    :param mdionum:
    :param msionum:
    :param outpath: 输出路径
    :return:
    """
    # 数据文件生成数据字典
    map1 = util.createDictionary(path1,name1,filetype,smjd,emjd)
    # 通过条件筛选字典
    mapmap1 = ser.screeByAV(map1, datatype, sysnum,mdtrnum,mdionum,msionum)

    map2 = util.createDictionary(path2,name2,filetype,smjd,emjd)
    mapmap2 = ser.screeByAV(map2, datatype, sysnum,mdtrnum,mdionum,msionum)

    # 比对两个文件并生成文件写出
    ser.outputByAV(mapmap1,mapmap2,name1,name2,datatype,outpath,path1,path2)


#-----------------------开始------------------------#


# 读取参数信息
conf = util.readConf()
view = conf["view"]
filetype = conf["filetype"]
smjd = conf["smjd"]
emjd = conf["emjd"]
datatype = conf["datatype"]
sysnum = int(conf["sysnum"])
mdtrnum = int(conf["mdtrnum"])
mdionum = int(conf["mdionum"])
msionum = int(conf["msionum"])
tichu = conf["tichu"]
outpath = conf["outpath"]
# 读取站点一的信息
name1 = conf["name1"]
datasource1= conf["datasource1"] #获取方式（本地或者ftp）
localpath1 = conf["localpath1"].replace("\t","\\t").replace("\r","\\r").replace("\n","\\n") #路径
ip1 = conf["ip1"]
port1 = int(conf["port1"])
user1 = conf["username1"]
pwd1 = conf["password1"]
ftppath1 = conf["ftppath1"]

Path = os.path.split(os.path.realpath(__file__))[0]+"/ftp"
if datasource1=="0":
    util.ftpDownload(ip1,port1,user1,pwd1,ftppath1,Path,name1)
    localpath1 = Path



# 读取站点二的信息
name2 = conf["name2"]
datasource2= conf["datasource2"] #获取方式（本地或者ftp）
localpath2 = conf["localpath2"].replace("\t","\\t").replace("\r","\\r").replace("\n","\\n") #路径
ip2 = conf["ip2"]
port2 = int(conf["port2"])
user2 = conf["username2"]
pwd2 = conf["password2"]
ftppath2 = conf["ftppath2"]

if datasource2=="0":
    util.ftpDownload(ip2,port2,user2,pwd2,ftppath2,Path,name2)
    localpath2 = Path

# 获取当前时间
now_time = str(datetime.datetime.now()).split(".")[0]
now_time = now_time.replace("-","").replace(" ","").replace(":","")


if view=="CV":
    print("-------------------------------------启动共视算法-----------------------------------------------")
    lg.mylog("info", "***************启动共视算法****************")
    commonView(localpath1, name1, localpath2, name2, filetype, datatype, smjd, emjd, sysnum, mdtrnum, mdionum, msionum)
    util.remFile(Path) #清空ftp下载的数据
    print("-----------------------------------计算完成 程序结束---------------------------------------------")
    lg.mylog("info", "***************程序结束****************")
else:
    print("-------------------------------------启动全视算法-----------------------------------------------")
    lg.mylog("info", "***************启动全视算法****************")
    outpath += "/" + name1 + "_" + name2 + "_" + datatype + "_" + view + now_time[2:12] + ".txt"
    allView(localpath1,name1,localpath2,name2,filetype,datatype,smjd,emjd,"","","","",outpath)
    util.remFile(Path)
    lg.mylog("info", "***************程序结束****************")
    print("-----------------------------------计算完成 程序结束---------------------------------------------")












