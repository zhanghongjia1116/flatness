import os.path

import numpy as np
import pandas as pd
import multiprocessing
from .TWOFEM import TWOFEM


# 定义并行函数
def myparfun(db, di, dw, bw, qs, sfti, bfi, bfw):
    # 辊形读取和输入
    path = os.path.dirname(__file__)
    BRshape = pd.read_excel(f"{path}/输入辊形.xlsx", 'BR', header=None).values
    IRshape = pd.read_excel(f"{path}/输入辊形.xlsx", 'IR', header=None).values
    WRshape = pd.read_excel(f"{path}/输入辊形.xlsx", 'WR', header=None).values
    out = TWOFEM(db, di, dw, bw, qs, sfti, bfi, bfw, BRshape, IRshape, WRshape)
    return out[1]


def get_K(BW, hout, C40base, CPtarget, IRB, WRB, IRS, QSbase, DB, DI, DW, pool_num):
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
        pool_num: CPU核心数.

    Returns:
        float: The calculated value of K.

    Raises:
        None
    """
    # # 辊形读取和输入
    # path = os.path.dirname(__file__)
    # BRshape = pd.read_excel(f"{path}/输入辊形.xlsx", 'BR', header=None).values
    # IRshape = pd.read_excel(f"{path}/输入辊形.xlsx", 'IR', header=None).values
    # WRshape = pd.read_excel(f"{path}/输入辊形.xlsx", 'WR', header=None).values

    # #定义并行函数
    # def myparfun(db, di, dw, bw, qs, sfti, bfi, bfw):
    #     out = TWOFEM(db, di, dw, bw, qs, sfti, bfi, bfw, BRshape, IRshape, WRshape)
    #     return out[1]

    # 有限元计算开始
    CPL = np.zeros(5)
    CPB = np.zeros(5)
    # for S in range(5):  # 依次计算各个机架
    #     QS = QSbase[S]  # 单位板宽轧制力
    #     SFTI = IRS[S]  # 正值代表上轧辊向左移动，即负窜
    #     BFI = IRB[S]  # 中间辊弯辊
    #     BFW = WRB[S]  # 工作辊弯辊 单侧弯辊 单位t
    #     OUT_L = TWOFEM(DB[S], DI[S], DW[S], BW, QS, SFTI, BFI, BFW, BRshape, IRshape, WRshape)  # 实际弯辊下计算/-
    #     # 输出：CW PHCW PHCQ QBI QIW  只需要第二个PHCW参数
    #     CPL[S] = OUT_L[1] / hout[S]  # 比例承载凸度
    #     print(CPL)
    #     SFTI = 0  # 正值代表上轧辊向左移动，即负窜
    #     BFI = 0  # 中间辊弯辊
    #     BFW = 0  # 工作辊弯辊 单侧弯辊 单位t
    #     OUT_B = TWOFEM(DB[S], DI[S], DW[S], BW, QS, SFTI, BFI, BFW, BRshape, IRshape, WRshape)  # 无弯辊基本凸度计算
    #     CPB[S] = OUT_B[1] / hout[S]  # 比例基本凸度
    data = []
    for i in range(10):
        S = np.mod(i, 5)
        if i >= 5:
            SFTI = 0
            BFI = 0
            BFW = 0
        else:
            SFTI = IRS[S]
            BFI = IRB[S]
            BFW = WRB[S]
        args = DB[S], DI[S], DW[S], BW, QSbase[S], SFTI, BFI, BFW
        data.append(args)

    pool = multiprocessing.Pool(processes=pool_num)
    results = pool.starmap(myparfun, data)

    K1 = 0
    temp_CPL = [C40base]
    temp_CPL.extend(CPL)  # 加入入口来料凸度
    temp_CPtarget = CPtarget  # 目标比例凸度
    for S in range(5):
        if abs(temp_CPL[S] - temp_CPtarget) > abs(temp_CPL[S + 1] - temp_CPtarget):
            K1 = K1 + 1
        else:
            K1 = K1

    K2 = 0
    temp_CPL = CPL
    temp_CPB = CPB
    temp_CPtarget = [CPtarget]
    for S in range(5):
        if abs(temp_CPL[S] - temp_CPtarget) > abs(temp_CPB[S] - temp_CPtarget):
            K2 = K2 + 1
        else:
            K2 = K2

    K3 = 0
    temp_CPL = CPL.tolist()  # 加入目标凸度
    temp_CPL.extend([CPtarget])
    for S in range(5):
        if abs(temp_CPL[S] - temp_CPL[S + 1]) < 1:  # 完全达到目标
            K3 = K3 + 1.0
        else:
            K3 = K3

    w = [0.33, 0.33, 0.33]  # 设定三个系数K的权重

    return (K1 * w[0] + K2 * w[1] + K3 * w[2]) / 5  # 这里更新了K的计算方案
