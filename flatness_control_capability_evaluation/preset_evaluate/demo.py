import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

columns = ['B1 WRB ref value start',
           'B1 IRB ref value start',
           'S1 top IR shfiting ref value start',

           'B2 WRB ref value start',
           'B2 IRB ref value start',
           'S2 top IR shfiting ref value start',

           'B3 WRB ref value start',
           'B3 IRB ref value start',
           'S3 top IR shfitingl ref value start',

           'WR bending actual value start',
           'B4 IRB ref value start',
           'S4 top  IR shfiting  ref value start',

           'B5 WRB ref value start',
           'B5 IRB ref value start',
           'S5 top IR shfiting ref value start']


def softmax(vector):
    """
    Implements the softmax function
    Args:
        vector: (np.array,list,tuple): A  numpy array of shape (1,n)
                consisting of real values or a similar list,tuple
    Returns:
        softmax_vec (np.array): The input numpy array  after applying
        softmax.
        The softmax vector adds up to one. We need to ceil to mitigate for
        precision
    """
    exponent_vector = np.exp(-1 * vector)  # 算向量中每个x的e^x，其中e是自然对数的底数（约2.718）
    # 把所有的指数加起来
    sum_of_exponents = np.sum(exponent_vector)
    # 将每个指数除以所有指数之和
    softmax_vector = exponent_vector / sum_of_exponents
    return softmax_vector


def coefficient_1(data, policyNo, proportion=0.5):
    """
    度量离均值中心越远，越不好，则softmax后的值越小
    Args:
        data:
        policyNo:
        proportion:

    Returns:

    """
    singlePolicyData = data[data['policyNo'] == policyNo]
    good = singlePolicyData[singlePolicyData['50米均值'] < 3]
    preset = singlePolicyData.loc[:, columns]
    good_preset = good.loc[:, columns]
    IU = singlePolicyData.loc[:, '50米均值']
    normIU = softmax(singlePolicyData.loc[:, '50米均值'])

    presetValueMean = good_preset.mean()
    distance = np.sqrt(np.square(preset - presetValueMean).sum(axis=1))
    normPrest = softmax(distance)
    # 计算欧氏距离
    s1 = proportion * normPrest + (1 - proportion) * normIU

    return s1


def coefficient_2():
    # TODO: no implement
    pass


def coefficient_3():
    # TODO: no implement
    pass


if __name__ == '__main__':
    data = pd.read_pickle('./data/预设定值初值表.pkl')
    # 删除columns为空的行
    data = data.dropna(subset=columns, how='any')
    all_policy = data['policyNo'].unique()
    s1 = coefficient_1(data, all_policy[0])
    print(s1)
