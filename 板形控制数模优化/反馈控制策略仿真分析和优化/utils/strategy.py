import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import FormatStrFormatter, MultipleLocator


def lerangde_fenjie(y, x):
    from numpy import array
    from scipy.optimize import leastsq
    def func(x, p):
        """
        数据拟合所用的函数:p0+p1*x+p2*pow(x,2)+p3*pow(x,3)+p4*pow(x,4)
        """
        p0, p1, p2, p3, p4 = p  # 给A,k,theta赋值,其中x作为输入,
        return p0 + p1 * x + p2 * pow(x, 2) + p3 * pow(x, 3) + p4 * pow(x, 4)

    def residuals(p, y, x):
        """
        实验数据x, y和拟合函数之间的差，p为拟合需要找到的系数
        """
        return y - func(x, p)

    def lerangde(p):
        p0, p1, p2, p3, p4 = p
        deg0 = p0 + (1 / 3) * p2 + (1 / 5) * p4
        deg1 = p1 + (3 / 5) * p3
        deg2 = (2 / 3) * p2 + (4 / 7) * p4
        deg3 = (2 / 5) * p3
        deg4 = (8 / 35) * p4
        # return round(deg0, 2), round(deg1, 2), round(deg2, 2), round(deg3, 2), round(deg4, 2)
        return deg0, deg1, deg2, deg3, deg4

    a0 = [1, 1, 1, 1, 1]  # 第一次猜测的函数拟合参数
    plsq = leastsq(residuals, a0, args=(y, x), maxfev=1000)
    # print("最小二乘法系数", plsq[0])  # 实验数据拟合后的参数
    lamda = array(lerangde(plsq[0]))
    return lamda


def lerangde_nihe(xishu, x):
    p1 = x
    p2 = 1.5 * pow(x, 2) - 1 / 2
    p3 = 0.5 * (5 * pow(x, 3) - 3 * x)
    p4 = (1 / 8) * (35 * pow(x, 4) - 30 * pow(x, 2) + 3)
    y = xishu[0] + xishu[1] * p1 + xishu[2] * p2 + xishu[3] * p3 + xishu[4] * p4
    return y


def sigema(ai, bi):
    result = []
    for i in range(len(ai)):
        result.append(ai[i] * bi[i])
    return result


def free_chazhi(row):
    """输入必须为偶数，否则会报错"""
    import numpy as np
    new_row = np.zeros(80)
    pot_62 = np.array(
        [13, 39, 65, 91, 117, 143, 169, 195, 221, 247, 273, 299, 325, 351, 377, 403, 429, 455, 481, 507, 533, 559, 585,
         611, 637,
         676, 728, 780, 832, 884, 936, 988, 1040, 1092, 1141, 1196, 1248,
         1287, 1313, 1339, 1365, 1391, 1417, 1443, 1469, 1495, 1521, 1547, 1573, 1599, 1625, 1651, 1677, 1703, 1729,
         1755, 1781, 1807, 1833, 1859, 1885, 1911])
    num = len(row)
    long = 12
    short = num - long
    length = long * 52 + short * 26
    before_pot = pot_62[int((62 - num) / 2):int((62 + num) / 2)] - (62 - num) * 13 * np.ones(num)
    after_pot = np.linspace(length / 160, length - length / 160, 80)
    k = 0
    for i in range(80):
        if i == 0:
            new_row[i] = row[0] - (row[1] - row[0]) * (before_pot[0] - after_pot[0]) / (before_pot[1] - before_pot[0])
        elif i == 79:
            new_row[i] = row[-1] + (row[-1] - row[-2]) * (after_pot[-1] - before_pot[-1]) / (
                        before_pot[-1] - before_pot[-2])
        else:
            if after_pot[i] > before_pot[k]:
                k += 1
                new_row[i] = ((row[k] - row[k - 1]) * (after_pot[i] - before_pot[k - 1])) / (
                            before_pot[k] - before_pot[k - 1]) + row[k - 1]
            elif after_pot[i] == before_pot[k]:
                new_row[i] = row[k]
            elif after_pot[i] < before_pot[k]:
                new_row[i] = ((row[k] - row[k - 1]) * (after_pot[i] - before_pot[k - 1])) / (
                            before_pot[k] - before_pot[k - 1]) + row[k - 1]
    return new_row, before_pot, after_pot


