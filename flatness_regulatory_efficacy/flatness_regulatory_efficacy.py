# -*- coding: utf-8 -*-

"""
Module implementing .
"""

import os

import numpy as np
import pandas as pd
from PyQt5 import QtWidgets, QtGui
from PyQt5.Qt import *  # 或上两行代替
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from . import css
# import css
from .Ui_flatness_regulatory_efficacy import Ui_RegulatoryEfficacy


def get_J(_w, _flat, _eff):
    """获取损失函数"""
    error = np.dot(_w, _eff) - _flat
    return np.mean(error ** 2) / 2


def get_dJ(_w, _flat, _eff):
    """获取梯度"""
    dj = np.dot(-_w.T, _flat - np.dot(_w, _eff)) / _flat.shape[0]
    return dj


class LsAdam:
    """ls的Adam优化算法，已知调控量求调控功效和已知调控功效求调控量梯度不一样"""

    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999):
        self.beta1 = beta1
        self.beta2 = beta2
        self.iter = 0
        self.lr = lr
        self.m = None  # 一阶矩估计
        self.v = None  # 二阶矩估计

    def update(self, params, grads):
        """
        更新值
        :param params:需要更新的值
        :param grads: 梯度
        :return:
        """
        if self.m is None:
            self.m, self.v = {}, {}
            for key, val in params.items():
                self.m[key] = np.zeros_like(val)
                self.v[key] = np.zeros_like(val)
        self.iter += 1

        lr_t = self.lr * np.sqrt(1.0 - self.beta2 ** self.iter) / (1.0 - self.beta1 ** self.iter)
        for key in params.keys():
            self.m[key] += (1 - self.beta1) * (grads[key] - self.m[key])
            self.v[key] += (1 - self.beta2) * (grads[key] ** 2 - self.v[key])
            params[key] -= lr_t * self.m[key] / (np.sqrt(self.v[key]) + 1e-7)


def my_leastq(flat):
    """
    基于勒让德正交多项式的最小二乘法
    :param flat: 需要识别的板形
    :return: 板形特征系数
    """
    flat_x = np.linspace(-1, 1, len(flat))
    p1 = flat_x
    p2 = 1.5 * pow(flat_x, 2) - 1 / 2
    p3 = 0.5 * (5 * pow(flat_x, 3) - 3 * flat_x)
    p4 = (1 / 8) * (35 * pow(flat_x, 4) - 30 * pow(flat_x, 2) + 3)
    X = np.array([p1, p2, p3, p4]).T
    # X = np.array([p1, p2, p4]).T
    inv_X = np.linalg.inv(np.dot(X.T, X))
    return np.dot(np.dot(inv_X, X.T), flat.T)


def ls_lerangde_nihe(xishu, have_0_xishu=True):
    flat_x = np.linspace(-1, 1, 80)
    p1 = flat_x
    p2 = 1.5 * pow(flat_x, 2) - 1 / 2
    p3 = 0.5 * (5 * pow(flat_x, 3) - 3 * flat_x)
    p4 = (1 / 8) * (35 * pow(flat_x, 4) - 30 * pow(flat_x, 2) + 3)
    if have_0_xishu:
        y = xishu[0] + xishu[1] * p1 + xishu[2] * p2 + xishu[3] * p3 + xishu[4] * p4
    else:
        y = xishu[0] * p1 + xishu[1] * p2 + xishu[2] * p3 + xishu[3] * p4
        # y = xishu[0] * p1 + xishu[1] * p2 + xishu[2] * p4
    return y


