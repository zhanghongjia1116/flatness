from itertools import combinations_with_replacement  # 按照顺序从可迭代对象中取r个元素进行组合，允许使用重复的元素，
from math import factorial  # 首先导入math模块，然后调用factorial()函数来计算阶乘
from pylab import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm


# dynamic_copies = 2
# expansion_order = 1

def CH():
    from matplotlib import font_manager
    # 设置中文字体的支持
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.sans-serif'] = ['SimHei']
    zh_font = font_manager.FontProperties(fname=r'c:\windows\fonts\simsun.ttc', size=14)
    plt.rc('font', **{'family': 'Microsoft YaHei, SimHei'})


def NAN_DROP(data):
    nan_rows = np.isnan(data).any(axis=1)
    if not np.any(nan_rows):
        non_nan_data = data
        # print("没有找到包含 NaN 的行！")
        # 在这里添加继续执行的代码
    else:
        non_nan_data = data[~nan_rows, :]
        # print("已删除包含 NaN 的行")
        # print(non_nan_data)
    return non_nan_data


def dynamize(dynamic_copies, data):
    """ Appends lagged copies to data将滞后副本附加到数据

    Creates lagged copies of the original dataSignal, where each copy is lagged
    by 1 sample more than the previous copy. The number of samples is then
    reduced by the number of copies by deleting samples from the beginning
    创建原始数据的滞后副本，其中每个副本比前一个副本滞后1个样本。然后，通过从一开始就删除样本，以减少样本的副本数量

    Parameters
    ----------
    data: numpy.ndarray
        The set of dataSignal to dynamize要动态化的数据集

    Returns
    -------
    data_dyn: numpy.ndarray
        The new set of dataSignal with the lagged copies added添加了滞后副本的新数据集

    """
    d = dynamic_copies
    if data.shape[1] < d:
        raise RuntimeError("Not enough samples have been passed")  # 通过的样品不够多
    elif d == 0:
        data_dyn = data
    else:
        data_dyn = np.copy(data)
        for i in range(1, d + 1):  # 1~d
            rolled = np.roll(data, i, axis=1)  # 同时向水平方向滚动1个位置
            data_dyn = np.append(data_dyn, rolled, axis=0)
        data_dyn = np.delete(data_dyn, range(d), axis=1)  # 删除前d列
    return (data_dyn)


def nonlinear_expansion(expansion_order, dynamic_copies, data):
    """ Performs nonlinear expansion on data对数据执行非线性扩展

    For a set of signals [x1, x2, ... xn], performs a nonlinear expansion
    and returns [x1, x2, ..., xn, x1*x1, x1*x2, ... xn*xn, ... x1*x2*...
    *xd, ... xn^k] where k is the expansion order.
    对于一组信号 [x1, x2, ... xn]，执行非线性展开
    并返回 [x1, x2, ..., xn, x1*x1, x1*x2, ... xn*xn, ... x1*x2*...*xd, ... xn^k] 其中 k 是展开顺序。

    Parameters
    ----------
    data: numpy.ndarray
        The set of dataSignal to expand要扩展的数据集

    Returns
    -------
    data_exp: numpy.ndarray
        The new set of expanded dataSignal 新的扩展数据集

    """
    if expansion_order == 1:
        data_exp = data
    else:

        m = data.shape[0]
        # m=0
        d = dynamic_copies
        n = expansion_order
        # From dynamization从稀释增效法
        m = m * (d + 1)
        # From expansion从膨胀
        # Order 1
        num_signals = m
        for r in range(2, n + 1):
            # Order 2 -> expansion_order  从2扩张
            num_signals += (factorial(r + m - 1)  # 阶乘
                            / (factorial(r) * (factorial(m - 1))))
        num_signals = int(num_signals)

        m = data.shape[0]
        n = data.shape[1]
        data_exp = np.empty((num_signals, n))  # num_signals输出维度
        # empty(shape[, dtype, order]) 依给定的shape, 和数据类型 dtype, 返回一个一维或者多维数组，数组的元素不为空，为随机产生的数据。

        # Add expanded signals添加扩展信号
        # Order 1
        data_exp[0:m, :] = data

        pos = m  # Where to add new signal
        for order in range(2, expansion_order + 1):
            # Order 2 -> expansion_order
            for comb in combinations_with_replacement(range(m), order):
                # combinations_with_replacement(iterable, r)回iterable中所有长度为r的子序列，返回的子序列中的项按输入iterable中的顺序排序, 带重复
                exp_signal = np.ones((1, n))
                for i in comb:
                    exp_signal = exp_signal * data[i, :]
                data_exp[pos, :] = exp_signal
                pos += 1
    return (data_exp)


