# -*- coding:utf-8 -*-
"""
@author:MR.W
@file:Wlearn.py
@time:2019/4/310:22
"""
import numpy as np


def search(array, target):
    array = list(array)
    return array.index(target)


def zhuzhuangtu(fengeshu, data):
    print('******************数据信息******************')
    print('此数据数量', len(data))
    data_min = min(data)
    data_max = max(data)
    data = list(map(lambda x: float(x), data))
    print('最大值', max(data))
    print('最小值', min(data))
    chazhi = data_max - data_min
    deleta = chazhi / fengeshu
    x = []
    y = []
    sum = 0
    for i in range(0, fengeshu):
        # print(min(data) + deleta * i)
        # print(max(data)-deleta*(fengeshu-i-1))
        for j in data:
            if i != fengeshu - 1:
                if (j >= data_min + deleta * i) and (j < data_max - deleta * (fengeshu - i - 1)):
                    sum += 1
            if i == fengeshu - 1:
                if (j >= data_min + deleta * i) and (j <= data_max - deleta * (fengeshu - i - 1)):
                    sum += 1
        x.append(str(round(data_min + deleta * i, 3)) + '-' + str(round(data_max - deleta * (fengeshu - i - 1), 3)))
        y.append(sum)
        sum = 0
    print('*******************结果*********************')
    print('x坐标', x)
    print('y坐标', y)
    print('********************************************')
    return x, y


def zhuzhuangtu(fengeshu, data):
    print('******************数据信息******************')
    print('此数据数量', len(data))
    data_min = min(data)
    data_max = max(data)
    data = list(map(lambda x: float(x), data))
    print('最大值', max(data))
    print('最小值', min(data))
    chazhi = data_max - data_min
    deleta = chazhi / fengeshu
    x = []
    y = []
    sum = 0
    for i in range(0, fengeshu):
        # print(min(data) + deleta * i)
        # print(max(data)-deleta*(fengeshu-i-1))
        for j in data:
            if i != fengeshu - 1:
                if (j >= data_min + deleta * i) and (j < data_max - deleta * (fengeshu - i - 1)):
                    sum += 1
            if i == fengeshu - 1:
                if (j >= data_min + deleta * i) and (j <= data_max - deleta * (fengeshu - i - 1)):
                    sum += 1
        x.append(str(round(data_min + deleta * i, 3)) + '-' + str(round(data_max - deleta * (fengeshu - i - 1), 3)))
        y.append(sum)
        sum = 0
    print('*******************结果*********************')
    print('x坐标', x)
    print('y坐标', y)
    print('********************************************')
    return x, y


def count_max(max, data):
    deleta = 0
    for i in data:
        if i > max:
            deleta += 1
    return deleta


def count_min(min, data):
    deleta = 0
    for i in data:
        if i < min:
            deleta += 1
    return deleta


