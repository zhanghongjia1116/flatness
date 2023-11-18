import matplotlib.patches as mpatches
import numpy as np

from .Wlearn import lerangde_nihe, lerangde_fenjie, sigema, jugde_row_col, free_chazhi, base_file_name, plot_3dflat
from .绘图 import iu_error, get_rms, get_cha, odd_lerangde_nihe, even_lerangde_nihe, qiujiaodu
from .MXL_Support import *
import matplotlib.pyplot as plt


def search(array, target):
    array = list(array)
    return array.index(target)


def plot_langxingbaifenbi(data, deadline=2.5):
    all_length = data.shape[0]  # 全部点数
    pda_iu = []
    for i in data:
        pda_iu.append(iu_error(i))

    result = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
    result_point = np.array([0 for _ in range(all_length)])
    x = np.linspace(-1, 1, 80)
    lambdas = np.array([0, 0.5063, 0.3947, 0.3336, 0.2968])
    for i in range(all_length):
        flatrow = data[i]
        coeff = lerangde_fenjie(flatrow, x)
        del_iu2 = coeff * lambdas
        del_iu = abs(del_iu2)
        if pda_iu[i] > deadline:
            pot = search(del_iu, max(del_iu))
            if del_iu2[pot] >= 0:
                result[pot] += 1
                # 待修改
                result_point[i] = pot
            else:
                result[pot + 4] += 1
                result_point[i] = pot + 4
        else:
            result[0] += 1
            result_point[i] = 0

    # plt.figure(figsize=(6, 4), dpi=300)
    # plt.xlabel('采样点')
    # plt.ylim(-0.5, 8.5)
    # plt.scatter(range(len(result_point)), result_point, color='red', s=5, label='缺陷类型')
    # plt.yticks(range(0, 9, 1), ['无', '右边浪', '双边浪', '左三分浪', '边中浪', '左边浪', '中浪', '右三分浪', '四分浪'])
    # plt.title("浪形缺陷图")
    # plt.legend()
    # plt.show()

    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)

    # ax.plot(result_point, color='red', linewidth=1.0, linestyle='-', label='缺陷类型')
    plt.scatter(range(len(result_point)), result_point, color='red', s=0.5, label='缺陷类型')
    ax.set_ylim(-0.5, 8.5)
    ax.set_yticks(range(9))
    ax.set_yticklabels(['无', '右边浪', '双边浪', '左三分浪', '边中浪', '左边浪', '中浪', '右三分浪', '四分浪'])
    ax.set_xlabel('采样点')
    ax.set_title("浪形缺陷图")

    plt.show()

    p_result = [round(i, 4) * 100 for i in result / sum(result)]

    labels = ['无', '右边浪', '双边浪', '左三分浪', '边中浪', '左边浪', '中浪', '右三分浪', '四分浪']
    explode = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    colors = ['lightskyblue', 'yellowgreen', 'purple', 'blue', 'coral', 'red', 'peachpuff', '#C1FFC1', 'lightpink']
    plt.pie(p_result, explode=explode, startangle=90, colors=colors)
    plt.legend(labels=['%s,%1.1f %%' % (l, s) for l, s in zip(labels, p_result)], fontsize=10, title="浪形",
               loc="center left", bbox_to_anchor=(0.91, 0, 0.3, 1))
    plt.show()

    return p_result


def plot_err_langxing(data, sat, deadline=2.5):
    all_length = data.shape[0]  # 全部点数
    pda_iu = []
    for i in data:
        pda_iu.append(iu_error(i))

    result = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
    result_point = np.array([0 for _ in range(all_length)])
    x = np.linspace(-1, 1, 80)
    lambdas = np.array([0, 0.5063, 0.3947, 0.3336, 0.2968])
    for i in range(all_length):
        flatrow = data[i]
        coeff = lerangde_fenjie(flatrow, x)
        del_iu2 = coeff * lambdas
        del_iu = abs(del_iu2)
        if pda_iu[i] > deadline:
            pot = search(del_iu, max(del_iu))
            if del_iu2[pot] >= 0:
                result[pot] += 1
                result_point[i] = pot
            else:
                result[pot + 4] += 1
                result_point[i] = pot + 4
        else:
            result[0] += 1
            result_point[i] = 0

    result_point2 = result_point * sat

    # 创建画布
    fig, ax = plt.subplots(figsize=(6, 4), dpi=150)

    # 根据 zero_mask 将点分别赋予颜色
    plt.scatter(
        range(len(result_point2)), result_point2,
        color=np.where(list(map(lambda x: not x, sat)), 'lightblue', 'red'),
        s=0.5, label='缺陷类型'
    )
    red_patch = mpatches.Patch(color='red', label='异常')
    green_patch = mpatches.Patch(color='lightblue', label='正常')  # lightblue
    plt.legend(handles=[red_patch, green_patch])
    # 设定坐标轴
    ax.set_ylim(-0.5, 8.5)
    ax.set_yticks(range(9))
    ax.set_yticklabels(['无', '右边浪', '双边浪', '左三分浪', '边中浪', '左边浪', '中浪', '右三分浪', '四分浪'])
    ax.set_xlabel('采样点')
    ax.set_title("浪形缺陷图")