def get_TE_data(train_data=None, test_data=None):
    data1 = train_data
    data2 = test_data

    train1 = data1[:, 0:22]
    train2 = data1[:, -11:]
    X_train = np.hstack((train1, train2))  # 横拼接

    test1 = data2[:, 0:22]
    test2 = data2[:, -11:]
    X_test = np.hstack((test1, test2))  # 横拼接

    train_data2 = np.array(X_train)
    test_data2 = np.array(X_test)

    return train_data2, test_data2


def get_TE_data2(train_data=None, test_data=None):
    X_train1 = train_data.values[:, :8]  # 提取前22行
    X_train2 = train_data.values[:, 9:]  # 提取前22行
    X_train = np.hstack((X_train1, X_train2))

    X_test1 = test_data.values[:, :8]  # 提取后11行
    X_test2 = test_data.values[:, 9:]  # 提取后11行
    X_test = np.hstack((X_test1, X_test2))

    return X_train, X_test


def get_canshu():
    canshu = [
        # 正常
        # 'FLC5-F5_strip_width',#恒定不变
        'F5 actual value after stand 5 smoothed',
        'F5 flatness error tilt',
        # 'FLC5-F5__flatness_error_WRbend',
        # 'FLC5-F5__flatness_error_IRbend',
        # 'FLC5-F5__flatness_error_IRshift',
        'F5 strip length',
        # 'FLC5-F5_smoothing_value_flatness_measurement',
        # 'F5 flatness error',
        # 正常
        # 'MTRADP-STAND_01_reduction',  # 压下率，恒定不变
        # 'MTRADP-STAND_02_reduction',
        # 'MTRADP-STAND_03_reduction',
        # 'MTRADP-STAND_04_reduction',
        # 'MTRADP-STAND_05_reduction',
        # 'THX-THC: act. thickness S1 entry',  # 厚度
        # 'THC act thickness S1 entry',  # 厚度
        'THC: act. thickness S1 entry',  # 厚度
        # 问题
        # 'THC-THC_act_thickness_S1_exit',
        # 'THX h act S5 exit',
        'THX: h act S5 exit',
        # 'THX-THX: h act S5 exit',

        'SLC laser speed behind S5',
        # 'SLC-SLC_act_speed_stand_1',
        # 'SLC-SLC_act_speed_stand_2',
        # 'SLC-SLC_act_speed_stand_3',
        # 'SLC-SLC_act_speed_stand_4',
        # 'SLC-SLC_actspeed_stand_5',
        # 'SLC-SLC_strip_speed_S1__S2',
        # 'SLC-SLC_strip_speed_S2__S3',
        # 'SLC-SLC_strip_speed_S3__S4',
        # 'SLC-SLC_strip_speed_S4__S5',
        'SLC Slip factor stand 1',  # 前滑因子实际值
        'SLC Slip factor stand 2',
        'SLC Slip factor stand 3',
        'SLC Slip factor stand 4',
        'SLC Slip factor stand 5',

        # 正常
        'N1 ITC tension actual value at ctrl',  # 前控制实际张力值
        'N2 ITC tension actual value at ctrl',
        'N3 ITC tension actual value at ctrl',
        'N4 ITC tension actual value at ctrl',
        'N5 ITC tension actual value at ctrl',

        # 正常
        'D1 XSS position actual value',  # 1架辊缝实际位置
        # 'SDS_1-D1_WSS_position_ref_value',  # 1架辊缝参考位置
        # 'SDS_1-D1_XFR_roll_force_actual_value',  # 1架轧制力实际值
        # 'SDS_1-D1_WFR_roll_force_ref_value',  # 1架轧制力参考值
        # 'D2 XSS position actual value',
        # 'SDS_2-D2_XSS_position_actual_value',
        # 'SDS_2-D2_WSS_position_ref_value',
        # 'SDS_2-D2_XFR_roll_force_actual_value',
        # 'SDS_2-D2_WFR_roll_force_ref_value',
        # 'D3 XSS position actual value',
        # 'SDS_3-D3_XSS_position_actual_value',
        # 'SDS_3-D3_WSS_position_ref_value',
        # 'SDS_3-D3_XFR_roll_force_actual_value',
        # 'SDS_3-D3_WFR_roll_force_ref_value',
        # 'D4 XSS position actual value',
        # 'SDS_4-D4_XSS_position_actual_value',
        # 'SDS_4-D4_WSS_position_ref_value',
        # 'SDS_4-D4_XFR_roll_force_actual_value',
        # 'SDS_4-D4_WFR_roll_force_ref_value',

        'D5 XSS position actual value',
        # 'SDS_5-D5_WSS_position_ref_value',
        'D5 XFR roll force actual value',
        # 'SDS_5-D5_WFR_roll_force_ref_value',

        # 正常
        'B5 WRB actual value',  # 5架工作辊弯辊实际值
        # 'RBS_5-B5_IRB_actual_value_ctrl1',  # 5架中间辊ctrl1实际值
        # 'RBS_5-B5_IRB_actual_value_ctrl2',  # 5架中间辊ctrl2实际值

        'S5 top IR shfiting actual value',  # 5架上中间辊窜辊实际值
        # 'RSS_5-S5_bot_IR_shfiting_actual_value'  # 5架下中间辊窜辊实际值
    ]
    return canshu