def mkdir(path):
    # 引入模块
    import os
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print(path + '创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False


def judge_cols(banxing, start_col):
    "start_col为板型区间第一列的列索引号，从0开始"
    cols = []
    banxing = list(banxing)
    for i in banxing:
        if int(i) != 0:
            eff = 62 - banxing.index(i) * 2
            cols = range(start_col + banxing.index(i), start_col + eff + banxing.index(i))
            break
    return eff, start_col + banxing.index(i) - 1


def pie_judge(data):
    leibie = set(data)
    data_sum = len(data)
    nums = []
    for i in leibie:
        num = 0
        for j in data:
            if j == i:
                num += 1
        nums.append(num)

    return list(leibie), nums


def file_extension(path):
    import os.path
    return os.path.splitext(path)[1]


def dir_name(path):
    import os.path
    return os.path.splitext(path)[0]


def base_file_name(path):
    import os.path
    return os.path.splitext(os.path.basename(path))[0]


def walkFile(file):
    import os
    result = []
    for root, dirs, files in os.walk(file):

        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list

        # 遍历文件
        for f in files:
            result.append(os.path.join(root, f))

        # 遍历所有的文件夹
        # for d in dirs:
        #     result.append(os.path.join(root, d))
    return result


def lerangde_nihe(xishu, x):
    p1 = x
    p2 = 1.5 * pow(x, 2) - 1 / 2
    p3 = 0.5 * (5 * pow(x, 3) - 3 * x)
    p4 = (1 / 8) * (35 * pow(x, 4) - 30 * pow(x, 2) + 3)
    y = xishu[0] + xishu[1] * p1 + xishu[2] * p2 + xishu[3] * p3 + xishu[4] * p4
    return y


def lerangde_nihe2(xishu, x):
    p1 = x
    p2 = pow(x, 2)
    p3 = pow(x, 3)  # 四次拟合使用
    p4 = pow(x, 4)
    # y = xishu[0] + xishu[1] * p1 + xishu[2] * p2 # 二次拟合
    y = xishu[0] + xishu[1] * p1 + xishu[2] * p2 + xishu[3] * p3 + xishu[4] * p4  # 四次拟合
    return y


def xlsx_to_csv(path):
    import pandas as pd
    data_xls = pd.read_excel(path, header=0, index_col=0)
    data_xls.to_csv(base_file_name(path) + '.csv', index=True, encoding='utf-8')


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


def ercifenjie(y, x):
    from numpy import array
    from scipy.optimize import leastsq
    def func(x, p):
        """
        数据拟合所用的函数:p0+p1*x+p2*pow(x,2)
        """
        p0, p1, p2 = p  # 给A,k,theta赋值,其中x作为输入,
        return p0 + p1 * x + p2 * pow(x, 2)

    def residuals(p, y, x):
        """
        实验数据x, y和拟合函数之间的差，p为拟合需要找到的系数
        """
        return y - func(x, p)

    p0 = [1, 1, -1]  # 第一次猜测的函数拟合参数
    plsq = leastsq(residuals, p0, args=(y, x))

    return plsq[0]


def sicifenjie(y, x):
    from numpy import array
    from scipy.optimize import leastsq
    def func(x, p):
        """
        数据拟合所用的函数:p0+p1*x+p2*pow(x,2)
        """
        p0, p1, p2, p3, p4 = p  # 给A,k,theta赋值,其中x作为输入,
        return p0 + p1 * x + p2 * x ** 2 + p3 * x ** 3 + p4 * x ** 4

    def residuals(p, y, x):
        """
        实验数据x, y和拟合函数之间的差，p为拟合需要找到的系数
        """
        return y - func(x, p)

    p0 = [1, 1, 1, 1, 1]  # 第一次猜测的函数拟合参数
    plsq = leastsq(residuals, p0, args=(y, x))

    return plsq[0]


def setpoint_fenjie(y, x):
    from numpy import array
    from scipy.optimize import leastsq
    def func(x, p):
        """
        数据拟合所用的函数:p0+p1*x+p2*pow(x,2)
        """
        p0, p2, p4 = p  # 给A,k,theta赋值,其中x作为输入,
        return p0 + p2 * x ** 2 + p4 * x ** 4

    def residuals(p, y, x):
        """
        实验数据x, y和拟合函数之间的差，p为拟合需要找到的系数
        """
        return y - func(x, p)

    p0 = [1, 1, 1]  # 第一次猜测的函数拟合参数
    plsq = leastsq(residuals, p0, args=(y, x))

    return plsq[0]


def setpoint_nihe(xishu, x):
    p2 = x ** 2
    p4 = x ** 4
    y = xishu[0] + xishu[1] * p2 + xishu[2] * p4
    return y


def sicinihe(xishu, x):
    p1 = x
    p2 = x ** 2
    p3 = x ** 3
    p4 = x ** 4
    y = xishu[0] + xishu[1] * p1 + xishu[2] * p2 + xishu[3] * p3 + + xishu[4] * p4
    return y


def cols_in(data_df, cutin_header, header, cols_value):
    import pandas as pd
    """
    path为源文件路径
    cutin_header为插在哪一列列名称前面
    header为插入的列名
    cols_value为插入列的值，可以为list,也可以为numpy
    new_path为新文件路径
    """
    # data_df=pd.read_csv(path, header=0,index_col=False,encoding='gbk', engine='python')
    cols = list(data_df.columns).index(cutin_header)
    df1_cols = list(data_df.columns[0:cols])
    df2_cols = list(data_df.columns[cols:])
    new_data_df = pd.DataFrame(cols_value, columns=header)
    # print(new_data_df)
    data_df1 = data_df[:][df1_cols]
    data_df2 = data_df[:][df2_cols]
    frames = [data_df1, new_data_df, data_df2]
    result = pd.concat(frames, axis=1)
    # print(result)
    # result.to_csv(new_path, index=False, encoding='gbk')
    return result


def judge_percent(data):
    from collections import Counter
    import numpy as np
    lables = set(data)
    result = Counter(data)
    nums = []
    for lable in lables:
        nums.append(result[lable])
    return list(lables), np.array(nums) / len(data)


def camera():
    # 打开摄像头并灰度化显示
    import cv2
    capture = cv2.VideoCapture(0)
    i = 0
    while (True):
        # 获取一帧
        ret, frame = capture.read()
        # 将这帧转换为灰度图
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow('frame', frame)

        # time.sleep(0.1)
        if cv2.waitKey(1) == ord('t'):
            cv2.imwrite(str(i) + ".jpg", frame)  # 将拍摄内容保存为png图片
            print('已保存照片' + " " + str(i) + ".jpg")
            i += 1
        if cv2.waitKey(1) == ord('q'):
            break


def make_lables_together(label1, label2, label2_front):
    import numpy as np
    if label1.shape == label2.shape:
        labels = np.array(np.zeros(label1.shape), dtype=str)
        for l_pot in range(label1.shape[0]):
            for w_pot in range(label1.shape[1]):
                labels[l_pot, w_pot] = (str('%0.2f' % (label1[l_pot, w_pot])) + '\n' + label2_front + ':' + str(
                    int(label2[l_pot, w_pot])))
        print(labels)
    else:
        labels = []
        print('请输入相同形状数组')
    return labels


def mat_read(path):
    import pandas as pd
    from h5py import File
    mat = File(path, 'r', libver='v108')  # 原始文件
    ganngjuanhao = list(mat.keys())[0]
    print('钢卷号', ganngjuanhao)
    group = mat[ganngjuanhao]
    steel_grade = ''.join([chr(i) for i in mat[ganngjuanhao]['fileinfo']['Technostring_1steel_grade']])
    steel_en_thick = ''.join(
        [chr(i) for i in mat[ganngjuanhao]['fileinfo']['Technostring_1entry_thickness']][:-2]).replace(',', '.')
    steel_out_thick = ''.join(
        [chr(i) for i in mat[ganngjuanhao]['fileinfo']['Technostring_1exit_thickness']][:-2]).replace(',', '.')
    steel_width = ''.join([chr(i) for i in mat[ganngjuanhao]['fileinfo']['Technostring_1entry_width']][:-2])
    zuming = list((group.keys()))
    zuming.remove('fileinfo')
    # zuming.remove('Virtual')
    # print('组名', zuming)  # 组层次
    pot = 0
    for big_name in zuming:
        # print('正在浏览组名', big_name)
        group_2 = group[big_name]
        bianliangming = list(sorted(group_2.keys()))  # 变量名层次
        bianliangming.remove('moduleinfo')
        # print('变量名', bianliangming)
        for small_name in bianliangming:

            # print('正在浏览变量名', small_name)
            group_3 = group_2[small_name]  # 变量
            data = group_3['data'][0]  # 变量数据
            lenth = len(data)
            if small_name == 'THC_act_thickness_S1_exit_devi_absolute':
                small_name = 'THC_act_thickness_S1_exit'
            small_name = str(big_name) + '-' + str(small_name)
            if pot == 0:
                result = pd.DataFrame(data[4:], columns=[small_name])
                pot += 1
            else:
                # if small_name not in result.columns:
                #     result.insert(0,small_name,data[:len(result)])
                result[small_name] = data[4:4 + len(result)]
                # else:
                #     result=pd.concat([result,pd.DataFrame(data[:len(result)],columns=[small_name])],axis=1)
                pot += 1
    # return  result
    return {'data': result, 'Cold_Num': ganngjuanhao, 'steel_grade': steel_grade, 'steel_en_thick': steel_en_thick,
            'steel_out_thick': steel_out_thick, 'group': zuming, 'steel_width': steel_width}


def jugde_row_col(data):
    # pot_1=0
    # pot_2=0
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
    for row in range(50, len(data)):
        if len(set(data[row])) <= 5:
            row_pot = row - 1
            break
        else:
            row_pot = 0
    return cols_pot, 62 - cols_pot, row_pot


def chazhi_80(row):
    import numpy as np
    new_row = np.zeros(80)
    new_row[0:25] = row[0:25]
    new_row[-25:] = row[-25:]
    new_row[25] = (3 * row[24] + 4 * row[25]) / 7

    new_row[26] = (9 * row[25] + row[26]) / 10
    new_row[27] = (row[25] + row[26]) / 2
    new_row[28] = (row[25] + 9 * row[26]) / 10
    new_row[29] = (7 * row[26] + 3 * row[27]) / 10
    new_row[30] = (3 * row[26] + 7 * row[27]) / 10

    new_row[31] = (9 * row[27] + row[28]) / 10
    new_row[32] = (row[27] + row[28]) / 2
    new_row[33] = (row[27] + 9 * row[28]) / 10
    new_row[34] = (7 * row[28] + 3 * row[29]) / 10
    new_row[35] = (3 * row[28] + 7 * row[29]) / 10

    new_row[36] = (9 * row[29] + row[30]) / 10
    new_row[37] = (row[29] + row[30]) / 2
    new_row[38] = (row[29] + 9 * row[30]) / 10
    new_row[39] = (7 * row[30] + 3 * row[31]) / 10
    new_row[40] = (3 * row[30] + 7 * row[31]) / 10

    new_row[41] = (9 * row[31] + row[32]) / 10
    new_row[42] = (row[31] + row[32]) / 2
    new_row[43] = (row[31] + 9 * row[32]) / 10
    new_row[44] = (7 * row[32] + 3 * row[33]) / 10
    new_row[45] = (3 * row[32] + 7 * row[33]) / 10

    new_row[46] = (9 * row[33] + row[34]) / 10
    new_row[47] = (row[33] + row[34]) / 2
    new_row[48] = (row[33] + 9 * row[34]) / 10
    new_row[49] = (7 * row[34] + 3 * row[35]) / 10
    new_row[50] = (3 * row[34] + 7 * row[35]) / 10

    new_row[51] = (9 * row[35] + row[36]) / 10
    new_row[52] = (row[35] + row[36]) / 2
    new_row[53] = (row[35] + 9 * row[36]) / 10
    new_row[54] = (4 * row[36] + 3 * row[37]) / 7
    return new_row


def chazhi_74(row):
    import numpy as np
    new_row = np.zeros(74)
    new_row[0:25] = row[0:25]
    new_row[-25:] = row[-25:]
    new_row[25] = (row[24] + 2 * row[25]) / 3

    new_row[26] = (3 * row[25] + row[26]) / 4
    new_row[27] = (row[25] + 3 * row[26]) / 4
    new_row[28] = (3 * row[26] + row[27]) / 4
    new_row[29] = (row[26] + 3 * row[27]) / 4

    new_row[30] = (3 * row[27] + row[28]) / 4
    new_row[31] = (row[27] + 3 * row[28]) / 4
    new_row[32] = (3 * row[28] + row[29]) / 4
    new_row[33] = (row[28] + 3 * row[29]) / 4

    new_row[34] = (3 * row[29] + row[30]) / 4
    new_row[35] = (row[29] + 3 * row[30]) / 4
    new_row[36] = (3 * row[30] + row[31]) / 4
    new_row[37] = (row[30] + 3 * row[31]) / 4

    new_row[38] = (3 * row[31] + row[32]) / 4
    new_row[39] = (row[31] + 3 * row[32]) / 4
    new_row[40] = (3 * row[32] + row[33]) / 4
    new_row[41] = (row[32] + 3 * row[33]) / 4

    new_row[42] = (3 * row[33] + row[34]) / 4
    new_row[43] = (row[33] + 3 * row[34]) / 4
    new_row[44] = (3 * row[34] + row[35]) / 4
    new_row[45] = (row[34] + 3 * row[35]) / 4

    new_row[46] = (3 * row[35] + row[36]) / 4
    new_row[47] = (row[35] + 3 * row[36]) / 4
    new_row[48] = (2 * row[36] + row[37]) / 3

    return new_row


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


# new_row,before_pot,after_pot=free_chazhi([1,0,0,1,0,0,1,2,5,2,0,1,0,2,4,6,4,1,0,1,3,4,6,3,2,0,2,1,0,0])
# import matplotlib.pyplot as plt
# # print(np.arange(1,81))
# plt.figure()
# plt.plot(before_pot,[1,0,0,1,2,5,2,0,1,0,2,4,6,4,1,0,1,3,4,6,3,2,0,2],'b-o')
# plt.plot(after_pot,new_row,'r-o')
# plt.show()

def sigema(ai, bi):
    result = []
    for i in range(len(ai)):
        result.append(ai[i] * bi[i])
    return result


def sigemas(ai, bi):
    result = []
    for i in range(len(ai)):
        result.append(ai[i] * bi[i])
    return result


def get_setpoint(guige):
    """guige格式为[代表后道产线，内部牌号，入口厚度，出口厚度，出口宽度]"""
    import pandas as pd
    data = pd.read_excel(r'C:\Users\wufaxianshi\Desktop\二级目标设定\内部牌号对应其强度分级.xls', header=0, usecols=[0, 1, 3])
    data = data[data['KEYTYPE'] == 'KOS']
    # print(data)
    num = [0, 0, 1, 0, 0]
    chanxian = {'迁顺连退': 1, '迁顺1#镀锌': 2, '迁顺2#镀锌': 3, '9A': 4, '9B': 5}
    num[0] = chanxian[guige[0]]
    if guige[3] >= 0.2 and guige[3] < 0.6:
        num[3] = 1
    elif guige[3] >= 0.6 and guige[3] < 1.2:
        num[3] = 2
    elif guige[3] >= 1.2 and guige[3] <= 5:
        num[3] = 3
    if guige[4] >= 700 and guige[4] < 1200:
        num[4] = 1
    elif guige[4] >= 1200 and guige[4] < 1500:
        num[4] = 2
    elif guige[4] >= 1500 and guige[4] <= 2801:
        num[4] = 3
    num[1] = data[data['KEYNAME'] == guige[1]].values[0, 2]
    return num[0] * 10000 + num[1] * 1000 + num[2] * 100 + num[3] * 10 + num[4]


def cal_thick(list, in_thick, exit_thick):
    result = []
    s12 = round(in_thick * (100 - list[0]) / 100, 3)
    s23 = round(s12 * (100 - list[1]) / 100, 3)
    s34 = round(s23 * (100 - list[2]) / 100, 3)
    s45 = round(s34 * (100 - list[3]) / 100, 3)
    s5 = round(s45 * (100 - list[4]) / 100, 3)
    result.append(in_thick)
    result.append(s12)
    result.append(s23)
    result.append(s34)
    result.append(s45)
    result.append(s5)
    return result
    # s23 = s12(100 - list[1]) / 100


def drop_dig(data):
    names = data.columns[:-63]
    for name in names:
        # print(set(data[name].values))
        set_value = set(data[name].values)
        if set_value == {0.0} or set_value == {1.0} or \
                set_value == {0.0, 1.0} or set_value == {1.0, 0.0}:
            data = data.drop([name], axis=1)
    return data


def get_files(dir_path, last_name):
    import glob, os
    return glob.glob(os.path.join(dir_path, last_name))


def make_df_todether(dir_path):
    import glob, os
    import pandas as pd
    pathes = glob.glob(os.path.join(dir_path, "*.csv"))
    # [start:end]
    print(pathes)
    for i in range(len(pathes)):
        data = pd.read_csv(pathes[i], header=0, low_memory=False, encoding='gbk')
        # data.drop(columns=['RCH_3-RCH3_Wedge_adj_OS_actual_pos'])
        # data=data[data['FLC5-F5_strip_length']>=50]
        if i == 0:
            result = data
        else:
            frames = [result, data]
            result = pd.concat(frames, axis=0)
    return result


def read_dat_col(path, name_target):
    from win32com import client
    from time import perf_counter
    import numpy as np
    import pandas as pd
    file = client.DispatchEx('{089CC1F3-E635-490B-86F8-7731A185DFD9}')  # 获取C#类
    Module_names = dict()  # 变量组名（字典dict）
    with open(path, 'rb') as f:
        for i in range(100):
            Module_name = str(f.readline())
            if 'Module_name_' in Module_name:
                key, value = Module_name[14:-5].split(':')
                Module_names[key] = value
    # print(Module_names)

    iba_data = pd.DataFrame()
    file.Open(path)  # 打开文件
    i = file.GetVersion()  # 获取iba版本
    iecr = file.EnumChannels()  # 获取组名
    icr = iecr.Next()  # 枚举频道

    # i = str(0)
    # info = str(0)
    # print(icr.IsInfoPresent(0))
    # print(icr.QueryInfoByIndex(1, i, info))
    # print(icr.QueryInfoByIndex(2, i, info))
    # print(icr.QueryInfoByIndex(3, i, info))

    bianliang_num = 0

    while (1):
        bianliang_num += 1
        if (icr != None):

            ChannelId = str(int(icr.QueryChannelId()))  # 频道ID
            name = icr.QueryInfoByName('name')
            if name != '':  # 判断变量名是否为空
                if name[0] == ' ':  # 去除变量组第一个变量前的空格
                    name = name[1:]
            else:
                name = str(icr.ModuleNumber) + ':' + str(icr.NumberInModule)  # 如果变量名为空，使用组号加变量号
            base = icr.QueryInfoByName('$PDA_Tbase')  # 获取当前频道的采样率，返回字符串
            if name in name_target:
                xbase = float(0)  # 获取当前频道的采样率，float
                xOffset = float(0)  # 获取当前频道的滞后时间，float
                data = object  # 获取当前频道的数据，返回touple

                if (icr.IsDefaultTimebased() == 1):  # 若是时间基础的数据

                    xbase, xOffset, data = icr.QueryTimebasedData(xbase, xOffset, data)
                else:
                    xbase, xOffset, data = icr.QueryLengthbasedData(xbase, xOffset, data)

                # print(type(xbase),type(xOffset))
                # print('{:.3f}'.format(xOffset),type(xOffset))
                if base == '0.008':

                    if (icr.IsAnalog() == 1):  # 判断是否是模拟量数据
                        new_data = np.array(data, dtype='float32')
                    else:
                        new_data = np.array(data, dtype='int8')

                    if name not in iba_data.columns:  # 如果变量名不在iba_data中
                        iba_data[name] = new_data
                    else:
                        iba_data.insert(iba_data.shape[1], name, new_data, allow_duplicates=True)
                else:

                    if (icr.IsAnalog() == 1):
                        data = np.array(data, dtype='float32')
                    else:
                        data = np.array(data, dtype='int8')
                    if '{:.3f}'.format(xOffset) != '0.000':  # 判断是否有滞后
                        start_pot = int(xOffset / 0.008)
                        end_pot = (int(float(base) / 0.008)) - start_pot

                        if (icr.IsAnalog() == 1):
                            new_data = np.array([None])
                            for i in range(start_pot - 1):
                                new_data = np.append(new_data, None)
                        else:
                            new_data = np.array([1])
                            for i in range(start_pot - 1):
                                new_data = np.append(new_data, 1)

                        new_data = np.append(new_data, np.repeat(data, (int(float(base) / 0.008)), axis=0)[:-start_pot])


                    else:
                        new_data = np.repeat(data, (int(float(base) / 0.008)), axis=0)

                    if name not in iba_data.columns:
                        iba_data[name] = new_data
                    else:
                        iba_data.insert(iba_data.shape[1], name, new_data, allow_duplicates=True)

                del data

            icr = iecr.Next()

        else:
            break

    file.Close()
    return iba_data


def flat_sampling(data, name):
    length = data.shape[0]
    flat = data[name].values
    need_index = []
    # print(flat)
    pot = 0
    for i in range(length):

        pot2 = flat[i]
        # print(i)
        if pot2 != pot:
            need_index.append(i)
            pot = pot2
    return data.iloc[need_index]


def plot_3dflat(data):
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    import numpy as np
    fig = plt.figure(figsize=(8, 4.5), dpi=200)
    ax = Axes3D(fig)
    ax.get_proj = lambda: np.dot(Axes3D.get_proj(ax), np.diag([0.7, 1.5, 1, 1]))
    Y = range(len(data))
    X = np.linspace(-1, 1, 80)
    X, Y = np.meshgrid(X, Y)
    # R = np.sqrt(X**2 + Y**2)
    Z = data
    # 具体函数方法可用 help(function) 查看，如：help(ax.plot_surface)
    a = ax.plot_surface(X, Y, Z, rstride=10, cstride=4, cmap='rainbow', vmin=-10, vmax=8, )
    # plt.colorbar(a,fig.add_axes([0.94,0.4,0.04,0.5]))
    plt.rcParams['font.sans-serif'] = ['FangSong']
    plt.rcParams['axes.unicode_minus'] = False
    position = fig.add_axes([0.14, 0.4, 0.02, 0.5])  # 位置[左,下,右,上]
    cb = plt.colorbar(a, cax=position)
    ax.set_xlabel('OS        归一化板宽        DS', fontsize=11)
    ax.set_ylabel('采样点', fontsize=11)
    ax.set_zlabel('板形偏差（IU）', fontsize=11)
    # plt.savefig(r"F:\首钢顺义冷连轧机板形大数据分析与挖掘利用\数据集\中浪\\"+base_file_name(path)+'.png')
    # plt.close()
    plt.show()


def pro_control(flat, setpoint):
    w1 = 0.6
    w3 = 0.4
    w2 = 0.6
    w4 = 0.4
    x = np.linspace(-1, 1, 52)
    xishu = lerangde_fenjie(flat - setpoint, x)
    cancha = flat - lerangde_nihe(xishu, x)
    tilt = 1 * (w1 * xishu[1] * Tilt_deleta[0] + w3 * xishu[3] * Tilt_deleta[1]) / (
            w1 * Tilt_deleta[0] ** 2 + w3 * Tilt_deleta[1] ** 2)
    xishu[1] -= tilt * Tilt_deleta[0]
    xishu[3] -= tilt * Tilt_deleta[1]
    WRB = 1 * (w2 * xishu[2] * WRB_deleta[0] + w4 * xishu[4] * WRB_deleta[1]) / (
            w2 * WRB_deleta[0] ** 2 + w4 * WRB_deleta[1] ** 2)
    xishu[2] -= WRB * WRB_deleta[0]
    xishu[4] -= WRB * WRB_deleta[1]
    IRB = 1 * (w2 * xishu[2] * IRB_deleta[0] + w4 * xishu[4] * IRB_deleta[1]) / \
          (w2 * IRB_deleta[0] ** 2 + w4 * IRB_deleta[1] ** 2)
    xishu[2] -= IRB * IRB_deleta[0]
    xishu[4] -= IRB * IRB_deleta[1]
    new_row = cancha + lerangde_nihe(xishu, x)
    return [tilt, WRB, IRB], new_row


def pro_control_op(flat, setpoint):
    w1 = 0.6
    w3 = 0.4
    w2 = 0.6
    w4 = 0.4
    x = np.linspace(-1, 1, 52)
    xishu = lerangde_fenjie(flat - setpoint, x)
    cancha = flat - lerangde_nihe(xishu, x)
    tilt = 1 * (w1 * xishu[1] * Tilt_deleta[0] + w3 * xishu[3] * Tilt_deleta[1]) / (
            w1 * Tilt_deleta[0] ** 2 + w3 * Tilt_deleta[1] ** 2)
    xishu[1] -= tilt * Tilt_deleta[0]
    xishu[3] -= tilt * Tilt_deleta[1]
    eff_A = np.array([WRB_deleta, IRB_deleta])
    [WRB, IRB] = np.dot([xishu[2], xishu[4]], np.linalg.inv(eff_A))
    xishu[2] -= WRB * WRB_deleta[0]
    xishu[4] -= WRB * WRB_deleta[1]
    xishu[2] -= IRB * IRB_deleta[0]
    xishu[4] -= IRB * IRB_deleta[1]
    new_row = cancha + lerangde_nihe(xishu, x)
    return [tilt, WRB, IRB], new_row


def fenge_x(data, min_linspace):
    min_value = min_linspace * int((min(data) // min_linspace))
    if int((min(data) // min_linspace) - 1) == 0:
        min_value = 0
    max_value = min_linspace * int((max(data) // min_linspace) + 1)
    print(min_value, max_value)
# print(fenge_x([0.16,1],0.05))
# import numpy
# # print(np.arange(0.15,1.05,0.05,dtype='int16'))
# a=dict()
# for i in np.arange(0.15,1.05,0.05):
#     a[i]=[]
# print(a)
