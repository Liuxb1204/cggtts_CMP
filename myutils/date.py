import math
import time
import datetime

def div(x, y):
    return int(round(x) / round(y))


def DF2DHMS(F):
    df = F

    day = math.floor(df)

    hour = math.floor((df - day) * 24)

    minute = math.floor((df - day - hour / 24) * 1440)

    sec = (df - day - hour / 24 - minute / 1440) * 86400

    return [day, hour, minute, int(sec)]


def strToTime(a):
    """
    时间字符串转时间戳
    :param a:时间字符串
    :return: 时间戳
    """
    timeArray = time.strptime(a, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp


def mjdToTime(MJD,time):
    """
    儒略日转时间字符串
    :param MJD: 儒略日
    :param time: 时间字符串
    :return: 时间字符串格式
    """

    MJD = int(MJD)

    DJMIN = -68569.5

    DJMAX = 1e9

    DJ1 = 2400000.5

    DJ2 = MJD

    DJ = DJ1 + DJ2

    D1 = ''

    D2 = ''

    J = ''

    JD = ''

    if (DJ < DJMIN or DJ > DJMAX):

        J = -1

        print("无效的日期"+str(MJD))
    else:

        J = 0

        if (DJ1 >= DJ2):

            D1 = DJ1

            D2 = DJ2

        else:

            D1 = DJ2

            D2 = DJ1

        D2 = D2 - 0.5

        F1 = D1 % 1.0

        F2 = D2 % 1.0

        F = (F1 + F2) % 1.0

        if (F < 0): F = F + 1.0

        D = round(D1 - F1) + round(D2 - F2) + round(F1 + F2 - F)

        JD = round(D) + 1

        L = JD + 68569

        N = div(4 * L, 146097)

        L = L - div((146097 * N + 3), 4)

        I = div(4000 * (L + 1), 1461001)

        L = L - div(1461 * I, 4) + 31

        K = div(80 * L, 2447)

        ID = L - div(2447 * K, 80)
        if len(str(ID))<2:
            ID = "0"+str(ID)

        L = div(K, 11)

        IM = K + 2 - 12 * L
        if len(str(IM))<2:
            IM = "0"+str(IM)

        IY = 100 * (N - 49) + I + L

        FD = DF2DHMS(F)

        # print
        # MJD, '对应日期为', [IY, IM, int(ID), int(FD[1]), int(FD[2]), FD[3]]
        # print(str(IY)+"-"+str(IM)+"-"+str(ID)+" "+str(FD[1])+":"+str(FD[2])+":"+str(FD[3]))
        ss=str(IY)+"-"+str(IM)+"-"+str(ID)+" "+time[0:2]+":"+time[2:4]+":"+time[4:]

        return ss

# str1=mjdToTime("58122","085000")
# print(str1)


def stampToDate(timeStamp):
    """
    时间戳转日期字符串
    :param timeStamp: 1545004815 (s)
    :return: 2018-12-17 00:00:15
    """
    dateArray = datetime.datetime.utcfromtimestamp(timeStamp)
    otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
    return otherStyleTime


# now_time = str(datetime.datetime.now()).split(".")[0]
# print(now_time)

def timeToMJD(mjd,time):

    mjd = int(mjd)
    d = int(time[0:2])*3600
    s = int(time[2:4])*60
    m = int(time[4:])
    num = round(mjd+(d+s+m)/86400,6)
    #print("{:x<12f}".format(num))
    return "{:x<12f}".format(num)
aa = timeToMJD("58260","121210")


def timestrToMjd(datestr):
    """
    时间字符串转mjd

    :param datestr: 2018-01-05 08:50:00
    :return: 58123
    """
    string = datestr.split(" ")[0]
    y = int(string.split("-")[0])
    m = int(string.split("-")[1])
    d = int(string.split("-")[2])

    jd = d - 32075 + 1461 * (y + 4800 + (m - 14) / 12) / 4 + 367 * (m - 2 - (m - 14) / 12 * 12) / 12 - 3 * (
    (y + 4900 + (m - 14) / 12) / 100) / 4

    mjdStr = str(jd - 2400000.5)

    x = mjdStr.index(".")
    if x == -1:
        return int(mjdStr)
    else:
        mjdStr = mjdStr[0:x]
        return int(mjdStr)

#a = timestrToMjd("2018-01-05 08:50:00")

#print(a)

#daytorulueri("58023","234200")
#print(date("58023","010200"))