def get_canshu3(Xtrain):
    canshu = pd.read_excel(r'D:\A_My_file\顺义灯塔工厂二期\特征选择_use.xlsx', header=None)

    # 提取第一列并转换为字符串数组
    first_column = canshu.iloc[:, 0].tolist()
    final_canshu = []
    for feature in first_column:
        if len(set(Xtrain[feature])) > 1:
            final_canshu.append(feature)
    missing_elements = set(first_column) - set(final_canshu)
    print('特征差别：', list(missing_elements))
    return final_canshu


def get_canshu2():
    canshu = ['F5 flatness error tilt', 'F5  flatness error WR-bend', 'F5  flatness error IR-bend',
              'F5  flatness error IR-shift', 'THC: dH act. S1 entry', 'THC: dH act. S1 exit',
              'THC: act. thickness S1 entry',
              'THC: act. thickness S1 exit', 'THX: h act S5 exit', 'THX: dh act S5 exit', 'SLC Slip factor stand 1',
              'SLC Slip factor stand 2', 'SLC Slip factor stand 3', 'SLC Slip factor stand 4',
              'SLC Slip factor stand 5',
              'SLC act. speed bridle 5/2', 'SLC laser speed behind S1', 'SLC laser speed behind S5',
              'SLC act. speed exit flatness roll', 'SLC act. speed stand 1', 'SLC act. speed stand 2',
              'SLC act. speed stand 3',
              'SLC act speed stand 4', 'SLC act.speed stand 5', 'SLC strip speed S1 - S2', 'SLC strip speed S2 - S3',
              'SLC strip speed S3 - S4', 'SLC strip speed S4 - S5', 'SLC strip speed after S5',
              # 'N1 ITC tension actual value DS',
              # 'N1 ITC tension actual value OS', 'N1 ITC tension actual value at ctrl', 'N1 ITC diff.tension at ctrl',
              'N2 ITC tension actual value DS', 'N2 ITC tension actual value OS', 'N2 ITC tension actual value at ctrl',
              'N2 ITC diff.tension at ctrl', 'N3 ITC tension actual value DS', 'N3 ITC tension actual value OS',
              'N3 ITC tension actual value at ctrl', 'N3 ITC diff.tension at ctrl', 'N4 ITC tension actual value DS',
              'N4 ITC tension actual value OS', 'N4 ITC tension actual value at ctrl', 'N4 ITC diff.tension at ctrl',
              'N5 ITC tension actual value DS', 'N5 ITC tension actual value OS', 'N5 ITC tension actual value at ctrl',
              'N5 ITC diff.tension at ctrl', 'N5 tension actual value DS after S5',
              'N5 tension actual value OS after S5',
              'F5 actual value after stand 5 smoothed', 'D1 XFR roll force actual value',
              'D1 XSSd tilting actual value',
              'D1 DIFF RF CTRL act value (DS-OS)', 'D2 XFR roll force actual value', 'D2 XSSd tilting actual value',
              'D2 DIFF RF CTRL act value (DS-OS)', 'D3 XFR roll force actual value', 'D3 XSSd tilting actual value',
              'D3 DIFF RF CTRL act value (DS-OS)', 'D4 XFR roll force actual value', 'D4 XSSd tilting actual value',
              'D4 DIFF RF CTRL act value (DS-OS)', 'D5 XFR roll force actual value', 'D5 XSSd tilting actual value',
              'D5 DIFF RF CTRL act value (DS-OS)', 'B1 WRB actual value', 'B1 IRB actual value ctrl1',
              'B1 IRB actual value ctrl2', 'B2 WRB actual value', 'B2 IRB actual value ctrl1',
              'B2 IRB actual value ctrl2',
              'B3 WRB actual value', 'B3 IRB actual value ctrl1', 'B3 IRB actual value ctrl2',
              'WR bending actual value',
              'B4 IRB actual value ctrl1', 'B4 IRB actual value ctrl2', 'B5 WRB actual value',
              'B5 IRB actual value ctrl1',
              'B5 IRB actual value ctrl2', 'S1 top IR shfitingl actual value', 'S1 bot IR shfitingl actual value',
              'S2 top IR shfiting actual value', 'S2 bot IR shfiting actual value', 'S3 top IR shfiting actual value',
              'S3 bot IR shfiting actual value', 'S4 top  IR shfiting actual value', 'S4 bot IR shfiting actual value',
              'S5 top IR shfiting actual value', 'S5 bot IR shfiting actual value', 'STAND_01_reduction',
              'STAND_02_reduction',
              'STAND_03_reduction', 'STAND_04_reduction', 'STAND_05_reduction', 'F5 flatness error']
    return canshu


