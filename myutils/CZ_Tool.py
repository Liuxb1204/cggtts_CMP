import myutils.date as d
import os,sys

def fileToDIC2(path):
    """
    文件直接转字典
    :param path:
    :return: 字典
    """
    f = open(path)
    i = 0
    FU = 0
    DU = 0
    strtime = ""
    satstr = ""
    list = []
    num = 0
    for line in f:
        i = i + 1
        if i >= 20:
            num += 1
            SAT = line[0:3].strip()
            MJD = line[7:12].strip()
            STTIME = line[13:19].strip()
            FEFUTC = line[133:139].strip()
            DUTC = line[144:148].strip()
            if len(SAT) == 2:
                SAT = " " + SAT
            elif len(SAT) == 1:
                SAT = " 0" + SAT
            str1 = MJD + ":" + STTIME


            if str1!=strtime and strtime!="" and i>20:
                MJD2 = strtime.split(":")[0]
                STTIME2 = strtime.split(":")[1]
                list.append(d.mjdToTime(MJD2,STTIME2)+ ("%8s" % " ") + strtime + ("%8s" % " ")+d.timeToMJD(MJD2,STTIME2)+
                            ("%8s" % " ") + str("%6.1f" % (FU/(num-1))) + ("%8s" % " ") + str(DU/(num-1)) + ("%8s" % " ") + satstr)
                FU = int(FEFUTC)
                DU = int(DUTC)
                satstr = SAT + ","
                strtime = str1
                num = 1
            else:
                strtime = str1
                FU += int(FEFUTC)
                DU += int(DUTC)
                satstr += SAT + ","
    list.append(d.mjdToTime(strtime.split(":")[0], strtime.split(":")[1]) + ("%8s" % " ") + strtime + ("%8s" % " ") +
                d.timeToMJD(strtime.split(":")[0], strtime.split(":")[1]) + ("%8s" % " ") + str("%6.1f" % (FU / num)) +
                ("%8s" % " ") + str(DU / num) + ("%8s" % " ") + satstr)
    f.close()
    return list

def aa(localpath1):
    dirs = os.listdir(localpath1)
    #map3 = OrderedDict()
    file1 = open("C:\\Users\\dancer\\Desktop\\data.txt", "w")
    for file in dirs:
        #print(file)
        a = fileToDIC2(localpath1+"\\"+file)
        for i in a:
            file1.write(i+"\n")
            #print(i)
    file1.close()

aa("G:\\IM21cz")