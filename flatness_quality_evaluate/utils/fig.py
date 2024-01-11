import os

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.ticker import FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D

from .draw_pic import set_plot, bili_to_jiaodu


def threedbanxing(fig, flat_3D):
    fig.clear()
    set_plot()
    data = np.array(flat_3D)
    # self.fig = plt.figure(figsize=(6, 4), dpi=200)
    ax = fig.add_subplot(111, projection='3d')
    ax.get_proj = lambda: np.dot(Axes3D.get_proj(ax), np.diag([0.9, 1.42, 1, 1]))
    Y = range(len(data))
    X = np.linspace(-1, 1, 80)
    X, Y = np.meshgrid(X, Y)
    # R = np.sqrt(X**2 + Y**2)
    Z = data
    print(X.shape, Y.shape, Z.shape)
    # 具体函数方法可用 help(function) 查看，如：help(ax.plot_surface)
    a = ax.plot_surface(X, Y, Z, rstride=5, cstride=2, cmap='rainbow', vmin=-10, vmax=10)
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.0f'))

    position = fig.add_axes([0.14, 0.4, 0.02, 0.5])  # 位置[左,下,右,上]
    cb = plt.colorbar(a, cax=position)
    ax.set_xlabel('OS        归一化板宽        DS', fontsize=11)
    ax.set_ylabel('采样点', fontsize=11)
    ax.set_zlabel('板形偏差（IU）', fontsize=11)
    ax.view_init(18, -76)
    # plt.savefig(r'C:\Users\wufaxianshi\Desktop\temp\\'+name+'.svg',dpi=500)
    # plt.close()
    # self.fig.tight_layout()
    # plt.show()
    # self.draw()


def redutu(fig, X, Y, flat_3D):
    print(X.shape, Y.shape, np.array(flat_3D).shape)
    # fig = plt.figure(figsize=(8, 2), dpi=200)
    # set_plot()
    # plt.plot(x, flaterrors, 'b-', label='Flatness error', linewidth=0.5)
    # plt.xlabel('r4/r2')
    # plt.ylabel('绝对值板形偏差（IU）')
    # plt.legend()
    # plt.tight_layout()
    # plt.savefig(r'C:\Users\wufaxianshi\Desktop\首钢非机理建模结果\板形偏差与热度图对比\\' + base_file_name(path) + 'flat_error.png')
    # plt.show()

    # self.fig = self.plt.figure(figsize=(8, 4), dpi=200)
    fig.clear()
    set_plot()
    ax = fig.add_subplot(1, 1, 1)
    c = ax.pcolormesh(X, Y, np.array(flat_3D).T, cmap='rainbow', vmin=-10, vmax=10)
    cb = fig.colorbar(c)
    cb.set_label('IU', fontsize=10)
    ax.set_xlabel('采样点', fontsize=10)
    ax.set_ylabel('OS           归一化板宽           DS', fontsize=10)
    # self.fig.tight_layout()
    # plt.savefig(r'C:\Users\wufaxianshi\Desktop\首钢非机理建模结果\板形偏差与热度图对比\\'+ base_file_name(path)+'热度图.png' )
    # plt.close()
    # self.plt.show()
    # self.draw()


