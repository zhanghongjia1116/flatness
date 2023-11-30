from pylab import *


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
        # 'MTRADP-STAND_01_reduction',  # compression_rate，恒定不变
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


def contribution(t_con, q_con, nu, name='贡献度'):
    plt.figure(dpi=120)
    ax1 = plt.subplot(2, 1, 1)
    plt.title(name)  # , size=15)
    plt.bar(range(len(t_con[0])), t_con[nu])
    ax1.set_ylabel('$T^2$贡献度')  # , size=13)

    ax2 = plt.subplot(2, 1, 2)
    plt.bar(range(len(q_con[0])), q_con[nu])
    ax2.set_ylabel('$SPE$贡献度')  # , size=13)


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
