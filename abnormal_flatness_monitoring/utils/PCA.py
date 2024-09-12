import pickle

import pandas as pd
import scipy
from scipy import stats

from .MXL_Support import *


def save_pca_model(v_I, p_k, data_mean, data_std, t_limit, spe_limit, v, P, k, filepath):
    model = {
        'v_I': v_I,
        'p_k': p_k,
        'data_mean': data_mean,
        'data_std': data_std,
        't_limit': t_limit,
        'spe_limit': spe_limit,
        'v': v,
        'P': P,
        'k': k
    }
    with open(filepath, 'wb') as f:
        pickle.dump(model, f)


def load_pca_model(filepath):
    with open(filepath, 'rb') as f:
        model = pickle.load(f)
    v_I = model['v_I']
    p_k = model['p_k']
    data_mean = model['data_mean']
    data_std = model['data_std']
    t_limit = model['t_limit']
    spe_limit = model['spe_limit']
    v = model['v']
    P = model['P']
    k = model['k']
    return v_I, p_k, data_mean, data_std, t_limit, spe_limit, v, P, k


def pca(data, div=0.85):
    data_mean = np.mean(data, 0)
    data_std = np.std(data, 0)
    data_nor = (data - data_mean) / data_std
    X = np.cov(data_nor.T)
    P, v, P_t = np.linalg.svd(X)  # 载荷矩阵计算  此函数返回三个值 u s v 此时v是u的转置
    Z = np.dot(P, P_t)
    v_sum = np.sum(v)
    k = []  # 主元个数
    if div < 1:
        for x in range(len(v)):
            PE_k = v[x] / v_sum
            if x == 0:
                PE_sum = PE_k
            else:
                PE_sum = PE_sum + PE_k
            if PE_sum < div:  # 累积方差贡献率
                pass
            else:
                k.append(x + 1)
                break
        n_components = k[0]
    else:
        n_components = div
    print('all_components:', len(v))
    print('n_components:', n_components)
    # 新主元
    p_k = P[:, :n_components]
    v_I = np.diag(1 / v[:n_components])

    confidence = 0.99
    # T统计量阈值计算
    coe = n_components * (np.shape(data)[0] - 1) * (np.shape(data)[0] + 1) / (
            (np.shape(data)[0] - n_components) * np.shape(data)[0])

    t_limit = coe * stats.f.ppf(confidence, n_components, (np.shape(data)[0] - n_components))

    # SPE统计量阈值计算
    theta1 = np.sum((v[n_components:]) ** 1)
    theta2 = np.sum((v[n_components:]) ** 2)
    theta3 = np.sum((v[n_components:]) ** 3)
    h0 = 1 - (2 * theta1 * theta3) / (3 * (theta2 ** 2))

    c_alpha = scipy.stats.norm.ppf(confidence)

    spe_limit = theta1 * (
            (h0 * c_alpha * ((2 * theta2) ** 0.5) / theta1 + 1 + theta2 * h0 * (h0 - 1) / (theta1 ** 2)) ** (
            1 / h0))

    return v_I, p_k, data_mean, data_std, t_limit, spe_limit, v, P, k


# 计算T统计量
def T2(data_in, data_mean, data_std, p_k, v_I):
    test_data_nor = ((data_in - data_mean) / data_std).reshape(len(data_in), 1)
    T_count = np.dot(np.dot((np.dot((np.dot(test_data_nor.T, p_k)), v_I)), p_k.T), test_data_nor)
    return T_count


# 计算SPE统计量
def SPE(data_in, data_mean, data_std, p_k):
    test_data_nor = ((data_in - data_mean) / data_std).reshape(len(data_in), 1)
    I = np.eye(len(data_in))
    Q_count = np.dot(np.dot((I - np.dot(p_k, p_k.T)), test_data_nor).T,
                     np.dot((I - np.dot(p_k, p_k.T)), test_data_nor))
    tmp = []
    I2 = np.eye(1)
    for i in range(np.size(test_data_nor)):
        tmp.append(np.dot(np.dot(test_data_nor[i, :],
                                 (I2 - np.dot(p_k[i, :], p_k[i, :].T))),
                          test_data_nor[i, :]))
    return Q_count, tmp


