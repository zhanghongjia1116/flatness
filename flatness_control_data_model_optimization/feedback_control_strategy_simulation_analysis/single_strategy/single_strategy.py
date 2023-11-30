# -*- coding: utf-8 -*-

"""
Module implementing single_strategy.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
import pandas as pd
from flatness_control_data_model_optimization.feedback_control_strategy_simulation_analysis.single_strategy.Ui_single_strategy import Ui_MainWindow
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5 import QtWidgets
from flatness_control_data_model_optimization.feedback_control_strategy_simulation_analysis.utils import strategy
import os
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class 单策略对比(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(单策略对比, self).__init__(parent)
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
        global name
        try:

            self.data = pd.read_csv(self.path, header=0, encoding='gbk')
            self.textEdit.append('数据集导入成功！')
            self.flat_data, self.row_pot, self.iu = strategy.shujuchuli(self.data)
            self.tilt_eff, self.WRBP_eff, self.IRB_eff, self.IRB_shift_eff = strategy.get_eff()

            self.lineEdit_danzhen_1.setText(str(self.row_pot))  # 设置文本
            self.lineEdit_danzhen_1.setEnabled(False)
        except Exception as e:
            print(e)
            QMessageBox.information(self, '提示信息', '导入数据集错误')
            return None

    @pyqtSlot()
    def on_radioButton_clicked(self):
        print(self.radioButton.text())
        self.name_shunxu = '固定优先序列'

    @pyqtSlot()
    def on_radioButton_2_clicked(self):
        print(self.radioButton_2.text())
        self.name_shunxu = '动态优先序列'

    @pyqtSlot()
    def on_pushButton_shunxu_clicked(self):
        try:
            if self.name_shunxu == '固定优先序列':
                self.w_org, self.row_org, self.iu_org = strategy.gudingyouxian(self.flat_data, self.row_pot,
                                                                               self.tilt_eff,
                                                                               self.WRBP_eff,
                                                                               self.IRB_eff, self.IRB_shift_eff)

                self.name = '固定优先序列'
                self.textEdit.setText("固定优先序列控制，完成计算！")
                QMessageBox.information(self, '提示信息', '固定优先序列完成计算！')
            if self.name_shunxu == '动态优先序列':
                self.w_dry, self.row_dry, self.iu_dry = strategy.dongtaiyouxian(self.flat_data, self.row_pot,
                                                                                self.tilt_eff,
                                                                                self.WRBP_eff,
                                                                                self.IRB_eff, self.IRB_shift_eff)
                self.name = '动态优先序列'
                self.textEdit.setText("动态优先序列控制，完成计算！")
                QMessageBox.information(self, '提示信息', '动态优先序列完成计算！')
        except:
            QMessageBox.information(self, '提示信息', '请先选择数据集')
            return None

    @pyqtSlot()
    def on_pushButton_bili_clicked(self):
        self.lineEdit_wrbbili.setText("0.4")  # 设置文本
        self.lineEdit_irbbili.setText("0.4")
        self.lineEdit_irsbili.setText("0.2")

    @pyqtSlot()
    def on_pushButton_bilijisuan_clicked(self):
        if (self.lineEdit_wrbbili.text() == "") or (self.lineEdit_irbbili.text() == "") or (
                self.lineEdit_irsbili.text() == ""):
            print("文本框内容为空")
            QMessageBox.information(self, '提示信息', '请初始化系数')
            return None
        try:
            self.k_wrb = self.lineEdit_wrbbili.text()
            self.k_irb = self.lineEdit_irbbili.text()
            self.k_irs = self.lineEdit_irsbili.text()
            self.k_wrb = float(self.k_wrb)
            self.k_irb = float(self.k_irb)
            self.k_irs = float(self.k_irs)
            if self.k_wrb + self.k_irb + self.k_irs != 1:
                QMessageBox.information(self, '提示信息', '比例分配错误，请重新输入')
                return None
            # print(a,b,c)
            self.w_pec, self.row_pec, self.iu_pec = strategy.bilikongzhi(self.flat_data, self.row_pot, self.k_wrb,
                                                                         self.k_irb, self.k_irs,
                                                                         self.tilt_eff, self.WRBP_eff, self.IRB_eff,
                                                                         self.IRB_shift_eff)
            self.name = '比例控制策略'
            self.textEdit.setText("比例控制，完成计算！")
            QMessageBox.information(self, '提示信息', '比例控制，完成计算！')
        except:
            QMessageBox.information(self, '提示信息', '请先选择数据集')
            return None

    @pyqtSlot()
    def on_pushButton_Adam_clicked(self):
        self.lineEdit_adam_1.setText("0.05")  # 设置文本
        self.lineEdit_adam_2.setText("0.9")
        self.lineEdit_adam_3.setText("0.999")

    @pyqtSlot()
    def on_pushButton_Adamjisuan_clicked(self):
        if (self.lineEdit_adam_1.text() == "") or (self.lineEdit_adam_2.text() == "") or (
                self.lineEdit_adam_3.text() == ""):
            QMessageBox.information(self, '提示信息', '请初始化系数')
            return None
        try:
            self.rate = self.lineEdit_adam_1.text()
            self.beta1 = self.lineEdit_adam_2.text()
            self.beta2 = self.lineEdit_adam_3.text()
            self.rate = float(self.rate)
            self.beta1 = float(self.beta1)
            self.beta2 = float(self.beta2)
            if (self.rate > 1) or (self.rate < 0):
                QMessageBox.information(self, '提示信息', '学习率应在0~1之间')
                return None
            if (self.beta1 > 1) or (self.beta1 < 0):
                QMessageBox.information(self, '提示信息', '一阶矩估计指数衰减率应在0~1之间')
                return None
            if (self.beta2 > 1) or (self.beta2 < 0):
                QMessageBox.information(self, '提示信息', '二阶矩估计指数衰减率应在0~1之间')
                return None
            self.w_org, self.row_a, self.iu_a = strategy.gudingyouxian(self.flat_data, self.row_pot, self.tilt_eff,
                                                                       self.WRBP_eff,
                                                                       self.IRB_eff, self.IRB_shift_eff)
            self.w_adam, self.row_adam, self.iu_adam = strategy.Adamyouhua(self.w_org, self.flat_data, self.row_pot,
                                                                           self.tilt_eff, self.WRBP_eff,
                                                                           self.IRB_eff, self.IRB_shift_eff, self.rate,
                                                                           self.beta1, self.beta2)  # Adam优化计算
            self.name = 'Adam优化控制策略'
            self.textEdit.setText("Adam优化控制，完成计算！")
            QMessageBox.information(self, '提示信息', 'Adam优化控制，完成计算！')
        except:
            QMessageBox.information(self, '提示信息', '请先选择数据集')
            return None

    @pyqtSlot()
    def on_pushButton_xianshituxiang_clicked(self):
        try:
            for i in range(1, self.gridLayout_9.count()):
                self.gridLayout_9.itemAt(i).widget().deleteLater()

            # for i in range(1, self.gridLayout_11.count()):
            #     self.gridLayout_11.itemAt(i).widget().deleteLater()
            self.graphicsView_tuxing.setVisible(False)
            self.figure = Figure()
            self.canvas = FigureCanvas(self.figure)
            self.gridLayout_9.addWidget(self.canvas)
            self.gridLayout_9.addWidget(NavigationToolbar(self.canvas, self))
            self.ax = self.figure.add_subplot(111, projection='3d')
            self.nameo = '原始板形'
            strategy.figure_3D(self.flat_data, self.ax, self.nameo, self.figure)
            if self.name == '固定优先序列':
                for i in range(1, self.gridLayout_10.count()):
                    self.gridLayout_10.itemAt(i).widget().deleteLater()
                self.graphicsView_tuxing_2.setVisible(False)
                self.figure = Figure()
                self.canvas = FigureCanvas(self.figure)
                self.gridLayout_10.addWidget(self.canvas)
                self.gridLayout_10.addWidget(NavigationToolbar(self.canvas, self))
                self.ax = self.figure.add_subplot(111, projection='3d')
                strategy.figure_3D(self.row_org, self.ax, self.name, self.figure)
                print(self.name)

            if self.name == '动态优先序列':
                for i in range(1, self.gridLayout_10.count()):
                    self.gridLayout_10.itemAt(i).widget().deleteLater()
                self.graphicsView_tuxing_2.setVisible(False)
                self.figure = Figure()
                self.canvas = FigureCanvas(self.figure)
                self.gridLayout_10.addWidget(self.canvas)
                self.gridLayout_10.addWidget(NavigationToolbar(self.canvas, self))
                self.ax = self.figure.add_subplot(111, projection='3d')
                strategy.figure_3D(self.row_dry, self.ax, self.name, self.figure)
                print(self.name)

            if self.name == '比例控制策略':
                for i in range(1, self.gridLayout_10.count()):
                    self.gridLayout_10.itemAt(i).widget().deleteLater()
                self.graphicsView_tuxing_2.setVisible(False)
                self.figure = Figure()
                self.canvas = FigureCanvas(self.figure)
                self.gridLayout_10.addWidget(self.canvas)
                self.gridLayout_10.addWidget(NavigationToolbar(self.canvas, self))
                self.ax = self.figure.add_subplot(111, projection='3d')
                strategy.figure_3D(self.row_pec, self.ax, self.name, self.figure)
                print(self.name)

            if self.name == 'Adam优化控制策略':
                for i in range(1, self.gridLayout_10.count()):
                    self.gridLayout_10.itemAt(i).widget().deleteLater()
                self.graphicsView_tuxing_2.setVisible(False)
                self.figure = Figure()
                self.canvas = FigureCanvas(self.figure)
                self.gridLayout_10.addWidget(self.canvas)
                self.gridLayout_10.addWidget(NavigationToolbar(self.canvas, self))
                self.ax = self.figure.add_subplot(111, projection='3d')
                strategy.figure_3D(self.row_adam, self.ax, self.name, self.figure)
                print(self.name)
        except:
            QMessageBox.information(self, '提示信息', '请先选择控制策略')
            return None

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
    def on_pushButton_xianshituxiang_2_clicked(self):
        try:
            self.danzhen = self.lineEdit_danzhen_2.text()
            self.danzhen = int(self.danzhen) - 1
            if self.name == '固定优先序列':
                for i in range(1, self.gridLayout_11.count()):
                    self.gridLayout_11.itemAt(i).widget().deleteLater()
                self.graphicsView_tuxing_3.setVisible(False)
                self.figure = Figure()
                self.canvas = FigureCanvas(self.figure)
                self.gridLayout_11.addWidget(self.canvas)
                self.gridLayout_11.addWidget(NavigationToolbar(self.canvas, self))
                self.ax = self.figure.add_subplot(111)
                strategy.plot_line(self.flat_data, self.row_org, self.danzhen, self.ax, self.name, self.figure)
                print(self.name)
            if self.name == '动态优先序列':
                for i in range(1, self.gridLayout_11.count()):
                    self.gridLayout_11.itemAt(i).widget().deleteLater()
                self.graphicsView_tuxing_3.setVisible(False)
                self.figure = Figure()
                self.canvas = FigureCanvas(self.figure)
                self.gridLayout_11.addWidget(self.canvas)
                self.gridLayout_11.addWidget(NavigationToolbar(self.canvas, self))
                self.ax = self.figure.add_subplot(111)
                strategy.plot_line(self.flat_data, self.row_dry, self.danzhen, self.ax, self.name, self.figure)
                print(self.name)
            if self.name == '比例控制策略':
                for i in range(1, self.gridLayout_11.count()):
                    self.gridLayout_11.itemAt(i).widget().deleteLater()
                self.graphicsView_tuxing_3.setVisible(False)
                self.figure = Figure()
                self.canvas = FigureCanvas(self.figure)
                self.gridLayout_11.addWidget(self.canvas)
                self.gridLayout_11.addWidget(NavigationToolbar(self.canvas, self))
                self.ax = self.figure.add_subplot(111)
                strategy.plot_line(self.flat_data, self.row_pec, self.danzhen, self.ax, self.name, self.figure)
                print(self.name)
            if self.name == 'Adam优化控制策略':
                for i in range(1, self.gridLayout_11.count()):
                    self.gridLayout_11.itemAt(i).widget().deleteLater()
                self.graphicsView_tuxing_3.setVisible(False)
                self.figure = Figure()
                self.canvas = FigureCanvas(self.figure)
                self.gridLayout_11.addWidget(self.canvas)
                self.gridLayout_11.addWidget(NavigationToolbar(self.canvas, self))
                self.ax = self.figure.add_subplot(111)
                strategy.plot_line(self.flat_data, self.row_adam, self.danzhen, self.ax, self.name, self.figure)
                print(self.name)
        except:
            QMessageBox.information(self, '提示信息', '请输入正确帧数')
            return None


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = 单策略对比()
    ui.show()
    sys.exit(app.exec_())
