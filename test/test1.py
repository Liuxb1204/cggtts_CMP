import numpy as np  # 引入numpy
import scipy as sp
import pylab as pl
from scipy.optimize import leastsq  # 引入最小二乘函数
import myutils2.util as util

n = 3  # 多项式次数


# 目标函数
def real_func(x):
    return np.sin(2 * np.pi * x)


# 多项式函数
def fit_func(p, x):
    f = np.poly1d(p)
    return f(x)


# 残差函数
def residuals_func(p, y, x):
    ret = fit_func(p, x) - y
    return ret


x1 = np.linspace(0, 1, 9)  # 随机选择9个点作为x
x_points = np.linspace(0, 1, 1000)  # 画图时需要的连续点

y0 = real_func(x1)  # 目标函数
y1 = [np.random.normal(0, 0.1) + y for y in y0]  # 添加正太分布噪声后的函数

p_init = np.random.randn(n)  # 随机初始化多项式参数

print(p_init)
print("x:",x1)
print("y1:",y1)

plsq = leastsq(residuals_func, p_init, args=(y1, x1))

print(plsq)

print ('Fitting Parameters: ', plsq[0])  # 输出拟合参数

# pl.plot(x_points, real_func(x_points), label='real')
pl.plot(x_points, fit_func(plsq[0], x_points), label='fitted curve')
pl.plot(x1, y1, 'bo', label='with noise')
pl.legend()
pl.show()


def getCurveFitting(x,y,n=3):
    """
    最小二乘法曲线拟合
    :param x: x轴数据
    :param y: y轴数据
    :param n: 多项式次数
    :return:
    """
    p_init = np.random.randn(n)  # 随机初始化多项式参数

    bzc = util.getStanDeviation(y) # 标准差

    plsq = leastsq(residuals_func, p_init, args=(y, x))[0]
    for i in range(len(x)):
        a = plsq[0]*pow(x[i],n-1)+plsq[1]*pow(x[i],n-2)+plsq[2]*pow(x[i],n-3)-y[i]
        if a>=bzc*3:
            print(x[i],"剔除",y[i])