def plot_curve(Xtest, max_t_indexes, max_q_indexes, IU, name):
    plt.figure(dpi=120)
    ax1 = plt.subplot(2, 1, 1)
    for index in max_t_indexes:
        print('t:', name[index])
        plt.plot(Xtest[:, index], label='{}'.format(name[index]))
    plt.plot(IU, label='IU')
    # plt.xlabel('X-axis')
    plt.ylabel('$T^2$溯源')
    plt.title('PCA溯源')
    plt.legend()

    ax2 = plt.subplot(2, 1, 2)

    for index in max_q_indexes:
        print('q:', name[index])
        plt.plot(Xtest[:, index], label='{}'.format(name[index]))
    plt.plot(IU, label='IU')
    plt.xlabel('采样点')
    plt.ylabel('$SPE$溯源')
    # plt.title('Curves for Max Three Indexes')
    plt.legend()
    plt.show()


def get_top_indexes(values):
    indexed_values = {index: value for index, value in enumerate(values[0])}
    sorted_values = sorted(indexed_values.items(), key=lambda x: x[1], reverse=True)
    top_three_indexes = [index for index, _ in sorted_values[:3]]
    return top_three_indexes


def softmax(x):
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            if np.isnan(x[i, j]) or np.isinf(x[i, j]):
                x[i, j] = 0
    # e_x = np.exp(x - (np.max(x) if np.max(x) != None or not math.isinf(
    #     np.max(x)) else 0))  # subtracting the maximum value for numerical stability
    e_x = np.exp(x - np.max(x))  # subtracting the maximum value for numerical stability
    return e_x / np.sum(e_x, axis=1, keepdims=True)


def run_pca(pth1, pth2, model_path):
    CH()
    train = pd.read_csv(pth1)
    test = pd.read_csv(pth2)
    train = train.dropna()
    test = test.dropna()

    up_limit = plot_box(train)
    # plt.close()

    Xtrain, Xtest, IU, IU_train, canshu = get_banxing_data(train, test, limit=up_limit)

    # X_train, X_test = normalize(Xtrain, Xtest)

    # N = 53

    v_I, p_k, data_mean, data_std, t_limit, spe_limit, v, P, k = load_pca_model(model_path)

    # v_I, p_k, data_mean, data_std, t_limit, spe_limit, v, P, k = pca(Xtrain, N)

    # 循环计算
    test_data = Xtest
    t_total = []
    q_total = []
    q_con_list = []
    for x in range(np.shape(test_data)[0]):
        data_in = Xtest[x, :]
        t = T2(data_in, data_mean, data_std, p_k, v_I)
        q, q_com = SPE(data_in, data_mean, data_std, p_k)
        t_total.append(t[0, 0])
        q_total.append(q[0, 0])
        q_con_list.append(q_com)
    #####################################计算T^2贡献度################################
    t_total_contribution = []
    X_test = test_data
    b = np.linalg.inv(np.dot(p_k.T, p_k))
    for i in range(X_test.shape[0]):
        tmp = []
        for j in range(X_test.shape[1]):
            tT = np.dot(np.mat(X_test[i, j]).T, [p_k[j, :].T])
            a = np.dot(tT, v_I)
            c = np.dot(p_k[j, :], X_test[i, j])
            tmp1 = np.dot(a, b)
            tmp2 = np.dot(tmp1, c)
            tmp.append(float(tmp2))
        t_total_contribution.append(tmp)

    IU = np.array(IU)

    MR, FAR, sat, id_err = cal_acc4(t_total, q_total, t_limit, spe_limit, IU, limit=up_limit)

    id_err = [x for x in id_err if x >= 0]

    T_C = softmax(normalize(np.array(t_total_contribution)))
    Q_C = softmax(normalize(np.array(q_con_list)))

    rows, cols = T_C.shape

    sum_TC = np.zeros((1, cols))
    sum_QC = np.zeros((1, cols))
    for kk in range(0, len(sat)):
        if sat[kk] == 1:
            sum_TC += T_C[kk, :]
            sum_QC += Q_C[kk, :]

    feature = Xtest
    feature = normalize(feature)

    return t_total, q_total, t_limit, spe_limit, t_total_contribution, q_con_list, feature, canshu, id_err, sum_TC, sum_QC, IU