def jugde_row_col(data):
    for i in data[10]:
        if i != 0:
            pot_1 = list(data[10]).index(i)
            break
    for i in data[25]:
        if i != 0:
            pot_2 = list(data[25]).index(i)
            break
    if pot_1 == pot_2:
        cols_pot = pot_1
    else:
        for i in data[30]:
            if i != 0:
                pot_3 = list(data[30]).index(i)
                break
        if pot_1 == pot_3:
            cols_pot = pot_1
        elif pot_2 == pot_3:
            cols_pot = pot_2
    for row in range(10, len(data)):
        if len(set(data[row])) <= 5:
            row_pot = row - 1
            break
        else:
            row_pot = 0
    if len(set(data[-1])) > 5:
        row_pot = len(data)
    return cols_pot, 62 - cols_pot, row_pot


def nums2_relevance(num1, num2):
    """计算两个数的相关性"""
    return np.exp(-(num1 - num2) ** 2)


def iu_error2(before):
    """计算板形偏差，不需要设定值"""
    # setpoint = np.zeros(len(before))
    return np.mean(abs(before - np.mean(before)))


def shujuchuli(data):
    '''
    对读取的数据进行预处理，未去边降，进行插值，返回插值后的80段值。
    '''
    flat = data.values[:, -62:]
    print('2222')
    start, end, row_pot = jugde_row_col(flat)
    flat_length = data.values[:, -63:]  # 带钢长度
    use_flat = flat[:, start + 1:end - 1] / -2100000  # 读取有效区间，并转换成IU
    x = np.linspace(-1, 1, 80)
    flatness = []
    iu = []
    for i in range(row_pot):
        row = use_flat[i]
        flat, beforepot, afterpot = free_chazhi(row)
        flatness.append(flat)
        iu.append(iu_error2(flat))
    # print(flatness)
    flatness = np.array(flatness)
    return flatness, row_pot, iu


def gudingyouxian(flat, row_pot, tilt_eff, WRBP_eff, IRB_eff, IRB_shift_eff):
    w_org = []
    row_org = []
    iu_org = []
    for j in range(row_pot):
        w_guding, row_guding = org_control(flat[j], tilt_eff, WRBP_eff, IRB_eff, IRB_shift_eff)
        w_org.append(w_guding)
        row_org.append(row_guding)
        iu_org.append(iu_error2(row_guding))
    w = np.array(w_org)
    row = np.array(row_org)
    iu_org = np.array(iu_org)
    return w, row, iu_org


def dongtaiyouxian(flat, row_pot, tilt_eff, WRBP_eff, IRB_eff, IRB_shift_eff):
    w_dry = []
    row_dry = []
    iu_dry = []
    for j in range(row_pot):
        w_dongtai, row_dongtai = dynamic_priority_sequence(flat[j], tilt_eff, WRBP_eff, IRB_eff, IRB_shift_eff)
        w_dry.append(w_dongtai)
        row_dry.append(row_dongtai)
        iu_dry.append(iu_error2(row_dongtai))

    print('64788')
    w_dry = np.array(w_dry)
    row_dry = np.array(row_dry)
    iu_dry = np.array(iu_dry)
    return w_dry, row_dry, iu_dry


def Adamyouhua(w_org, flat, row_pot, tilt_eff, WRBP_eff, IRB_eff, IRB_shift_eff, rate, beta1, beta2):
    w_adam = []
    row_adam = []
    iu_adam = []
    for j in range(row_pot):
        w_youhua, row_youhua = Adam(w_org[j], flat[j], tilt_eff, WRBP_eff, IRB_eff, IRB_shift_eff, rate, beta1, beta2)
        w_adam.append(w_youhua)
        row_adam.append(row_youhua)
        iu_adam.append(iu_error2(row_youhua))
    print('64788')
    w_adam = np.array(w_adam)
    row_adam = np.array(row_adam)
    iu_adam = np.array(iu_adam)
    return w_adam, row_adam, iu_adam


def bilikongzhi(flat, row_pot, k_wrb, k_irb, k_irs, tilt_eff, WRBP_eff, IRB_eff, IRB_shift_eff):
    w_pec = []
    row_pec = []
    iu_pec = []
    # k_wrb = float(k_wrb)
    # k_irb = float(k_irb)
    # k_irs = float(k_irs)
    for j in range(row_pot):
        w_bili, row_bili = pec_control(flat[j], k_wrb, k_irb, k_irs, tilt_eff, WRBP_eff, IRB_eff, IRB_shift_eff)
        w_pec.append(w_bili)
        row_pec.append(row_bili)
        iu_pec.append(iu_error2(row_bili))

    iu_pec = np.array(iu_pec)
    w_pec = np.array(w_pec)
    row_pec = np.array(row_pec)
    return w_pec, row_pec, iu_pec


