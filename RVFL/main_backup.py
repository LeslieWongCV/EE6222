# -*- coding: utf-8 -*-
# @Time    : 2021/4/4 10:01 上午
# @Author  : Yushuo Wang
# @FileName: ELM.py
# @Software: PyCharm
# @Blog    ：https://lesliewongcv.github.io/

import numpy as np
import os
from scipy.io import loadmat
from sklearn.model_selection import KFold
from sklearn.preprocessing import scale


def sigmoid(a, b, x):
    return 1.0 / (1 + np.exp(-1.0 * (x.dot(a) + b)))


def RVFL_prototype(X, T, C, n, L, node_num):
    '''
    回归问题的RVFL标准算法
    变量：X - input 输入数据；No. of samples * No. of feature（N*n）
           ：H - H matrix；No. of samples * No. of hidden layers（N*L）
           ：T - Target；No. of samples * No. of output layers（N*M）
           ：C - Hyper-parm of the regularization
    '''
    # init the weight of hidden layers randomly
    a = np.random.normal(0, 1, (n, node_num))
    b = np.random.normal(0, 1)
    T = one_hot(T)
    H = sigmoid(a, b, X)
    D = np.concatenate((X, H), axis=1)
    DD = D.T.dot(D)
    DT = D.T.dot(T)
    # calculate the weight of output layers(beta) and output
    if L > n:
        beta = np.linalg.pinv(DD + np.identity(node_num + n) / C).dot(DT)
    else:
        beta = D.T.dot(np.linalg.pinv(D.dot(D.T) + np.identity(node_num + n) / C)).dot(T)
    output = D.dot(beta)
    return beta, output, a, b


def one_hot(l):
    y = np.zeros([len(l), np.max(l)+1])
    for i in range(len(l)):
        y[i, l[i]] = 1
    return y


def predict(X, BETA, a, b):
    H = sigmoid(a, b, X)
    D = np.concatenate((X, H), axis=1)
    Y = D.dot(BETA)
    Y = Y.argmax(1)
    return Y


def evaluation(y_hat, goundtruth):
    y_hat = y_hat[:, np.newaxis]
    return np.sum(np.equal(y_hat, goundtruth) / len(y_hat))


KFOLD = 4
PATH = '/Users/leslie/Downloads/MatDataset/'  # Path to the dataset
folders = os.listdir(PATH)
RES = []
describe = []
C_list = [1e-3, 1e-2, 1e-1, 1, 1e1, 1e2, 1e3, 1e5]  # # hyper-pram 1/C
progress = 0
best_C = 0
res2 = []
best__C = []

for folder_name in folders[:12]:
    best_acc = 0
    progress += 100/12

    file_name = folder_name
    if folder_name == '.DS_Store':
        continue
    else:
        matfn = PATH + folder_name + '/' + folder_name + '_Train.mat'
        matfn_t = PATH + folder_name + '/' + folder_name + '_Test.mat'

        df_data_t = scale(loadmat(matfn_t)['Data'])
        df_label_t = loadmat(matfn_t)['Label']
        df_data = scale(loadmat(matfn)['Data'])
        df_label = loadmat(matfn)['Label']

        kf = KFold(n_splits=4, shuffle=False)
        for C in C_list:
            vali_res = 0
            for train_index, test_index in kf.split(df_label):  # 4-fold
                beta, Fl, A, B = RVFL_prototype(df_data[train_index], df_label[train_index], C=C, n=len(df_data[1]), L=len(train_index), node_num=100)
                y_valid = predict(df_data[test_index], beta, A, B)
                acc_valid = evaluation(y_valid, df_label[test_index])
                vali_res += acc_valid
            RES += [folder_name + ':   ' + str(round(10 ** 4 * vali_res/4) / 10 ** 4) + '   C = ' + str(C)]
            if vali_res/4 > best_acc:
                best_acc = vali_res/4
                best_C = C
        res2 += [folder_name + ':' + str(best_acc) + '   best C = ' + str(best_C)]
        best__C += [best_C]

    print(str(round(progress)) + "%")  # show progress
RES = np.array(RES)
np.savetxt("RVFL_acc_1e-3 1e5.txt", RES, fmt='%s', delimiter=',')
np.savetxt("RVFL_test_1e-3 1e5.txt", res2, fmt='%s', delimiter=',')


