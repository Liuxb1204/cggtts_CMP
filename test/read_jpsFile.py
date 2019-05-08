import binascii
import struct
import math
import collections


def dayTime(seconds):
    """
    天内秒转时间
    单位：秒
    :param seconds:
    :return:
    """
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h<10:
        return ("%02d:%02d:%02d" % (h, m, s))
    else:
        return ("%d:%02d:%02d" % (h, m, s))

def mysortDic(dic):
    """
    字典排序
    :param dic:
    :return:
    """
    dic2 = collections.OrderedDict()
    diclist = sorted(dic)

    for d in diclist:
        dic2[d] = dic[d]
    return dic2


f = open("G:\\ts03\\TF14_log_2018_12_31_00.00.00.jps", "rb")

# f.seek(156999990, 0)
f2 = open("G:\\ts03\\jsp_data2.txt","w+")
f2.write(("time".rjust(19, " "))+("prn".rjust(12, " "))+("EL".rjust(11, " "))+("rc".rjust(18, " "))+
         ("rx".rjust(18, " "))+("CE".rjust(18, " "))+("1r".rjust(18, " "))+("1E".rjust(18, " "))+
         ("2r".rjust(18, " "))+("2E".rjust(18, " "))+("3r".rjust(18, " "))+("3E".rjust(18, " "))+
         ("5r".rjust(18, " "))+("5E".rjust(18, " "))+"\n\n")

GK = 1e-11
RK = 1e-11
EK = 2e-11
BK = 2e-11
LD = 299792458
num = 0

print("开始解析数据...")

prnlist = []
rxdic = collections.OrderedDict()
date1 = ""

