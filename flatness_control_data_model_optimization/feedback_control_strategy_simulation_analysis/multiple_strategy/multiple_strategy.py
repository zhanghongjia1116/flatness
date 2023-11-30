# -*- coding: utf-8 -*-

"""
Module implementing SinglePolicyCompare.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
import pandas as pd
from flatness_control_data_model_optimization.feedback_control_strategy_simulation_analysis.multiple_strategy.Ui_multiple_strategy import Ui_MainWindow
from flatness_control_data_model_optimization.feedback_control_strategy_simulation_analysis.utils import strategy
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5 import QtWidgets
import os
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class 多策略对比(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):

        super(多策略对比, self).__init__(parent)
        self.setupUi(self)

    @pyqtSlot()
    def on_pushButton_xuanzeshuju_clicked(self):
        # 获取当前位置，选择数据集
        try:
            self.cwd = os.path.abspath(__file__)  # 获取当前程序文件位置
            self.path = QFileDialog.getOpenFileName(self, "ADD", self.cwd, "CSV Files(*.csv);;XLSX Files(*.xlsx)")[0]
            self.textEdit.setText(self.path)
        except:
            QMessageBox.information(self, '提示信息', '选择数据集错误')
            return None
        # 导入选择数据集
        global sta1
        global sta2
        try:

            self.data = pd.read_csv(self.path, header=0, encoding='gbk')
            self.textEdit.append('数据集导入成功！')
            self.flat_data, self.row_pot, self.iu = strategy.shujuchuli(self.data)
            self.tilt_eff, self.WRBP_eff, self.IRB_eff, self.IRB_shift_eff = strategy.get_eff()

        except:
            QMessageBox.information(self, '提示信息', '导入数据集错误')
            return None

    @pyqtSlot(int)
    def on_comboBox_celue1_currentIndexChanged(self, index):
        try:
            print('您选择的控制策略1为', self.comboBox_celue1.currentText())
            self.sta1 = self.comboBox_celue1.currentText()
            self.textEdit.setText("完成控制策略1选择！")
            if self.sta1 == '---请选择控制策略---':
                QMessageBox.information(self, '提示信息', '请选择控制策略')
                return None
            if self.sta1 == '固定优先序列':
                self.w_org1, self.row_1, self.iu1 = strategy.gudingyouxian(self.flat_data, self.row_pot, self.tilt_eff,
                                                                           self.WRBP_eff,
                                                                           self.IRB_eff, self.IRB_shift_eff)

                self.textEdit.setText("固定优先序列控制，完成计算！")
                QMessageBox.information(self, '提示信息', '固定优先序列完成计算！')
            if self.sta1 == '动态优先序列':
                self.w_dry1, self.row_1, self.iu1 = strategy.dongtaiyouxian(self.flat_data, self.row_pot, self.tilt_eff,
                                                                            self.WRBP_eff,
                                                                            self.IRB_eff, self.IRB_shift_eff)
                self.textEdit.setText("动态优先序列控制，完成计算！")
                QMessageBox.information(self, '提示信息', '动态优先序列完成计算！')
            if self.sta1 == '比例控制策略':
                self.k_wrb = 0.4
                self.k_irb = 0.4
                self.k_irs = 0.2
                self.w_pec1, self.row_1, self.iu1 = strategy.bilikongzhi(self.flat_data, self.row_pot, self.k_wrb,
                                                                         self.k_irb,
                                                                         self.k_irs,
                                                                         self.tilt_eff, self.WRBP_eff, self.IRB_eff,
                                                                         self.IRB_shift_eff)
                self.textEdit.setText("比例控制，完成计算！")
                QMessageBox.information(self, '提示信息', '比例控制，完成计算！')

            if self.sta1 == 'Adam优化控制策略':
                self.rate = 0.05
                self.beta1 = 0.9
                self.beta2 = 0.999
                self.w_org1, self.row_a1, self.iu11 = strategy.gudingyouxian(self.flat_data, self.row_pot,
                                                                             self.tilt_eff, self.WRBP_eff,
                                                                             self.IRB_eff, self.IRB_shift_eff)
                self.w_adam1, self.row_1, self.iu1 = strategy.Adamyouhua(self.w_org1, self.flat_data, self.row_pot,
                                                                         self.tilt_eff,
                                                                         self.WRBP_eff,
                                                                         self.IRB_eff, self.IRB_shift_eff, self.rate,
                                                                         self.beta1,
                                                                         self.beta2)  # Adam优化计算
                self.textEdit.setText("Adam优化控制，完成计算！")
                QMessageBox.information(self, '提示信息', 'Adam优化控制，完成计算！')
        except:
            QMessageBox.information(self, '提示信息', '请先选择数据集')
            return None

    @pyqtSlot(int)
    def on_comboBox_celue2_currentIndexChanged(self, index):
        print('您选择的控制策略2为', self.comboBox_celue2.currentText())
        self.sta2 = self.comboBox_celue2.currentText()
        self.textEdit.setText("完成控制策略2选择！")
        try:
            print('您选择的控制策略2为', self.comboBox_celue2.currentText())
            self.sta2 = self.comboBox_celue2.currentText()
            self.textEdit.setText("完成控制策略2选择！")
            if self.sta2 == '---请选择控制策略---':
                QMessageBox.information(self, '提示信息', '请选择控制策略')
                return None
            if self.sta2 == '固定优先序列':
                self.w_org2, self.row_2, self.iu2 = strategy.gudingyouxian(self.flat_data, self.row_pot, self.tilt_eff,
                                                                           self.WRBP_eff,
                                                                           self.IRB_eff, self.IRB_shift_eff)
                self.textEdit.setText("固定优先序列控制，完成计算！")
                QMessageBox.information(self, '提示信息', '固定优先序列完成计算！')
            if self.sta2 == '动态优先序列':
                self.w_dry2, self.row_2, self.iu2 = strategy.dongtaiyouxian(self.flat_data, self.row_pot, self.tilt_eff,
                                                                            self.WRBP_eff,
                                                                            self.IRB_eff, self.IRB_shift_eff)
                self.textEdit.setText("动态优先序列控制，完成计算！")
                QMessageBox.information(self, '提示信息', '动态优先序列完成计算！')
            if self.sta2 == '比例控制策略':
                self.k_wrb = 0.4
                self.k_irb = 0.4
                self.k_irs = 0.2
                self.w_pec2, self.row_2, self.iu2 = strategy.bilikongzhi(self.flat_data, self.row_pot, self.k_wrb,
                                                                         self.k_irb,
                                                                         self.k_irs,
                                                                         self.tilt_eff, self.WRBP_eff, self.IRB_eff,
                                                                         self.IRB_shift_eff)
                self.textEdit.setText("比例控制，完成计算！")
                QMessageBox.information(self, '提示信息', '比例控制，完成计算！')

            if self.sta2 == 'Adam优化控制策略':
                self.rate = 0.05
                self.beta1 = 0.9
                self.beta2 = 0.999
                self.w_org2, self.row_a2, self.iu22 = strategy.gudingyouxian(self.flat_data, self.row_pot,
                                                                             self.tilt_eff, self.WRBP_eff,
                                                                             self.IRB_eff, self.IRB_shift_eff)
                self.w_adam2, self.row_2, self.iu2 = strategy.Adamyouhua(self.w_org2, self.flat_data, self.row_pot,
                                                                         self.tilt_eff,
                                                                         self.WRBP_eff,
                                                                         self.IRB_eff, self.IRB_shift_eff, self.rate,
                                                                         self.beta1,
                                                                         self.beta2)  # Adam优化计算
                self.textEdit.setText("Adam优化控制，完成计算！")
                QMessageBox.information(self, '提示信息', 'Adam优化控制，完成计算！')
        except:
            QMessageBox.information(self, '提示信息', '请先选择数据集')
            return None

    @pyqtSlot()
    def on_pushButton_xianshituxiang_clicked(self):
        try:
            if (self.comboBox_celue1.currentText() == "---请选择控制策略---") or (
                    self.comboBox_celue2.currentText() == "---请选择控制策略---"):
                QMessageBox.information(self, '提示信息', '请先选择控制策略')
                return None
            for i in range(1, self.gridLayout_9.count()):
                self.gridLayout_9.itemAt(i).widget().deleteLater()
            for i in range(1, self.gridLayout_10.count()):
                self.gridLayout_10.itemAt(i).widget().deleteLater()
            for i in range(1, self.gridLayout_11.count()):
                self.gridLayout_11.itemAt(i).widget().deleteLater()
            for i in range(1, self.gridLayout_12.count()):
                self.gridLayout_12.itemAt(i).widget().deleteLater()
            self.graphicsView_tuxing.setVisible(False)
            self.figure = Figure()
            self.canvas = FigureCanvas(self.figure)
            self.ax = self.figure.add_subplot(111, projection='3d')
            self.nameo = '原始板形'
            strategy.figure_3D2(self.flat_data, self.ax, self.nameo, self.figure)
            self.gridLayout_9.addWidget(self.canvas)
            self.gridLayout_9.addWidget(NavigationToolbar(self.canvas, self))

            self.graphicsView_tuxing_2.setVisible(False)
            self.figure = Figure()
            self.canvas = FigureCanvas(self.figure)
            self.ax = self.figure.add_subplot(111, projection='3d')
            strategy.figure_3D2(self.row_1, self.ax, self.sta1, self.figure)
            self.gridLayout_10.addWidget(self.canvas)
            self.gridLayout_10.addWidget(NavigationToolbar(self.canvas, self))

            self.graphicsView_tuxing_3.setVisible(False)
            self.figure = Figure()
            self.canvas = FigureCanvas(self.figure)
            self.ax = self.figure.add_subplot(111, projection='3d')
            strategy.figure_3D2(self.row_2, self.ax, self.sta2, self.figure)
            self.gridLayout_11.addWidget(self.canvas)
            self.gridLayout_11.addWidget(NavigationToolbar(self.canvas, self))

            self.graphicsView_tuxing_4.setVisible(False)
            self.figure = Figure()
            self.canvas = FigureCanvas(self.figure)
            self.ax = self.figure.add_subplot(111)
            strategy.plot_line2(self.iu, self.iu1, self.iu2, self.ax, self.sta1, self.sta2, self.figure)
            self.gridLayout_12.addWidget(self.canvas)
            self.gridLayout_12.addWidget(NavigationToolbar(self.canvas, self))

        except:
            QMessageBox.information(self, '提示信息', '请先选择数据集')
            return None

    @pyqtSlot()
    def on_pushButton_qingkonghuabu_clicked(self):
        """
        清空绘图区
        """
        self.graphicsView_tuxing.setVisible(True)
        try:
            for i in range(1, self.gridLayout_9.count()):
                self.gridLayout_9.itemAt(i).widget().deleteLater()
        except:
            pass

    @pyqtSlot()
    def on_pushButton_qingkonghuabu_2_clicked(self):
        """
        清空绘图区
        """
        self.graphicsView_tuxing_2.setVisible(True)
        try:
            for i in range(1, self.gridLayout_10.count()):
                self.gridLayout_10.itemAt(i).widget().deleteLater()
        except:
            pass

    @pyqtSlot()
    def on_pushButton_qingkonghuabu_3_clicked(self):
        """
        清空绘图区
        """
        self.graphicsView_tuxing_3.setVisible(True)
        try:
            for i in range(1, self.gridLayout_11.count()):
                self.gridLayout_11.itemAt(i).widget().deleteLater()
        except:
            pass

    @pyqtSlot()
    def on_pushButton_qingkonghuabu_4_clicked(self):
        """
        清空绘图区
        """
        self.graphicsView_tuxing_3.setVisible(True)
        try:
            for i in range(1, self.gridLayout_12.count()):
                self.gridLayout_12.itemAt(i).widget().deleteLater()
        except:
            pass


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = 多策略对比()
    ui.show()
    sys.exit(app.exec_())
