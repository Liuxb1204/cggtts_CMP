import binascii
import struct
import datetime


def stampToDate(timeStamp):
    dateArray = datetime.datetime.utcfromtimestamp(timeStamp)
    otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
    return otherStyleTime



f = open("G:\\ts03\\TS0358468", "rb")
#f = open("G:\\ts03\\tt", "rb")
time1 = 315964800
f1 = open("G:\\ts03\\data.txt","w")
f1.write("%10s" % "time_stamp")
f1.write("%22s" % "utc_time")
f1.write("%6s" % "num")
f1.write("%8s" % "az")
f1.write("%8s" % "el")
f1.write("%5s" % "#1")
f1.write("%7s" % "#2\n\n")
s = ""


while True:
    data = f.read(2)
    if not data:
        break
    sync = b'\x24\x40'
    # hexstr = binascii.b2a_hex(data)  # 2 - 16
    # hexstr = str(hexstr)[2:6]
    # t = int(hexstr,16)             # 16 - 10
    # t2 = bin(t)
    # data = f.read(1)
    # if not data:
    #     break
    # hexstr1 = struct.unpack('B', data)[0]
    # hexstr2 = struct.unpack('B', f.read(1))[0]
    # if hexstr1==36 and hexstr2==64:
    #if "2440" == hexstr:
    if data == sync:
        #print(hexstr)
        crc = struct.unpack('H', f.read(2))[0]
        id1 = struct.unpack('H', f.read(2))[0]
        #data2 = binascii.b2a_hex(f.read(2))
        # data3 = str(binascii.b2a_hex(f.read(2)))
        # st = data3[4:6]+data3[2:4]
        # t = int(st, 16)
        if id1 & 8191 == 4012:
            print("---------------------------------------------------")
            # data4 = str(binascii.b2a_hex(f.read(2)))
            # st1 = data4[4:6]+data4[2:4]
            # size = int(st1,16)
            length = struct.unpack('H', f.read(2))[0]

            tow = struct.unpack('I', f.read(4))[0]
            tow1 = tow * 0.001
            #tow = str(binascii.b2a_hex(f.read(4)))
            #tow = int(tow[2:10],16)*0.001


            wnc = struct.unpack('H', f.read(2))[0]
            wnc2 = hex(wnc)
            wnc1 = wnc * 604800
            # wnc = str(binascii.b2a_hex(f.read(2)))
            # wnc = int(wnc[2:6],16)*604800

            time2 = time1 + wnc1 + tow1
            time3 = stampToDate(time2)

            if time3=="2018-12-17 12:41:10":
                print()

            n = struct.unpack('B', f.read(1))[0]
            n2 = hex(n)
            # n = str(binascii.b2a_hex(f.read(1)))
            # n = int(n[2:4])
            sblen = struct.unpack('B', f.read(1))[0]
            sblen2 = hex(sblen)
            for i in range(n):
                #sid = str(binascii.b2a_hex(f.read(1))) # 卫星号
                #sid = int(sid[2:4],16)
                sid = struct.unpack('B', f.read(1))[0] #卫星号
                sid2 = hex(sid)

                sname = ""
                sname +=str(int(time2))+"   "+time3+"   "
                if sid>=1 and sid<=37:
                    if sid<10:
                        sname += "G0" + str(sid)
                    else:
                        sname += "G"+str(sid)
                elif sid>=38 and sid<=61:
                    if sid-37<10:
                        sname += "R0" + str(sid - 37)
                    else:
                        sname += "R" + str(sid-37)
                elif sid >=63 and sid <=68:
                    if sid-38<10:
                        sname += "R0" + str(sid - 38)
                    else:
                        sname += "R" + str(sid - 38)
                elif sid>=71 and sid<=106:
                    if sid-70<10:
                        sname += "E0" + str(sid - 70)
                    else:
                        sname += "E" + str(sid-70)
                elif sid >= 141 and sid <= 177:
                    if sid-140<10:
                        sname += "C0" + str(sid - 140)
                    else:
                        sname += "C" + str(sid-140)
                else:
                   a = f.read(7)
                   continue
                fre = struct.unpack('B', f.read(1))[0]
                fre2 = hex(fre)

                az = struct.unpack('H', f.read(2))[0]
                az = round(az * 0.01,2)
                #az = str(binascii.b2a_hex(f.read(2)))
                #az = az[4:6]+az[2:4]
                #az = round(int(az[2:6],16)*0.01,2)
                sname +="%8s" % str(az)

                el = struct.unpack('h', f.read(2))[0]
                el = round(el * 0.01,2)
                #el = str(binascii.b2a_hex(f.read(2)))
                #el = el[4:6]+el[2:4]
                #el = round(int(el[2:6],16)*0.01,2)
                sname +="%8s" % str(el)
                # rset = str(binascii.b2a_hex(f.read(1)))
                # rset = int(rset[2:4],16)
                # rset = str(rset)
                rset = struct.unpack('B', f.read(1))[0]
                #rset = struct.unpack('H', f.read(2))
                #rset = str(rset).split("(")[1].split(",")[0]
                sname +="%5s" % str(rset)
                # sinfo = str(binascii.b2a_hex(f.read(1)))
                # sinfo = int(sinfo[2:4], 16)
                # sinfo = str(sinfo)
                sinfo = struct.unpack('B', f.read(1))[0]
                sname +="%5s" % str(sinfo)
                print(sname)
                f1.write(sname+"\n")
        else:
            pass
f.close()
f1.close()
print("end......")


# c = '\xbb\x2f'
# print(c)



