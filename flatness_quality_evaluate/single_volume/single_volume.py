# -*- coding: utf-8 -*-

"""
Module implementing FullLengthQuality.
"""
import os

import numpy as np
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from flatness_quality_evaluate.single_volume.Ui_single_volume import Ui_MainWindow
from flatness_quality_evaluate.utils import Wlearn, fig
from flatness_quality_evaluate.utils.Wlearn import base_file_name
from flatness_quality_evaluate.utils.flatpingjia import iu_percent_fendaitou, IU_zhibiao_fendaitou, shuju, shuju_redutu, \
    shuju_langxin, \
    langhxing_fenbu, langhxing_fenbufuza, iu_percent, IU_mean, IU_zhibiao
from flatness_quality_evaluate.utils.draw_pic import iu_error, get_rms, get_cha


class FullLengthQuality(QMainWindow, Ui_MainWindow):
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
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.pushButton_4.setEnabled(False)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        tmp = os.path.abspath(__file__)
        path = QFileDialog.getOpenFileName(self, u"打开文件", tmp, "CSV Files(*.csv);;XLSX Files(*.xlsx)")
        self.lineEdit.setText(path[0])
        if path[0] != '':
            self.pushButton_2.setEnabled(True)
            self.pushButton_3.setEnabled(True)
            self.pushButton_4.setEnabled(True)

    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        """
        Slot documentation goes here.
        """
        # pass
        if self.lineEdit.text() != '':
            path = self.lineEdit.text()
        else:
            # self.cwd = os.getcwd()  # 获取当前程序文件位置
            tmp = os.path.abspath(__file__)
            self.cwd = os.path.dirname(tmp)
            print(self.cwd.replace('\\', '/'))
            path = self.cwd.replace('\\', '/') + '/HB19B14703700_1flat.csv'
            self.lineEdit.setText(path)
        try:
            data = pd.read_csv(path, header=0, encoding='gbk')
            name = base_file_name(path)[:15]
            flat = data.values[:, -62:] / -2100000
            pot1, pot2, row_pot = Wlearn.jugde_row_col(flat)
            data = data.iloc[:row_pot, :]
            useflat = flat[:row_pot, pot1:pot2]
            iu_mean = []
            iu_rms = []
            iu_max = []
            iu_max_min = []
            for i in useflat:
                iu_mean.append(iu_error(i))
                iu_rms.append(get_rms(i))
                iu_max.append(max(abs(i)))
                iu_max_min.append(get_cha(i))
            avg_iu_mean = np.array(iu_mean).mean()
            avg_iu_rms = np.array(iu_rms).mean()
            avg_iu_max = np.array(iu_max).mean()
            avg_iu_max_min = np.array(iu_max_min).mean()
            iu = [avg_iu_mean, avg_iu_rms, avg_iu_max, avg_iu_max_min]

            # 带头部分
            daitou = data[data['POS'] < 100]
            flat_daitou = daitou.values[:, -62:] / -2100000
            flat_daitou = flat_daitou[:, pot1:pot2]
            iu_mean1 = []
            iu_rms1 = []
            iu_max1 = []
            iu_max_min1 = []
            for i in flat_daitou:
                iu_mean1.append(iu_error(i))
                iu_rms1.append(get_rms(i))
                iu_max1.append(max(abs(i)))
                iu_max_min1.append(get_cha(i))
            avg_iu_mean1 = np.array(iu_mean1).mean()
            avg_iu_rms1 = np.array(iu_rms1).mean()
            avg_iu_max1 = np.array(iu_max1).mean()
            avg_iu_max_min1 = np.array(iu_max_min1).mean()
            iu1 = [avg_iu_mean1, avg_iu_rms1, avg_iu_max1, avg_iu_max_min1]
            # 带尾部分
            dg_length = data['POS'].iloc[-1]
            daiwei = data[data['POS'] > dg_length - 100]
            flat_daiwei = daiwei.values[:, -62:] / -2100000
            flat_daiwei = flat_daiwei[:, pot1:pot2]
            iu_mean3 = []
            iu_rms3 = []
            iu_max3 = []
            iu_max_min3 = []
            for i in flat_daiwei:
                iu_mean3.append(iu_error(i))
                iu_rms3.append(get_rms(i))
                iu_max3.append(max(abs(i)))
                iu_max_min3.append(get_cha(i))
            avg_iu_mean3 = np.array(iu_mean3).mean()
            avg_iu_rms3 = np.array(iu_rms3).mean()
            avg_iu_max3 = np.array(iu_max3).mean()
            avg_iu_max_min3 = np.array(iu_max_min3).mean()
            iu3 = [avg_iu_mean3, avg_iu_rms3, avg_iu_max3, avg_iu_max_min3]
            # 带中部分
            daizhong = data[(data['POS'] >= 100) & (data['POS'] <= dg_length - 100)]
            flat_daizhong = daizhong.values[:, -62:] / -2100000
            flat_daizhong = flat_daizhong[:, pot1:pot2]
            iu_mean2 = []
            iu_rms2 = []
            iu_max2 = []
            iu_max_min2 = []
            for i in flat_daizhong:
                iu_mean2.append(iu_error(i))
                iu_rms2.append(get_rms(i))
                iu_max2.append(max(abs(i)))
                iu_max_min2.append(get_cha(i))
            avg_iu_mean2 = np.array(iu_mean2).mean()
            avg_iu_rms2 = np.array(iu_rms2).mean()
            avg_iu_max2 = np.array(iu_max2).mean()
            avg_iu_max_min2 = np.array(iu_max_min2).mean()
            iu2 = [avg_iu_mean2, avg_iu_rms2, avg_iu_max2, avg_iu_max_min2]

            columns = ['IU绝对值均值', 'IU均方根均值', 'IU最大值均值', 'IU最大-最小均值']
            index = ['全长', '带头100米', '带中', '带尾100米']
            res = [iu, iu1, iu2, iu3]
            df = pd.DataFrame(res, columns=columns, index=index)

            # 打开文件对话框，获取保存文件路径
            file_path, _ = QFileDialog.getSaveFileName(self, 'Save CSV File', '', 'CSV Files (*.csv)')

            if file_path:
                # 将 DataFrame 保存为 CSV 文件
                df.to_csv(file_path, index=False)
                print(f"DataFrame saved to {file_path}")

        except Exception as e:
            print(e)
            QMessageBox.information(self, '警告信息', '文件选择出错')

    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        """
        Slot documentation goes here.
        """
        for i in range(1, self.gridLayout.count()):
            self.gridLayout.itemAt(i).widget().deleteLater()

        if self.lineEdit.text() != '':
            path = self.lineEdit.text()
        else:
            # 生成资源文件目录访问路径 相对路径
            import sys
            def resource_path(relative_path):
                if getattr(sys, 'frozen', False):  # 是否Bundle Resource 捆绑资源
                    base_path = sys._MEIPASS
                else:
                    base_path = os.path.abspath(".")
                return os.path.join(base_path, relative_path)

            self.cwd = os.getcwd()  # 获取当前程序文件位置
            print(self.cwd.replace('\\', '/'))
            path = resource_path(self.cwd.replace('\\', '/') + '板形综合评价报表/single_volume/HB19B14703700_1flat.csv')
            self.lineEdit.setText(path)
        # print(path)
        name = self.comboBox_3.currentText()
        print(name)

        # try:
        if name == '三维板形':
            self.graphicsView.setVisible(False)
            self.F = Figure(figsize=(12, 10))
            self.canvas = FigureCanvas(self.F)
            self.gridLayout.addWidget(self.canvas)
            self.gridLayout.addWidget(NavigationToolbar(self.canvas, self))
            a = shuju(path)
            fig.threedbanxing(self.F, a)

        elif name == '热度图':
            self.graphicsView.setVisible(False)
            self.F = Figure()
            self.canvas = FigureCanvas(self.F)
            self.gridLayout.addWidget(self.canvas)
            self.gridLayout.addWidget(NavigationToolbar(self.canvas, self))
            flat_3D, X, Y = shuju_redutu(path)
            fig.redutu(self.F, X, Y, flat_3D)

        elif name == '浪形模态图-绝对值均值':
            jiaodu1, iu1, jiaodu2, iu2, colors = shuju_langxin(path, 1)
            self.graphicsView.setVisible(False)
            self.F = Figure(figsize=(4, 2))
            self.canvas = FigureCanvas(self.F)
            self.gridLayout.addWidget(self.canvas)
            self.gridLayout.addWidget(NavigationToolbar(self.canvas, self))
            fig.langxingmotai(self.F, jiaodu1, iu1, jiaodu2, iu2, colors, 1)


        elif name == '浪形模态图-均方根':
            jiaodu1, iu1, jiaodu2, iu2, colors = shuju_langxin(path, 2)
            self.graphicsView.setVisible(False)
            self.F = Figure()
            self.canvas = FigureCanvas(self.F)
            self.gridLayout.addWidget(self.canvas)
            self.gridLayout.addWidget(NavigationToolbar(self.canvas, self))
            fig.langxingmotai(self.F, jiaodu1, iu1, jiaodu2, iu2, colors, 2)
            # self.gridlayout = QGridLayout(self.widget)  # 继承容器


        elif name == '浪形模态图-最大-最小':
            jiaodu1, iu1, jiaodu2, iu2, colors = shuju_langxin(path, 3)
            self.graphicsView.setVisible(False)
            self.F = Figure()
            self.canvas = FigureCanvas(self.F)
            self.gridLayout.addWidget(self.canvas)
            self.gridLayout.addWidget(NavigationToolbar(self.canvas, self))
            fig.langxingmotai(self.F, jiaodu1, iu1, jiaodu2, iu2, colors, 3)


        elif name == '浪形百分比':
            p_result = langhxing_fenbu(path)
            self.graphicsView.setVisible(False)
            self.F = Figure()
            self.canvas = FigureCanvas(self.F)
            self.gridLayout.addWidget(self.canvas)
            self.gridLayout.addWidget(NavigationToolbar(self.canvas, self))
            fig.langxingfenbu1(self.F, p_result)

        elif name == 'IU百分比':

            p_result = iu_percent(path)
            self.graphicsView.setVisible(False)
            self.F = Figure()
            self.canvas = FigureCanvas(self.F)
            self.gridLayout.addWidget(self.canvas)
            self.gridLayout.addWidget(NavigationToolbar(self.canvas, self))
            fig.IUfenbu1(self.F, p_result)


        elif name == 'IU概率密度图':
            p_result = IU_mean(path)
            self.graphicsView.setVisible(False)
            self.F = Figure()
            self.canvas = FigureCanvas(self.F)
            self.gridLayout.addWidget(self.canvas)
            self.gridLayout.addWidget(NavigationToolbar(self.canvas, self))
            fig_path = fig.Gailvmidutu(self.F, p_result)

            if os.path.exists(fig_path):  # 如果文件存在
                # 删除文件，可使用以下两种方法。
                os.remove(fig_path)

        elif name == 'IU的4个指标折线图':
            iu_mean, iu_max, iu_max_min, iu_rms = IU_zhibiao(path)
            self.graphicsView.setVisible(False)
            self.F = Figure()
            self.canvas = FigureCanvas(self.F)
            self.gridLayout.addWidget(self.canvas)
            self.gridLayout.addWidget(NavigationToolbar(self.canvas, self))
            fig.zhexiantu(self.F, iu_mean, iu_max, iu_rms, iu_max_min)

        elif name == '浪形百分比-复杂浪形':
            p_result = langhxing_fenbufuza(path)
            self.graphicsView.setVisible(False)
            self.F = Figure()
            self.canvas = FigureCanvas(self.F)
            self.gridLayout.addWidget(self.canvas)
            self.gridLayout.addWidget(NavigationToolbar(self.canvas, self))
            fig.langxingfenbu2(self.F, p_result)

        # except:
        #     my_button = QMessageBox.information(self, '警告信息', '文件选择出错')

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        # 带头部分

        for i in range(1, self.gridLayout_2.count()):
            self.gridLayout_2.itemAt(i).widget().deleteLater()
        # 带中部分
        for i in range(1, self.gridLayout_3.count()):
            self.gridLayout_3.itemAt(i).widget().deleteLater()
        # 带尾部分
        for i in range(1, self.gridLayout_5.count()):
            self.gridLayout_5.itemAt(i).widget().deleteLater()

        if self.lineEdit.text() != '':
            path = self.lineEdit.text()
        else:
            self.cwd = os.getcwd()  # 获取当前程序文件位置
            print(self.cwd.replace('\\', '/'))
            path = self.cwd.replace('\\', '/') + '/HB19B14703700_1flat.csv'
            self.lineEdit.setText(path)
        # print(path)
        zhibiao = self.comboBox.currentText()
        fangfa = self.comboBox_2.currentText()

        # try:
        if fangfa == '百分比分布' and zhibiao == 'IU绝对值均值':
            p_result0, p_result1, p_result2 = iu_percent_fendaitou(path, zhibiao)
            self.graphicsView_2.setVisible(False)
            self.F = Figure()
            self.canvas = FigureCanvas(self.F)
            # self.F_ntb = NavigationToolbar(self.canvas, self)
            self.gridLayout_2.addWidget(self.canvas)
            self.gridLayout_2.addWidget(NavigationToolbar(self.canvas, self))
            fig.IUfenbu(self.F, p_result0)

            self.graphicsView_3.setVisible(False)
            self.F = Figure()
            self.canvas = FigureCanvas(self.F)
            # self.F_ntb = NavigationToolbar(self.canvas, self)
            self.gridLayout_3.addWidget(self.canvas)
            self.gridLayout_3.addWidget(NavigationToolbar(self.canvas, self))
            fig.IUfenbu(self.F, p_result1)

            self.graphicsView_4.setVisible(False)
            self.F = Figure()
            self.canvas = FigureCanvas(self.F)
            # self.F_ntb = NavigationToolbar(self.canvas, self)
            self.gridLayout_5.addWidget(self.canvas)
            self.gridLayout_5.addWidget(NavigationToolbar(self.canvas, self))
            fig.IUfenbu(self.F, p_result2)


        elif fangfa == '百分比分布' and zhibiao == 'IU均方根':
            p_result0, p_result1, p_result2 = iu_percent_fendaitou(path, zhibiao)
            self.graphicsView_2.setVisible(False)
            self.F = Figure()
            self.canvas = FigureCanvas(self.F)
            # self.F_ntb = NavigationToolbar(self.canvas, self)
            self.gridLayout_2.addWidget(self.canvas)
            self.gridLayout_2.addWidget(NavigationToolbar(self.canvas, self))
            fig.IUfenbu(self.F, p_result0)

            self.graphicsView_3.setVisible(False)
            self.F = Figure()
            self.canvas = FigureCanvas(self.F)
            # self.F_ntb = NavigationToolbar(self.canvas, self)
            self.gridLayout_3.addWidget(self.canvas)
            self.gridLayout_3.addWidget(NavigationToolbar(self.canvas, self))
            fig.IUfenbu(self.F, p_result1)

            self.graphicsView_4.setVisible(False)
            self.F = Figure()
            self.canvas = FigureCanvas(self.F)
            # self.F_ntb = NavigationToolbar(self.canvas, self)
            self.gridLayout_5.addWidget(self.canvas)
            self.gridLayout_5.addWidget(NavigationToolbar(self.canvas, self))
            fig.IUfenbu(self.F, p_result2)

        elif fangfa == '百分比分布' and zhibiao == 'IU最大-最小':
            p_result0, p_result1, p_result2 = iu_percent_fendaitou(path, zhibiao)
            self.graphicsView_2.setVisible(False)
            self.F = Figure()
            self.canvas = FigureCanvas(self.F)
            # self.F_ntb = NavigationToolbar(self.canvas, self)
            self.gridLayout_2.addWidget(self.canvas)
            self.gridLayout_2.addWidget(NavigationToolbar(self.canvas, self))
            fig.IUfenbu(self.F, p_result0)

            self.graphicsView_3.setVisible(False)
            self.F = Figure()
            self.canvas = FigureCanvas(self.F)
            # self.F_ntb = NavigationToolbar(self.canvas, self)
            self.gridLayout_3.addWidget(self.canvas)
            self.gridLayout_3.addWidget(NavigationToolbar(self.canvas, self))
            fig.IUfenbu(self.F, p_result1)

            self.graphicsView_4.setVisible(False)
            self.F = Figure()
            self.canvas = FigureCanvas(self.F)
            # self.F_ntb = NavigationToolbar(self.canvas, self)
            self.gridLayout_5.addWidget(self.canvas)
            self.gridLayout_5.addWidget(NavigationToolbar(self.canvas, self))
            fig.IUfenbu(self.F, p_result2)

        elif fangfa == '百分比分布' and zhibiao == 'IU最大值':
            p_result0, p_result1, p_result2 = iu_percent_fendaitou(path, zhibiao)
            self.graphicsView_2.setVisible(False)
            self.F = Figure()
            self.canvas = FigureCanvas(self.F)
            # self.F_ntb = NavigationToolbar(self.canvas, self)
            self.gridLayout_2.addWidget(self.canvas)
            self.gridLayout_2.addWidget(NavigationToolbar(self.canvas, self))
            fig.IUfenbu(self.F, p_result0)

            self.graphicsView_3.setVisible(False)
            self.F = Figure()
            self.canvas = FigureCanvas(self.F)
            # self.F_ntb = NavigationToolbar(self.canvas, self)
            self.gridLayout_3.addWidget(self.canvas)
            self.gridLayout_3.addWidget(NavigationToolbar(self.canvas, self))
            fig.IUfenbu(self.F, p_result1)

            self.graphicsView_4.setVisible(False)
            self.F = Figure()
            self.canvas = FigureCanvas(self.F)
            # self.F_ntb = NavigationToolbar(self.canvas, self)
            self.gridLayout_5.addWidget(self.canvas)
            self.gridLayout_5.addWidget(NavigationToolbar(self.canvas, self))
            fig.IUfenbu(self.F, p_result2)

        elif fangfa == '概率密度图' and zhibiao == 'IU绝对值均值':
            iu1, iu2, iu3 = IU_zhibiao_fendaitou(path, zhibiao)
            self.graphicsView_2.setVisible(False)
            self.F = Figure()
            self.canvas = FigureCanvas(self.F)
            # self.F_ntb = NavigationToolbar(self.canvas, self)
            self.gridLayout_2.addWidget(self.canvas)
            self.gridLayout_2.addWidget(NavigationToolbar(self.canvas, self))
            fig_path = fig.Gailvmidutu(self.F, iu1)

            if os.path.exists(fig_path):  # 如果文件存在
                # 删除文件，可使用以下两种方法。
                os.remove(fig_path)
            self.graphicsView_3.setVisible(False)
            self.F = Figure()
            self.canvas = FigureCanvas(self.F)
            # self.F_ntb = NavigationToolbar(self.canvas, self)
            self.gridLayout_3.addWidget(self.canvas)
            self.gridLayout_3.addWidget(NavigationToolbar(self.canvas, self))
            fig_path = fig.Gailvmidutu(self.F, iu2)

            if os.path.exists(fig_path):  # 如果文件存在
                # 删除文件，可使用以下两种方法。
                os.remove(fig_path)

            self.graphicsView_4.setVisible(False)
            self.F = Figure()
            self.canvas = FigureCanvas(self.F)
            # self.F_ntb = NavigationToolbar(self.canvas, self)
            self.gridLayout_5.addWidget(self.canvas)
            self.gridLayout_5.addWidget(NavigationToolbar(self.canvas, self))
            fig_path = fig.Gailvmidutu(self.F, iu3)

            if os.path.exists(fig_path):  # 如果文件存在
                # 删除文件，可使用以下两种方法。
                os.remove(fig_path)

        elif fangfa == '概率密度图' and zhibiao == 'IU均方根':
            iu1, iu2, iu3 = IU_zhibiao_fendaitou(path, zhibiao)
            self.graphicsView_2.setVisible(False)
            self.F = Figure()
            self.canvas = FigureCanvas(self.F)
            # self.F_ntb = NavigationToolbar(self.canvas, self)
            self.gridLayout_2.addWidget(self.canvas)
            self.gridLayout_2.addWidget(NavigationToolbar(self.canvas, self))
            fig_path = fig.Gailvmidutu(self.F, iu1)

            if os.path.exists(fig_path):  # 如果文件存在
                # 删除文件，可使用以下两种方法。
                os.remove(fig_path)
            self.graphicsView_3.setVisible(False)
            self.F = Figure()
            self.canvas = FigureCanvas(self.F)
            # self.F_ntb = NavigationToolbar(self.canvas, self)
            self.gridLayout_3.addWidget(self.canvas)
            self.gridLayout_3.addWidget(NavigationToolbar(self.canvas, self))
            fig_path = fig.Gailvmidutu(self.F, iu2)

            if os.path.exists(fig_path):  # 如果文件存在
                # 删除文件，可使用以下两种方法。
                os.remove(fig_path)

            self.graphicsView_4.setVisible(False)
            self.F = Figure()
            self.canvas = FigureCanvas(self.F)
            # self.F_ntb = NavigationToolbar(self.canvas, self)
            self.gridLayout_5.addWidget(self.canvas)
            self.gridLayout_5.addWidget(NavigationToolbar(self.canvas, self))
            fig_path = fig.Gailvmidutu(self.F, iu3)
            if os.path.exists(fig_path):  # 如果文件存在
                # 删除文件，可使用以下两种方法。
                os.remove(fig_path)

        elif fangfa == '概率密度图' and zhibiao == 'IU最大-最小':
            iu1, iu2, iu3 = IU_zhibiao_fendaitou(path, zhibiao)
            self.graphicsView_2.setVisible(False)
            self.F = Figure()
            self.canvas = FigureCanvas(self.F)
            # self.F_ntb = NavigationToolbar(self.canvas, self)
            self.gridLayout_2.addWidget(self.canvas)
            self.gridLayout_2.addWidget(NavigationToolbar(self.canvas, self))
            fig_path = fig.Gailvmidutu(self.F, iu1)

            if os.path.exists(fig_path):  # 如果文件存在
                # 删除文件，可使用以下两种方法。
                os.remove(fig_path)
            self.graphicsView_3.setVisible(False)
            self.F = Figure()
            self.canvas = FigureCanvas(self.F)
            # self.F_ntb = NavigationToolbar(self.canvas, self)
            self.gridLayout_3.addWidget(self.canvas)
            self.gridLayout_3.addWidget(NavigationToolbar(self.canvas, self))
            fig_path = fig.Gailvmidutu(self.F, iu2)

            if os.path.exists(fig_path):  # 如果文件存在
                # 删除文件，可使用以下两种方法。
                os.remove(fig_path)

            self.graphicsView_4.setVisible(False)
            self.F = Figure()
            self.canvas = FigureCanvas(self.F)
            # self.F_ntb = NavigationToolbar(self.canvas, self)
            self.gridLayout_5.addWidget(self.canvas)
            self.gridLayout_5.addWidget(NavigationToolbar(self.canvas, self))
            fig_path = fig.Gailvmidutu(self.F, iu3)
            if os.path.exists(fig_path):  # 如果文件存在
                # 删除文件，可使用以下两种方法。
                os.remove(fig_path)

        elif fangfa == '概率密度图' and zhibiao == 'IU最大值':
            iu1, iu2, iu3 = IU_zhibiao_fendaitou(path, zhibiao)
            self.graphicsView_2.setVisible(False)
            self.F = Figure()
            self.canvas = FigureCanvas(self.F)
            # self.F_ntb = NavigationToolbar(self.canvas, self)
            self.gridLayout_2.addWidget(self.canvas)
            self.gridLayout_2.addWidget(NavigationToolbar(self.canvas, self))
            fig_path = fig.Gailvmidutu(self.F, iu1)

            if os.path.exists(fig_path):  # 如果文件存在
                # 删除文件，可使用以下两种方法。
                os.remove(fig_path)
            self.graphicsView_3.setVisible(False)
            self.F = Figure()
            self.canvas = FigureCanvas(self.F)
            # self.F_ntb = NavigationToolbar(self.canvas, self)
            self.gridLayout_3.addWidget(self.canvas)
            self.gridLayout_3.addWidget(NavigationToolbar(self.canvas, self))
            fig_path = fig.Gailvmidutu(self.F, iu2)

            if os.path.exists(fig_path):  # 如果文件存在
                # 删除文件，可使用以下两种方法。
                os.remove(fig_path)

            self.graphicsView_4.setVisible(False)
            self.F = Figure()
            self.canvas = FigureCanvas(self.F)
            # self.F_ntb = NavigationToolbar(self.canvas, self)
            self.gridLayout_5.addWidget(self.canvas)
            self.gridLayout_5.addWidget(NavigationToolbar(self.canvas, self))
            fig_path = fig.Gailvmidutu(self.F, iu3)
            if os.path.exists(fig_path):  # 如果文件存在
                # 删除文件，可使用以下两种方法。
                os.remove(fig_path)
        # except:
        #     my_button = QMessageBox.information(self, '警告信息', '文件选择出错')


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = FullLengthQuality()
    ui.show()
    sys.exit(app.exec())
