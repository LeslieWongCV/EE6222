# -*- coding: utf-8 -*-
# @Time    : 2021/11/4 1:07 下午
# @Author  : Yushuo Wang
# @FileName: 8points.py
# @Software: PyCharm
# @Blog    ：https://lesliewongcv.github.io/
import numpy as np
import math
# X = '1986 944 1807 815 1639 972 1421 862 1500 1361 2108 2067 3351 1094 3420 1090'
X = '1646 665 1492 509 1279 668 1079 519 1127 1040 1654 1819 2864 936 2917 936'
# P = '1943 809 1903 657 1509 822 1388 663 1429 1249 1732 2003 3060 1042 3113 1042'
P = '1055 1012 911 883 666 1005 447 879 500 1406 1092 2150 2265 1260 2318 1266'
X_ = X.split()  # [8,2]
P_ = P.split()
f = 2678.2
i = 0
Xn = []
tmp = []
for j in range(16):
    if i < 2:
        tmp.append(int(X_[j]))
        i += 1
    else:
        tmp.append(int(f))  # add f [8,2] - [8,3]
        Xn.append(tmp)
        tmp = []
        i = 0
        tmp.append(int(X_[j]))
        i += 1
tmp.append(int(f))
Xn.append(tmp)

i = 0
Pn = []
tmp = []
for j in range(16):
    if i < 2:
        tmp.append(int(P_[j]))
        i += 1
    else:
        tmp.append(int(f))
        Pn.append(tmp)
        tmp = []
        i = 0
        tmp.append(int(P_[j]))
        i += 1
tmp.append(int(f))
Pn.append(tmp)

Xn = np.array(Xn)
Pn = np.array(Pn)

Xn = [np.divide(_, np.linalg.norm(_)) for _ in Xn]
Pn = [np.divide(_, np.linalg.norm(_)) for _ in Pn]


Xn_mean = np.mean(Xn, axis=0)
Pn_mean = np.mean(Pn, axis=0)

Xn_dev = Xn - Xn_mean
Pn_dev = Pn - Pn_mean
# np.transpose(Xn_dev[0][np.newaxis, : ], (1,0))

M = np.zeros((3, 3))
for i in range(8):
    M += np.dot(np.transpose(Xn_dev[i][np.newaxis, :], (1, 0)), Pn_dev[i][np.newaxis, :])

# W_2 = np.dot(np.transpose(Xn_dev, (1,0)), Pn_dev)
U,sigma,VT = np.linalg.svd(M)

R = np.dot(U, VT)

theta = math.degrees(np.arccos((np.trace(R)-1)/2))
