import pandas as pd
import numpy as np
from flatness.Wlearn import lerangde_fenjie,lerangde_nihe,jugde_row_col,free_chazhi
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import math
import os
import glob
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from urllib import request
from mpl_toolkits.mplot3d import Axes3D


def set_plot():
    plt.rcParams['xtick.direction'] = 'in'  # 将x周的刻度线方向设置向内
    plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内
    # plt.rcParams['font.sans-serif'] = ['Times new roman']
    config = {
        "font.family": 'serif',
        "font.size": 10,
        "mathtext.fontset": 'stix',
        "font.serif": ['SimSun'],
    }
    plt.rcParams.update(config)
    plt.rcParams['axes.unicode_minus'] = False
    bwith = 0.5  # 边框宽度设置为2
    ax = plt.gca()  # 获取边框
    ax.spines['bottom'].set_linewidth(bwith)
    ax.spines['left'].set_linewidth(bwith)
    ax.spines['top'].set_linewidth(bwith)
    ax.spines['right'].set_linewidth(bwith)
    plt.xticks(fontfamily="Times New Roman", fontsize=12)
    plt.yticks(fontfamily="Times New Roman", fontsize=12)

def plot_3dflat(data):
    from matplotlib.ticker import LinearLocator, FormatStrFormatter
    fig = plt.figure(figsize=(6,4), dpi=200)
    ax = Axes3D(fig)
    ax.get_proj = lambda: np.dot(Axes3D.get_proj(ax), np.diag([0.9, 1.7, 1, 1]))
    Y = range(len(data))
    X = np.linspace(-1, 1, 80)
    X, Y = np.meshgrid(X, Y)
    # R = np.sqrt(X**2 + Y**2)
    Z = data
    print(X.shape, Y.shape, Z.shape)
    # 具体函数方法可用 help(function) 查看，如：help(ax.plot_surface)
    a = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='rainbow', vmin=-10, vmax=10)
    # a = ax.plot_surface(X, Y, Z, rcount=10000, ccount=10000, cmap='rainbow', vmin=-10, vmax=10)
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    # plt.colorbar(a,fig.add_axes([0.94,0.4,0.04,0.5]))
    plt.rcParams['font.sans-serif'] = ['FangSong']
    plt.rcParams['axes.unicode_minus'] = False
    position = fig.add_axes([0.14, 0.4, 0.02, 0.5])  # 位置[左,下,右,上]
    cb = plt.colorbar(a, cax=position)
    ax.set_xlabel('OS        归一化板宽        DS', fontsize=11)
    ax.set_ylabel('采样点',fontsize=11)
    ax.set_zlabel('板形偏差（IU）', fontsize=11)
    ax.view_init(18, -76)
    # plt.savefig(r'C:\Users\wufaxianshi\Desktop\temp\\'+name+'.svg',dpi=500)
    # plt.close()
    fig.tight_layout()
    # plt.show()
def file_name(file_dir):
  for root, dirs, files in os.walk(file_dir):
      return root, dirs, files
def iu_error(before):
    """计算板形偏差"""
    setpoint=np.zeros(len(before))
    return np.mean(abs(before-setpoint-np.mean(before-setpoint)))

if __name__ == '__main__':
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # dir_path = r'F:\转移\原始板形数据\spcc'
    # dir_path = r'D:\刘帅\u盘\转移\原始板形数据\spcc'  # 台式机上
    dir_path = r'D:\刘帅\u盘\转移\原始板形数据\780980'  # 台式机上

    pathes = glob.glob(os.path.join(dir_path, "*.csv"))
    # print(len(pathes))
    for i in range(len(pathes)):
        data = pd.read_csv(pathes[i], header=0, encoding='gbk')

        flat = data.values[:, 1:]/-2100000
        width = np.linspace(-1, 1, 80)
        flat = data.values[:, 1:] / -2100000
        pot1, pot2, row_pot = jugde_row_col(flat)
        length = list(range(0, row_pot))
        X, Y = np.meshgrid(width, length)
        useflat = flat[:row_pot, pot1:pot2]
        flat_3D = []
        for j in range(row_pot):
            new_row = free_chazhi(useflat[j])[0]
            flat_3D.append(new_row)
        plot_3dflat(np.array(flat_3D))

        plt.show()


        a = file_name(dir_path)
        b = os.path.splitext(a[2][i])
        # save_path = r'F:\转移\画IU比例图\\%s\\' % b[0]
        # save_path = r'D:\刘帅\u盘\转移\画IU比例图\\%s\\' % b[0]
        save_path = r'D:\刘帅\u盘\转移\画IU比例图2\\%s\\' % b[0]

        if not os.path.exists(save_path):
            os.makedirs(save_path)
        # plt.savefig(save_path + '三维板形图.jpg', dpi=200, bbox_inches='tight')
        plt.close()