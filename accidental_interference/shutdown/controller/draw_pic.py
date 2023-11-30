import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


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

    # 计划检修扇形统计图
    def reasonAnnualShutdown(self, year, proportion_1, proportion_2):
        reason = ['变规格', '到产', '计划检修', '躲峰限电', '其他']
        explode = [0, 0, 0.1, 0, 0]
        self.fig.subplots_adjust(left=0.030, right=0.900, top=0.940, bottom=0.050, hspace=0.335)
        self.axes1 = self.fig.add_subplot(121)

        self.axes1.pie(proportion_1, labels=reason, explode=explode, autopct='%.2f%%')
        self.axes1.set_title(f'{year}停机原因')
        self.axes2 = self.fig.add_subplot(122)
        self.axes2.pie(proportion_2, labels=reason, explode=explode, autopct='%.2f%%')
        self.axes2.set_title(f'{year}停机时间')

    def barIU(self, IU_1, name_1, IU_2, name_2):
        self.fig.clear()
        self.ax = self.fig.add_subplot(111)
        # 调整柱状图的宽度，例如设置为0.4
        # Use numeric positions for ticks
        x_positions = np.arange(len(name_1) + len(name_2))

        # Set ticks and labels
        self.ax.set_xticks(x_positions)
        try:
            self.ax.set_xticklabels(name_1 + name_2, rotation='vertical', va='bottom')
        except TypeError as e:
            print(e)
            pass

        # Plot bars
        self.ax.bar(x_positions[:len(name_1)], IU_1, width=0.4, color='red', label='停机前')
        self.ax.bar(x_positions[len(name_1):], IU_2, width=0.4, color='blue', label='停机后')
        # 添加标签和图例
        self.ax.set_xlabel('入口材料号')
        self.ax.set_ylabel('IU均值')
        self.ax.set_title('停机前后钢卷柱状图')
        self.ax.legend()


