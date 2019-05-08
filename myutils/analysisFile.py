import myutils.date as d
import struct

def analysisFile(filepath):
    """
    解析二进制文件
    语句：4012
    :return:
    """
    filename = filepath.split("/")[-1]
    path = filepath.split(filename)[0]
    outfilepath = path+filename+"_data.txt"
    print("开始解析文件："+filepath)
    TIME1 = 315964800
    f = open(filepath, "rb")
    f1 = open(outfilepath, "w")
    f1.write("%10s" % "time_stamp")
    f1.write("%22s" % "utc_time")
    f1.write("%6s" % "num")
    f1.write("%8s" % "az")
    f1.write("%8s" % "el")
    f1.write("%5s" % "#1")
    f1.write("%7s" % "#2\n\n")

    while True:
        data = f.read(2)
        if not data:
            break
        sync = b'\x24\x40'
        if data == sync:
            crc = struct.unpack('H', f.read(2))[0]
            id1 = struct.unpack('H', f.read(2))[0]
            if id1 & 8191 == 4012:
                print("---------------------------------------------------")
                length = struct.unpack('H', f.read(2))[0]
                tow = struct.unpack('I', f.read(4))[0]
                tow1 = tow * 0.001
                wnc = struct.unpack('H', f.read(2))[0]
                #wnc2 = hex(wnc)
                wnc1 = wnc * 604800
                time2 = TIME1 + wnc1 + tow1
                time3 = d.stampToDate(time2)
                n = struct.unpack('B', f.read(1))[0]
                #n2 = hex(n)
                sblen = struct.unpack('B', f.read(1))[0]
                #sblen2 = hex(sblen)
                for i in range(n):
                    sid = struct.unpack('B', f.read(1))[0]  # 卫星号
                    # sid2 = hex(sid)
                    sname = ""
                    sname += str(int(time2)) + "   " + time3 + "   "
                    if sid >= 1 and sid <= 37:
                        if sid < 10:
                            sname += "G0" + str(sid)
                        else:
                            sname += "G" + str(sid)
                    elif sid >= 38 and sid <= 61:
                        if sid - 37 < 10:
                            sname += "R0" + str(sid - 37)
                        else:
                            sname += "R" + str(sid - 37)
                    elif sid >= 63 and sid <= 68:
                        if sid - 38 < 10:
                            sname += "R0" + str(sid - 38)
                        else:
                            sname += "R" + str(sid - 38)
                    elif sid >= 71 and sid <= 106:
                        if sid - 70 < 10:
                            sname += "E0" + str(sid - 70)
                        else:
                            sname += "E" + str(sid - 70)
                    elif sid >= 141 and sid <= 177:
                        if sid - 140 < 10:
                            sname += "C0" + str(sid - 140)
                        else:
                            sname += "C" + str(sid - 140)
                    else:
                        a = f.read(7)
                        continue
                    fre = struct.unpack('B', f.read(1))[0]
                    # fre2 = hex(fre)

                    az = struct.unpack('H', f.read(2))[0]
                    az = round(az * 0.01, 2)
                    sname += "%8s" % str(az)

                    el = struct.unpack('h', f.read(2))[0]
                    el = round(el * 0.01, 2)
                    sname += "%8s" % str(el)
                    rset = struct.unpack('B', f.read(1))[0]
                    sname += "%5s" % str(rset)
                    sinfo = struct.unpack('B', f.read(1))[0]
                    sname += "%5s" % str(sinfo)
                    print(sname)
                    f1.write(sname + "\n")
            else:
                pass
    f.close()
    f1.close()
    print("文件解析完毕："+outfilepath)


analysisFile("G:/ts03/TS0358467")