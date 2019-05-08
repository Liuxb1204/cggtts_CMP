# 遍历字典, 分别打印key, value, key:value
import myutils2.util as util
import os
max = 105
b = 6


suzu1 = [54.2,55.1,57.5,59.3,61.9,max]
suzu2 = [54.2,55.1,57.5,59.3,61.9]

# suzu1 = [4542046,4542056,4542102,4542059,4542055,4542044,4542077,max]
# suzu2 = [4542046,4542056,4542102,4542059,4542055,4542044,4542077]

avg1 = util.getAvg(suzu1)
avg2 = util.getAvg(suzu2)
bzc1 = util.getStanDeviation(suzu1)
bzc2 = util.getStanDeviation(suzu2)





print("平均数          ",avg1,"    ",avg2)
print("最大值减平均值    ",max-avg1,"    ",max-avg2)
print("标准差          ",bzc1,"    ",bzc2)
print(b,"倍的标准差     ",bzc1*b,"    ",bzc2*b)



for i in suzu1:
    if i-avg1>=bzc1*b:
        print("剔除数据：",i)

if bzc1>bzc2*b:
    print("2剔除数据：",max)

import math
print(math.pow(10,-11))








