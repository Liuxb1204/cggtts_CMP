# FTP操作
import ftplib
import os
import easygui as g

host = '111.205.213.13'
port = 21
username = 'GNSS'
password = '1234567890'


f = ftplib.FTP()  # 实例化FTP对象
f.connect(host,port)
f.login(username, password)  # 登录

# 获取当前路径
# pwd_path = f.pwd()
# print("FTP当前路径:", pwd_path)


def ftp_download(ftpPath,localPath):
    '''以二进制形式下载文件'''
    try:
        bufsize = 1024  # 设置缓冲器大小
        filename = ftpPath.split("/")[-1]
        fp = open(localPath+"\\"+filename, 'wb')
        f.retrbinary('RETR %s' % ftpPath, fp.write, bufsize)
        print(ftpPath, "下载成功")
        fp.close()
    except:
        print(ftpPath,"下载失败")




def ftp_upload(ftpPath,localPath):
    '''以二进制形式上传文件'''
    bufsize = 1024  # 设置缓冲器大小
    fp = open(localPath, 'rb')
    f.storbinary('STOR ' + ftpPath, fp, bufsize)
    fp.close()

# ftp = "/UPLOAD/CGGTTS/TS04/GMTS0458.071"
# print(ftp.split("/")[-1])

folder = os.getcwd()[:-4] + '\\ftp'
print(folder)
# 获取此py文件路径，在此路径选创建在new_folder文件夹中的test文件夹
# if not os.path.exists(folder):
#     os.makedirs(folder)


# ftp_download("/UPLOAD/CGGTTS/TS04/GMTS0458.071",'C:\\Users\\dancer\\Desktop')
# ftp_upload()
name = "GMTS0458065"
f.cwd("/CGGTTS/IM04")

print(f.nlst())
for i in f.nlst():
    for y in range(58065, 58068 + 1):
        if "GM" + "IM04" + str(y) == i.replace(".", ""):
            print("/CGGTTS/IM04"+"/"+i)


f.quit()