import matplotlib

matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
import math
import numpy as np
import matplotlib as mpl


# 重写一个matplotlib图像绘制类
class MyFigure(FigureCanvas):
    """FigureCanvas的最终的父类其实是QWidget。"""

    def __init__(self, parent=None, width=15, height=7.5, dpi=80):
        # 配置中文显示
        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        plt.rcParams["toolbar"] = "toolbar2"

        self.fig = Figure(figsize=(width, height), dpi=dpi)  # 新建一个figure

        # self.axes = self.fig.add_subplot(111)  # 建立一个子图，如果要建立复合图，可以在这里修改
        self.canvas = FigureCanvas(self.fig)
        # self.axes.hold(False)  # 每次绘图的时候不保留上一次绘图的结果
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        self.resize(width, height)
        '''定义FigureCanvas的尺寸策略，这部分的意思是设置FigureCanvas，使之尽可能的向外填充空间。'''
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        # Adjust layout to fill the entire canvas
        self.fig.tight_layout()

    '''绘制静态图，可以在这里定义自己的绘图逻辑'''

    def visualization2(self, mse_loss, threshold):
        self.fig.subplots_adjust(left=0.12, right=0.92, bottom=0.1, top=0.92, hspace=0.8)
        self.axes1 = self.fig.add_subplot(111)
        self.axes1.plot(mse_loss, color='steelblue')
        self.axes1.set_title('板形IU异常判别图')  # , size=15)
        self.axes1.set_ylabel('IU')  # , size=13)
        self.axes1.set_xlabel('样本点')
        self.axes1.legend(labels=['IU'], loc='upper left')
        self.axes2 = self.axes1.twinx()
        self.axes2.get_shared_y_axes().join(self.axes1, self.axes2)
        self.axes2.spines['right'].set_visible(False)
        self.axes2.yaxis.set_visible(False)
        self.axes2.plot(range(len(mse_loss)), [threshold] * len(mse_loss), "r--", color='lightcoral')
        self.axes2.legend(labels=['IU阈值'], loc='upper right')

        # plt.title(name)
        # self.axes2.set_xlabel('样本点')
        # plt.ylabel('IU统计值')
        # plt.legend()

    def visualization4(self, T2, S2, T2_threshold, S2_threshold, name='PCA监测图'):
        self.fig.subplots_adjust(left=0.12, right=0.92, bottom=0.1, top=0.92, hspace=0.8)
        self.axes1 = self.fig.add_subplot(211)

        self.axes1.plot(range(len(T2)), [T2_threshold] * len(T2), "r--", color='lightcoral')
        self.axes1.set_title(name)  # , size=15)
        self.axes1.set_ylabel('$T^2$统计量')  # , size=13)
        self.axes1.legend(labels=['$T^2$统计量限值'], loc='upper left')
        # self.axes1.legend(labels=['$T^2$统计量限值', '$T^2$统计量值'], loc=0)
        self.axes2 = self.axes1.twinx()
        self.axes2.get_shared_y_axes().join(self.axes1, self.axes2)
        self.axes2.spines['right'].set_visible(False)
        self.axes2.yaxis.set_visible(False)

        # self.axes2 = self.fig.add_subplot(212, sharey=self.axes1)
        self.axes2.plot(T2, color='steelblue')
        self.axes2.legend(labels=['$T^2$统计量值'], loc='upper right')
        self.axes2.set_xlabel('样本点')

        self.axes3 = self.fig.add_subplot(212)
        self.axes3.plot(range(len(S2)), [S2_threshold] * len(S2), "r--", color='lightcoral')
        self.axes3.set_ylabel('$SPE$统计量')  # , size=13)
        self.axes3.legend(labels=['$SPE$统计量限值'], loc='upper left')
        # self.axes3.legend(labels=['$SPE$统计量限值','$SPE$统计量值'], loc=0)

        self.axes4 = self.axes3.twinx()
        self.axes4.get_shared_y_axes().join(self.axes3, self.axes4)
        self.axes4.spines['right'].set_visible(False)
        self.axes4.yaxis.set_visible(False)
        self.axes4.plot(S2, color='steelblue')
        self.axes4.legend(labels=['$SPE$统计量值'], loc='upper right')
        self.axes4.set_xlabel('样本点')

    def contribution(self, t_con, q_con, nu):
        ok = nu
        if nu == -1:
            nu = 0
        self.fig.subplots_adjust(left=0.08, right=0.92, bottom=0.1, top=0.92, hspace=0.8)
        self.axes1 = self.fig.add_subplot(211)
        self.axes1.bar(range(len(t_con[0])), t_con[nu], color='steelblue')
        if ok != -1:
            self.axes1.set_title('第{}帧贡献度'.format(nu))  # , size=15)
        else:
            self.axes1.set_title('全长贡献度')

        self.axes1.set_ylabel('$T^2$贡献度')

        self.axes2 = self.fig.add_subplot(212)
        self.axes2.bar(range(len(q_con[0])), q_con[nu], color='steelblue')
        # self.axes1.set_title(name)  # , size=15)
        self.axes2.set_ylabel('$SPE$贡献度')
        self.axes2.set_xlabel('样本点')

    def relate(self, t_con, q_con):
        self.fig.subplots_adjust(left=0.08, right=0.92, bottom=0.1, top=0.92, hspace=0.8)
        self.axes1 = self.fig.add_subplot(211)
        self.axes1.bar(range(len(t_con)), t_con, color='steelblue')
        self.axes1.set_title('皮尔逊相关系数图')
        self.axes1.set_ylabel('相关系数值')
        self.axes1.set_xlabel('样本点')

        self.axes2 = self.fig.add_subplot(212)
        self.axes2.bar(range(len(q_con)), q_con, color='steelblue')
        self.axes2.set_title('斯皮尔曼相关系数图')  # , size=15)
        self.axes2.set_ylabel('相关系数值')
        self.axes2.set_xlabel('样本点')

        # 自定义横坐标刻度步长
        x_ticks = np.arange(0, len(t_con), 2)
        plt.setp(self.axes1, xticks=x_ticks)
        plt.setp(self.axes2, xticks=x_ticks)

    def feature_IU(self, feature, i, name, IU):
        self.fig.subplots_adjust(left=0.08, right=0.92, bottom=0.1, top=0.92, hspace=0.8)
        self.axes = self.fig.add_subplot(111)
        self.axes.plot(feature[:, i], label=name[i], color='steelblue')
        self.axes.set_title('{}特征-IU图'.format(name[i]))  # , size=15)
        self.axes.set_ylabel('{}'.format(name[i]))
        self.axes.legend(labels=['{}'.format(name[i])], loc='upper left')

        # self.axes.legend()  # 在每个子图上添加图例对象
        self.axes4 = self.axes.twinx()
        self.axes4.plot(IU, color='lightcoral')
        self.axes4.legend(labels=['IU'], loc='upper right')
        self.axes4.set_ylabel('IU')
        self.axes4.set_xlabel('样本点')
