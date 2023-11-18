import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
from my_utils.zhhj_file import *

# from my_utils.zhhj_data


data = pd.read_csv('./data/合并.csv')
# 将'停机时间列'由大到小排序
data = data.sort_values(by='停机时间(分钟)', ascending=False)


# ic(data)

# 定义函数绘制机组停机时间密度估计图
def plot_stop_time(_data):
    # 设置绘图风格
    plt.style.use('ggplot')
    # 设置中文显示
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # 绘制机组停机时间密度估计图
    plt.figure(figsize=(10, 8))
    sns.kdeplot(data=_data, shade=True, color='steelblue')
    plt.xlabel('停机时间(分钟)')
    plt.title('机组停机时间密度估计图')
    plt.show()


#  定义函数绘制机组停机时间箱线图
def plot_stop_time_box(_data):
    # 设置绘图风格
    plt.style.use('ggplot')
    # 设置中文显示
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # 绘制机组停机时间箱线图, 中位数颜色为红色
    plt.figure(figsize=(10, 8))
    sns.boxplot(x=_data, color='steelblue', medianprops={'color': 'red'})
    plt.xlabel('停机时间(分钟)')
    plt.title('机组停机时间箱线图')
    plt.show()


if __name__ == '__main__':
    plot_stop_time(data['停机时间(分钟)'])
    # plot_stop_time_box(data['停机时间(分钟)'])
    # path = r'./data/raw'
    # print(os.listdir(path))