def spearman(data):
    import matplotlib.pyplot as plt
    import seaborn as sns
    from scipy.stats import spearmanr

    df0 = data.iloc[:, :-63]
    df_scaled = normalize(np.array(df0))
    # 创建新的DataFrame来存储处理后的数据
    df = pd.DataFrame(df_scaled, columns=df0.columns)

    correlation, _ = spearmanr(df)
    correlation = pd.DataFrame(correlation, columns=df.columns, index=df.columns)
    top_features = correlation['F5 flatness error'].sort_values(ascending=False)[1:7]
    print('spearmanr:', top_features)

    plt.figure(figsize=(12, 8))
    sns.barplot(x=top_features.index, y=top_features.values)
    plt.xlabel('特征名')
    plt.ylabel('相关度')
    plt.title('斯皮尔曼-前六个板形相关度特征')
    plt.xticks(rotation=10)
    plt.show()
    plt.close()

    f5_flatness_error = df['F5 flatness error']
    fea = top_features.index
    print(fea)

    fig, axs = plt.subplots(3, 2, figsize=(12, 12))

    for i, ax in enumerate(axs.flatten()):
        if i < 6:
            ax.plot(df[fea[i]], label='{}'.format(fea[i]))
            ax.plot(f5_flatness_error, label='F5 Flatness Error')
            ax.set_title('{}'.format(fea[i]) + '(相关系数：' + '{:.2f}'.format(top_features.values[i]) + ')')
            ax.legend()  # 在每个子图上添加图例对象

    fig.suptitle('斯皮尔曼-相关系数较高特征曲线', fontsize=16)
    fig.tight_layout()

    plt.show()


def draw_sat(sat, name='IU异常监控图'):
    # 分别获取 x, y 坐标
    x = [i for i in range(len(sat))]
    y = sat

    # 遍历 sat 列表，将值为 1 的点设置为红色
    colors = ['red' if i == 1 else 'lightblue' for i in sat]  # palegreen,lightcoral
    # 设置 y 轴刻度显示0和1
    plt.yticks([0, 1], [0, 1])
    # 绘制散点图，并为不同颜色的点添加标签
    # 绘制散点图，并添加 label 标签
    plt.scatter(x, y, s=1, color=colors)

    # 添加图例
    red_patch = mpatches.Patch(color='red', label='异常')
    green_patch = mpatches.Patch(color='lightblue', label='正常')  # lightblue
    plt.legend(handles=[red_patch, green_patch])
    # 添加图表标题和坐标轴标签
    plt.title(name)
    plt.xlabel('样本点')
    plt.ylabel('异常情况')


def related_all(data):

    df0 = data.iloc[:, :-63]
    df_scaled = normalize(np.array(df0))
    # 创建新的DataFrame来存储处理后的数据
    df = pd.DataFrame(df_scaled, columns=df0.columns)

    correlation = df.corr()['F5 flatness error'].sort_values(ascending=False)
    # top_features = correlation[1:7]  # 取前五个相关性最高的特征，排除 f 本身

    # plt.figure(figsize=(12, 8))
    # sns.barplot(x=top_features.index, y=top_features.values)
    # plt.xlabel('特征名')
    # plt.ylabel('相关度')
    # plt.title('皮尔逊-前六个板形相关度特征')
    # plt.xticks(rotation=10)
    # plt.show()
    # plt.close()

    # 绘制六边形分析图的函数
    # def plot_hexagon(dataSignal, labels):
    #     angles = np.linspace(0, 2 * np.pi, len(dataSignal), endpoint=False).tolist()
    #     angles += angles[:1]  # 闭合图形
    #
    #     values = dataSignal.tolist()
    #     values += values[:1]  # 闭合图形
    #
    #     fig = plt.figure(figsize=(6, 6))
    #     ax = fig.add_subplot(111, polar=True)
    #     ax.plot(angles, values, 'o-', linewidth=2)
    #     ax.fill(angles, values, alpha=0.25)
    #     ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    #     ax.grid(True)
    #
    #     plt.title('六边形分析图')
    #     plt.show()
    #     plt.close()
    #
    # # 原始数据
    # top_features_ = pd.Series(top_features.values)  # 示例数据，请替换为您的实际数据
    # feature_names = top_features.index  # 示例特征名，请替换为您的实际特征名
    #
    # # 绘制六边形分析图
    # plot_hexagon(top_features_, feature_names)
    #
    #
    # f5_flatness_error = df['F5 flatness error']
    # fea = top_features.index
    # print(fea)
    #
    # fig, axs = plt.subplots(3, 2, figsize=(12, 12))
    #
    # for i, ax in enumerate(axs.flatten()):
    #     if i < 6:
    #         ax.plot(df[fea[i]], label='{}'.format(fea[i]))
    #         ax.plot(f5_flatness_error, label='F5 Flatness Error')
    #         ax.set_title('{}'.format(fea[i]) + '(相关系数：' + '{:.2f}'.format(top_features.values[i]) + ')')
    #         ax.legend()  # 在每个子图上添加图例对象
    #
    # fig.suptitle('皮尔逊-相关系数较高特征曲线', fontsize=16)
    # fig.tight_layout()
    #
    # plt.show()


