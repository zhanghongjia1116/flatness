# Philxt
# TIME: 2022/9/23 15:59

import matplotlib
from matplotlib.ticker import FormatStrFormatter
from matplotlib.widgets import Cursor

matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
import numpy as np
import pandas as pd
import sys


# 重写一个matplotlib图像绘制类
class MyFigure(FigureCanvas):
    """FigureCanvas的最终的父类其实是QWidget。"""

    def __init__(self, parent=None, width=13, height=7, dpi=100):
        # 配置中文显示
        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        self.fig = plt.figure(figsize=(width, height), dpi=dpi)  # 新建一个figure
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
    def draw_yaxialv(self,data,n,w,t,x):
        varitions = ['STAND_01_reduction start', 'STAND_02_reduction start', 'STAND_03_reduction start',
                     'STAND_04_reduction start', 'STAND_05_reduction start']  # '压下率'

        ymajorFormatter = FormatStrFormatter('%1.2f')  # 设置y轴标签文本的格式
        self.fig.clear() #清除图形
        self.fig.canvas.draw_idle() #更新图形
        self.fig.subplots_adjust(left=0.050, right=0.990, top=0.940, bottom=0.085, hspace=0.335)
        title='钢种：' + n + '-宽度：' + w + '-厚度：' + t
        self.fig.suptitle(title)
        for m, var in enumerate(varitions):
            line='61'+'%s'%(m+1)
            self.s = self.fig.add_subplot(int(line))
            j = str(m + 1)
            r_m = data[var].values
            self.s.plot(x, r_m, 'bo', markersize='3')
            self.s.set_ylabel('机架_' + j)
            if r_m.size==0:
                self.s.set_ylim(-30,30)
            else:
                self.s.set_ylim(np.min(r_m) - 1, np.max(r_m) + 1)  # 设置临界
            self.s.yaxis.set_major_formatter(ymajorFormatter)  # 设置y坐标轴的格式
            self.s.grid(True)
        #绘制IU
        self.axes3 = self.fig.add_subplot(616)
        r_6 = data['板形均值IU'].values
        self.axes3.plot(x, r_6, color='red', marker="o", markersize='3')
        self.axes3.set_ylabel('IU均值')
        self.axes3.set_xlabel('钢卷样本')
        if r_6.size == 0:
            self.axes3.set_ylim(0, 4)
        else:
            self.axes3.set_ylim(np.min(r_6) - 1, np.max(r_6) + 1)
        if '/' in n:
            n = n.replace('/', '_')
        self.axes3.grid(True)




    def biaoding(self,x,y):
         if len(self.fig.get_axes())<6 and len(self.fig.get_axes())==6 and len(self.fig.get_axes())==7 :
             print(self.fig.get_axes())
             pass
         else:
             for i in range(len(self.fig.get_axes())-6):
                 self.fig.delaxes(self.fig.get_axes()[6+i])
         self.fig.canvas.draw()
         self.axes2 = self.fig.add_subplot(111)
         self.axes2.set_facecolor('none')
         c = self.axes2.axvline(x, color='red')
         self.axes2.grid(False)
         self.axes2.get_xaxis().set_visible(True)
         self.axes2.get_yaxis().set_visible(True)
         self.axes2.set_ylabel('A')
         self.axes2.draw_artist(self.axes2.patch)
         self.axes2.draw_artist(c)
         print(self.fig.get_axes())


    def IU(self,data,n,x):
        print(self.fig.gca())
        self.fig.canvas.draw_idle()  # 更新图形
        self.axes3 = self.fig.add_subplot(616)
        r_6 = data['板形均值IU'].values
        self.axes3.plot(x, r_6, color='red',marker="o",markersize='3')
        self.axes3.set_ylabel('IU均值')
        self.axes3.set_xlabel('钢卷样本')
        if r_6.size == 0:
            self.axes3.set_ylim(0, 4)
        else:
            self.axes3.set_ylim(np.min(r_6) - 1, np.max(r_6) + 1)
        if '/' in n:
            n = n.replace('/', '_')
        self.axes3.grid(True)