class 板形调控功效挖掘(QMainWindow, Ui_RegulatoryEfficacy):
    """
    Class documentation goes here.
    """

    # path: str

    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super().__init__()
        self.setupUi(self)
        # 定义文本标签
        self.statusLabel = QLabel()

        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(14)
        self.statusLabel.setFont(font)

        # 设置文本标签显示内容
        self.statusLabel.setText("请先选择文件")
        self.statusLabel.setContentsMargins(25, 0, 0, 0)
        self.statusLabel.setObjectName('statusLabel')
        # 定义水平进度条
        self.pb = QProgressBar()
        # 设置进度条的范围，参数1为最小值，参数2为最大值（可以调得更大，比如1000
        self.pb.setRange(0, 100)
        # 设置进度条的初始值,最大值，最小值
        self.pb.setValue(0)
        self.pb.setMinimum(0)
        self.pb.setMaximum(100)
        self.pb.setStyleSheet(
            "QProgressBar {   border: 2px solid grey;   border-radius: 5px;   background-color: #FFFFFF;font-size:20px;}QProgressBar::chunk {   background-color: #007FFF;   width: 10px;}QProgressBar {   border: 2px solid grey;   border-radius: 5px;   text-align: center;}"
            "QProgressBar::chunk { background-color: #007FFF; width: 10px;margin:0.5px }")
        # 往状态栏中添加组件（stretch应该是拉伸组件宽度）-->会添加到状态栏左侧
        # self.statusbar.addWidget(self.statusLabel)
        # self.statusbar.addWidget(self.progressBar)
        self.statusbar.addPermanentWidget(self.statusLabel, stretch=2)
        self.statusbar.addPermanentWidget(self.pb, stretch=12)
        # 子线程
        self.work = WorkThread()
        self.pushButton_jisuan.clicked.connect(self.excute)  # 触发子线程连接函数，函数不要添加()
        self.is_done = 0

    #   qthread启动函数
    def excute(self):
        """
        Slot documentation goes here.
        """
        global path_jdt

        a1 = os.path.abspath(__file__)
        a = os.path.dirname(a1)
        b = self.comboBox.currentText()
        self.path = a + '\\third_res\\' + b + '.pkl'
        path_jdt = self.path
        self.textEdit.setText(self.path)

        # 启动子线程
        self.work.start()
        # 根据槽函数trigger,tishi,连接函数，输送emit传出来的值
        self.work.trigger.connect(self.drawp)
        self.work.trigger2.connect(self.drawp)
        # self.work.tishi.connect(self.box)
        self.work.progressBarValue.connect(self.callback)
        self.work.signal_done.connect(self.callback_done)

    # 回传进度条参数
    def callback(self, i):
        if i != 100:
            self.statusLabel.setText('模型正在计算')
            self.pb.setValue(i)
        else:
            self.pb.setValue(i)
            self.statusLabel.setText('模型计算完成！')

    # 回传结束信号
    def callback_done(self, i):
        self.is_done = i
        if self.is_done == 1:
            self.statusLabel.setText('模型正在计算！')
        elif self.is_done == 2:
            self.statusLabel.setText('模型计算完成！')

    def drawp(self, flag):
        self.work.disconnect()  # 断开连接，避免重复运行
        self.flag = flag

    @pyqtSlot()
    def on_pushButton_qingkong_clicked(self):
        """
        清空操作显示信息栏
        """
        self.textEdit.clear()

    @pyqtSlot()
    def on_pushButton_xianshijieguo_clicked(self):
        """
        图像显示
        """
        try:
            for i in range(1, self.gridLayout_9.count()):
                self.gridLayout_9.itemAt(i).widget().deleteLater()
            self.graphicsView_tuxing.setVisible(False)
            self.figure = Figure()
            self.canvas = FigureCanvas(self.figure)
            self.gridLayout_9.addWidget(self.canvas)
            self.gridLayout_9.addWidget(NavigationToolbar(self.canvas, self))
            self.ax1 = self.figure.add_subplot(221)
            self.ax2 = self.figure.add_subplot(222)
            self.ax3 = self.figure.add_subplot(223)
            self.ax4 = self.figure.add_subplot(224)
            css.plot_line(nihe_jdt, self.ax1, self.ax2, self.ax3, self.ax4, self.figure)

        except:
            QMessageBox.information(self, '提示信息', '请先完成模型计算，再进行此操作！')

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
    def on_pushButton_qingkongxianshijieguo_clicked(self):
        """
        清空结果区
        """
        self.model = QStandardItemModel(0, 0)  # 行数，列数
        self.tableView.setModel(self.model)  # 实例化表格

    @pyqtSlot()
    def on_pushButton_baocun_clicked(self):
        """
        保存结果区内容
        """
        res_path = QFileDialog.getSaveFileName(self, "ADD", os.getcwd(), "CSV Files(*.csv)")[0]
        try:
            deg = pd.DataFrame(xishu_jdt, columns=['1次项系数', '2次项系数', '3次项系数', '4次项系数'],
                               index=['Tilt_eff', 'WRB_eff', 'IRB_eff', 'IRS_eff'])
            deg.to_csv(res_path, index=True, encoding='gbk')
            QMessageBox.information(self, '提示', '已导出！')
        except Exception as e:
            print(e)
            QMessageBox.information(self, '提示', '导出失败！')

    @pyqtSlot()
    def on_pushButton_jisuanjieguo_clicked(self):

        try:
            self.model = QStandardItemModel(4, 4)  # 行数，列数，不含标题行
            self.model.setHorizontalHeaderLabels(['1次项系数', '2次项系数', '3次项系数', '4次项系数'])
            self.model.setVerticalHeaderLabels(['Tilt_eff', 'WRB_eff', 'IRB_eff', 'IRS_eff'])

            for row in range(4):
                for column in range(4):
                    item = QStandardItem('{:.6f}'.format(xishu_jdt[row][column]))
                    self.model.setItem(row, column, item)

            self.tableView.horizontalHeader().setStretchLastSection(True)  # 二行代码让表枨满窗口显示，不出现滚动条
            self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.tableView.setModel(self.model)  # 实例化表格


        except:
            QMessageBox.information(self, '提示信息', '请先完成模型计算，再进行此操作！')
            return None

    @pyqtSlot(int)
    def on_comboBox_currentIndexChanged(self, index):
        print('您选择的宽度范围为', self.comboBox.currentText())
        b = self.comboBox.currentText()
        self.textEdit.setText("完成宽度选择！")

    @pyqtSlot()
    def on_radioButton_3_clicked(self):
        print(self.radioButton_3.text())
        self.textEdit.setText("选择光辊！")

    @pyqtSlot()
    def on_radioButton_4_clicked(self):
        QMessageBox.information(self, '提示', '毛辊目前无数据')
        self.textEdit.setText("毛辊目前无数据，选择光辊！")

    # **************子线程计算部分开始*********************************************


