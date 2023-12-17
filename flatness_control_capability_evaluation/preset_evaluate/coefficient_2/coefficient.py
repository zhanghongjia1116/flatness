import os.path

import numpy as np
import pandas as pd

from .TWOFEM import TWOFEM


# def get_K(BW, hout, C40base, CPtarget, IRB, WRB, IRS, QSbase, DB, DI, DW):
#     """
#     Calculate the value of K based on various parameters.
#
#     Args:
#         BW: 板宽.
#         hout: 出口厚度.
#         C40base: 来料凸度.
#         CPtarget: 目标凸度.
#         IRB: 中间辊弯辊.
#         WRB: 工作辊弯辊.
#         IRS: 中间辊窜辊.
#         QSbase: 单位轧制力.
#         DB: 支撑辊直径.
#         DI: 中间辊直径.
#         DW: 工作辊直径.
#
#     Returns:
#         float: The calculated value of K.
#
#     Raises:
#         None
#     """
#
#     xiuzheng = [150, 150, 150, 150, 100]  # 凸度修正量
#     # 辊形读取和输入
#     path = os.path.dirname(__file__)
#     BRshape = pd.read_excel(f"{path}/输入辊形.xlsx", 'BR', header=None).values
#     IRshape = pd.read_excel(f"{path}/输入辊形.xlsx", 'IR', header=None).values
#     WRshape = pd.read_excel(f"{path}/输入辊形.xlsx", 'WR', header=None).values
#     # 有限元计算开始
#     CPL = np.zeros(5)
#     CPB = np.zeros(5)
#     for S in range(5):  # 依次计算各个机架
#         QS = QSbase[S]  # 单位板宽轧制力
#         SFTI = IRS[S]  # 正值代表上轧辊向左移动，即负窜
#         BFI = IRB[S]  # 中间辊弯辊
#         BFW = WRB[S]  # 工作辊弯辊 单侧弯辊 单位t
#         OUT_L = TWOFEM(DB[S], DI[S], DW[S], BW, QS, SFTI, BFI, BFW, BRshape, IRshape, WRshape)  # 实际弯辊下计算/-
#         # 输出：CW PHCW PHCQ QBI QIW  只需要第二个PHCW参数
#         CPL[S] = OUT_L[1] / hout[S]  # 比例承载凸度
#         SFTI = 0  # 正值代表上轧辊向左移动，即负窜
#         BFI = 0  # 中间辊弯辊
#         BFW = 0  # 工作辊弯辊 单侧弯辊 单位t
#         OUT_B = TWOFEM(DB[S], DI[S], DW[S], BW, QS, SFTI, BFI, BFW, BRshape, IRshape, WRshape)  # 无弯辊基本凸度计算
#         CPB[S] = OUT_B[1] / hout[S]  # 比例基本凸度
#
#     K1 = 0
#     # temp_CPL = np.concatenate(C40base, CPL + xiuzheng)
#     temp_CPL = [C40base] + list(CPL + xiuzheng)
#     temp_CPtarget = CPtarget  # 目标比例凸度
#     for S in range(4):
#         if abs(temp_CPL[S] - temp_CPtarget) > abs(temp_CPL[S + 1] - temp_CPtarget):
#             K1 += 1
#     K1 /= 5
#
#     K2 = 0
#     temp_CPL = CPL + xiuzheng
#     temp_CPB = CPB + xiuzheng
#     temp_CPtarget = CPtarget
#     for S in range(4):
#         if abs(temp_CPL[S] - temp_CPtarget) > abs(temp_CPB[S] - temp_CPtarget):
#             K2 += 1
#     K2 /= 5
#
#     K3 = 0
#     # temp_CPL = np.concatenate((CPL.iloc[n, :] + xiuzheng, [CPtarget[n]]))  # 加入目标凸度
#     temp_CPL = [CPL + xiuzheng] + CPtarget
#     # 二维数组变为一维数组
#     temp_CPL = temp_CPL.flatten()
#     temp_CPtarget = CPtarget
#     for S in range(4):
#         K3 += abs(temp_CPL[S] - temp_CPL[S + 1])
#     K3 = 0.5 if abs(K3) < 1 else abs(temp_CPL[0] - temp_CPtarget)
#     K3 /= 5
#     return K1 + K2 + K3


