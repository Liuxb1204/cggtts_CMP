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


filename = "TS0458503.dat"
f = open("G:\\ts03\\" + filename, "rb")
f2 = open("G:\\ts03\\" + filename.split(".")[0]+"_data.txt","w+")

f2.write("time".rjust(8," ") + "tow".rjust(10, " ") + "wnc".rjust(12, " ") + "prn".rjust(6, " ") +"wn".rjust(10, " ")+
         "t_oc".rjust(20, " ")+"t_oe".rjust(20, " ") + "wnt_oc".rjust(10, " ") + "wnt_oe".rjust(10, " ")+"\n")


while True:
    data1 = f.read(1)
    datad1 = binascii.b2a_hex(data1)
    if not data1:
        break
    elif data1 == b'\x24':
        data2 = f.read(1)
        datad2 = binascii.b2a_hex(data2)
        if data2 == b'\x40':
            try:
                CRC = struct.unpack('H', f.read(2))[0]
                ID = struct.unpack('H', f.read(2))[0]
            except:
                continue
            Length = struct.unpack('H', f.read(2))[0]
            if Length % 4 == 0 and Length == 140:
                datestr = ""
                data3 = f.read(4)
                datad3 = binascii.b2a_hex(data3)

                TOW = struct.unpack('I', data3)[0]/1000
                TOW1 = TOW % 86400
                h = str(TOW1 / 3600).split(".")[0]
                m = str((TOW1 % 3600) / 60).split(".")[0]
                s = str((TOW1 % 3600) % 60).split(".")[0]

                if len(h)<2:
                    h = "0"+h
                if len(m)<2:
                    m = "0"+m
                if len(s)<2:
                    s = "0"+s
                datestr = datestr +h+":"+m+":"+s

                data5 = f.read(2)
                datad5 = binascii.b2a_hex(data5)
                WNC = struct.unpack('H', data5)[0]
                data6 = f.read(1)
                datad6 = binascii.b2a_hex(data6)
                PRN = struct.unpack('B', data6)[0]
                Reserved = struct.unpack('B', f.read(1))[0]
                data7 = f.read(2)
                datad7 = binascii.b2a_hex(data7)
                WN = struct.unpack('H', data7)[0]
                CAorPronL2 = struct.unpack('B', f.read(1))[0]
                URA = struct.unpack('B', f.read(1))[0]
                health = struct.unpack('B', f.read(1))[0]
                L2DataFlag = struct.unpack('B', f.read(1))[0]
                IODC = struct.unpack('H', f.read(2))[0]
                IODE2 = struct.unpack('B', f.read(1))[0]
                IODE3 = struct.unpack('B', f.read(1))[0]
                FitIntFlag = struct.unpack('B', f.read(1))[0]
                Reserved2 = struct.unpack('B', f.read(1))[0]
                T_gd = struct.unpack('f', f.read(4))[0]
                t_oc = struct.unpack('I', f.read(4))[0]
                a_f2 = struct.unpack('f', f.read(4))[0]
                a_f1 = struct.unpack('f', f.read(4))[0]
                a_f0 = struct.unpack('f', f.read(4))[0]
                C_rs = struct.unpack('f', f.read(4))[0]
                DEL_N = struct.unpack('f', f.read(4))[0]
                M_0 = struct.unpack('d', f.read(8))[0]
                C_uc = struct.unpack('f', f.read(4))[0]
                e = struct.unpack('d', f.read(8))[0]
                C_us = struct.unpack('f', f.read(4))[0]
                SQRT_A = struct.unpack('d', f.read(8))[0]
                t_oe = struct.unpack('I', f.read(4))[0]

                C_ic = struct.unpack('f', f.read(4))[0]
                OMEGA_0 = struct.unpack('d', f.read(8))[0]
                C_is = struct.unpack('f', f.read(4))[0]
                i_0 = struct.unpack('d', f.read(8))[0]
                C_rc = struct.unpack('f', f.read(4))[0]
                omega = struct.unpack('d', f.read(8))[0]
                OMEGADOT = struct.unpack('f', f.read(4))[0]
                IDOT = struct.unpack('f', f.read(4))[0]
                Wnt_oc = struct.unpack('H', f.read(2))[0]
                Wnt_oe = struct.unpack('H', f.read(2))[0]
                Padding = struct.unpack('B', f.read(1))[0]

                print("time:"+datestr+"  wnc:"+str(WNC)+"  prn:"+str(PRN).ljust(5," ")+"  wn:"+str(WN)+
                      "  t_oc:"+str(t_oc)+"  t_oe:"+str(t_oe)+"  WNT_OC:"+str(Wnt_oc)+"  WNT_OE:"+str(Wnt_oe))

                f2.write(datestr.ljust(8, " ")+ str(TOW).rjust(10, " ") + str(WNC).rjust(12, " ") + str(PRN).rjust(6, " ") + str(WN).rjust(10, " ") +
                         str(t_oc).rjust(20, " ")+ str(t_oe).rjust(20, " ") + str(Wnt_oc).rjust(10, " ") + str(Wnt_oe).rjust(10, " ") + "\n")
f.close()
f2.close()