def plot_box(data):
    feature = data['F5 flatness error']

    # 计算分位点值
    q1 = feature.quantile(0.25)
    q2 = feature.quantile(0.50)
    q3 = feature.quantile(0.75)

    # 计算上边缘和下边缘
    iqr = q3 - q1
    upper_fence = q3 + 1.5 * iqr
    lower_fence = q1 - 1.5 * iqr

    # 绘制箱线图
    # plt.boxplot(feature, vert=True)

    # 打印分位点值
    # print("第一四分位数（Q1）：", q1)
    # print("中位数（Q2）：", q2)
    # print("第三四分位数（Q3）：", q3)
    # print("上边缘（Upper Fence）：", upper_fence)
    # print("下边缘（Lower Fence）：", lower_fence)

    # 显示箱线图
    # plt.show()
    return upper_fence


def get_banxing_data(train_data=None, test_data=None, limit=2):
    df1 = train_data
    df2 = test_data
    df1 = NAN_DROP(df1)
    df2 = NAN_DROP(df2)
    canshu = get_canshu2()
    IU = df2['F5 flatness error']
    Xtrain = df1[(df1['F5 flatness error'] < limit) & (df1['F5 flatness error'] > 0.3)]
    IU2 = Xtrain['F5 flatness error']
    canshu = [qq for qq in canshu if qq in canshu and qq != 'F5 flatness error']
    Xtrain = Xtrain[canshu]
    Xtest = df2[canshu]
    Xtrain = np.array(Xtrain)
    Xtest = np.array(Xtest)


    return Xtrain, Xtest, IU, IU2, canshu


def draw_IU(IU):
    plt.plot(IU)
    plt.xlabel(u'Sample')
    plt.ylabel(u'IU')
    plt.title("IU values")
    # plt.savefig(r'D:\A_My_file\A_MyWork\SFA_for_Fault_Diagnosis-master\picture\IU.png',
    #             dpi=1200, bbox_inches='tight')
    plt.show()


def normalize(*args):
    """
    对正常数据和测试数据进行标准化，输入数据一般为训练数据矩阵X_normal和测试数据矩阵X_new
    （注意：测试数据需要按照正常数据的均值和方差标准化）
    """
    X_normal = args[0]
    X_normal_mean = np.mean(X_normal, axis=0)
    X_normal_std = np.std(X_normal, axis=0)
    # X_normal_row, X_normal_col = X_normal.shape
    X_normal_center = (X_normal - X_normal_mean) / X_normal_std

    if len(args) == 2:
        X_new = args[1]
        X_new_row, X_new_col = X_new.shape
        X_new_center = (X_new - X_normal_mean) / X_normal_std
        return (X_normal_center, X_new_center)

    return X_normal_center


