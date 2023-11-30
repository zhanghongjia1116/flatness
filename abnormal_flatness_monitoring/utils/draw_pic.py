# -*- coding: utf-8 -*-
"""
@Author : MR.W
@File : 初值统计.py
@Time : 2020/10/29 19:24
@Software: PyCharm
"""
import pandas as pd
import numpy as np
from .Wlearn import lerangde_fenjie, lerangde_nihe, jugde_row_col, free_chazhi
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import math
import os
import glob
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from urllib import request


def get_rms(records):
    return math.sqrt(sum([x ** 2 for x in records]) / len(records))


def get_cha(records):
    return max(records) - min(records)


def iu_error(before):
    """计算板形偏差"""
    setpoint = np.zeros(len(before))
    return np.mean(abs(before - setpoint - np.mean(before - setpoint)))
    # return np.mean(abs(before-setpoint))


def set_plot():
    plt.rcParams['xtick.direction'] = 'in'  # 将x周的刻度线方向设置向内
    plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内
    # plt.rcParams['font.sans-serif'] = ['Times new roman']
    config = {
        "font.family": 'serif',
        "font.size": 10,
        "mathtext.fontset": 'stix',
        "font.serif": ['SimSun'],
    }
    plt.rcParams.update(config)
    plt.rcParams['axes.unicode_minus'] = False
    bwith = 0.5  # 边框宽度设置为2
    ax = plt.gca()  # 获取边框
    ax.spines['bottom'].set_linewidth(bwith)
    ax.spines['left'].set_linewidth(bwith)
    ax.spines['top'].set_linewidth(bwith)
    ax.spines['right'].set_linewidth(bwith)
    plt.xticks(fontfamily="Times New Roman", fontsize=12)
    plt.yticks(fontfamily="Times New Roman", fontsize=12)


def lerangde_nihe(xishu, x):
    """根据板形缺陷系数拟合"""
    p1 = x
    p2 = 1.5 * pow(x, 2) - 1 / 2
    p3 = 2.5 * pow(x, 3) - 1.5 * x
    p4 = (35 * pow(x, 4) - 30 * pow(x, 2) + 3) / 8
    y = xishu[0] + xishu[1] * p1 + xishu[2] * p2 + xishu[3] * p3 + xishu[4] * p4
    return y


def odd_lerangde_nihe(xishu, x):
    """根据板形缺陷系数拟合"""
    p1 = x
    p2 = 0
    p3 = 2.5 * pow(x, 3) - 1.5 * x
    p4 = 0
    p0 = 0
    y = xishu[0] * p0 + xishu[1] * p1 + xishu[2] * p2 + xishu[3] * p3 + xishu[4] * p4
    return y


def even_lerangde_nihe(xishu, x):
    """根据板形缺陷系数拟合"""
    p1 = 0
    p2 = 1.5 * pow(x, 2) - 1 / 2
    p3 = 0
    p4 = (35 * pow(x, 4) - 30 * pow(x, 2) + 3) / 8
    p0 = 0
    y = xishu[0] * p0 + xishu[1] * p1 + xishu[2] * p2 + xishu[3] * p3 + xishu[4] * p4
    return y


def colormap():
    # 白青绿黄红
    cdict = ['#0000FF', '#00FFFF']
    # 按照上面定义的colordict，将数据分成对应的部分，indexed：代表顺序
    return colors.ListedColormap(colors, 'indexed')


def plotline(xymax, r):
    temp = xymax ** 2
    x = (temp / (1 + r ** 2)) ** 0.5
    y = x * r
    plt.plot([-x, x], [-y, y], 'k--', linewidth=0.5)


def qiujiaodu(lamda4, lamda2):
    seita = []
    if (lamda4 >= 0) and (lamda2 > 0):
        seita.append(math.atan(lamda4 / lamda2))
    if (lamda4 >= 0) and (lamda2 < 0):
        seita.append(math.atan(lamda4 / lamda2) + math.pi)
    if (lamda4 < 0) and (lamda2 < 0):
        seita.append(math.atan(lamda4 / lamda2) + math.pi)
    if (lamda4 < 0) and (lamda2 > 0):
        seita.append(math.atan(lamda4 / lamda2) + 2 * math.pi)
    if (lamda2 == 0) & (lamda4 >= 0):
        seita.append(math.pi / 2)
    if (lamda2 == 0) & (lamda4 < 0):
        seita.append(3 * math.pi / 2)
    return seita


def bili_to_jiaodu(seita):
    return (math.atan(seita) / math.pi * 180, (math.atan(seita) + math.pi) / math.pi * 180,
            (math.atan(seita) + 2 * math.pi) / math.pi * 180)


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return root, dirs, files


