# Philxt
# TIME: 2022/9/23 15:59

import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
import pandas as pd
import sys


# 重写一个matplotlib图像绘制类
class MyFigure(FigureCanvas):
    """FigureCanvas的最终的父类其实是QWidget。"""

    def __init__(self, parent=None, width=12, height=7, dpi=100):
        # 配置中文显示
        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        self.fig = Figure(figsize=(width, height), dpi=dpi)  # 新建一个figure
        # self.axes = self.fig.add_subplot(111)  # 建立一个子图，如果要建立复合图，可以在这里修改
        self.canvas=FigureCanvas(self.fig)
        # self.axes.hold(False)  # 每次绘图的时候不保留上一次绘图的结果

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        '''定义FigureCanvas的尺寸策略，这部分的意思是设置FigureCanvas，使之尽可能的向外填充空间。'''
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    '''绘制静态图，可以在这里定义自己的绘图逻辑'''
    def inquiryClass(self,y):

        self.fig.clear()
        x = ['甲','乙','丙','丁']
        self.axes1 = self.fig.add_subplot(111)
        self.fig.subplots_adjust(top=0.845,
        bottom=0.230,
        left=0.100,
        right=0.950,
        hspace=0.335,
        wspace=0.2)
        ymin = min(y)-0.02
        ymax = max(y)+0.02
        self.axes1.bar(x,y,0.5)
        self.axes1.set_title('class_group-IU均值柱状图')
        self.axes1.set_ylabel('IU均值')
        self.axes1.set_xlabel('class_group')
        self.axes1.set_ylim(ymin,ymax)
        for a, b in zip(x, y):
            self.axes1.text(a, b+0.004, round(b,3), ha='center', va='bottom', fontsize=10)
        self.draw()

    def inquiryClassEachMonth(self,x,y,banzu):
        # x = ['7月','8月','9月','10月']
        # y = [1.6419673308386433, 1.771724181652735, 1.905561256631907, 1.7930501510241303]

        xx = []
        for i in x:
            xx.append(i[0] + '—' + i[1])

        self.fig.clear()
        self.fig.subplots_adjust(top = 0.845,
        bottom = 0.230,
        left = 0.130,
        right = 0.945,
        hspace = 0.335,
        wspace = 0.2)
        self.axes1 = self.fig.add_subplot(111)
        self.axes1.bar(xx,y,0.5)
        self.axes1.set_title('class_group-月份-IU均值柱状图')
        self.axes1.set_ylabel('IU均值')
        self.axes1.set_xlabel('月份')
        self.axes1.legend([banzu],loc='upper right')
        ymin = min(y)
        ymax = max(y)+0.2
        if ymin == 0:
            self.axes1.set_ylim(ymin,ymax)
        else:
            self.axes1.set_ylim(ymin-0.2, ymax)
        for tick in self.axes1.get_xticklabels():
            tick.set_rotation(20)
        for a, b in zip(xx, y):
            self.axes1.text(a, b+0.004, round(b,3), ha='center', va='bottom', fontsize=10)
        self.draw()

    def inquiryClassEachZhaGun(self,x,y,t,zhazhiclass):
        self.fig.clear()
        self.fig.subplots_adjust(top = 0.885,
        bottom = 0.250,
        left = 0.055,
        right = 0.99,
        hspace = 0.335,
        wspace = 0.2)
        self.axes1 = self.fig.add_subplot(111)
        self.axes1.bar(x,y,0.5)
        title=str(zhazhiclass)+'class_group-月份-工作辊-IU均值柱状图'
        self.axes1.set_title(title)
        self.axes1.set_ylabel('IU均值')
        self.axes1.set_xlabel('轧辊工作辊辊号')
        legend=str(zhazhiclass)+' '+str(t)
        self.axes1.legend([legend],loc='upper right')
        ymin = min(y)-0.02
        ymax = max(y)+0.2
        self.axes1.set_ylim(ymin,ymax)
        for tick in self.axes1.get_xticklabels():
            tick.set_rotation(20)
        for a, b in zip(x, y):
            self.axes1.text(a, b+0.004, round(b,3), ha='center', va='bottom', fontsize=10)
        self.draw()

