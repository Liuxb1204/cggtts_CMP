from collections import OrderedDict
f = open("E:\\pythonconfig\\TX10\\GZTX1058.216")
i = 0
list = []
for line in f:
    i = i + 1
    if i>=20:
        SAT = line[0:3].strip()
        MJD = line[7:12].strip()
        STTIME = line[13:19].strip()
        REFSYS = line[53:64].strip()
        MDTR = line[81:85].strip()
        MDIO = line[91:95].strip()
        MSIO = line[101:105].strip()
        FRC = line[121:124].strip()
        if len(SAT) == 2:
            SAT = " " + SAT
        elif len(SAT) == 1:
            SAT = " 0" + SAT
        str1 = SAT+"++"+MJD+"++"+STTIME+"++"+REFSYS+"++"+MDTR+"++"+MDIO+"++"+MSIO+"++"+FRC
        list.append(str1)
f.close()


data1 = OrderedDict()  # 创建有序字典

list2 = []
time = ""
for i in list:
    sat = i.split("++")[0]
    mjd = i.split("++")[1]
    time1 = mjd + "," + i.split("++")[2]
    if time=="":
        time=time1
    sys = i.split("++")[3]
    mdtr = i.split("++")[4]
    mdio = i.split("++")[5]
    msio = i.split("++")[6]
    frc = i.split("++")[7]
    str = ""

    if time!=time1:
        data1[time]=list2
        list2 = []
        time = time1
        str += sat + "," + time1.split(",")[1] + "," + sys + "," + mdtr + "," + mdio + "," + msio + "," + frc
        list2.append(str)
    else:
        str += sat + "," + time1.split(",")[1] + "," + sys + "," + mdtr + "," + mdio + "," + msio + "," + frc
        list2.append(str)
        time=time1
data1[time]=list2

print("--")