def langxingmotai(fig, jiaodu1, iu1, jiaodu2, iu2, colors, mode):
    matplotlib.rcParams.update({'font.size': 14})
    # 画IU在图上.
    # self.plt.figure(figsize=(6, 4), dpi=200)
    fig.clear()

    fig.subplots_adjust(top=0.95,
                        bottom=0.045,
                        left=0.07,
                        right=0.91,
                        hspace=0.315,
                        wspace=0.7)

    set_plot()
    axprops = dict(xticks=[], yticks=[])
    ax0 = fig.add_axes([0, 0, 1, 1], label='ax0', **axprops)
    print('浪x模态图')

    cwd = os.path.abspath(__file__)  # 获取当前程序文件位置
    tmp = os.path.dirname(cwd)  # 获取当前程序文件位置的目录
    # path = cwd.replace('\\', '/') + '/背景2.jpg'
    path = f'{tmp}/背景2.jpg'

    print(path)
    imgP = plt.imread(path)

    # imgP = plt.imread(r'C:\Users\wlp\Desktop\程序\界面\界面_总\picture\背景1.jpg')

    ax0.imshow(imgP)  # 背景图片
    ax = fig.add_subplot(1, 2, 1, projection='polar')

    # self.ax = self.plt.gca(projection='polar')
    # 模态图上的几个分界处和极小值处
    # 0度,0.4,1.5,90度,-1,-0.3,180度,0.4,1.5,270度,-1,-0.3,360度

    # e = [0.0, bili_to_jiaodu(0.4)[0], bili_to_jiaodu(1.5)[0], 90, bili_to_jiaodu(-1)[1], bili_to_jiaodu(-0.3)[1],
    #      180, bili_to_jiaodu(0.4)[1], bili_to_jiaodu(1.5)[1], 270, bili_to_jiaodu(-1)[2], bili_to_jiaodu(-0.3)[2]]
    # labels = np.array(['0', '0.4', '1.5极小值处', '+∞', '-1', '-0.3', '0', '0.4', '1.5极小值处', '-∞', '-1', '-0.3'])
    # # labels = np.array([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])

    e = [0.0, bili_to_jiaodu(0.4)[0], bili_to_jiaodu(4 / 3)[0], 90, bili_to_jiaodu(-2.4)[1], bili_to_jiaodu(-1)[1],
         bili_to_jiaodu(-0.3)[1],
         180, bili_to_jiaodu(0.4)[1], bili_to_jiaodu(4 / 3)[1], 270, bili_to_jiaodu(-2.4)[2], bili_to_jiaodu(-1)[2],
         bili_to_jiaodu(-0.3)[2]
         ]

    # labels = np.array(['0', '0.4', '+∞', '-1', '-0.3', '0', '0.4', '-∞', '-1', '-0.3'])
    labels = np.array(
        ['0', '0.4', '1.33', '+∞', '-2.4', '-1', '-0.3', '0', '0.4', '1.33', '-∞', '-2.4', '-1', '-0.3'])

    ax.set_thetagrids(e, labels)
    ax.set_rlabel_position(45)

    c = ax.scatter(jiaodu1, iu1, color=colors, s=3)
    # max_r = max(iu1)
    # min_r = min(iu1)
    # max_r = 6
    # self.ax.set_title('对称项', fontsize=10)
    title1 = '对称项 均方根IU'
    title2 = '非对称项 均方根IU'
    if mode == 1 or mode == 2:
        ax.set_rgrids((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), ('0', '', '', '', '', '5', '', '', '', '', '10'))
        # self.ax.set_title(90, 18, title1, fontsize=12)
        max_r = 10
    else:
        ax.set_rgrids((0, 10, 20, 30, 40), ('0', '', '20', '', '40'))
        # self.plt.text(90, 65, title1, fontsize=12)
        max_r = 40
    ax.set_rlim(0, max_r)

    ax1 = fig.add_subplot(1, 2, 2, projection='polar')
    # self.plt.figure(figsize=(6, 4), dpi=200)
    # set_plot()
    # self.ax1 = self.plt.gca(projection='polar')

    e = [0.0, bili_to_jiaodu(0.67)[0], 90, bili_to_jiaodu(-1)[1], bili_to_jiaodu(-0.17)[1],
         180, bili_to_jiaodu(0.67)[1], 270, bili_to_jiaodu(-1)[2], bili_to_jiaodu(-0.17)[2]]
    labels = np.array(['0', '0.67', '+∞', '-1', '-0.17', '0', '0.67', '-∞', '-1', '-0.17'])
    # labels = np.array([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])

    ax1.set_thetagrids(e, labels)
    ax1.set_rlabel_position(45)
    # self.ax1.set_xticks([])
    # self.ax1.set_yticks([])

    # self.ax1.yaxis.set_ticks_position('left')
    c = ax1.scatter(jiaodu2, iu2, color=colors, s=3)
    # ax.set_xticklabels(['0', '1', '无穷大', '-1', '0', '1', '无穷大', '-1'], fontsize=8)

    # self.ax1.set_rlim(0, max_r)
    if mode == 1 or mode == 2:
        max_r = 10
        ax1.set_rgrids((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), ('0', '', '', '', '', '5', '', '', '', '', '10'))
        # self.plt.text(90, 18, title2, fontsize=12)
    else:
        max_r = 40
        # self.plt.text(90, 65, title2, fontsize=12)
        ax1.set_rgrids((0, 10, 20, 30, 40), ('0', '', '20', '', '40'))
    # self.plt.tick_params(labelsize=10)
    ax1.set_rlim(0, max_r)
    # self.ax1.set_title('非对称项', fontsize=10)
    # plt.savefig(save_path+'%s\\' %b[0]+'奇数项', bbox_inches='tight')
    # plt.show()
    # plt.savefig(save_path + '非对称项.jpg', bbox_inches='tight')
    # plt.savefig(save_path + '非对称项.jpg')
    return


def langxingfenbu(fig, que, num):
    labels = ['左边浪', '右边浪', '左三分浪', '右三分浪', '双边浪', '中浪', '四分浪', '边中浪', '无']
    explode = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    colors = ['red', 'yellowgreen', 'blue', '#C1FFC1', 'purple', 'peachpuff', 'lightpink', 'coral', 'lightskyblue']
    fig.clear()
    set_plot()
    fig.subplots_adjust(top=0.885, bottom=0.11, left=0.11, right=0.69, hspace=0.24, wspace=0.2)
    ax1 = fig.add_subplot(1, 1, 1)
    ax, texts = ax1.pie(x=que, explode=explode, startangle=90, colors=colors)
    ax1.legend(ax, labels=['%s,%1.1f %%' % (l, s) for l, s in zip(labels, que)], fontsize=10, title="浪形",
               loc="center left", bbox_to_anchor=(0.91, 0, 0.3, 1))
    #             plt.legend([labels,colors],loc='upper right')
    ax1.set_title('全年数据的浪形分布%d卷' % num, loc='right')


