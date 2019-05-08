import serial
import binascii
import struct
from time import strftime, localtime


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


num1 = "COM3"
num2 = 115200

def run(num1,num2):

    if "COM" in num1 or "com" in num1:
        pass
    else:
        num1="COM"+num1

    ser = serial.Serial(num1, num2)  # 打开串口

    file = open("E:\\TDC.dat", "wb+")

    f1 = open("E:\\TD1.txt", "w+")
    f1.write(str("时间").rjust(23, " ") + str("time").rjust(13, " ") + str("时间类型").rjust(11, " ") +
             str("通道").rjust(13," ") + str("时间差").rjust(17, " ") + "\n")
    f2 = open("E:\\TD2.txt", "w+")
    f2.write(str("时间").rjust(23, " ") + str("time").rjust(13, " ") + str("时间类型").rjust(11, " ") +
             str("通道").rjust(13," ") + str("时间差").rjust(17, " ") + "\n")
    f3 = open("E:\\TD3.txt", "w+")
    f3.write(str("时间").rjust(23, " ") + str("time").rjust(13, " ") + str("时间类型").rjust(11, " ") +
             str("通道").rjust(13," ") + str("时间差").rjust(17, " ") + "\n")

    while (True):
        ch = ser.read(1)
        file.write(ch)
        datad2 = binascii.b2a_hex(ch)
        if ch == b'$':
            data2 = ser.read(1)
            file.write(data2)
            if data2 == b'T':
                data1 = ser.read(1)
                file.write(data1)
                if data1 == b'D':
                    #print("******进入*******")
                    data3 = ser.read(4)
                    file.write(data3)
                    datad3 = binascii.b2a_hex(data3)
                    time = struct.unpack('I', data3)[0]  # 时间
                    #time = dayTime(time)

                    data5 = ser.read(1)
                    file.write(data5)
                    datad5 = binascii.b2a_hex(data5)
                    td = struct.unpack('B', data5)[0]  # 通道

                    data6 = ser.read(4)
                    file.write(data6)
                    datad6 = binascii.b2a_hex(data6)
                    t1 = struct.unpack('i', data6)[0]  # 时间差1

                    data7 = ser.read(4)
                    file.write(data7)
                    datad7 = binascii.b2a_hex(data7)
                    t2 = struct.unpack('i', data7)[0]  # 时间差2

                    t3 = '%.3f' % (t1 * 100 + t2 / 1000)

                    data4 = ser.read(1)
                    file.write(data4)
                    datad4 = binascii.b2a_hex(data4)
                    timetype = struct.unpack('B', data4)[0]  # 时间类型

                    data8 = ser.read(1)
                    file.write(data8)
                    datad8 = binascii.b2a_hex(data8)
                    jyw = struct.unpack('B', data8)[0]  # 校验位

                    file.write(ser.read())

                    ti = strftime("%Y-%m-%d %H:%M:%S", localtime())
                    print(str(ti).rjust(20, " ") + str(time).rjust(10, " ") + str(timetype).rjust(5, " ") +
                          str(td).rjust(5, " ") + str(t3).rjust(20, " "))

                    if td == 1:
                        f1.write(str(ti).rjust(25, " ") + str(time).rjust(15, " ") + str(timetype).rjust(15, " ") +
                                 str(td).rjust(15, " ") + str(t3).rjust(20, " ") + "\n")
                    elif td == 2:
                        f2.write(str(ti).rjust(25, " ") + str(time).rjust(15, " ") + str(timetype).rjust(15, " ") +
                                 str(td).rjust(15, " ") + str(t3).rjust(20, " ") + "\n")
                    elif td == 3:
                        f3.write(str(ti).rjust(25, " ") + str(time).rjust(15, " ") + str(timetype).rjust(15, " ") +
                                 str(td).rjust(15, " ") + str(t3).rjust(20, " ") + "             "+str(datad3)+
                                 str(datad5)+str(datad6)+str(datad7)+str(datad4)+str(datad8)+"\n")

    f1.close()
    f2.close()
    f3.close()
    file.close()




#run(num1,num2)

def main():

    while True:
        print("******************欢迎使用*******************")
        port = input("》请输入串口号:")
        btl = input("》请输入波特率:")
        try:
            run(str(port),btl)
            print("参数设置完毕，程序开始运行，文件默认保存在E盘...")
        except:
            print("串口打开失败或波特率设置错误")

main()