def org_control(flat, tilt_eff, WRBP_eff, IRB_eff, IRB_shift_eff):
    tilt = sum(sigema(tilt_eff, flat)) / sum(sigema(tilt_eff, tilt_eff))
    new_row = flat - tilt * tilt_eff
    WRBP = sum(sigema(WRBP_eff, new_row)) / sum(sigema(WRBP_eff, WRBP_eff))
    WRBP_step = 8
    IRB_step = 6
    if WRBP >= WRBP_step:
        WRBP = WRBP_step
    elif WRBP <= -WRBP_step:
        WRBP = -WRBP_step

    new_row = new_row - WRBP * WRBP_eff
    IRB = sum(sigema(IRB_eff, new_row)) / sum(sigema(IRB_eff, IRB_eff))
    if IRB >= IRB_step:
        IRB = IRB_step
    elif IRB <= -IRB_step:
        IRB = -IRB_step
    new_row = new_row - IRB * IRB_eff
    IRB_shift = sum(sigema(IRB_shift_eff, new_row)) / sum(sigema(IRB_shift_eff, IRB_shift_eff))
    new_row = new_row - IRB_shift * IRB_shift_eff
    print([tilt, WRBP, IRB, IRB_shift])
    return [tilt, WRBP, IRB, IRB_shift], new_row


def dynamic_priority_sequence(my_flat, tilt_eff, WRBP_eff, IRB_eff, IRB_shift_eff):
    """
    动态优先序列
    :param my_flat:需要调节的板形 （1*80）
    :param my_eff: 调控功效 （4*80）
    :return: 计算调控量 （1*4）
    """
    x = np.linspace(-1, 1, 80)

    a_wrb = lerangde_fenjie(WRBP_eff, x)  # 识别系数
    a_irb = lerangde_fenjie(IRB_eff, x)

    r_wrb = a_wrb[4] / a_wrb[2]  # 计算比例
    r_irb = a_irb[4] / a_irb[2]

    a_flat = lerangde_fenjie(my_flat, x)
    r_flat = a_flat[4] / a_flat[2]

    r_wrb_flat = nums2_relevance(r_wrb, r_flat)  # 计算相似度
    r_irb_flat = nums2_relevance(r_irb, r_flat)

    r_list = np.array([r_wrb_flat, r_irb_flat])
    names = {0: "wrb", 1: "irb"}
    eff0 = tilt_eff
    eff3 = IRB_shift_eff
    order = np.argsort(r_list)  # 从小到大的序号
    w1_name = names[order[1]]
    w2_name = names[order[0]]
    print(w1_name)
    print(w2_name)

    if w1_name == "wrb" and w2_name == "irb":
        eff1 = WRBP_eff
        eff2 = IRB_eff
    elif w1_name == "irb" and w2_name == "wrb":
        eff1 = IRB_eff
        eff2 = WRBP_eff
    else:
        print("error")

    # 顺序控制
    tilt = sum(sigema(eff0, my_flat)) / sum(sigema(eff0, eff0))
    new_row = my_flat - tilt * eff0
    w1 = sum(sigema(eff1, new_row)) / sum(sigema(eff1, eff1))
    new_row = new_row - w1 * eff1
    w2 = sum(sigema(eff2, new_row)) / sum(sigema(eff2, eff2))
    new_row = new_row - w2 * eff2
    w3 = sum(sigema(eff3, new_row)) / sum(sigema(eff3, eff3))
    new_row = new_row - w3 * eff3

    if w1_name == "wrb" and w2_name == "irb":
        my_d_w = [tilt, w1, w2, w3]
    elif w1_name == "irb" and w2_name == "wrb":
        my_d_w = [tilt, w2, w1, w3]

    return my_d_w, new_row


