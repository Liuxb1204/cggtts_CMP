import time
a = -8.60
a1 = '%.3f' % a

from time import strftime, localtime


print(a1)
print(time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time())))
print(strftime("%Y-%m-%d %H:%M:%S", localtime()))