# -*- coding:utf-8 -*-
"""
调控功效智能识别
2022/7/16
实际使用的程序
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def set_plot(size):
    """设置画图格式"""
    plt.rcParams['xtick.direction'] = 'in'  # 将x周的刻度线方向设置向内
    plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内
    plt.rcParams['font.sans-serif'] = ['Times new roman']
    # plt.rcParams['font.sans-serif'] = ['SimHei']
    config = {
        "font.family": 'serif',
        "font.size": size,
        "mathtext.fontset": 'stix',
        # "font.serif": ['Times new roman'],
        "font.serif": ['SimHei'],
    }
    plt.rcParams.update(config)
    plt.rcParams['axes.unicode_minus'] = False
    bwith = 0.5  # 边框宽度设置为2
    ax = plt.gca()  # 获取边框
    ax.spines['bottom'].set_linewidth(bwith)
    ax.spines['left'].set_linewidth(bwith)
    ax.spines['top'].set_linewidth(bwith)
    ax.spines['right'].set_linewidth(bwith)
    plt.xticks(fontfamily="Times New Roman", fontsize=size)
    plt.yticks(fontfamily="Times New Roman", fontsize=size)


def get_dJ(_w, _flat, _eff):
    """获取梯度"""
    dj = np.dot(-_w.T, _flat - np.dot(_w, _eff)) / _flat.shape[0]
    return dj


def get_J(_w, _flat, _eff):
    """获取损失函数"""
    error = np.dot(_w, _eff) - _flat
    return np.mean(error ** 2) / 2


class LsAdam:
    """ls的Adam优化算法，已知调控量求调控功效和已知调控功效求调控量梯度不一样"""

    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999):
        self.beta1 = beta1
        self.beta2 = beta2
        self.iter = 0
        self.lr = lr
        self.m = None  # 一阶矩估计
        self.v = None  # 二阶矩估计

    def update(self, params, grads):
        """
        更新值
        :param params:需要更新的值
        :param grads: 梯度
        :return:
        """
        if self.m is None:
            self.m, self.v = {}, {}
            for key, val in params.items():
                print(key)
                self.m[key] = np.zeros_like(val)
                self.v[key] = np.zeros_like(val)
        self.iter += 1

        lr_t = self.lr * np.sqrt(1.0 - self.beta2 ** self.iter) / (1.0 - self.beta1 ** self.iter)
        for key in params.keys():
            # print(grads[key])
            self.m[key] += (1 - self.beta1) * (grads[key] - self.m[key])
            self.v[key] += (1 - self.beta2) * (grads[key] ** 2 - self.v[key])
            params[key] -= lr_t * self.m[key] / (np.sqrt(self.v[key]) + 1e-7)


def ls_lerangde_nihe(xishu, have_0_xishu=True):
    flat_x = np.linspace(-1, 1, 80)
    p1 = flat_x
    p2 = 1.5 * pow(flat_x, 2) - 1 / 2
    p3 = 0.5 * (5 * pow(flat_x, 3) - 3 * flat_x)
    p4 = (1 / 8) * (35 * pow(flat_x, 4) - 30 * pow(flat_x, 2) + 3)
    if have_0_xishu:
        y = xishu[0] + xishu[1] * p1 + xishu[2] * p2 + xishu[3] * p3 + xishu[4] * p4
    else:
        y = xishu[0] * p1 + xishu[1] * p2 + xishu[2] * p3 + xishu[3] * p4
        # y = xishu[0] * p1 + xishu[1] * p2 + xishu[2] * p4
    return y


def my_leastq(flat):
    """
    基于勒让德正交多项式的最小二乘法
    :param flat: 需要识别的板形
    :return: 板形特征系数
    """
    flat_x = np.linspace(-1, 1, len(flat))
    p1 = flat_x
    p2 = 1.5 * pow(flat_x, 2) - 1 / 2
    p3 = 0.5 * (5 * pow(flat_x, 3) - 3 * flat_x)
    p4 = (1 / 8) * (35 * pow(flat_x, 4) - 30 * pow(flat_x, 2) + 3)
    X = np.array([p1, p2, p3, p4]).T
    # X = np.array([p1, p2, p4]).T
    inv_X = np.linalg.inv(np.dot(X.T, X))
    return np.dot(np.dot(inv_X, X.T), flat.T)


def sub_flatness_heatmap(flats1, flats2, have_lim=False, vmin=-15, vmax=15):
    fig = plt.figure(figsize=(8, 4), dpi=200)
    # set_plot(12)
    ax = fig.add_subplot(2, 1, 1)
    plt.title("需要调节的板形偏差", fontsize=12)
    y = np.linspace(-1, 1, flats1.shape[1])
    x = np.arange(flats1.shape[0])
    print(y.shape)

    X, Y = np.meshgrid(x, y)
    if have_lim:
        c = ax.pcolormesh(X, Y, flats1.T, cmap='rainbow', shading='auto',
                          vmin=vmin, vmax=vmax
                          )
    else:
        c = ax.pcolormesh(X, Y, flats1.T, shading='auto', cmap='rainbow')
    cb = fig.colorbar(c)
    cb.set_label('IU', fontsize=10)
    plt.xlabel('长度方向采样点数', fontsize=10)
    plt.ylabel('OS   归一化板宽   DS', fontsize=10)
    plt.tight_layout()

    ax = fig.add_subplot(2, 1, 2)
    plt.title("调节后的板形偏差", fontsize=12)
    X, Y = np.meshgrid(x, y)
    if have_lim:
        c = ax.pcolormesh(X, Y, flats2.T, cmap='rainbow', shading='auto',
                          vmin=vmin, vmax=vmax
                          )
    else:
        c = ax.pcolormesh(X, Y, flats2.T, shading='auto', cmap='rainbow')
    cb = fig.colorbar(c)
    cb.set_label('IU', fontsize=10)
    plt.xlabel('长度方向采样点数', fontsize=10)
    plt.ylabel('OS   归一化板宽   DS', fontsize=10)
    plt.tight_layout()
    plt.show()


def efficacy(self, path, data):
    data = pd.read_csv(path)
    d_flats_nihe = data.values[:, -80:]
    x = np.linspace(-1, 1, 80)
    d_w = data.values[:, :-80]
    print('shape', d_w.shape)
    my_sgd = LsAdam(0.3)
    param = {"eff": np.zeros((d_w.shape[1], d_flats_nihe.shape[1]))}

    for i in range(1000):
        grad = {"eff": get_dJ(d_w, d_flats_nihe, param["eff"])}
        J = get_J(d_w, d_flats_nihe, param["eff"])
        if np.all(np.absolute(grad["eff"]) <= 1e-9):
            break
        my_sgd.update(param, grad)

    nihe = []
    xishus = []
    for i in range(param["eff"].shape[0]):
        xishu = my_leastq(param["eff"][i])
        xishus.append(xishu)
        flt = ls_lerangde_nihe(xishu, False)
        nihe.append(flt)
    a, b = np.array(nihe), np.array(xishus)
    print(b)
    return a, b


def plot_line(nihe, ax1, ax2, ax3, ax4, figure):
    print('r')
    set_plot(10)
    ax1.plot(nihe[0], "r-o", markersize=2, label="Tilt_eff")
    ax2.plot(nihe[1], "g-*", markersize=2, label="WRB_eff")
    ax3.plot(nihe[2], "b->", markersize=2, label="IRB_eff")
    ax4.plot(nihe[3], "k-p", markersize=2, label="IRS_eff")
    plt.rcParams['font.sans-serif'] = ['FangSong']
    plt.rcParams['axes.unicode_minus'] = False
    ax1.set_title("Tilt_eff")
    ax1.set_ylabel('IU/1%', fontsize=10)
    ax1.set_xlabel('OS           归一化板宽           DS', fontsize=10)
    ax2.set_title("WRB_eff")

    ax2.set_ylabel('IU/1%', fontsize=10)
    ax2.set_xlabel('OS           归一化板宽           DS', fontsize=10)
    ax3.set_title("IRB_eff")

    ax3.set_ylabel('IU/1%', fontsize=10)
    ax3.set_xlabel('OS           归一化板宽           DS', fontsize=10)
    ax4.set_title("IRS_eff")

    ax4.set_ylabel('IU/1%', fontsize=10)
    ax4.set_xlabel('OS           归一化板宽           DS', fontsize=10)
    figure.subplots_adjust(top=0.950, bottom=0.106, left=0.092, right=0.977, hspace=0.4, wspace=0.2)
