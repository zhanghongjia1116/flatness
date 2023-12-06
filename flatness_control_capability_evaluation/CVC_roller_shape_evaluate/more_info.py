import sys

import pandas as pd
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem, QHBoxLayout, QVBoxLayout, QGraphicsScene, \
    QSizePolicy, QMainWindow, qApp
from matplotlib.cm import get_cmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedFormatter

from qtResource.MyIcon import MyIcon
from qfluentwidgets import CardWidget


class MatplotlibWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1600, 500)
        self.setWindowTitle('详细信息显示')
        self.setWindowIcon(QIcon(MyIcon.板形描述.path()))

        self.layout = QHBoxLayout(self)

        self.leftCardWidget = CardWidget()
        self.leftLayout = QVBoxLayout(self.leftCardWidget)

        self.rightCardWidget = CardWidget()
        self.rightLayout = QVBoxLayout(self.rightCardWidget)

        self.layout.addWidget(self.leftCardWidget)
        self.layout.addWidget(self.rightCardWidget)

    def closeEvent(self, event):
        # 处理窗口关闭事件
        self.close()


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

    def plotBarCVC(self, data: pd.DataFrame, high_value_data: pd.DataFrame):
        self.ax = self.fig.add_subplot(111)
        highUniqueLevels = high_value_data['aDirNoAi'].unique()
        xLabels = [str(i) for i in highUniqueLevels]
        y1 = [data[data['aDirNoAi'] == i]['aDirNoAi'].count() for i in highUniqueLevels]
        y2 = [high_value_data[high_value_data['aDirNoAi'] == i]['aDirNoAi'].count() for i in highUniqueLevels]
        self.ax.bar(xLabels, y1, label='导入钢卷的卷数')
        self.ax.bar(xLabels, y2, label='打满值的卷数')
        self.ax.set_xticklabels(xLabels, rotation=45)  # 设置横轴标签
        self.ax.set_xlabel('策略号')
        self.ax.set_ylabel('卷数')
        # 显示数量
        for x, y in enumerate(y1):
            self.ax.text(x, y + 0.3, '%s' % y, ha='center', va='bottom')
        for x, y in enumerate(y2):
            self.ax.text(x, y + 0.3, '%s' % y, ha='center', va='bottom')
        # 显示图例
        self.ax.legend()
        self.ax.set_title('同aDirNoAi下的卷数分布')

    def plotPieCVC(self, high_value_data: pd.DataFrame):
        self.ax = self.fig.add_subplot(111)
        # 获取不同等级的唯一值
        unique_levels = high_value_data['aDirNoAi'].unique()
        # 获取每个唯一值的计数
        value_counts = high_value_data['aDirNoAi'].value_counts()
        cmap = get_cmap('viridis')  # 使用'viridis'颜色映射
        colors = [cmap(i / len(unique_levels)) for i in range(len(unique_levels))]
        patches, texts, autoTexts = self.ax.pie(value_counts, labels=unique_levels,
                                                autopct='%1.1f%%', colors=colors,
                                                startangle=140, textprops={'fontsize': 7})
        # 将扇形图内部的百分比文本颜色设置为白色
        for autotext in autoTexts:
            autotext.set_color('white')
        self.ax.set_title('打满钢卷不同策略号的分布')
        self.ax.axis('equal')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MatplotlibWidget()
    ex.show()
    sys.exit(app.exec_())