def langxingfenbu1(fig, que):
    labels = ['无', '右边浪', '双边浪', '左三分浪', '边中浪', '左边浪', '中浪', '右三分浪', '四分浪']
    explode = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    colors = ['lightskyblue', 'yellowgreen', 'purple', 'blue', 'coral', 'red', 'peachpuff', '#C1FFC1', 'lightpink']
    fig.clear()
    set_plot()
    fig.subplots_adjust(top=0.885, bottom=0.11, left=0.11, right=0.69, hspace=0.24, wspace=0.2)
    ax1 = fig.add_subplot(1, 1, 1)
    ax, texts = ax1.pie(x=que, explode=explode, startangle=90, colors=colors)
    ax1.legend(ax, labels=['%s,%1.1f %%' % (l, s) for l, s in zip(labels, que)], fontsize=10, title="浪形",
               loc="center left", bbox_to_anchor=(0.91, 0, 0.3, 1))


def langxingfenbu2(fig, que):
    labels = ['无', '右边浪', '双边浪', '左三分浪', '边中浪', '左边浪', '中浪', '右三分浪', '四分浪', '多模态复杂浪形',
              '高次复杂浪形', '双模态主导浪形']
    explode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    colors = ['lightskyblue', 'yellowgreen', 'purple', 'blue', 'coral', 'red', 'peachpuff', '#C1FFC1', 'lightpink',
              'Violet', 'DeepPink', 'MediumBlue']
    fig.clear()
    set_plot()
    fig.subplots_adjust(top=0.885, bottom=0.11, left=0.11, right=0.69, hspace=0.24, wspace=0.2)
    ax1 = fig.add_subplot(1, 1, 1)
    ax, texts = ax1.pie(x=que, explode=explode, startangle=90, colors=colors)
    ax1.legend(ax, labels=['%s,%1.1f %%' % (l, s) for l, s in zip(labels, que)], fontsize=10, title="浪形",
               loc="center left", bbox_to_anchor=(0.91, 0, 0.3, 1))


def IUfenbu(fig, que):
    labels = ['0-1IU', '1-2IU', '2-3IU', '3-4IU', '4-5IU', '5-6IU', '6IU以上']
    explode = [0, 0, 0, 0, 0, 0, 0]
    colors = ['lightskyblue', 'coral', 'blue', 'lightpink', 'purple', 'peachpuff', '#C1FFC1']
    fig.clear()
    set_plot()
    fig.subplots_adjust(top=0.963, bottom=0.088, left=0.0, right=0.507, hspace=0.24, wspace=0.2)
    ax1 = fig.add_subplot(1, 1, 1)

    ax, texts = ax1.pie(x=que, explode=explode, startangle=90, colors=colors)
    ax1.legend(ax, labels=['%s,%1.1f %%' % (l, s) for l, s in zip(labels, que)], fontsize=10, title="IU比例",
               loc="center left", bbox_to_anchor=(0.91, 0, 0.3, 1))


def IUfenbu1(fig, que):
    labels = ['0-1IU', '1-2IU', '2-3IU', '3-4IU', '4-5IU', '5-6IU', '6IU以上']
    explode = [0, 0, 0, 0, 0, 0, 0]
    colors = ['lightskyblue', 'coral', 'blue', 'lightpink', 'purple', 'peachpuff', '#C1FFC1']
    fig.clear()
    set_plot()
    fig.subplots_adjust(top=0.885, bottom=0.11, left=0.11, right=0.69, hspace=0.24, wspace=0.2)
    ax1 = fig.add_subplot(1, 1, 1)

    ax, texts = ax1.pie(x=que, explode=explode, startangle=90, colors=colors)
    ax1.legend(ax, labels=['%s,%1.1f %%' % (l, s) for l, s in zip(labels, que)], fontsize=10, title="IU比例",
               loc="center left", bbox_to_anchor=(0.91, 0, 0.3, 1))


def Gailvmidutu(fig, data):
    # print(data)
    fig.clear()
    set_plot()
    # self.fig.subplots_adjust(top=0.885, bottom=0.11, left=0.11, right=0.69, hspace=0.24, wspace=0.2)
    axprops = dict(xticks=[], yticks=[])
    ax0 = fig.add_axes([0, 0, 1, 1], label='ax0', **axprops)

    sns.kdeplot(data, fill=True, color='b')
    plt.title('IU值概率密度图')
    cwd = os.getcwd()  # 获取当前程序文件位置
    path1 = cwd.replace('\\', '/') + '/IU概率密度图.png'
    plt.savefig(path1)
    plt.close()
    imgP = plt.imread(path1)
    ax0.imshow(imgP)
    return path1

    # plt.show()


def zhexiantu(fig, iu_mean, iu_max, iu_rms, iu_max_min):
    fig.clear()
    set_plot()
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.plot(iu_mean)
    ax1.plot(iu_max)
    ax1.plot(iu_rms)
    ax1.plot(iu_max_min)
    ax1.legend(['IU绝对值均值', 'IU绝对值最大值', 'IU均方根', 'IU最大-最小'])