if __name__ == '__main__':
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # dir_path = r'F:\转移\原始板形数据\spcc'
    dir_path = r'D:\刘帅\u盘\转移\原始板形数据\780980'
    pathes = glob.glob(os.path.join(dir_path, "*.csv"))
    # print(len(pathes))
    for i in range(len(pathes)):
        data = pd.read_csv(pathes[i], header=0, encoding='gbk')
        # dataSignal=pd.read_csv(r'F:\转移\原始板形数据\spcc\H120116104200_1flat.csv',header=0,encoding='gbk')
        # dataSignal=pd.read_csv(r'E:\转移\原始板形数据\spcc\H120116104200_1flat.csv',header=0,encoding='gbk')
        # print(dataSignal)
        flat = data.values[:, 1:] / -2100000
        pot1, pot2, row_pot = jugde_row_col(flat)
        # row_pot=len(dataSignal)

        x = np.linspace(-1, 1, 80)
        lamda0 = []
        lamda1 = []
        lamda2 = []
        lamda3 = []
        lamda4 = []
        colors = []
        iu1 = []
        iu2 = []
        jiaodu1 = []
        jiaodu2 = []

        useflat = flat[:row_pot, pot1:pot2]
        for j in range(row_pot):
            new_row = free_chazhi(useflat[j])[0]
            # print(new_row)
            xishu = lerangde_fenjie(new_row, x)
            odd_flat = odd_lerangde_nihe(xishu, x)
            even_flat = even_lerangde_nihe(xishu, x)

            # 残差
            deta = new_row - lerangde_nihe(xishu, x)
            # print(deta)
            # 此处滤去奇次项 +-合适？
            new_flat_1 = new_row - odd_flat - deta / 2

            # 此处滤去偶次项
            # new_flat_2 = new_row - even_flat
            new_flat_2 = odd_flat + deta / 2

            # 此处为原插值板形
            # new_flat = new_row

            iu1.append(iu_error(new_flat_1))
            iu2.append(iu_error(new_flat_2))

            lamda0.append(xishu[0])
            lamda1.append(xishu[1])
            lamda2.append(xishu[2])
            lamda3.append(xishu[3])
            lamda4.append(xishu[4])
            colors.append((0, 1 - j / row_pot, 1))
            jiaodu1.append(qiujiaodu(xishu[4], xishu[2]))
            jiaodu2.append(qiujiaodu(xishu[3], xishu[1]))

        # ax = plt.subplot(3, 1, 2, projection='polar')
        a = file_name(dir_path)
        b = os.path.splitext(a[2][i])

        # save_path = r'F:\转移\画IU比例图\\%s\\'%b[0]
        save_path = r'D:\刘帅\u盘\转移\画IU比例图2\\%s\\' % b[0]

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        plt.figure(figsize=(6, 4), dpi=200)
        set_plot()
        ax = plt.gca(projection='polar')
        # 模态图上的几个分界处和极小值处
        # 0度,0.4,1.5,90度,-1,-0.3,180度,0.4,1.5,270度,-1,-0.3,360度

        e = [0.0, bili_to_jiaodu(0.4)[0], bili_to_jiaodu(1.5)[0], 90, bili_to_jiaodu(-1)[1], bili_to_jiaodu(-0.3)[1],
             180, bili_to_jiaodu(0.4)[1], bili_to_jiaodu(1.5)[1], 270, bili_to_jiaodu(-1)[2], bili_to_jiaodu(-0.3)[2]]
        labels = np.array(['0', '0.4', '1.5极小值处', '+∞', '-1', '-0.3', '0', '0.4', '1.5极小值处', '-∞', '-1', '-0.3'])

        ax.set_thetagrids(e, labels)
        ax.set_rlabel_position(45)
        c = ax.scatter(jiaodu1, iu1, color=colors, s=3)
        # max_r = max(iu1)
        # min_r = min(iu1)
        max_r = 6
        ax.set_rlim(0, max_r)
        plt.title('对称项', fontsize=10)
        # plt.savefig(save_path + '对称项.jpg', bbox_inches='tight')
        # plt.savefig(save_path + '对称项.jpg')

        # plt.savefig(pathes[i])
        # plt.show()
        # ax = plt.subplot(3, 1, 3, projection='polar')
        plt.figure(figsize=(6, 4), dpi=200)
        set_plot()
        ax = plt.gca(projection='polar')

        e = [0.0, bili_to_jiaodu(0.67)[0], bili_to_jiaodu(1.3)[0], 90, bili_to_jiaodu(-1)[1], bili_to_jiaodu(-0.17)[1],
             180, bili_to_jiaodu(0.67)[1], bili_to_jiaodu(1.3)[1], 270, bili_to_jiaodu(-1)[2], bili_to_jiaodu(-0.17)[2]]
        labels = np.array(['0', '0.67', '1.3极小值处', '+∞', '-1', '-0.17', '0', '0.67', '1.3极小值处', '-∞', '-1', '-0.17'])

        ax.set_thetagrids(e, labels)
        ax.set_rlabel_position(45)

        c = ax.scatter(jiaodu2, iu2, color=colors, s=3)
        # ax.set_xticklabels(['0', '1', '无穷大', '-1', '0', '1', '无穷大', '-1'], fontsize=8)

        ax.set_rlim(0, max_r)
        plt.title('非对称项', fontsize=10)
        # plt.savefig(save_path+'%s\\' %b[0]+'奇数项', bbox_inches='tight')
        # plt.show()
        # plt.savefig(save_path + '非对称项.jpg', bbox_inches='tight')
        # plt.savefig(save_path + '非对称项.jpg')

        plt.close()
