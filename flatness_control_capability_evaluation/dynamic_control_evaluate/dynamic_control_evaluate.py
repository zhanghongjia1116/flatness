# -*- coding: utf-8 -*-

"""
Module implementing FullLengthQuality.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
import pandas as pd
from flatness_control_capability_evaluation.dynamic_control_evaluate.Ui_dynamic_control_evaluate import Ui_DynamicControl
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5 import QtWidgets
from flatness_control_capability_evaluation.dynamic_control_evaluate import strategy
from flatness_control_capability_evaluation.dynamic_control_evaluate import evaluate
import os
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class DynamicControl(QMainWindow, Ui_DynamicControl):

    def __init__(self, parent=None):

        super(DynamicControl, self).__init__(parent)
        self.setupUi(self)

    @pyqtSlot()
    def on_pushButton_xuanzeshuju_clicked(self):
        # 获取当前位置，选择数据集
        tmp = os.path.abspath(__file__)
        # self.cwd = os.getcwd()  # 获取当前程序文件位置
        self.path = QFileDialog.getOpenFileName(self, "ADD", tmp, "CSV Files(*.csv);;XLSX Files(*.xlsx)")[0]
        self.textEdit_1.setText(self.path)
        # 导入选择数据集
        global name
        try:

            self.data = pd.read_csv(self.path, header=0, encoding='gbk')
            self.flat_data, self.row_pot, self.iu = strategy.shujuchuli(self.data)
            self.textEdit_1.append('数据集导入成功！')

        except:
            QMessageBox.information(self, '提示信息', '导入数据集错误')
            return None

    @pyqtSlot()
    def on_pushButton_fenxi_clicked(self):
        """
        Slot documentation goes here.
        """
        self.IUzhi, self.IUlv, = evaluate.shujufenxi(self.data)
        print(self.IUzhi, self.IUlv)
        self.lineEdit_xiajingzhi.setText(str(self.IUzhi))  # 设置文本
        self.lineEdit_xiajingzhi.setEnabled(False)
        self.lineEdit_xiajianglv.setText(str(self.IUlv * 100))  # 设置文本
        self.lineEdit_xiajianglv.setEnabled(False)
        for i in range(1, self.gridLayout_2.count()):
            self.gridLayout_2.itemAt(i).widget().deleteLater()
        self.graphicsView_tuxing.setVisible(False)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.gridLayout_2.addWidget(self.canvas)
        self.gridLayout_2.addWidget(NavigationToolbar(self.canvas, self))
        self.ax = self.figure.add_subplot(111, projection='3d')
        self.name = '实测板形三维图'
        strategy.figure_3D(self.flat_data, self.ax, self.name, self.figure)
        print(self.name)

        for i in range(1, self.gridLayout_3.count()):
            self.gridLayout_3.itemAt(i).widget().deleteLater()
        self.graphicsView_tuxing_2.setVisible(False)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.gridLayout_3.addWidget(self.canvas)
        self.gridLayout_3.addWidget(NavigationToolbar(self.canvas, self))
        self.ax = self.figure.add_subplot(111)
        evaluate.plot_line(self.iu, self.ax, self.figure)

    @pyqtSlot()
    def on_pushButton_qingkonghuabu_clicked(self):
        """
        清空绘图区
        """
        self.graphicsView_tuxing.setVisible(True)
        try:
            for i in range(1, self.gridLayout_2.count()):
                self.gridLayout_2.itemAt(i).widget().deleteLater()
        except:
            pass

    @pyqtSlot()
    def on_pushButton_qingkonghuabu_2_clicked(self):
        """
        清空绘图区
        """
        self.graphicsView_tuxing_2.setVisible(True)
        try:
            for i in range(1, self.gridLayout_3.count()):
                self.gridLayout_3.itemAt(i).widget().deleteLater()
        except:
            pass


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = DynamicControl()
    ui.show()
    sys.exit(app.exec_())
