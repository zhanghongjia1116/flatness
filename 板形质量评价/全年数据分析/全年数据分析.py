# -*- coding: utf-8 -*-

"""
Module implementing dialog.
"""
import os
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QGridLayout
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from .Ui_全年数据分析 import Ui_MainWindow
from ..utils import fig
from matplotlib.figure import Figure


class PerYearAnalysis(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget (defaults to None)
        @type QWidget (optional)
        """
        super().__init__(parent)
        self.setupUi(self)
        self.initComboBox()

    def initComboBox(self):
        self.comboBox.clear()
        self.comboBox.addItem('浪形百分比')
        self.comboBox.addItem('IU百分比')
        self.comboBox.addItem('IU概率密度图')

    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """

        tmp = os.path.abspath(__file__)
        path = QFileDialog.getOpenFileName(self, u"打开文件", tmp, "CSV Files(*.csv);;XLSX Files(*.xlsx)")
        self.lineEdit.setText(path[0])

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        # self.F = Figure()
        # self.canvas = FigureCanvas(self.F)
        # self.F_ntb = NavigationToolbar(self.canvas, self)
        # # self.gridlayout = QGridLayout(self.widget)  # 继承容器
        # # self.gridlayout = QGridLayout(self.graphicsView)
        # self.gridlayout.deleteLater()
        for i in range(1, self.gridLayout.count()):
            self.gridLayout.itemAt(i).widget().deleteLater()

        if self.lineEdit.text() != '':
            path = self.lineEdit.text()
        else:
            self.cwd = os.getcwd()  # 获取当前程序文件位置
            print(self.cwd.replace('\\', '/'))
            path = self.cwd.replace('\\', '/') + '/201912到202011初值统计（去公式）最新.csv'
            self.lineEdit.setText(path)
        # print(path)
        name = self.comboBox.currentText()
        print(name)

        #  浪形分布
        def shuju_lxfenbu(path):
            data = pd.read_csv(path, header=0, encoding='gbk')
            num = data.shape[0]
            labels = ['左边浪', '右边浪', '左三分浪', '右三分浪', '双边浪', '中浪', '四分浪', '边中浪', '无']
            num = data.shape[0]
            que = []
            for i in labels:
                pot_data3 = data.loc[data['浪形'] == i]
                num2 = pot_data3.shape[0]
                n = num2 / num * 100
                que.append(n)
            return que, num

        def Iu_percent(path):
            data = pd.read_csv(path, header=0, encoding='gbk')
            all_length = data.shape[0]  # 全部点数

            iu = data['原始IU'].values

            # 0-1, 1-2,     (7个区间)
            result = np.array([0, 0, 0, 0, 0, 0, 0])
            x = np.linspace(-1, 1, 80)
            for i in range(all_length):
                if iu[i] <= 1:
                    result[0] += 1
                elif iu[i] > 1 and iu[i] <= 2:
                    result[1] += 1
                elif iu[i] > 2 and iu[i] <= 3:
                    result[2] += 1
                elif iu[i] > 3 and iu[i] <= 4:
                    result[3] += 1
                elif iu[i] > 4 and iu[i] <= 5:
                    result[4] += 1
                elif iu[i] > 5 and iu[i] <= 6:
                    result[5] += 1
                else:
                    result[6] += 1
            p_result = [round(i, 4) * 100 for i in result / sum(result)]
            return p_result

        def Iu_get(path):
            data = pd.read_csv(path, header=0, encoding='gbk')
            # all_length = data.shape[0]  # 全部点数

            iu = data['原始IU'].values
            return iu

        try:
            if name == '浪形百分比':
                que, num = shuju_lxfenbu(path)
                self.graphicsView.setVisible(False)
                self.F = Figure()
                self.canvas = FigureCanvas(self.F)
                # self.F_ntb = NavigationToolbar(self.canvas, self)
                self.gridLayout.addWidget(self.canvas)
                self.gridLayout.addWidget(NavigationToolbar(self.canvas, self))
                fig.langxingfenbu(self.F, que, num)
                # self.gridlayout = QGridLayout(self.widget)  # 继承容器

            elif name == 'IU百分比':
                self.graphicsView.setVisible(False)
                self.F = Figure()
                self.canvas = FigureCanvas(self.F)
                # self.F_ntb = NavigationToolbar(self.canvas, self)
                self.gridLayout.addWidget(self.canvas)
                self.gridLayout.addWidget(NavigationToolbar(self.canvas, self))
                que = Iu_percent(path)
                fig.IUfenbu1(self.F, que)


            elif name == 'IU概率密度图':
                self.graphicsView.setVisible(False)
                self.F = Figure()
                self.canvas = FigureCanvas(self.F)
                # self.F_ntb = NavigationToolbar(self.canvas, self)
                self.gridLayout.addWidget(self.canvas)
                self.gridLayout.addWidget(NavigationToolbar(self.canvas, self))
                p_result = Iu_get(path)
                path = fig.Gailvmidutu(self.F, p_result)
                # self.gridlayout = QGridLayout(self.widget)  # 继承容器

                if os.path.exists(path):  # 如果文件存在
                    # 删除文件，可使用以下两种方法。
                    os.remove(path)
        except:
            my_button = QMessageBox.information(self, '警告信息', '文件选择出错')


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = PerYearAnalysis()
    ui.show()
    sys.exit(app.exec())