def related(data, i):
    import matplotlib.pyplot as plt
    import seaborn as sns
    try:
        df0 = data.iloc[i:i + 2, :-63]
    except:
        df0 = data.iloc[i - 2:i, :-63]
    df_scaled = normalize(np.array(df0))
    # 创建新的DataFrame来存储处理后的数据
    df = pd.DataFrame(df_scaled, columns=df0.columns)

    correlation = df.corr()['F5 flatness error'].sort_values(ascending=False)
    top_features = correlation[1:7]  # 取前五个相关性最高的特征，排除 f 本身

    plt.figure(figsize=(12, 8))
    sns.barplot(x=top_features.index, y=top_features.values)
    plt.xlabel('特征名')
    plt.ylabel('相关度')
    plt.title('前六个板形相关度特征')
    plt.xticks(rotation=10)
    plt.show()
    plt.close()

    f5_flatness_error = df['F5 flatness error']
    fea = top_features.index
    print(fea)

    fig, axs = plt.subplots(3, 2, figsize=(12, 12))

    for ii, ax in enumerate(axs.flatten()):
        if ii < 6:
            ax.plot(df[fea[ii]], label='{}'.format(fea[ii]))
            ax.plot(f5_flatness_error, label='F5 Flatness Error')
            ax.set_title('{}'.format(fea[ii]))
            ax.legend()  # 在每个子图上添加图例对象

    fig.suptitle('相关系数较高特征曲线', fontsize=16)
    fig.tight_layout()

    plt.show()