def visualization4(T2, S2, T2_threshold, S2_threshold, name='监测图'):
    # plt.figure(figsize=(10, 10), dpi=120)
    plt.figure(dpi=120)
    ax1 = plt.subplot(2, 1, 1)
    plt.title(name)  # , size=15)
    ax1.plot(T2)
    # ax1.plot(IU, label='IU')
    ax1.plot(range(len(T2)), [T2_threshold] * len(T2), "r--")
    ax1.set_ylabel('$T^2$统计量')  # , size=13)
    ax1.legend(labels=['$T^2$统计量值', '$T^2$统计量限值'], loc=0)

    ax2 = plt.subplot(2, 1, 2)
    ax2.plot(S2)
    ax2.plot(range(len(S2)), [S2_threshold] * len(S2), "r--")
    ax2.legend(labels=['$SPE$统计量值', '$SPE$统计量限值'], loc=0)
    ax2.set_ylabel('$SPE$统计量')  # , size=13)
    plt.xlabel(u'样本点')  # , size=13)


# def visualization2(mse_loss, threshold,name='监测图'):
#     plt.plot(range(len(mse_loss)), mse_loss)
#     plt.axhline(y=threshold, color='r', linestyle='--')
#     plt.title(name)
#     plt.xlabel('样本点')
#     plt.ylabel('IU统计值')
#     plt.show()

def visualization2(mse_loss, threshold, name='监测图'):
    plt.plot(range(len(mse_loss)), mse_loss, label='实际IU值')
    plt.axhline(y=threshold, color='r', linestyle='--', label='IU阈值')
    plt.title(name)
    plt.xlabel('样本点')
    plt.ylabel('IU统计值')
    plt.legend()
    # plt.show()


def cal_acc2(T2_unfiy_value, T2limit_unfiy, IU):
    TT = 0
    TF = 0
    FT = 0
    FF = 0
    for i in range(len(T2_unfiy_value)):
        if IU[i] >= 2:
            if T2_unfiy_value[i] > T2limit_unfiy:
                FF += 1
            else:
                FT += 1
        else:
            if T2_unfiy_value[i] > T2limit_unfiy:
                TF += 1
            else:
                TT += 1
    return TT, TF, FT, FF


def cal_acc4(T2_unfiy_value, SPE_unfiy_value, T2limit_unfiy, SPElimit_unfiy, IU, limit=2):
    TT = 0
    TF = 0
    FT = 0
    FF = 0
    sat = []
    id_err = []
    for i in range(len(SPE_unfiy_value)):
        if IU[i] >= limit:
            if T2_unfiy_value[i] > T2limit_unfiy and SPE_unfiy_value[i] > SPElimit_unfiy:
                FF += 1
                sat.append(1)
                id_err.append(i)
            else:
                FT += 1
                sat.append(0)
                id_err.append(-1)
        else:
            if T2_unfiy_value[i] > T2limit_unfiy and SPE_unfiy_value[i] > SPElimit_unfiy:
                TF += 1
                sat.append(0)
                id_err.append(i)
            else:
                TT += 1
                sat.append(0)
                id_err.append(-1)
    try:
        MR = (FF / (FF + FT)) * 100
    except:
        MR = 'ERROR'
    try:
        FAR = (TF / (TF + TT)) * 100
    except:
        FAR = 'ERROR'
    print('监测率:', MR, '%')
    print('误报率:', FAR, '%')

    return MR, FAR, sat, id_err


def cal_acc_TE2(T2_unfiy_value, T2limit_unfiy):
    TT = 0
    TF = 0
    FT = 0
    FF = 0
    for i in range(len(T2_unfiy_value)):
        if i > 160:
            if T2_unfiy_value[i] > T2limit_unfiy:
                FF += 1
            else:
                FT += 1
        else:
            if T2_unfiy_value[i] > T2limit_unfiy:
                TF += 1
            else:
                TT += 1

    return TT, TF, FT, FF


def cal_acc_TE4(T2_unfiy_value, T2limit_unfiy, SPE_unfiy_value, SPElimit_unfiy):
    TT = 0
    TF = 0
    FT = 0
    FF = 0
    for i in range(len(SPE_unfiy_value)):
        if i > 160:
            if T2_unfiy_value[i] > T2limit_unfiy and SPE_unfiy_value[i] > SPElimit_unfiy:
                FF += 1
            else:
                FT += 1
        else:
            if T2_unfiy_value[i] > T2limit_unfiy and SPE_unfiy_value[i] > SPElimit_unfiy:
                TF += 1
            else:
                TT += 1

    return TT, TF, FT, FF