def get_K(BW, hout, C40base, CPtarget, IRB, WRB, IRS, QSbase, DB, DI, DW):
    """
    Calculate the value of K based on various parameters.

    Args:
        BW: 板宽.
        hout: 出口厚度.
        C40base: 来料凸度.
        CPtarget: 目标凸度.
        IRB: 中间辊弯辊.
        WRB: 工作辊弯辊.
        IRS: 中间辊窜辊.
        QSbase: 单位轧制力.
        DB: 支撑辊直径.
        DI: 中间辊直径.
        DW: 工作辊直径.

    Returns:
        float: The calculated value of K.

    Raises:
        None
    """

    xiuzheng = [150, 150, 150, 150, 100]  # 凸度修正量
    # 辊形读取和输入
    path = os.path.dirname(__file__)
    BRshape = pd.read_excel(f"{path}/输入辊形.xlsx", 'BR', header=None).values
    IRshape = pd.read_excel(f"{path}/输入辊形.xlsx", 'IR', header=None).values
    WRshape = pd.read_excel(f"{path}/输入辊形.xlsx", 'WR', header=None).values
    # 有限元计算开始
    CPL = np.zeros(5)
    CPB = np.zeros(5)
    for S in range(5):  # 依次计算各个机架
        QS = QSbase[S]  # 单位板宽轧制力
        SFTI = IRS[S]  # 正值代表上轧辊向左移动，即负窜
        BFI = IRB[S]  # 中间辊弯辊
        BFW = WRB[S]  # 工作辊弯辊 单侧弯辊 单位t
        OUT_L = TWOFEM(DB[S], DI[S], DW[S], BW, QS, SFTI, BFI, BFW, BRshape, IRshape, WRshape)  # 实际弯辊下计算/-
        # 输出：CW PHCW PHCQ QBI QIW  只需要第二个PHCW参数
        CPL[S] = OUT_L[1] / hout[S]  # 比例承载凸度
        print(CPL)
        SFTI = 0  # 正值代表上轧辊向左移动，即负窜
        BFI = 0  # 中间辊弯辊
        BFW = 0  # 工作辊弯辊 单侧弯辊 单位t
        OUT_B = TWOFEM(DB[S], DI[S], DW[S], BW, QS, SFTI, BFI, BFW, BRshape, IRshape, WRshape)  # 无弯辊基本凸度计算
        CPB[S] = OUT_B[1] / hout[S]  # 比例基本凸度

    K1 = 0
    temp_CPL = C40base + CPL  # 加入入口来料凸度
    temp_CPtarget = CPtarget  # 目标比例凸度
    for S in range(4):
        print(temp_CPL[S],temp_CPtarget)
        if abs(temp_CPL[S] - temp_CPtarget) > abs(temp_CPL[S + 1] - temp_CPtarget):
            K1 += 1
        else:
            K1 = K1
    K1 /= 5

    K2 = 0
    temp_CPL = CPL
    temp_CPB = CPB
    temp_CPtarget = [CPtarget]
    for S in range(4):
        if abs(temp_CPL[S] - temp_CPtarget) > abs(temp_CPB[S] - temp_CPtarget):
            K2 += 1
        else:
            K2 = K2
    K2 /= 5

    K3 = 0
    temp_CPL = CPL+CPtarget  # 加入目标凸度
    for S in range(4):
        if abs(temp_CPL[S] - temp_CPL[S + 1]) < 1:  # 完全达到目标
            K3 += 1
        else:
            K3 = K3

    w = [0.33, 0.33, 0.33]  # 设定三个系数K的权重
    return (K1 * w[0] + K2 * w[1] + K3 * w[2]) / 5  # 这里更新了K的计算方案


