import binascii
import struct
from time import strftime, localtime

filepath = "G:\\aaaaaa\\tdc2"

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


def readFile(filepath):

    f = open(filepath,"rb")

    f1 = open("E:\\TD1.txt", "w+")
    f1.write(str("时间").rjust(23," ")+str("time").rjust(13, " ")+str("时间类型").rjust(11 ," ")+
             str("通道").rjust(13 ," ")+str("时间差").rjust(17 ," ")+ "\n")
    f2 = open("E:\\TD2.txt", "w+")
    f2.write(str("时间").rjust(23," ")+str("time").rjust(13, " ") + str("时间类型").rjust(11, " ") +
             str("通道").rjust(13, " ") + str("时间差").rjust(17," ") + "\n")
    f3 = open("E:\\TD3.txt", "w+")
    f3.write(str("时间").rjust(23," ")+str("time").rjust(13, " ") + str("时间类型").rjust(11, " ") +
             str("通道").rjust(13, " ") + str("时间差").rjust(17," ") + "\n")
    while True:
        data1 = f.read(1)
        datad1 = binascii.b2a_hex(data1)
        if not data1:
            break
        elif data1 == b'$':
            data2 = f.read(1)
            datad2 = binascii.b2a_hex(data2)
            if data2 == b'T':
                data = f.read(1)
                if data == b'D':
                    data3 = f.read(4)
                    datad3 = binascii.b2a_hex(data3)
                    time = struct.unpack('I', data3)[0] #时间
                    #time = dayTime(int(time)/1000)

                    data5 = f.read(1)
                    datad5 = binascii.b2a_hex(data5)
                    td = struct.unpack('B', data5)[0]  # 通道

                    data6 = f.read(8)
                    datad6 = binascii.b2a_hex(data6)
                    t1 = struct.unpack('q', data6)[0]  # 时间差1

                    # data7 = ser.read(4)
                    # file.write(data7)
                    # datad7 = binascii.b2a_hex(data7)
                    # t2 = struct.unpack('i', data7)[0]  # 时间差2

                    t3 = '%.3f' % (t1 / 1000)

                    data4 = f.read(1)
                    datad4 = binascii.b2a_hex(data4)
                    timetype = struct.unpack('B', data4)[0]  # 时间类型

                    data8 = f.read(1)
                    datad8 = binascii.b2a_hex(data8)
                    jyw = struct.unpack('B', data8)[0]  # 校验位


                    ti = strftime("%Y-%m-%d %H:%M:%S", localtime())
                    print(str(ti).rjust(25, " ") + str(time).rjust(15, " ") + str(timetype).rjust(15, " ") +
                          str(td).rjust(15, " ") + str(t3).rjust(25, " "))

                    if td == 1:
                        f1.write(str(ti).rjust(25, " ") + str(time).rjust(15, " ") + str(timetype).rjust(15, " ") +
                                 str(td).rjust(15, " ") + str(t3).rjust(20, " ") + "\n")
                    elif td == 2:
                        f2.write(str(ti).rjust(25, " ") + str(time).rjust(15, " ") + str(timetype).rjust(15, " ") +
                                 str(td).rjust(15, " ") + str(t3).rjust(20, " ") + "\n")
                    elif td == 3:
                        f3.write(str(ti).rjust(25, " ") + str(time).rjust(15, " ") + str(timetype).rjust(15, " ") +
                                 str(td).rjust(15, " ") + str(t3).rjust(20, " ") + "\n")
    f.close()
    f1.close()
    f2.close()
    f3.close()

readFile(filepath)
