def pec_control(flat, k_wrb, k_irb, k_irs, tilt_eff, WRBP_eff, IRB_eff, IRB_shift_eff):
    WRBP_step = 8
    IRB_step = 6
    new_row = flat
    tilt = sum(sigema(tilt_eff, new_row)) / sum(sigema(tilt_eff, tilt_eff))
    new_row = new_row - tilt * tilt_eff
    WRBP_flat = k_wrb * (new_row)
    IRB_flat = k_irb * (new_row)
    IRS_flat = k_irs * (new_row)
    WRBP = sum(sigema(WRBP_eff, WRBP_flat)) / sum(sigema(WRBP_eff, WRBP_eff))
    if WRBP >= WRBP_step:
        WRBP = WRBP_step
    elif WRBP <= -WRBP_step:
        WRBP = -WRBP_step
    IRB = sum(sigema(IRB_eff, IRB_flat)) / sum(sigema(IRB_eff, IRB_eff))
    if IRB >= IRB_step:
        IRB = IRB_step
    elif IRB <= -IRB_step:
        IRB = -IRB_step
    IRS = sum(sigema(IRB_shift_eff, IRS_flat)) / sum(sigema(IRB_shift_eff, IRB_shift_eff))
    new_row = new_row - WRBP * WRBP_eff - IRB * IRB_eff - IRS * IRB_shift_eff
    return [tilt, WRBP, IRB, IRS], new_row


def Adam(w_start, flat, tilt_eff, WRBP_eff, IRB_eff, IRB_shift_eff, rate, beta1, beta2):
    # rate = 0.05
    echo = 300
    # beta1 = 0.9
    # beta2 = 0.999
    min_error = 10
    line_history = []
    error_history = []

    r = 0  # 梯度
    s = np.zeros(4)
    sigma = 10e-8
    w = w_start
    eff = np.array([tilt_eff, WRBP_eff, IRB_eff, IRB_shift_eff])
    WRBP_step = 8
    IRB_step = 6
    for i in range(1, echo):
        g = -2 * np.dot(eff, (flat - np.dot(w, eff)).T) / 80
        s = beta1 * s + (1 - beta1) * g.T
        r = beta2 * r + (1 - beta2) * g * g
        # print(r)
        # rate=rate*np.sqrt(1-beta2**(i+1))/(1-beta1**(i+1))
        w = w - rate * s / (np.sqrt(r) + sigma)
        # if w[0] >= 5:  # 限值处理
        #     w[0] = 5
        # elif w[0] <= -5:
        #     w[0] = -5
        if w[1] >= WRBP_step:
            w[1] = WRBP_step
        elif w[1] <= -WRBP_step:
            w[1] = -WRBP_step
        if w[2] >= IRB_step:
            w[2] = IRB_step
        elif w[2] <= -IRB_step:
            w[2] = -IRB_step
        if w[3] >= 8:
            w[3] = 8
        elif w[3] <= -8:
            w[3] = -8
        # w = judge_add(w, add)
        tilt = w[0]
        WRBP = w[1]
        IRB = w[2]
        IRB_shift = w[3]
        new_row = flat - tilt * tilt_eff - WRBP * WRBP_eff - IRB * IRB_eff - IRB_shift * IRB_shift_eff
        f_error = iu_error2(new_row)
        error_history.append(f_error)
        if f_error <= min_error:
            min_error = f_error
            best_w = w
            best_row = new_row
        line_history.append(w)
    line_history = np.array(line_history)

    return w, new_row


def get_eff():
    x_size = np.linspace(-1, 1, 80)
    # tilt_eff = lerangde_nihe([0, 0.5955, 0,0.446626, 0], x_size)
    WRBP_eff = lerangde_nihe([0, 0, 2.50279, 0, 9.16244498e-01], x_size)
    IRB_eff = lerangde_nihe([0, 0, 1.30603351e+00, 0, -9.74762406e-02], x_size)
    IRB_shift_eff = lerangde_nihe([0, 0, 2.16080998e+00, 0, 4.52634755e-01], x_size)
    tilt_eff = 4 * np.array(
        [-7.2, -6.7, -6.2, -5.7, -5.2, -4.7, -4.2, -3.7, -3.25, -2.9, -2.7, -2.4, -2.3, -2.15, -2.08, -2.00, -1.9,
         -1.85, -1.8, -1.78, -1.7, -1.65, -1.6, -1.6, -1.58, -1.5, -1.4, -1.3, -1.26,
         -1.25, -1.2, -1.2, -1.15, -1.00, -0.85, -0.7, -0.5, -0.25, -0.1, 0, 0, 0.1, 0.25, 0.5, 0.7, 0.85, 1.0, 1.15,
         1.2, 1.2, 1.25, 1.26, 1.3, 1.4,
         1.5, 1.58, 1.6, 1.6, 1.65, 1.7, 1.78, 1.8, 1.85, 1.9, 2.0, 2.08, 2.15, 2.3, 2.4, 2.7, 2.9, 3.25, 3.7, 4.2, 4.7,
         5.2, 5.7, 6.2, 6.7, 7.2])
    return tilt_eff, WRBP_eff, IRB_eff, IRB_shift_eff