class WorkThread(QThread):
    trigger = pyqtSignal(list)  # 两个信号
    trigger2 = pyqtSignal(list)
    progressBarValue = pyqtSignal(int)  # 更新进度条
    signal_done = pyqtSignal(int)  # 是否结束信号

    def __init__(self):
        super(WorkThread, self).__init__()

    def run(self):
        # try:
        # global path
        # self.nihe, self.xishus = css.efficacy(self, self.path, self.new_data)

        # ******************计算调控功效过程
        # def efficacy(self, path, data):
        global nihe_jdt, xishu_jdt
        try:
            data = pd.read_pickle(path_jdt)
        except Exception as e:
            print(e)
            return
        d_flats_nihe = data.values[:, -80:]
        x = np.linspace(-1, 1, 80)
        d_w = data.values[:, :-80]
        my_sgd = LsAdam(0.3)
        param = {"eff": np.zeros((d_w.shape[1], d_flats_nihe.shape[1]))}
        # 显示进度条
        self.progressBarValue.emit(2)
        for i in range(1000):
            grad = {"eff": get_dJ(d_w, d_flats_nihe, param["eff"])}
            J = get_J(d_w, d_flats_nihe, param["eff"])
            # 显示进度条，按比例分配
            if i % 10 == 0:
                self.progressBarValue.emit(2 + int(i * 96 / 1000))

            if np.all(np.absolute(grad["eff"]) <= 1e-9):
                break
            my_sgd.update(param, grad)

        nihe = []
        xishus = []
        for i in range(param["eff"].shape[0]):
            xishu = my_leastq(param["eff"][i])
            xishus.append(xishu)
            flt = ls_lerangde_nihe(xishu, False)
            nihe.append(flt)
        # 显示进度条
        self.progressBarValue.emit(99)
        nihe_jdt, xishu_jdt = np.array(nihe), np.array(xishus)

        self.signal_done.emit(0)
        self.progressBarValue.emit(100)
        # self.signal_done.emit(1)
        self.trigger.emit(list(nihe_jdt))  # 子线程传递参数
        self.trigger2.emit(list(xishu_jdt))  # 子线程传递参数
        # except:
        #     self.progressBarValue.emit(0)
        #     self.signal_done.emit(2)
        #     self.tishi.emit()


# **************子线程计算部分结束*********************************************


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)  # 生成程序
    w = 板形调控功效挖掘()  # 用窗体的类生产实例
    w.show()  # 显示窗体
    sys.exit(app.exec_())  # 关闭程序，返回退出类型 正常0 异常1
