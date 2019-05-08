import myutils.date as d
import os,sys
from collections import OrderedDict

def fileToDIC(path):

    f = open(path)
    i = 0
    data1 = OrderedDict()
    list = []
    key = ""
    for line in f:
        i=i+1
        if i >31:
            if ">" in line:
                if len(list) and key!="" and key!=line:
                    data1[key[2:21]]=list
                    list=[]
                key = line
            elif "G" in line[0:3]:
                list.append(line[0:3]+":"+line[36:50]+","+line[85:98])
    data1[key[2:21]] = list
    #print(data1)
    return  data1

def fileToDIC2(path):

    f = open(path)
    i = 0
    data1 = OrderedDict()
    list = []
    key = ""
    for line in f:
        i=i+1
        if i >203:
            if ">" in line:
                if len(list) and key!="" and key!=line:
                    data1[key[2:21]]=list
                    list=[]
                key = line
            elif "G" in line[0:3]:
                list.append(line[0:3]+":"+line[84:98]+","+line[148:162])
    data1[key[2:21]] = list
    #print(data1)
    return  data1

#fileToDIC("G:\\TF113290.18O\\TF113290.18O")
#fileToDIC("G:\\TS213290.18O\\TS213290.18O")

def getDiff(path1,path2):
    d1 = fileToDIC(path1)
    d2 = fileToDIC(path2)
    list = []

    sitelist = []
    for k in d1:
        str1 = ""
        k1 = d1[k]
        list2 = []
        if k in d2.keys():
            y1 = d2[k]
            for z in y1:
                list2.append(z.split(":")[0][-2:])
            sp =  k.split(" ")
            if sp[5]=="":
                sp[5] = "00"
            str1 += "%-30s" % (sp[0]+"-"+sp[1]+"-"+sp[2]+" "+sp[3]+":"+sp[4]+":"+sp[5])
            #str1 += sp[0] + "-" + sp[1] + "-" + sp[2] + " " + sp[3] + ":" + sp[4] + ":" + sp[5] +"---"
            for z2 in k1:
                a = z2.split(":")[0][-2:]
                if a in list2:
                    try:
                        k1v1 = float(z2.split(":")[1].split(",")[0])
                        k1v2 = float(z2.split(":")[1].split(",")[1])
                    except:
                        print(k+" G"+ a +" is null...")
                        continue
                    for x in y1:
                        if "G"+a in x:
                            if "G"+a not in sitelist:
                                sitelist.append("G"+a)
                            try:
                                y1v1 = float(x.split(":")[1].split(",")[0])
                                y1v2 = float(x.split(":")[1].split(",")[1])
                            except:
                                print(k +" G"+ a+ " is null...")
                                continue
                            str1 += ("%-27s" % ("G"+a+":"+str(k1v1-y1v1))) + ("%-28s" % str(k1v2-y1v2))
                            #str1 += "G" + a + ":" + str(k1v1 - y1v1) +","+ str(k1v2 - y1v2)+"---"
                            break
            str1 += "\n"
            list.append(str1)

    #print("--")
    return list,sitelist


def writeFile():
    list,sitelist = getDiff("G:\\aaaaaa\\TF143380.18O","G:\\aaaaaa\\TS023380.18O")
    file1 = open("C:\\Users\\dancer\\Desktop\\OZ_data.txt", "w")
    for i in list:
        file1.write(i)
    file1.close()

def writeFile2():
    list,sitelist = getDiff("G:\\TF113290.18O\\TF113290.18O","G:\\TS213290.18O\\TS213290.18O")
    sitelist.sort()
    #sitedata = OrderedDict()
    x = 0
    list3 = []
    #for i in sitelist:
     #   x+=45
      #  sitedata[i] = str(x)
    file1 = open("C:\\Users\\dancer\\Desktop\\OZ_data.txt", "w")
    ss = ""
    for b in list:
        file1.write("%-30s" % b.split("---")[0])
        ss+="%-30s" % b.split("---")[0]
        for a in sitelist:
           # file1.write(a+":")
            #ss+=a+":"
            #inde = sitelist.index(a)+1
            #for c in range(inde):
             #   file1.write("%45s" % " ")
              #  ss+="%45s" % " "
            for d in b.split("---"):
                if "-" not in d:
                    if a in d:
                        file1.write("%-45s" % d)
                        ss+="%-45s" % d
                        break
                    else:
                        file1.write("%-45s" % a)
                        ss+="%-45s" % a
        file1.write("\n")
        ss = ""
    file1.close()

writeFile()