def figure_3D(flat_3D, ax, name, fig):
    # set_plot(12)
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签，黑体的 name 为 SimHei
    plt.rcParams['font.size'] = 10  # 设置字体大小
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号，跟是否显示中文没关系，你可以考虑加或不加
    data = np.array(flat_3D)
    ax.get_proj = lambda: np.dot(Axes3D.get_proj(ax), np.diag([0.9, 1.42, 1, 1]))  # 用于调整3D图形的显示位置
    Y = range(len(data))
    X = np.linspace(-1, 1, 80)
    X, Y = np.meshgrid(X, Y)
    # R = np.sqrt(X**2 + Y**2)
    Z = data
    print(X.shape, Y.shape, Z.shape)
    a = ax.plot_surface(X, Y, Z, rstride=5, cstride=2, cmap='rainbow', vmin=-10, vmax=10)
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.0f'))

    position = fig.add_axes([0.14, 0.4, 0.02, 0.5])  # 位置[左,下,右,上]
    ax.set_zlim(-15, 8)
    cb = plt.colorbar(a, cax=position)
    ax.set_xlabel('OS        归一化板宽        DS', fontsize=11)
    ax.set_ylabel('采样点', fontsize=11)
    ax.set_zlabel('板形偏差（IU）', fontsize=11)
    ax.set_title(name, fontsize=11)
    # fig.subplots_adjust(top=0.885, bottom=0.13, left=0.11, right=0.69, hspace=0.24, wspace=0.2)

    ax.view_init(18, -76)


def figure_3D2(flat_3D, ax, name, fig):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签，黑体的 name 为 SimHei
    plt.rcParams['font.size'] = 10  # 设置字体大小
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号，跟是否显示中文没关系，你可以考虑加或不加
    data = np.array(flat_3D)
    ax.get_proj = lambda: np.dot(Axes3D.get_proj(ax), np.diag([0.9, 1.42, 1, 1]))  # 用于调整3D图形的显示位置
    Y = range(len(data))
    X = np.linspace(-1, 1, 80)
    X, Y = np.meshgrid(X, Y)
    Z = data
    print(X.shape, Y.shape, Z.shape)
    a = ax.plot_surface(X, Y, Z, rstride=5, cstride=2, cmap='rainbow', vmin=-10, vmax=10)
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))

    position = fig.add_axes([0.14, 0.4, 0.02, 0.5])  # 位置[左,下,右,上]
    ax.set_zlim(-15, 8)
    cb = plt.colorbar(a, cax=position)
    ax.set_xlabel('OS        归一化板宽        DS', fontsize=11)
    ax.set_ylabel('采样点', fontsize=11)
    ax.set_zlabel('板形偏差（IU）', fontsize=11)
    ax.set_title(name, fontsize=11)
    x_major_locator = MultipleLocator(0.5)  # 设置刻度值间隔为2
    ax.xaxis.set_major_locator(x_major_locator)
    ax.view_init(15, -70)
    plt.show()


def plot_line(flat, flat_new, zhenshu, ax1, name, figure):
    # set_plot(10)
    x = np.linspace(-1, 1, 80)
    ax1.plot(x, flat[zhenshu], "r-o", markersize=2, label="原始板形", linewidth=0.5)
    ax1.plot(x, flat_new[zhenshu], "g-*", markersize=2, label=name, linewidth=0.5)
    ax1.legend()
    plt.rcParams['font.sans-serif'] = ['FangSong']
    plt.rcParams['axes.unicode_minus'] = False
    ax1.set_title("控制效果")
    ax1.set_ylabel('IU', fontsize=10)
    ax1.set_xlabel('OS           归一化板宽           DS', fontsize=10)


def plot_line2(iu, iu1, iu2, ax1, name1, name2, figure):
    # set_plot(10)
    x = np.linspace(-1, 1, 80)
    ax1.plot(iu, "r-o", markersize=2, label='原始板形', linewidth=0.5)
    ax1.plot(iu1, "b-o", markersize=2, label=name1, linewidth=0.5)
    ax1.plot(iu2, "g-*", markersize=2, label=name2, linewidth=0.5)
    ax1.legend()
    plt.rcParams['font.sans-serif'] = ['FangSong']
    plt.rcParams['axes.unicode_minus'] = False
    ax1.set_title("iu值下降比较")
    ax1.set_ylabel('IU', fontsize=10)
    ax1.set_xlabel('OS           归一化板宽           DS', fontsize=10)
