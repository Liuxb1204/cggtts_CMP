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


filename = "TS0258471.dat"
f = open(filename, "rb")
f2 = open(filename.split(".")[0]+"_data.txt","w+")
f2.write("datetime".rjust(19, " ") +"   "+ "a0".rjust(30, " ") + "a1".rjust(30, " ") +
                      "tot".rjust(10, " ") + "wnt".rjust(10, " ") +
                      "dtls".rjust(10, " ") + "dn".rjust(10, " ") +
                      "wnlsf".rjust(10, " ") + "dtlsf".rjust(10, " ")+"\n")

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
                datestr = date1 +" "+ time1
        elif data2 == b'CU':
            data5 = f.read(3)
            datad5 = binascii.b2a_hex(data5)
            if data5 == b'\x30\x31\x38':
                bin_data = ""
                a0 = str(struct.unpack('d', f.read(8))[0])
                a1 = str(struct.unpack('f', f.read(4))[0])
                tot = str(struct.unpack('I', f.read(4))[0])
                wnt = str(struct.unpack('H', f.read(2))[0])
                dtls = str(struct.unpack('b', f.read(1))[0])
                dn = str(struct.unpack('B', f.read(1))[0])
                wnlsf = str(struct.unpack('H', f.read(2))[0])
                dtlsf = str(struct.unpack('b', f.read(1))[0])

                print(datestr.ljust(22, " ") + str(a0).rjust(30, " ") + str(a1).rjust(30, " ") +
                         str(tot).rjust(10, " ") + str(wnt).rjust(10, " ") +
                         str(dtls).rjust(10, " ") + str(dn).rjust(10, " ") +
                         str(wnlsf).rjust(10, " ") + str(dtlsf).rjust(10, " "))

                f2.write(datestr.ljust(22, " ") + str(a0).rjust(30, " ") + str(a1).rjust(30, " ") +
                      str(tot).rjust(10, " ") + str(wnt).rjust(10, " ") +
                      str(dtls).rjust(10, " ") + str(dn).rjust(10, " ") +
                      str(wnlsf).rjust(10, " ") + str(dtlsf).rjust(10, " ")+"\n")
f.close()
f2.close()