if __name__ == "__main__":
    CH()

    # train = pd.read_csv(r'D:\A_My_file\DATA\TE_csv\train\d00.csv', header=None, engine='python')
    # test = pd.read_csv(r'D:\A_My_file\DATA\TE_csv\test\d05_te.csv', header=None, engine='python')
    # Xtrain, Xtest = get_TE_data2(train, test)
    train = pd.read_csv(r'D:\A_My_file\DATA\DX51D+Z\DX51D_all.csv')
    test = pd.read_csv(r'D:\A_My_file\DATA\DX51D+Z\DX51D_ALL\H219C34305000_1.csv')
    # Xtrain, Xtest, IU, IU2, canshu = get_banxing_data(train, test)
    # print(canshu)
    # Xtrain, Xtest, IU, IU2, canshu
    # train = pd.read_csv(r'F:\GANG2\merged3.csv')
    # # test = pd.read_csv(r'H:\GANG2\降采样73AA2\H122C26206900_1.csv')
    #
    # test = pd.read_csv(r'F:\GANG2\降采样73AA2\HB13215408000_1.csv')
    df2 = normalize(NAN_DROP(test))
    nor_IU = df2['F5 flatness error']

    up_limit = plot_box(train)
    plt.close()
    print('up_limit:', up_limit)

    Xtrain, Xtest, IU, IU_train, canshu = get_banxing_data(train, test, limit=up_limit)
    X_train, X_test = normalize(Xtrain, Xtest)

    N = 53
    for div in range(N, N + 1):
        v_I, p_k, data_mean, data_std, t_limit, spe_limit, v, P, k = pca(Xtrain, 0.99)
        # 循环计算
        test_data = Xtest
        t_total = []
        q_total = []
        q_con_list = []

        for x in range(np.shape(test_data)[0]):
            data_in = Xtest[x, :]
            t = T2(data_in, data_mean, data_std, p_k, v_I)
            q, q_com = SPE(data_in, data_mean, data_std, p_k)
            t_total.append(t[0, 0])
            q_total.append(q[0, 0])
            q_con_list.append(q_com)

        #####################################计算T^2贡献度################################
        t_total_contribution = []
        X_test = test_data
        b = np.linalg.inv(np.dot(p_k.T, p_k))
        for i in range(X_test.shape[0]):
            tmp = []
            for j in range(X_test.shape[1]):
                tT = np.dot(np.mat(X_test[i, j]).T, [p_k[j, :].T])
                a = np.dot(tT, v_I)
                c = np.dot(p_k[j, :], X_test[i, j])
                tmp1 = np.dot(a, b)
                tmp2 = np.dot(tmp1, c)
                tmp.append(float(tmp2))
            t_total_contribution.append(tmp)

        MR, FAR, sat, id_err = cal_acc4(t_total, q_total, t_limit, spe_limit, IU, limit=up_limit)
        id_err = [x for x in id_err if x > 0]
        print('id_err :', id_err)
        visualization4(t_total, q_total, t_limit, spe_limit, name='监测图')
        plt.show()
        plt.close()

        contribution(t_total_contribution, q_con_list, 11)
        plt.show()
        plt.close()

        T_C = softmax(normalize(np.array(t_total_contribution)))
        Q_C = softmax(normalize(np.array(q_con_list)))

        rows, cols = T_C.shape

        sum_TC = np.zeros((1, cols))
        sum_QC = np.zeros((1, cols))
        for kk in range(0, len(sat)):
            if sat[kk] == 1:
                sum_TC += T_C[kk, :]
                sum_QC += Q_C[kk, :]

        max_T_ind = get_top_indexes(sum_TC)
        max_Q_ind = get_top_indexes(sum_QC)

        print(max_T_ind)
        print(max_Q_ind)
        dat = normalize(Xtest)
        plot_curve(dat, max_T_ind, max_Q_ind, nor_IU, canshu)
        # plot_curve(dat, max_Q_ind, nor_IU, canshu)

        canshu = get_canshu()
        feature = Xtest[:, 5]
        feature_IU(feature, IU, name=canshu[5])
        # plt.show()
        plt.close()