while True:
    data = f.read(1)
    # datad = binascii.b2a_hex(data)
    if not data:
        break

    if data == b'~':
        data2 = f.read(1)
        if data2 == b'~':
            strs = ""
            data3 = f.read(3)
            # data4 = binascii.b2a_hex(data3)
            if data3 == b'\x30\x30\x35':
                data8 = f.read(4)
                # data9 = binascii.b2a_hex(data8)
                rt = struct.unpack('I', data8)[0]   #天内秒
                if rt == 4294967295:
                    continue  # 无效值
                dat = dayTime(rt / 1000)
                # if dat == "00:00:06":
                #      print("-----bug-----") #记录曾经消灭bug的地方
                if rt == 4294967295:
                    print("~~无效值")
                    continue
                f.read(1)
                data5 = f.read(1)
                if data5 == b'\x0A':
                    a = 0
                    b = 0
                    dic = collections.OrderedDict()
                    strline = ""
                    while True:
                        rdh = f.read(1)
                        # data7 = binascii.b2a_hex(rdh)
                        if rdh == b'R':
                            rdh2 = f.read(1)
                            # data77 = binascii.b2a_hex(rdh2)
                            if rdh2 == b'D':
                                rdh3 = f.read(3)
                                if rdh3 == b'\x30\x30\x36':
                                    y = struct.unpack('H', f.read(2))[0]    #年
                                    m = struct.unpack('B', f.read(1))[0]    #月
                                    d = struct.unpack('B', f.read(1))[0]    #日
                                    b = struct.unpack('B', f.read(1))[0]
                                    if y == 65535 or m == 255 or d == 255:
                                        print("rd无效值")
                                        break
                                    date1 = str(y) + "-" + str(m) + "-" + str(d)
                                    # strs += date1+" "+dayTime(rt/1000)+"         "
                                    # strline += date1+" "+dayTime(rt/1000)+"         "
                                    a = 1
                            else:
                                f.seek(-1, 1)
                        elif rdh == b'\x0A':
                            sih1 = f.read(1)
                            # datasih1 = binascii.b2a_hex(sih1)
                            if sih1 == b'S':
                                sih2 = f.read(1)
                                # datasih2 = binascii.b2a_hex(sih2)
                                if sih2 == b'I':
                                    data12 = f.read(1)
                                    # data13 = binascii.b2a_hex(data12)
                                    s1 = str(chr(int(struct.unpack('B', data12)[0])))
                                    data14 = f.read(1)
                                    # data15 = binascii.b2a_hex(data14)
                                    s2 = str(chr(int(struct.unpack('B', data14)[0])))
                                    data16 = f.read(1)
                                    # data17 = binascii.b2a_hex(data16)
                                    s3 = str(chr(int(struct.unpack('B', data16)[0])))
                                    try:
                                        num = int(s1 + s2 + s3, 16)
                                    except:
                                        continue
                                    prnlenght = int(s1 + s2 + s3, 16) - 1  # 卫星个数
                                    prnlist = []
                                    for i in range(prnlenght):
                                        data18 = f.read(1)
                                        # data19 = binascii.b2a_hex(data18)
                                        prn1 = struct.unpack('B', data18)[0]
                                        prnlist.append(prn1)
                                    b = 1
                                else:
                                    f.seek(-2, 1)
                            elif sih1 == b'E':
                                rdh2 = f.read(1)
                                # data40 = binascii.b2a_hex(rdh2)
                                if rdh2 == b'L':

                                    data41 = f.read(1)
                                    # data42 = binascii.b2a_hex(data41)
                                    s41 = str(chr(int(struct.unpack('B', data41)[0])))
                                    data43 = f.read(1)
                                    # data44 = binascii.b2a_hex(data43)
                                    s43 = str(chr(int(struct.unpack('B', data43)[0])))
                                    data45 = f.read(1)
                                    # data46 = binascii.b2a_hex(data45)
                                    s45 = str(chr(int(struct.unpack('B', data45)[0])))
                                    try:
                                        num = int(s41 + s43 + s45, 16)
                                    except:
                                        continue
                                    len40 = math.ceil((int(s41 + s43 + s45, 16) - 1))  # 伪距个数

                                    if len40 != len(prnlist):
                                        print(date1+" "+dayTime(rt/1000)+" EL卫星个数不一样")
                                        break

                                    for i in range(len40):
                                        data47 = f.read(1)
                                        # data48 = binascii.b2a_hex(data47)
                                        el = struct.unpack('b', data47)[0]
                                        prn = prnlist[i]
                                        if prn == 255:
                                            continue  # 无效值
                                        if prn >= 1 and prn <= 37:
                                            if prn < 10:
                                                prn = "G0" + str(prn)
                                            else:
                                                prn = "G" + str(prn)
                                        elif prn >= 70 and prn <= 119:
                                            if prn - 70 < 10:
                                                prn = "E0" + str(prn - 70)
                                            else:
                                                prn = "E" + str(prn - 70)
                                        elif prn >= 211 and prn <= 247:
                                            if prn - 210 < 10:
                                                prn = "C0" + str(prn - 210)
                                            else:
                                                prn = "C" + str(prn - 210)
                                        else:
                                            continue

                                        if el == 127:
                                            # print("rc无效值..."+prn)
                                            # strs += (prn + "_el:0.000").ljust(20, " ")
                                            dic[prn] = "0.000".rjust(10, " ")
                                            continue

                                        el = round(el, 3)
                                        dic[prn] = str(el).rjust(10, " ")
                                else:
                                    f.seek(-2, 1)
                            elif sih1 == b'r':
                                rdh2 = f.read(1)
                                # datardh2 = binascii.b2a_hex(rdh2)
                                if rdh2 == b'c':

                                    data21 = f.read(1)
                                    # data22 = binascii.b2a_hex(data21)
                                    s4 = str(chr(int(struct.unpack('B', data21)[0])))
                                    data23 = f.read(1)
                                    # data24 = binascii.b2a_hex(data23)
                                    s5 = str(chr(int(struct.unpack('B', data23)[0])))
                                    data25 = f.read(1)
                                    # data26 = binascii.b2a_hex(data25)
                                    s6 = str(chr(int(struct.unpack('B', data25)[0])))
                                    try:
                                        num = int(s4 + s5 + s6, 16)
                                    except:
                                        continue
                                    len3 = math.ceil((int(s4 + s5 + s6, 16) - 1) / 4)  # 伪距个数
                                    if len3 != len(prnlist):
                                        print(date1+" "+dayTime(rt/1000)+" rc卫星个数不一样")
                                        break

                                    for i in range(len3):

                                        data27 = f.read(4)
                                        rc = struct.unpack('i', data27)[0]
                                        # data28 = binascii.b2a_hex(data27)
                                        prn = prnlist[i]
                                        if prn == 255:
                                            continue    # 无效值
                                        if prn >= 1 and prn <= 37:
                                            if prn < 10:
                                                prn = "G0" + str(prn)
                                            else:
                                                prn = "G" + str(prn)
                                        elif prn >= 70 and prn <= 119:
                                            if prn - 70 < 10:
                                                prn = "E0" + str(prn - 70)
                                            else:
                                                prn = "E" + str(prn - 70)
                                        elif prn >= 211 and prn <= 247:
                                            if prn - 210 < 10:
                                                prn = "C0" + str(prn - 210)
                                            else:
                                                prn = "C" + str(prn - 210)
                                        else:
                                            continue

                                        if rc == 2147483647:
                                            # print("rc无效值..."+prn)
                                            # strs += (prn+"_rc:0.000").ljust(20, " ")
                                            dic[prn] = dic[prn] + "0.000".rjust(18, " ")
                                            continue

                                        type = prn[0:1]
                                        if type == "G":
                                            rc = (rc * GK + 0.075) * LD
                                        elif type == "E":
                                            rc = (rc * EK + 0.085) * LD
                                        elif type == "C":
                                            rc = (rc * BK + 0.105) * LD
                                        rc = round(rc, 3)
                                        dic[prn] = dic[prn] + str(rc).rjust(18, " ")
                                        # strs += (prn + "_rc:" + str(rc)).ljust(20, " ")

                                elif rdh2 == b'x':

                                    data21 = f.read(1)
                                    # data22 = binascii.b2a_hex(data21)
                                    s4 = str(chr(int(struct.unpack('B', data21)[0])))
                                    data23 = f.read(1)
                                    # data24 = binascii.b2a_hex(data23)
                                    s5 = str(chr(int(struct.unpack('B', data23)[0])))
                                    data25 = f.read(1)
                                    # data26 = binascii.b2a_hex(data25)
                                    s6 = str(chr(int(struct.unpack('B', data25)[0])))
                                    try:
                                        num = int(s4 + s5 + s6, 16)
                                    except:
                                        continue
                                    len3 = math.ceil((int(s4 + s5 + s6, 16) - 1) / 4)  # 伪距个数
                                    if len3 != len(prnlist):
                                        print(date1+" "+dayTime(rt/1000)+" rx卫星个数不一样")
                                        break

                                    rxdic = collections.OrderedDict()
                                    for i in range(len3):

                                        data27 = f.read(4)
                                        rx = struct.unpack('i', data27)[0]

                                        # data28 = binascii.b2a_hex(data27)
                                        prn = prnlist[i]
                                        if prn == 255:
                                            continue    # 无效值
                                        if prn >= 1 and prn <= 37:
                                            if prn < 10:
                                                prn = "G0" + str(prn)
                                            else:
                                                prn = "G" + str(prn)
                                        elif prn >= 71 and prn <= 119:
                                            if prn - 70 < 10:
                                                prn = "E0" + str(prn - 70)
                                            else:
                                                prn = "E" + str(prn - 70)
                                        elif prn >= 211 and prn <= 247:
                                            if prn - 210 < 10:
                                                prn = "C0" + str(prn - 210)
                                            else:
                                                prn = "C" + str(prn - 210)
                                        else:
                                            continue

                                        # rxdic[prn] = rx    # 存储一下rx的值(REF)

                                        if rx == 2147483647:
                                            print("rx无效值..."+prn)
                                            # strs += (prn+"_rx:0.000").ljust(20, " ")
                                            dic[prn] = dic[prn] + ("0.000".rjust(18, " "))
                                            continue

                                        type = prn[0:1]
                                        if type == "G":
                                            rxdic[prn] = (rx * GK + 0.075)
                                            rx = (rx * GK + 0.075) * LD
                                        elif type == "E":
                                            rxdic[prn] = (rx * EK + 0.085)
                                            rx = (rx * EK + 0.085) * LD
                                        elif type == "C":
                                            rxdic[prn] = (rx * BK + 0.105)
                                            rx = (rx * BK + 0.105) * LD

                                        rx = round(rx, 3)
                                        dic[prn] = dic[prn] + str(rx).rjust(18, " ")
                                        # strs += (prn + "_rx:" + str(rx)).ljust(20, " ")
                                else:
                                    f.seek(-2, 1)
                            elif sih1 == b'C':
                                rdh2 = f.read(1)
                                # data50 = binascii.b2a_hex(rdh2)
                                if rdh2 == b'E':

                                    data51 = f.read(1)
                                    # data52 = binascii.b2a_hex(data51)
                                    s51 = str(chr(int(struct.unpack('B', data51)[0])))
                                    data53 = f.read(1)
                                    # data54 = binascii.b2a_hex(data53)
                                    s53 = str(chr(int(struct.unpack('B', data53)[0])))
                                    data55 = f.read(1)
                                    # data56 = binascii.b2a_hex(data55)
                                    s55 = str(chr(int(struct.unpack('B', data55)[0])))
                                    try:
                                        num = int(s51 + s53 + s55, 16)
                                    except:
                                        continue
                                    len50 = math.ceil((int(s51 + s53 + s55, 16) - 1))  # 伪距个数

                                    if len50 != len(prnlist):
                                        print(date1+" "+dayTime(rt/1000)+" CE卫星个数不一样")
                                        break

                                    for i in range(len50):
                                        data57 = f.read(1)
                                        # data58 = binascii.b2a_hex(data57)
                                        ce = struct.unpack('B', data57)[0]
                                        prn = prnlist[i]
                                        if prn == 255:
                                            continue  # 无效值
                                        if prn >= 1 and prn <= 37:
                                            if prn < 10:
                                                prn = "G0" + str(prn)
                                            else:
                                                prn = "G" + str(prn)
                                        elif prn >= 70 and prn <= 119:
                                            if prn - 70 < 10:
                                                prn = "E0" + str(prn - 70)
                                            else:
                                                prn = "E" + str(prn - 70)
                                        elif prn >= 211 and prn <= 247:
                                            if prn - 210 < 10:
                                                prn = "C0" + str(prn - 210)
                                            else:
                                                prn = "C" + str(prn - 210)
                                        else:
                                            continue

                                        if ce == 255:
                                            # print("rc无效值..."+prn)
                                            # strs += (prn + "_ce:0.000").ljust(20, " ")
                                            dic[prn] = dic[prn] + ("0.00".rjust(18, " "))
                                            continue

                                        ce = round(ce * 0.25, 3)
                                        dic[prn] = dic[prn] + (str(ce).rjust(18, " "))
                                else:
                                    f.seek(-2, 1)
                            elif sih1 == b'1' or sih1 == b'2' or sih1 == b'3' or sih1 == b'5':
                                rdh2 = f.read(1)
                                # datardh2 = binascii.b2a_hex(rdh2)
                                if rdh2 == b'r':
                                    typename = str(chr(int(struct.unpack('B', sih1)[0]))) + "r"
                                    data21 = f.read(1)
                                    # data30 = binascii.b2a_hex(data21)
                                    s7 = str(chr(int(struct.unpack('B', data21)[0])))
                                    data23 = f.read(1)
                                    # data31 = binascii.b2a_hex(data23)
                                    s8 = str(chr(int(struct.unpack('B', data23)[0])))
                                    data25 = f.read(1)
                                    # data32 = binascii.b2a_hex(data25)
                                    s9 = str(chr(int(struct.unpack('B', data25)[0])))
                                    try:
                                        num = int(s7 + s8 + s9, 16)
                                    except:
                                        continue
                                    len5 = math.ceil((int(s7 + s8 + s9, 16) - 1) / 2)  # 伪距个数
                                    if len5 != len(prnlist):
                                        print(date1+" "+dayTime(rt/1000)+" "+typename+"卫星个数不一样")
                                        break

                                    for y in range(len5):

                                        data27 = f.read(2)
                                        # data33 = binascii.b2a_hex(data27)
                                        rrr = struct.unpack('h', data27)[0]  # 伪距的值
                                        prn = prnlist[y]
                                        if prn == 255:
                                            continue    # 无效值
                                        if prn>= 1 and prn<= 37:
                                            if prn < 10:
                                                prn = "G0" + str(prn)
                                            else:
                                                prn = "G" + str(prn)
                                        elif prn >= 71 and prn<= 119:
                                            if prn - 70 < 10:
                                                prn = "E0" + str(prn - 70)
                                            else:
                                                prn = "E" + str(prn - 70)
                                        elif prn >= 211 and prn <= 247:
                                            if prn - 210 < 10:
                                                prn = "C0" + str(prn - 210)
                                            else:
                                                prn = "C" + str(prn - 210)
                                        else:
                                            continue

                                        if rrr == 32767:
                                            # print(typename+"无效值..."+prn)
                                            # strs += (prn+"_"+typename+"0.000").ljust(20, " ")
                                            dic[prn] = dic[prn] + "0.000".rjust(18, " ")
                                            continue

                                        REF = rxdic[prn]
                                        rr2 = rrr * 1e-11 + 2e-7 + REF
                                        rr3 = round(rr2 * LD, 3)
                                        dic[prn] = dic[prn] + str(rr3).rjust(18, " ")
                                elif rdh2 == b'E':
                                    typename2 = str(chr(int(struct.unpack('B', sih1)[0]))) + "E"
                                    data61 = f.read(1)
                                    # data62 = binascii.b2a_hex(data61)
                                    s61 = str(chr(int(struct.unpack('B', data61)[0])))
                                    data63 = f.read(1)
                                    # data64 = binascii.b2a_hex(data63)
                                    s63 = str(chr(int(struct.unpack('B', data63)[0])))
                                    data65 = f.read(1)
                                    # data66 = binascii.b2a_hex(data65)
                                    s65 = str(chr(int(struct.unpack('B', data65)[0])))
                                    try:
                                        num = int(s61 + s63 + s65, 16)
                                    except:
                                        continue
                                    len60 = math.ceil(int(s61 + s63 + s65, 16) - 1)  # 伪距个数
                                    if len60 != len(prnlist):
                                        print(date1+" "+dayTime(rt/1000)+" "+typename2+" 卫星个数不一样")
                                        break

                                    for y in range(len60):

                                        data67 = f.read(1)
                                        # data68 = binascii.b2a_hex(data67)
                                        ee = struct.unpack('B', data67)[0]  # 伪距的值
                                        prn = prnlist[y]
                                        if prn == 255:
                                            continue  # 无效值
                                        if prn >= 1 and prn <= 37:
                                            if prn < 10:
                                                prn = "G0" + str(prn)
                                            else:
                                                prn = "G" + str(prn)
                                        elif prn >= 71 and prn <= 119:
                                            if prn - 70 < 10:
                                                prn = "E0" + str(prn - 70)
                                            else:
                                                prn = "E" + str(prn - 70)
                                        elif prn >= 211 and prn <= 247:
                                            if prn - 210 < 10:
                                                prn = "C0" + str(prn - 210)
                                            else:
                                                prn = "C" + str(prn - 210)
                                        else:
                                            continue

                                        if ee == 255:
                                            # print(typename+"无效值..."+prn)
                                            # strs += (prn + "_" + typename2 + "0.00").ljust(20, " ")
                                            dic[prn] = dic[prn] + "0.00".rjust(18, " ")
                                            continue

                                        ee = round(ee * 0.25, 3)
                                        dic[prn] = dic[prn] + str(ee).rjust(18, " ")

                                    if typename2 == "5E":
                                        i = 0
                                        dic = mysortDic(dic)
                                        for x in dic:
                                            strline += date1 + " " + dayTime(rt / 1000) + "         "
                                            strline += (x + " " + dic[x])
                                            if i != len(dic) - 1:
                                                strline += "\n"
                                            i = i + 1
                                        f2.write(strline + "\n")
                                        # print(strs)
                                        break
                                else:
                                    f.seek(-2, 1)
                            else:
                                f.seek(-1, 1)
                        elif rdh == b'E':
                            eldata = f.read(1)
                            # eldata2 = binascii.b2a_hex(eldata)
                            if eldata == b'L':
                                f.seek(-3, 1)
                                eldata = f.read(1)
                                # eldata3 = binascii.b2a_hex(eldata)
                                if eldata == b'\x0A':
                                    f.seek(-1, 1)
                                else:
                                    f.seek(3, 1)
                            else:
                                f.seek(-1, 1)
print("数据解析完毕。")
f2.close()
f.close()