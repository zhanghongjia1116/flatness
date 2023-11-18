from .Wlearn import jugde_row_col, free_chazhi, lerangde_fenjie, lerangde_nihe, search
from .绘图 import iu_error, get_rms, get_cha, odd_lerangde_nihe, even_lerangde_nihe, qiujiaodu
import pandas as pd
import numpy as np


# 3维版型图
def shuju(path):
    data = pd.read_csv(path, header=0, encoding='gbk')
    flat = data.values[:, 1:] / -2100000
    width = np.linspace(-1, 1, 80)
    flat = data.values[:, 1:] / -2100000
    pot1, pot2, row_pot = jugde_row_col(flat)
    length = list(range(0, row_pot))
    # X, Y = np.meshgrid(width, length)
    useflat = flat[:row_pot, pot1:pot2]
    flat_3D = []
    for j in range(row_pot):
        new_row = free_chazhi(useflat[j])[0]
        flat_3D.append(new_row)

    return flat_3D


# 热度图
def shuju_redutu(path):
    data = pd.read_csv(path, header=0, encoding='gbk')
    # data=pd.read_csv(r'F:\转移\原始板形数据\spcc\H120116104200_1flat.csv',header=0,encoding='gbk')
    # data=pd.read_csv(r'E:\转移\原始板形数据\spcc\H120116104200_1flat.csv',header=0,encoding='gbk')
    # print(data)
    flat = data.values[:, 1:] / -2100000
    pot1, pot2, row_pot = jugde_row_col(flat)
    useflat = flat[:row_pot, pot1:pot2]
    flat_3D = []
    flaterrors = []
    for j in range(row_pot):
        new_row = free_chazhi(useflat[j])[0]

        # print(new_row)
        flaterrors.append(iu_error(new_row))
        flat_3D.append(new_row)
    # print(flaterrors)
    x = np.linspace(0, row_pot - 1, row_pot)
    y = np.linspace(-1, 1, 80)
    X, Y = np.meshgrid(x, y)
    # print(X)
    # print(Y)
    return flat_3D, X, Y


# 浪型模态图
def shuju_langxin(path, mode):
    """
    :param path:
    :param mode:
    mode==1:绝对值平均板形偏差
    mode==2：均方根IU
    mode==3：最大-最小IU
    mode==else 退出程序
    :return:
    """

    # name = path.split('\\')[-1].split('.')[0]
    # print(name)
    # plt.rcParams['font.sans-serif'] = ['SimHei']
    # plt.rcParams['axes.unicode_minus'] = False
    data = pd.read_csv(path, header=0, encoding='gbk')
    flat = data.values[:, 1:] / -2100000
    pot1, pot2, row_pot = jugde_row_col(flat)
    x = np.linspace(-1, 1, 80)
    lamda0 = []
    lamda1 = []
    lamda2 = []
    lamda3 = []
    lamda4 = []
    colors = []
    iu1 = []  # 记录对称项IU
    iu2 = []
    jiaodu1 = []
    jiaodu2 = []

    useflat = flat[:row_pot, pot1:pot2]
    flat_list = []
    for j in range(row_pot):
        new_row = free_chazhi(useflat[j])[0]
        xishu = lerangde_fenjie(new_row, x)
        odd_flat = odd_lerangde_nihe(xishu, x)
        even_flat = even_lerangde_nihe(xishu, x)
        flat_list.append(new_row)
        # 残差
        # deta = new_row - lerangde_nihe(xishu, x)
        # print(deta)
        # 此处滤去奇次项 +-合适？
        new_flat_1 = even_flat

        # 此处滤去偶次项
        # new_flat_2 = new_row - even_flat
        new_flat_2 = odd_flat

        # 此处为原插值板形
        # new_flat = new_row
        if mode == 1:
            max_r = 10
            iu1.append(iu_error(new_flat_1))
            iu2.append(iu_error(new_flat_2))
            # save_path1 = r'F:\给周老师的\改的极坐标图\%s\对称项 绝对值均值IU.png' % name
            # save_path2 = r'F:\给周老师的\改的极坐标图\%s\非对称项 绝对值均值IU.png' % name

            title1 = '对称项 绝对值均值IU'
            title2 = '非对称项 绝对值均值IU'
        elif mode == 2:
            max_r = 10
            iu1.append(get_rms(new_flat_1))
            iu2.append(get_rms(new_flat_2))
            # save_path1 = r'F:\给周老师的\改的极坐标图\%s\对称项 均方根IU' % name
            # save_path2 = r'F:\给周老师的\改的极坐标图\%s\非对称项 均方根IU' % name

            title1 = '对称项 均方根IU'
            title2 = '非对称项 均方根IU'

        elif mode == 3:
            max_r = 40
            iu1.append(get_cha(new_flat_1))
            iu2.append(get_cha(new_flat_2))
            # save_path1 = r'F:\给周老师的\改的极坐标图\%s\对称项 最大-最小IU' % name
            # save_path2 = r'F:\给周老师的\改的极坐标图\%s\非对称项 最大-最小IU' % name

            title1 = '对称项 最大-最小IU'
            title2 = '非对称项 最大-最小IU'
        else:
            print('请输入正确的mode')
            return 0
        lamda0.append(xishu[0])
        lamda1.append(xishu[1])
        lamda2.append(xishu[2])
        lamda3.append(xishu[3])
        lamda4.append(xishu[4])
        colors.append((0, 1 - j / row_pot, 1))
        jiaodu1.append(qiujiaodu(xishu[4], xishu[2]))
        jiaodu2.append(qiujiaodu(xishu[3], xishu[1]))

    for j in range(len(iu1)):
        if iu1[j] > max_r:
            iu1[j] = max_r
        if iu2[j] > max_r:
            iu2[j] = max_r
    return jiaodu1, iu1, jiaodu2, iu2, colors


