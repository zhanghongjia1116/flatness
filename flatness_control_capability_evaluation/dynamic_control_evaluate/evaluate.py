import numpy as np
import matplotlib.pyplot as plt


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


def iu_error(before):
    """计算板形偏差"""
    setpoint = np.zeros(len(before))
    return np.mean(abs(before - setpoint - np.mean(before - setpoint)))


def shujufenxi(data):
    flat = data.values[:, -62:] / -2100000
    pot1, pot2, row_pot = jugde_row_col(flat)

    daitou = data[(data['POS'] > 0) & (data['POS'] < 100)]
    flat_daitou = daitou.values[:, -62:] / -2100000
    flat_daitou = flat_daitou[:, pot1:pot2]
    iu_mean1 = []
    # iu_mean2 = []
    iu_mean3 = []

    for i in flat_daitou:
        iu_mean1.append(iu_error(i))

    dg_length = data['POS'].iloc[row_pot]
    daiwei = data[data['POS'] > dg_length - 100]
    daizhong = data[(data['POS'] >= 100) & (data['POS'] <= dg_length - 100)]
    flat_daizhong = daizhong.values[:, -62:] / -2100000
    flat_daizhong = flat_daizhong[:, pot1:pot2]
    daizhong_length = flat_daizhong.shape[0]
    for i in flat_daizhong:
        iu_mean3.append(iu_error(i))
    iu_daitou = np.mean(iu_mean1)
    iu_daizhong = np.mean(iu_mean3)
    iu_xiajiangzhi = iu_daitou - iu_daizhong
    iu_xiajianglv = iu_xiajiangzhi / iu_daitou
    iu_xiajiangzhi = round(iu_xiajiangzhi, 3)
    iu_xiajianglv = round(iu_xiajianglv, 3)

    return iu_xiajiangzhi, iu_xiajianglv


def plot_line(iu, ax1, figure):
    # set_plot(10)
    x = np.linspace(-1, 1, 80)
    ax1.plot(iu, "r-o", markersize=2, label='原始板形', linewidth=0.5)
    # ax1.plot(iu1, "b-o", markersize=2, label=name1, linewidth=0.5)
    # ax1.plot(iu2, "g-*", markersize=2, label=name2, linewidth=0.5)
    ax1.legend()
    plt.rcParams['font.sans-serif'] = ['FangSong']
    plt.rcParams['axes.unicode_minus'] = False
    ax1.set_title("iu值下降比较")
    ax1.set_ylabel('IU', fontsize=10)
    ax1.set_xlabel('OS           归一化板宽           DS', fontsize=10)
