import serial
import binascii
import struct
from time import strftime, localtime

port = "COM3"
btl = 115200
path1 = "G:\\aaaaaa\\file1"

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

def run(num1,num2):

    ser = serial.Serial(num1, num2)  # 打开串口

    while (True):
        ch = ser.read(1)
        datad2 = binascii.b2a_hex(ch)
        if ch == b'$':
            data2 = ser.read(2)
            if data2 == b'TD':
                print("******进入*******")
                data3 = ser.read(4)
                datad3 = binascii.b2a_hex(data3)
                time = struct.unpack('I', data3)[0]  # 时间

                time = dayTime(time)

                data4 = ser.read(1)
                datad4 = binascii.b2a_hex(data4)
                timetype = struct.unpack('B', data4)[0]  # 时间类型

                data5 = ser.read(1)
                datad5 = binascii.b2a_hex(data5)
                td = struct.unpack('B', data5)[0]  # 通道

                data6 = ser.read(4)
                datad6 = binascii.b2a_hex(data6)
                t1 = struct.unpack('i', data6)[0]  # 时间差1

                data7 = ser.read(4)
                datad7 = binascii.b2a_hex(data7)
                t2 = struct.unpack('i', data7)[0]  # 时间差2

                t3 = '%.3f' % (t1 * 100 + t2 / 1000)

                data8 = ser.read(1)
                datad8 = binascii.b2a_hex(data8)
                jyw = struct.unpack('B', data8)[0]  # 校验位

                print(str(time).rjust(15, " ") + str(timetype).rjust(15, " ") + str(td).rjust(15, " ") + str(t3).rjust(20," "))

def readFile(filepath):

    f = open(filepath,"rb")

    f1 = open("E:\\TD1.txt", "w+")
    f1.write(str("时间").rjust(13, " ")+str("时间类型").rjust(11 ," ")+str("通道").rjust(13 ," ")+
             str("时间差").rjust(17 ," ")+ "\n")
    f2 = open("E:\\TD2.txt", "w+")
    f2.write(str("时间").rjust(13, " ") + str("时间类型").rjust(11, " ") + str("通道").rjust(13, " ") +
             str("时间差").rjust(17," ") + "\n")
    f3 = open("E:\\TD3.txt", "w+")
    f3.write(str("时间").rjust(13, " ") + str("时间类型").rjust(11, " ") + str("通道").rjust(13, " ") +
             str("时间差").rjust(17," ") + "\n")
    while True:
        data1 = f.read(1)
        datad1 = binascii.b2a_hex(data1)
        if not data1:
            break
        elif data1 == b'$':
            data2 = f.read(2)
            datad2 = binascii.b2a_hex(data2)
            if data2 == b'TD':
                data3 = f.read(4)
                datad3 = binascii.b2a_hex(data3)
                time = struct.unpack('I', data3)[0] #时间

                time = dayTime(time)

                data5 = f.read(1)
                datad5 = binascii.b2a_hex(data5)
                td = struct.unpack('B',data5)[0] #通道

                data6 = f.read(4)
                datad6 = binascii.b2a_hex(data6)
                t1 = struct.unpack('i', data6)[0] #时间差1

                data7 = f.read(4)
                datad7 = binascii.b2a_hex(data7)
                t2 = struct.unpack('i', data7)[0] #时间差2
                t3 = '%.3f' % (t1*100+t2/1000)

                data4 = f.read(1)
                datad4 = binascii.b2a_hex(data4)
                timetype = struct.unpack('B', data4)[0]  # 时间类型

                data8 = f.read(1)
                datad8 = binascii.b2a_hex(data8)
                jyw = struct.unpack('B', data8)[0] #校验位

                ti = strftime("%Y-%m-%d %H:%M:%S", localtime())
                print(str(ti).rjust(25," ")+str(time).rjust(15, " ")+str(timetype).rjust(15 ," ")+str(td).rjust(15 ," ")+str(t3).rjust(20 ," "))

                if td==1:
                    f1.write(str(time).rjust(15, " ")+str(timetype).rjust(15 ," ")+str(td).rjust(15 ," ")+str(t3).rjust(20 ," ")+ "\n")
                elif td==2:
                    f2.write(str(time).rjust(15, " ")+str(timetype).rjust(15 ," ")+str(td).rjust(15 ," ")+str(t3).rjust(20 ," ")+ "\n")
                elif td==3:
                    f3.write(str(time).rjust(15, " ")+str(timetype).rjust(15 ," ")+str(td).rjust(15 ," ")+str(t3).rjust(20 ," ")+ "\n")
    f.close()
    f1.close()
    f2.close()
    f3.close()

def main():

    while True:
        print("******************欢迎使用*******************")
        type = input("》请选择使用方式（1：实时串口 2：事后文件）：")
        if type == '1':
            port = input("》请输入端口号:")
            btl = input("》请输入波特率:")
            # print("端口号为："+port+"\n"+"波特率为："+btl+"\n"+"程序启动...")
            print("参数设置完毕，程序开始运行...")
            out = input("是否继续? （y/n）：")
            if out == "n":
                return
        else:
            filepath = input("》请输入文件路径（默认路径为："+path1+"）：")
            if filepath == '':
                filepath = path1
            #print("文件路径:"+filepath)
            out = input("是否继续? （y/n）：")
            if out == "n":
                return


        #print(str(port) + "-----" + str(btl))
        # type1 = input("是否继续？(y/n):")
        # if type1=="n":
        #     return
main()