def langhxing_fenbu(path):
    columns = ['无', '右边浪', '双边浪', '左三分浪', '边中浪', '左边浪', '中浪', '右三分浪', '四分浪']
    data = pd.read_csv(path, header=0)

    temp = data.values[:, -62:] / -2100000
    pot1, pot2, end = jugde_row_col(temp)  # 板形有值的始末位置
    flat = temp[:end, pot1:pot2]
    all_length = end  # 全部点数
    pda_iu = []
    for i in flat:
        pda_iu.append(iu_error(i))

    res = []
    deadline = 2.5
    flat_iu = []
    flat_3D = []
    result = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
    result50 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
    result100 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
    x = np.linspace(-1, 1, 80)
    lambdas = np.array([0, 0.5063, 0.3947, 0.3336, 0.2968])
    for i in range(all_length):
        flatrow = flat[i]
        new_row = free_chazhi(flatrow)[0]
        coeff = lerangde_fenjie(new_row, x)
        del_iu2 = coeff * lambdas
        del_iu = abs(del_iu2)
        if pda_iu[i] > deadline:
            pot = search(del_iu, max(del_iu))
            if del_iu2[pot] >= 0:
                result[pot] += 1
            else:
                result[pot + 4] += 1
        else:
            result[0] += 1

    p_result = [round(i, 4) * 100 for i in result / sum(result)]
    return p_result


