import sys
import matplotlib
import numpy as np
from matplotlib.ticker import MultipleLocator

matplotlib.use("Qt5Agg")
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QSizePolicy, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

class MyFigure(FigureCanvas):

    def __init__(self,width=50, height=40, dpi=10):
        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        #第一步：创建一个创建Figure

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        # self.fig = plt.figure(figsize=(width, height), dpi=dpi)


        #第二步：在父类中激活Figure窗口
        super(MyFigure,self).__init__(self.fig) #此句必不可少，否则不能显示图形
        #第三步：创建一个子图，用于绘制图形用，111表示子图编号，如matlab的subplot(1,1,1)