def contribution(t_con, q_con, nu, name='贡献度'):
    plt.figure(dpi=120)
    ax1 = plt.subplot(2, 1, 1)
    plt.title(name)  # , size=15)
    plt.bar(range(len(t_con[0])), t_con[nu])
    ax1.set_ylabel('$T^2$贡献度')  # , size=13)

    ax2 = plt.subplot(2, 1, 2)
    plt.bar(range(len(q_con[0])), q_con[nu])
    ax2.set_ylabel('$SPE$贡献度')  # , size=13)


def contribution2(t_con, q_con, nu, name='贡献度', feat_names=None):
    plt.figure(dpi=120)
    ax1 = plt.subplot(2, 1, 1)
    plt.title(name, size=15)
    if feat_names:
        ax1.set_xticks(range(len(feat_names)))
        ax1.set_xticklabels(feat_names, rotation=45)
    plt.bar(range(len(t_con[0])), t_con[nu])
    ax1.set_ylabel('$T^2$贡献度', size=13)

    ax2 = plt.subplot(2, 1, 2)
    if feat_names:
        ax2.set_xticks(range(len(feat_names)))
        ax2.set_xticklabels(feat_names, rotation=45)
    plt.bar(range(len(q_con[0])), q_con[nu])
    ax2.set_ylabel('$SPE$贡献度', size=13)


def iu_one_frame(before):
    setpoint = np.zeros(len(before))
    return abs(before - setpoint - np.mean(before - setpoint))


def judge_err(value, IU):
    ERR = 0
    NOR = 0
    sat = []
    for i in range(len(value)):
        if value[i] > IU:
            ERR += 1
            sat.append(1)
        else:
            NOR += 1
            sat.append(0)
    return ERR, NOR, sat


def feature_IU(feature, IU, name='canshu'):
    fig, ax = plt.subplots()
    feature = normalize(feature)  # 创建一个新的图形和一个子图
    IU = normalize(IU)
    ax.plot(feature, label=name)
    ax.plot(IU, label='IU')
    ax.set_title('特征-IU图')
    ax.legend()  # 在每个子图上添加图例对象
    # plt.show()  # 显


def BATCH():
    rootdir = r'D:\A_My_file\A_MyWork\SFA_for_Fault_Diagnosis-master\data\_te'
    a = os.listdir(rootdir)
    TT = []
    TF = []
    FT = []
    FF = []
    JC = []
    WB = []
    FM = []
    for ii in a:
        file_path = r'D:\A_My_file\A_MyWork\SFA_for_Fault_Diagnosis-master\data\_te\\' + ii
        file_name = file_path.split('\\')[-1].split('.')[0]
        # print('file_name:', file_name)

        X_train_ = pd.read_csv()
        X_test_ = pd.read_csv(file_path)
        X_train_, X_test_ = get_TE_data(train_data=X_train_, test_data=X_test_)

        X_train_, X_test_ = normalize(X_train_, X_test_)
        T2, S2, T2_threshold, S2_threshold = fit_model
        visualization4(T2, S2, T2_threshold, S2_threshold, name='监测图')
        plt.savefig(r'D:\A_My_file\A_MyWork\SFA_for_Fault_Diagnosis-master\picture\te\NSFA\\' + file_name)  # 保存图片
        TT2, TF2, FT2, FF2 = cal_acc4(test_T2, T2_threshold, test_S2, S2_threshold, IU)
        # print('监测率：', (FF2 / (FF2 + FT2)) * 100, '%')
        # print('误报率：', (TF2 / (TF2 + TT2)) * 100, '%')
        # print('\n')
        TT.append(TT2)
        TF.append(TF2)
        FT.append(FT2)
        FF.append(FF2)
        JC.append((FF2 / (FF2 + FT2)) * 100)
        WB.append((TF2 / (TF2 + TT2)) * 100)
        FM.append(file_name)
    index = ['TT', 'TF', 'FT', 'FF', '监测率', '误报率']
    res = [TT, TF, FT, FF, JC, WB]
    column = [FM]
    df = pd.DataFrame(res, index=index, columns=column)
    df = df.T
    df.to_csv(r'D:\A_My_file\A_MyWork\SFA_for_Fault_Diagnosis-master\picture\te\nsfa_te.csv', index=True,
              encoding='gbk')