def langhxing_fenbufuza(path):
    columns = ['无', '右边浪', '双边浪', '左三分浪', '边中浪', '左边浪', '中浪', '右三分浪', '四分浪', '多模态复杂浪形',
               '高次复杂浪形', '双模态主导浪形']
    data = pd.read_csv(path, header=0)

    temp = data.values[:, -62:] / -2100000
    pot1, pot2, end = jugde_row_col(temp)  # 板形有值的始末位置
    flat = temp[:end, pot1:pot2]
    all_length = end  # 全部点数
    pda_iu = []
    for i in flat:
        pda_iu.append(iu_error(i))

    res = []
    deadline = 2.5

    # result = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])

    x = np.linspace(-1, 1, 80)
    lambdas = np.array([0, 0.5063, 0.3947, 0.3336, 0.2968])
    # result_quanchang = []  # 每一帧板形的浪形分布
    label = np.array([0] * all_length)
    flatness = []
    for j in range(all_length):
        flatness1 = free_chazhi(flat[j])[0]
        flatness1 = flatness1 - np.mean(flatness1)  # 0均值处理
        flatness.append(flatness1)
    use_flat = np.array(flatness)
    for i in range(all_length):
        flatrow = use_flat[i]
        if pda_iu[i] > deadline:
            width = np.linspace(-1, 1, 80)
            coeff = lerangde_fenjie(flatrow, x)
            nihehou = lerangde_nihe(coeff, width)
            iu_nihe = iu_error(nihehou)
            if abs(pda_iu[i] - iu_nihe) / pda_iu[i] > 0.2:
                label[i] = '999'
            else:
                del_iu2 = coeff * lambdas
                del_iu = abs(del_iu2)
                fenhe = abs(del_iu2[1]) + abs(del_iu2[2]) + abs(del_iu2[3]) + abs(del_iu2[4])
                del_iu22 = [0, 0, 0, 0, 0]
                del_iu22[1] = del_iu2[1] / fenhe
                del_iu22[2] = del_iu2[2] / fenhe
                del_iu22[3] = del_iu2[3] / fenhe
                del_iu22[4] = del_iu2[4] / fenhe
                del_iu22 = np.array(del_iu22)
                del_iu22a = abs(del_iu22)
                delx = list(del_iu22a.copy())
                del_max = np.max(delx)  # 最大百分比
                index_max = delx.index(del_max)
                delx[index_max] = 0
                del_max2 = np.max(delx)  # 次大百分比
                index_max2 = delx.index(del_max2)
                if del_iu22a[1] >= 0.7:
                    if del_iu22[1] > 0:
                        label[i] = '1'
                    else:
                        label[i] = '-1'
                elif del_iu22a[2] >= 0.7:
                    if del_iu22[2] > 0:
                        label[i] = '2'
                    else:
                        label[i] = '-2'
                elif del_iu22a[3] >= 0.7:
                    if del_iu22[3] > 0:
                        label[i] = '3'
                    else:
                        label[i] = '-3'
                elif del_iu22a[4] >= 0.7:
                    if del_iu22[4] > 0:
                        label[i] = '4'
                    else:
                        label[i] = '-4'
                elif abs(del_max) + abs(del_max2) > 0.8 and abs(del_max) / abs(del_max2) > 2:
                    # print('最大百分比',del_max)
                    label[i] = index_max
                elif abs(del_max) + abs(del_max2) > 0.8 and abs(del_max) / abs(del_max2) < 2:
                    label[i] = '222'
                else:
                    label[i] = '5'
        else:
            label[i] = '0'
    k00 = list(label).count(0)
    k11 = list(label).count(1)
    k22 = list(label).count(2)
    k33 = list(label).count(3)
    k44 = list(label).count(4)
    k55 = list(label).count(5)
    k11_ = list(label).count(-1)
    k22_ = list(label).count(-2)
    k33_ = list(label).count(-3)
    k44_ = list(label).count(-4)
    k999 = list(label).count(999)
    k222 = list(label).count(222)
    result = [k00, k11, k22, k33, k44, k11_, k22_, k33_, k44_, k55, k999, k222]
    result = np.array(result)
    p_result = [round(i, 4) * 100 for i in result / sum(result)]

    # new_lab = '无'
    # pp = k00 / all_length
    # if k00 / all_length >= 0.8:
    #     new_lab = '无浪形'
    # elif k55 / all_length >= 0.8:
    #     new_lab = '多模态复杂浪形'
    # elif k44 / all_length >= 0.8:
    #     new_lab = '四次浪形'
    # elif k33 / all_length >= 0.8:
    #     new_lab = '三次浪形'
    # elif k22 / all_length >= 0.8:
    #     new_lab = '二次浪形'
    # elif k11 / all_length >= 0.8:
    #     new_lab = '一次浪形'
    # elif k999 / all_length >= 0.8:
    #     new_lab = '高次复杂浪形'
    # elif k222 / all_length >= 0.8:
    #     new_lab = '双模态主导浪形'
    # else:
    #     new_lab = '纵向波动复杂浪形'

    # new_row = free_chazhi(flatrow)[0]
    # coeff = lerangde_fenjie(new_row, x)
    # del_iu2 = coeff * lambdas
    # del_iu = abs(del_iu2)
    # if pda_iu[i] > deadline:
    #     pot = search(del_iu, max(del_iu))
    #     if del_iu2[pot] >= 0:
    #         result[pot] += 1
    #     else:
    #         result[pot + 4] += 1
    # else:
    #     result[0] += 1

    # p_result = [round(i, 4) * 100 for i in result / sum(result)]
    return p_result