if __name__ == "__main__":
    CH()
    id_err = []
    threshold = 2
    po = 1
    path = r'D:\A_My_file\顺义灯塔工厂二期\监测\H219C34305000_1.csv'
    data = pd.read_csv(path, header=0, encoding='gbk')
    name_all = path.split('\\')[-1].split('.')[0]
    name = name_all[:13]
    print('file_name:', name)

    flat = data.values[:, -62:] / -2100000
    pot1, pot2, row_pot2 = jugde_row_col(flat)
    row_pot = flat.shape[0]
    data_n = data.iloc[:row_pot, :]
    useflat = flat[:row_pot, pot1:pot2]
    flatness = []
    iu_mean = []
    iu_rms = []
    iu_max = []
    iu_max_min = []
    for j in range(row_pot):
        flatness1 = free_chazhi(useflat[j])[0]
        flatness1 = flatness1 - np.mean(flatness1)  # 0均值处理
        flatness.append(flatness1)

    for i in useflat:
        iu_mean.append(iu_error(i))
        iu_rms.append(get_rms(i))
        iu_max.append(max(abs(i)))
        iu_max_min.append(get_cha(i))
    avg_iu_mean = np.array(iu_mean).mean()
    avg_iu_rms = np.array(iu_rms).mean()
    avg_iu_max = np.array(iu_max).mean()
    avg_iu_max_min = np.array(iu_max_min).mean()
    iu = [avg_iu_mean, avg_iu_rms, avg_iu_max, avg_iu_max_min]

    # # 带头部分
    # daitou = dataSignal[dataSignal['POS'] < 100]
    # flat_daitou = daitou.values[:, -62:] / -2100000
    # flat_daitou = flat_daitou[:, pot1:pot2]
    # iu_mean1 = []
    # iu_rms1 = []
    # iu_max1 = []
    # iu_max_min1 = []
    # for i in flat_daitou:
    #     iu_mean1.append(iu_error(i))
    #     iu_rms1.append(get_rms(i))
    #     iu_max1.append(max(abs(i)))
    #     iu_max_min1.append(get_cha(i))
    # avg_iu_mean1 = np.array(iu_mean1).mean()
    # avg_iu_rms1 = np.array(iu_rms1).mean()
    # avg_iu_max1 = np.array(iu_max1).mean()
    # avg_iu_max_min1 = np.array(iu_max_min1).mean()
    # iu1 = [avg_iu_mean1, avg_iu_rms1, avg_iu_max1, avg_iu_max_min1]
    # # 带尾部分
    # dg_length = dataSignal['POS'].iloc[-1]
    # daiwei = dataSignal[dataSignal['POS'] > dg_length - 100]
    # flat_daiwei = daiwei.values[:, -62:] / -2100000
    # flat_daiwei = flat_daiwei[:, pot1:pot2]
    # iu_mean3 = []
    # iu_rms3 = []
    # iu_max3 = []
    # iu_max_min3 = []
    # for i in flat_daiwei:
    #     iu_mean3.append(iu_error(i))
    #     iu_rms3.append(get_rms(i))
    #     iu_max3.append(max(abs(i)))
    #     iu_max_min3.append(get_cha(i))
    # avg_iu_mean3 = np.array(iu_mean3).mean()
    # avg_iu_rms3 = np.array(iu_rms3).mean()
    # avg_iu_max3 = np.array(iu_max3).mean()
    # avg_iu_max_min3 = np.array(iu_max_min3).mean()
    # iu3 = [avg_iu_mean3, avg_iu_rms3, avg_iu_max3, avg_iu_max_min3]
    # # 带中部分
    # daizhong = dataSignal[(dataSignal['POS'] >= 100) & (dataSignal['POS'] <= dg_length - 100)]
    # flat_daizhong = daizhong.values[:, -62:] / -2100000
    # flat_daizhong = flat_daizhong[:, pot1:pot2]
    # iu_mean2 = []
    # iu_rms2 = []
    # iu_max2 = []
    # iu_max_min2 = []
    # for i in flat_daizhong:
    #     iu_mean2.append(iu_error(i))
    #     iu_rms2.append(get_rms(i))
    #     iu_max2.append(max(abs(i)))
    #     iu_max_min2.append(get_cha(i))
    # avg_iu_mean2 = np.array(iu_mean2).mean()
    # avg_iu_rms2 = np.array(iu_rms2).mean()
    # avg_iu_max2 = np.array(iu_max2).mean()
    # avg_iu_max_min2 = np.array(iu_max_min2).mean()
    # iu2 = [avg_iu_mean2, avg_iu_rms2, avg_iu_max2, avg_iu_max_min2]
    # # 全长（带头-带中）除去带尾100米
    # # quanchang_4 = dataSignal[dataSignal['POS'] < (dg_length - 100)]
    # quanchang_4 = dataSignal  # 全长数据
    # flat_quanchang_4 = quanchang_4.values[:, -62:] / -2100000
    # flat_quanchang_4 = flat_quanchang_4[:, pot1:pot2]
    # iu_mean4 = []
    # iu_rms4 = []
    # iu_max4 = []
    # iu_max_min4 = []
    # for i in flat_quanchang_4:
    #     iu_mean4.append(iu_error(i))
    #     iu_rms4.append(get_rms(i))
    #     iu_max4.append(max(abs(i)))
    #     iu_max_min4.append(get_cha(i))
    # avg_iu_mean4 = np.array(iu_mean4).mean()
    # avg_iu_rms4 = np.array(iu_rms4).mean()
    # avg_iu_max4 = np.array(iu_max4).mean()
    # avg_iu_max_min4 = np.array(iu_max_min4).mean()
    # iu4 = [avg_iu_mean4, avg_iu_rms4, avg_iu_max4, avg_iu_max_min4]

    ERR, NOR, sat = judge_err(iu_mean, threshold)
    for idx, val in enumerate(sat):
        if val == 1:
            id_err.append(idx)
            # print("The index of error is:", idx)
    print("The index of error is:", id_err)

    # 绘制全长IU统计图
    visualization2(iu_mean, threshold, name='\'{}\''.format(name) + 'IU图')
    # plt.show()
    plt.close()

    # 绘制一帧IU统计图
    visualization2(flatness[po], threshold, name='{}'.format(name) + '第{}帧'.format(po + 1) + 'IU图')
    # plt.show()
    plt.close()

    # 绘制全长异常二值图
    draw_sat(sat, name='\'{}\''.format(name) + 'IU异常监控图')
    # plt.show()
    plt.close()

    # 绘制全长浪形模态图
    use_flat = np.array(flatness)
    # plot_langxingbaifenbi(use_flat,deadline=threshold)
    plt.close()

    # 绘制三维图
    # plot_3dflat(use_flat)

    # 绘制全长异常浪形模态图
    use_flat = np.array(flatness)
    plot_err_langxing(use_flat, sat, deadline=threshold)
    # plt.show()
    plt.close()

    # 绘制相关性图片
    related_all(data)

    spearman(data)

    # 绘制第i帧和i+帧图片，单帧无法计算
    related(data, 2)
