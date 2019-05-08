import sys
import myutils2.util as util
import  collections
import struct
import operator
# import compileall
#
# compileall.compile_dir('C:\\Users\\dancer\\Desktop\\python\\work') #path是包括.py文件名的路径
# pathname = "E:\\pythonconfig\\TX10\\GZTX1058.216"
# map1 = util.fileToDictionary(pathname)
# map2 = util.fileToDIC(pathname)
# print("--")
dic = collections.OrderedDict()
dic["d02"] = 4
dic["b22"] = 2
dic["c31"] = 3
dic["d03"] = 7
dic["b20"] = 8
dic["c50"] = 9
# print(type(dic))
# dic = sorted(dic)
#
# # sorted(dic.items(),key=lambda item:item[0])
# # sorted(dic.items(),key=operator.itemgetter(0))
# print(type(dic))
# dic = list(dic)
# print(dic)

def sortdic(dic):

    dic2 = collections.OrderedDict()
    diclist = sorted(dic)

    for d in diclist:
        dic2[d] = dic[d]
    return dic2
base = [str(x) for x in range(10)] + [ chr(x) for x in range(ord('A'),ord('A')+6)]
# 十六进制 to 十进制
def hex2dec(string_num):
 return str(int(string_num.upper(), 16))

# 十进制 to 二进制: bin()
def dec2bin(string_num):
    num = int(string_num)
    mid = []
    while True:
        if num == 0: break
    num, rem = divmod(num, 2)
    mid.append(base[rem])

    return ''.join([str(x) for x in mid[::-1]])

# hex2tobin
# 十六进制 to 二进制: bin(int(str,16))
def hex2bin(string_num):
 return dec2bin(hex2dec(string_num.upper()))


# aaa = bin(int("254c41e2", 16))
# print(aaa)


import sys
import binascii
# def LongToInt(value):
#     assert isinstance(value, (int, long))
#     return int(value & sys.maxint)

# dic2 = sortdic(dic)
# print(dic2)

def intToBin32(i):
    return (bin(((1 << 32) - 1) & i)[2:]).zfill(32)

s = "123456789"
num = int("111", 2)
num2 = bin(2)
num4 = 1028 * pow(2,24)

bt2 = bytearray(4)
bt2[0] = int("FF",16)
bt2[1] = 0xFC
al = type(0xFF)
print(al)
a = str.encode(hex(10))


b = bytearray()
b.append(15)
b.append(20)
print(b)