def iu_percent(path):
    data = pd.read_csv(path, header=0)

    temp = data.values[:, -62:] / -2100000
    pot1, pot2, end = jugde_row_col(temp)  # 板形有值的始末位置
    all_length = end  # 全部点数
    flat = temp[:end, pot1:pot2]
    iu = []
    for i in flat:
        iu.append(iu_error(i))
    # 0-1, 1-2...     (7个区间)
    result = np.array([0, 0, 0, 0, 0, 0, 0])
    x = np.linspace(-1, 1, 80)
    for i in range(all_length):
        if iu[i] <= 1:
            result[0] += 1
        elif iu[i] > 1 and iu[i] <= 2:
            result[1] += 1
        elif iu[i] > 2 and iu[i] <= 3:
            result[2] += 1
        elif iu[i] > 3 and iu[i] <= 4:
            result[3] += 1
        elif iu[i] > 4 and iu[i] <= 5:
            result[4] += 1
        elif iu[i] > 5 and iu[i] <= 6:
            result[5] += 1
        else:
            result[6] += 1
    p_result = [round(i, 4) * 100 for i in result / sum(result)]
    return p_result


def IU_mean(path):
    data = pd.read_csv(path, header=0)
    all_length = data.shape[0]  # 全部点数
    temp = data.values[:, -62:] / -2100000
    pot1, pot2, end = jugde_row_col(temp)  # 板形有值的始末位置
    flat = temp[:end, pot1:pot2]
    # print(flat)
    iu = []
    for i in flat:
        iu.append(iu_error(i))
    return iu


def IU_zhibiao(path):
    data = pd.read_csv(path, header=0)
    all_length = data.shape[0]  # 全部点数
    temp = data.values[:, -62:] / -2100000
    pot1, pot2, end = jugde_row_col(temp)  # 板形有值的始末位置
    flat = temp[:end, pot1:pot2]
    iu_mean = []
    iu_rms = []
    iu_max = []
    iu_max_min = []
    for i in flat:
        iu_mean.append(iu_error(i))
        iu_max_min.append(get_cha(i))
        iu_rms.append(get_rms(i))
        iu_max.append(max(abs(i)))
    return iu_mean, iu_max, iu_max_min, iu_rms


