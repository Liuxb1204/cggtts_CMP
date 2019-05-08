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


def signeddata(val,nbits):
    result = 0x0
    result = (val << (32-nbits)) & 2147483647
    result = result >> (32-nbits)
    return result


f = open("G:\\ts03\\bds_cd03", "rb")
f2 = open("G:\\ts03\\bds_data3.txt","w+")
f2.write("datetime".rjust(19, " ") +"   "+ "prn".rjust(5, " ") + "time".rjust(10, " ") +
        "type".rjust(15, " ") + "A0_utc".rjust(28, " ") + "A1_utc".rjust(28, " ") +
        "dT_ls".rjust(10, " ") + "dT_lsf".rjust(10, " ") + "DN_lsf".rjust(10, " ") +
         "WN_lsf".rjust(10, " ") + "\n")

date1 = ""
datestr = ""

while True:
    data1 = f.read(1)
    datad1 = binascii.b2a_hex(data1)
    if not data1:
        break
    elif data1 == b'\x0A':
        data2 = f.read(2)
        datad2 = binascii.b2a_hex(data2)
        if data2 == b'RD':
            data3 = f.read(3)
            datad3 = binascii.b2a_hex(data3)
            if data3 == b'\x30\x30\x36':
                y = struct.unpack('H', f.read(2))[0]  # 年
                m = struct.unpack('B', f.read(1))[0]  # 月
                d = struct.unpack('B', f.read(1))[0]  # 日
                b = struct.unpack('B', f.read(1))[0]
                if y == 65535 or m == 255 or d == 255:
                    print("rd无效值")
                    break
                date1 = str(y) + "-" + str(m) + "-" + str(d)
        elif data2 == b'~~':
            data4 = f.read(3)
            datad4 = binascii.b2a_hex(data4)
            if data4 == b'\x30\x30\x35':
                data5 = f.read(4)
                datad5 = binascii.b2a_hex(data5)
                rt = struct.unpack('I', data5)[0]  # 天内秒
                if rt == 4294967295:
                    continue  # 无效值
                time1 = dayTime(rt / 1000)
                if date1 == "":
                    date1 = "          "
                datestr = date1 +" "+ time1
        elif data2 == b'cd':
            data5 = f.read(3)
            datad5 = binascii.b2a_hex(data5)
            if data5 == b'\x30\x33\x30':
                bin_data = ""
                prn_u = struct.unpack('B', f.read(1))[0]
                if prn_u > 5:
                    if prn_u<10:
                        prn_u = "C0" + str(prn_u)
                    else:
                        prn_u = "C" + str(prn_u)
                    s1 = f.read(4)
                    datas1 = binascii.b2a_hex(s1)
                    time_u = struct.unpack('I', s1)[0]
                    s2 = f.read(1)
                    datas2 = binascii.b2a_hex(s2)
                    type_u = struct.unpack('B', s2)[0]
                    if type_u == 0:
                        type_u = "B1"
                    elif type_u == 1:
                        type_u = "B2"
                    elif type_u == 2:
                        type_u = "B3"
                    elif type_u == 3:
                        type_u = "B1 from CEO"
                    elif type_u == 4:
                        type_u = "B2 from CEO"
                    elif type_u == 5:
                        type_u = "B2 from CEO"
                    elif type_u == 6:
                        type_u = "B1C"
                    elif type_u == 7:
                        type_u = "B1-2"

                    s3 = f.read(1)
                    datas3 = binascii.b2a_hex(s3)
                    len_u = struct.unpack('B', s3)[0]

                    pinput = []
                    # pinput2 = []
                    poutput = []
                    for i in range(len_u):
                        data6 = f.read(4)
                        datad6 = binascii.b2a_hex(data6)
                        data_u = struct.unpack('I', data6)[0]
                        # pinput2.append(data6)
                        pinput.append(data_u)
                    poutput.append((pinput[0] >> 2) & 0x3FFFFFFF)
                    poutput.append(((pinput[0] & 0x000003) << 28) | ((pinput[1] >> 4) & 0x0FFFFFFF))
                    poutput.append(((pinput[1] & 0x00000F) << 26) | ((pinput[2] >> 6) & 0x03FFFFFF))
                    poutput.append(((pinput[2] & 0x00003F) << 24) | ((pinput[3] >> 8) & 0x00FFFFFF))
                    poutput.append(((pinput[3] & 0x0000FF) << 22) | ((pinput[4] >> 10) & 0x003FFFFF))
                    poutput.append(((pinput[4] & 0x0003FF) << 20) | ((pinput[5] >> 12) & 0x000FFFFF))
                    poutput.append(((pinput[5] & 0x000FFF) << 18) | ((pinput[6] >> 14) & 0x0003FFFF))
                    poutput.append(((pinput[6] & 0x003FFF) << 16) | ((pinput[7] >> 16) & 0x0000FFFF))
                    poutput.append(((pinput[7] & 0x00FFFF) << 14) | ((pinput[8] >> 18) & 0x00003FFF))
                    poutput.append(((pinput[8] & 0x03FFFF) << 12) | ((pinput[9] >> 16) & 0x00000FFF))

                    for y in range(len_u):
                        poutput[y] <<= 2

                    FraID = (poutput[0] & 0x0001C000) >> 14
                    if FraID == 5:
                        Pnum = (poutput[1] & 0x0007F000) >> 12
                        if Pnum == 10:
                            utcmap = ((poutput[1] >> 10) & 0x03 << 6) | (poutput[2] >> 26) & 0x3F
                            tls = utcmap
                            tlsf = signeddata(poutput[2] >> 18, 8)
                            WNlsf = (poutput[2] >> 10) & 0xFF
                            utc1 = poutput[3] & 0xFFFFFC00
                            utch = hex(utc1)[2:]
                            fmt = ""
                            bts = bytearray()
                            for u1 in range(0, len(utch), 2):
                                bts.append(int(utch[u1:u1+2], 16))
                            if len(bts) == 4:
                                fmt = "!i"
                            elif len(bts) == 1:
                                fmt = "!b"
                            utc1 = struct.unpack(fmt, bts)[0]
                            utc2 = (poutput[4] >> 22) & 0x03FF
                            A0utc = (utc1 | utc2) * 9.31322574615479e-10
                            utcmap = ((poutput[4] & 0x003FFC00) << 2) | ((poutput[5] >> 20) & 0x0FFF)
                            if utcmap & 0x800000:
                                utcmap |=0xFF000000
                            utcmapu = hex(utcmap)[2:]
                            if len(utcmapu)==1:
                                utcmapu = "0"+utcmapu
                            bts2 = bytearray()
                            for u2 in range(0, len(utcmapu) ,2):
                                bts2.append(int(utcmapu[u2:u2+2], 16))
                            if len(bts2) == 4:
                                fmt = "!i"
                            elif len(bts2) == 1:
                                fmt = "!b"
                            utcmap2 = struct.unpack(fmt, bts2)[0]
                            A1utc = utcmap2 * 8.881784197e-16
                            DN = (poutput[5] >> 12) & 0xFF
                            print("datetime:" + datestr + "\n" + "prn:" + str(prn_u) + "\n" + "time:" + str(time_u) + "\n" +
                                "type:" + str(type_u) + "\n" + "A0_utc:" + str(A0utc) + "\n" + "A1_utc:" + str(A1utc) + "\n" +
                                "dT_ls:" + str(tls) + "\n" + "dT_lsf:" + str(tlsf) + "\n" + "DN_lsf:" + str(DN) + "\n" +
                                "WN_lsf:" + str(WNlsf) + "\n" + "------------------------------")
                            f2.write(datestr+ "   " + str(prn_u).rjust(5, " ") + str(time_u).rjust(10, " ") +
                                str(type_u).rjust(15, " ") + str(A0utc).rjust(28, " ") + str(A1utc).rjust(28, " ") +
                                str(tls).rjust(10, " ") + str(tlsf).rjust(10, " ") + str(DN).rjust(10, " ") +
                                str(WNlsf).rjust(10, " ") + "\n")
f.close()
f2.close()




