"""
定义画图的函数库
"""
import sys
import matplotlib

matplotlib.use("Qt5Agg")
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QSizePolicy, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


# from DataProcessing import set_plot

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=10, height=8, dpi=100):
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
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        # Adjust layout to fill the entire canvas
        self.fig.tight_layout()
        self.ax = self.fig.add_subplot(111)

    def scatter_iu(self, x_target, y_target, df):
        self.ax.clear()
        x = df[x_target].to_list()
        y = df[y_target].to_list()
        self.ax.set_title('相关性散点图')  # 修改为 set_title
        self.ax.scatter(x, y, s=10, color='red')
        self.ax.set_xlabel('%s' % x_target)
        self.ax.set_ylabel('冷轧平均板形偏差(IU)')

    def plot_bar(self, all_num, mean_num, x_lis, x_target, y_target):
        self.ax.clear()
        sum_num = sum(all_num)
        colors = []
        for _ in all_num:
            if _ > 10:
                colors.append('royalblue')
            else:
                colors.append('lightsteelblue')
        self.ax.set_title('相关性柱状图')  # 修改为 set_title
        self.ax.bar(x_lis, mean_num, 0.5, color=colors)
        for i in range(len(all_num)):
            self.ax.text(i, mean_num[i], '%.2f' % (100 * all_num[i] / sum_num) + '%' + '\n%.0f' % all_num[i],
                         ha='center',
                         va='bottom', fontsize=6)
        self.ax.set_xlabel(x_target)
        self.ax.set_ylabel(y_target)
        self.ax.set_xticks(ticks=x_lis)
        self.ax.set_xticklabels(labels=x_lis, rotation=45, fontsize=8)