def iu_percent_fendaitou(path, zhibiao):  # 分带头带尾
    data = pd.read_csv(path, header=0)

    temp = data.values[:, -62:] / -2100000
    pot1, pot2, end = jugde_row_col(temp)  # 板形有值的始末位置
    all_length = end  # 全部点数
    data = data.iloc[:end, :]
    # 带头部分
    daitou = data[data['POS'] < 100]
    flat_daitou = daitou.values[:, -62:] / -2100000
    flat_daitou = flat_daitou[:, pot1:pot2]
    # 带尾部分
    dg_length = data['POS'].iloc[-1]
    daiwei = data[data['POS'] > dg_length - 100]
    flat_daiwei = daiwei.values[:, -62:] / -2100000
    flat_daiwei = flat_daiwei[:, pot1:pot2]
    # 带中部分
    daizhong = data[(data['POS'] >= 100) & (data['POS'] <= dg_length - 100)]
    flat_daizhong = daizhong.values[:, -62:] / -2100000
    flat_daizhong = flat_daizhong[:, pot1:pot2]

    iu1 = []
    iu2 = []
    iu3 = []
    if zhibiao == 'IU绝对值均值':
        for i in flat_daitou:
            iu1.append(iu_error(i))
        for i in flat_daizhong:
            iu2.append(iu_error(i))
        for i in flat_daiwei:
            iu3.append(iu_error(i))
    elif zhibiao == 'IU均方根':
        for i in flat_daitou:
            iu1.append(get_rms(i))
        for i in flat_daizhong:
            iu2.append(get_rms(i))
        for i in flat_daiwei:
            iu3.append(get_rms(i))
    elif zhibiao == 'IU最大-最小':
        for i in flat_daitou:
            iu1.append(get_cha(i))
        for i in flat_daizhong:
            iu2.append(get_cha(i))
        for i in flat_daiwei:
            iu3.append(get_cha(i))
    else:
        for i in flat_daitou:
            iu1.append(max(abs(i)))
        for i in flat_daizhong:
            iu2.append(max(abs(i)))
        for i in flat_daiwei:
            iu3.append(max(abs(i)))
    iu_ = [iu1, iu2, iu3]
    # 0-1, 1-2...     (7个区间)
    result = np.array([0, 0, 0, 0, 0, 0, 0])
    x = np.linspace(-1, 1, 80)
    p_result = [[], [], []]
    for k in range(3):
        iu = iu_[k]
        for i in range(len(iu)):
            if iu[i] <= 1:
                result[0] += 1
            elif iu[i] > 1 and iu[i] <= 2:
                result[1] += 1
            elif iu[i] > 2 and iu[i] <= 3:
                result[2] += 1
            elif iu[i] > 3 and iu[i] <= 4:
                result[3] += 1
            elif iu[i] > 4 and iu[i] <= 5:
                result[4] += 1
            elif iu[i] > 5 and iu[i] <= 6:
                result[5] += 1
            else:
                result[6] += 1
        p_result[k] = [round(i, 4) * 100 for i in result / sum(result)]
    return p_result[0], p_result[1], p_result[2]


def IU_zhibiao_fendaitou(path, zhibiao):
    data = pd.read_csv(path, header=0)
    temp = data.values[:, -62:] / -2100000
    pot1, pot2, end = jugde_row_col(temp)  # 板形有值的始末位置
    all_length = end  # 全部点数
    data = data.iloc[:end, :]
    # 带头部分
    daitou = data[data['POS'] < 100]
    flat_daitou = daitou.values[:, -62:] / -2100000
    flat_daitou = flat_daitou[:, pot1:pot2]
    # 带尾部分
    dg_length = data['POS'].iloc[-1]
    daiwei = data[data['POS'] > dg_length - 100]
    flat_daiwei = daiwei.values[:, -62:] / -2100000
    flat_daiwei = flat_daiwei[:, pot1:pot2]
    # 带中部分
    daizhong = data[(data['POS'] >= 100) & (data['POS'] <= dg_length - 100)]
    flat_daizhong = daizhong.values[:, -62:] / -2100000
    flat_daizhong = flat_daizhong[:, pot1:pot2]

    iu1 = []
    iu2 = []
    iu3 = []
    if zhibiao == 'IU绝对值均值':
        for i in flat_daitou:
            iu1.append(iu_error(i))
        for i in flat_daizhong:
            iu2.append(iu_error(i))
        for i in flat_daiwei:
            iu3.append(iu_error(i))
    elif zhibiao == 'IU均方根':
        for i in flat_daitou:
            iu1.append(get_rms(i))
        for i in flat_daizhong:
            iu2.append(get_rms(i))
        for i in flat_daiwei:
            iu3.append(get_rms(i))
    elif zhibiao == 'IU最大-最小':
        for i in flat_daitou:
            iu1.append(get_cha(i))
        for i in flat_daizhong:
            iu2.append(get_cha(i))
        for i in flat_daiwei:
            iu3.append(get_cha(i))
    else:
        for i in flat_daitou:
            iu1.append(max(abs(i)))
        for i in flat_daizhong:
            iu2.append(max(abs(i)))
        for i in flat_daiwei:
            iu3.append(max(abs(i)))
    return iu1, iu2, iu3
