# -*- coding: utf-8 -*-

"""
Module implementing Dialog_3.
"""
import os

import numpy as np
import pandas as pd
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QMessageBox
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from accidental_interference.roller.view.Ui_rolling_time_weight import Ui_RollingInfo
from accidental_interference.roller.controller.myplot import MyFigure


class RollingInfo(QDialog, Ui_RollingInfo):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (defaults to None)
        @type QWidget (optional)
        """
        super(RollingInfo, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(
            QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.WindowMinimizeButtonHint)

        self.comboBox_IMR.setEnabled(False)
        self.comboBox_WR.setEnabled(False)
        self.comboBox_BUR.setEnabled(False)
        # self.comboBox_steel.setEnabled(False)
        self.pushButton_BUR.setEnabled(False)
        self.pushButton_BUR_shang.setVisible(False)
        self.pushButton_BUR_xia.setVisible(False)
        self.pushButton_IMR.setEnabled(False)
        self.pushButton_IMR_shang.setEnabled(False)
        self.pushButton_IMR_xia.setEnabled(False)
        self.pushButton_WR.setEnabled(False)
        self.pushButton_WR_xia.setEnabled(False)
        self.pushButton_WR_shang.setEnabled(False)
        # self.pushButton.setEnabled(False)
        # self.biaozhun = 0
        self.lineEdit_WR.setReadOnly(True)
        self.lineEdit_IMR.setReadOnly(True)
        self.textEdit.setReadOnly(True)
        self.textEdit_2.setReadOnly(True)
        self.textEdit_3.setReadOnly(True)

    @pyqtSlot(str)
    def on_comboBox_jijia_activated(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type str
        """
        try:
            self.jijia = p0
            self.imr2wr = np.load(os.path.dirname(os.path.dirname(__file__)) + '\\data\\npy\imr2wr_%s.npy' % p0,
                                  allow_pickle=True).item()
            self.bur2imr = np.load(os.path.dirname(os.path.dirname(__file__)) + '\\data\\npy\\bur2imr_%s.npy' % p0,
                                   allow_pickle=True).item()
            # self.wr2steel = np.load(os.getcwd() + '\\npy\\wr2quality_%s.npy' % p0, allow_pickle=True).item()
            self.comboBox_BUR.clear()

            self.comboBox_BUR.addItems(self.bur2imr.keys())
            self.comboBox_BUR.setEnabled(True)
        except:
            QMessageBox.information(self, '提示框', '机架选择出错', QMessageBox.Ok)

    @pyqtSlot(str)
    def on_comboBox_BUR_activated(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type str
        """
        try:
            self.comboBox_IMR.setEnabled(True)
            self.pushButton_BUR.setEnabled(True)
            self.comboBox_IMR.clear()
            self.BUR = p0
            imr = self.bur2imr[p0]
            self.comboBox_IMR.addItems(imr)
        except:
            QMessageBox.information(self, '提示框', '支撑辊选择出错', QMessageBox.Ok)

    @pyqtSlot(str)
    def on_comboBox_IMR_activated(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type str
        """
        try:
            self.comboBox_WR.setEnabled(True)
            self.pushButton_IMR.setEnabled(True)
            self.comboBox_WR.clear()
            self.IMR = p0
            wr = self.imr2wr[p0]
            self.comboBox_WR.addItems(wr)
            xuhao = int(self.bur2imr[self.comboBox_BUR.currentText()].index(p0) / 2) + 1
            zong = int(len(self.bur2imr[self.comboBox_BUR.currentText()]) / 2)
            self.lineEdit_IMR.setText('%s/%s' % (xuhao, zong))
        except:
            QMessageBox.information(self, '提示框', '中间辊选择出错', QMessageBox.Ok)

    @pyqtSlot(str)
    def on_comboBox_WR_activated(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type str
        """
        # self.comboBox_steel.setEnabled(True)
        try:
            self.pushButton_WR.setEnabled(True)
            self.WR = p0
            # self.comboBox_steel.clear()
            # steel = self.wr2steel[p0]
            # self.comboBox_steel.addItems(steel)
            xuhao = int(self.imr2wr[self.comboBox_IMR.currentText()].index(p0) / 2) + 1
            zong = int(len(self.imr2wr[self.comboBox_IMR.currentText()]) / 2)
            self.lineEdit_WR.setText('%s/%s' % (xuhao, zong))
        except:
            QMessageBox.information(self, '提示框', '工作辊选择出错', QMessageBox.Ok)

    @pyqtSlot()
    def on_pushButton_BUR_shang_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_pushButton_BUR_clicked(self):
        """
        Slot documentation goes here.
        """
        try:
            self.textEdit.setVisible(False)
        except:
            pass
        try:
            self.horizontalLayout_BUR.itemAt(1).widget().deleteLater()
            self.verticalLayout.itemAt(0).widget().deleteLater()
        except:
            pass
        try:
            F = self.fuyiqi_plot(self.BUR, 'BUR')
            self.horizontalLayout_BUR.addWidget(F)
            mpl_ntb = NavigationToolbar(F, self)
            self.verticalLayout.addWidget(mpl_ntb)
        except:
            QMessageBox.information(self, '提示框', '轧辊为空', QMessageBox.Ok)

    @pyqtSlot()
    def on_pushButton_BUR_xia_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_pushButton_IMR_shang_clicked(self):
        """
        Slot documentation goes here.
        """
        try:
            self.imr_index = self.imr_index - 2
            try:
                self.textEdit_2.setVisible(False)
            except:
                pass
            try:
                self.horizontalLayout_IMR.itemAt(1).widget().deleteLater()
                self.verticalLayout_2.itemAt(0).widget().deleteLater()
            except:
                pass
            if self.imr_index > -1:
                shangyige = self.bur2imr[self.BUR][self.imr_index]
                F = self.fuyiqi_plot(shangyige, 'IMR')
                self.horizontalLayout_IMR.addWidget(F)
                mpl_ntb = NavigationToolbar(F, self)
                self.verticalLayout_2.addWidget(mpl_ntb)
            else:
                QMessageBox.information(self, '提示框', '当前中间辊已是支撑辊服役期的第一个', QMessageBox.Ok)
                self.textEdit_2.setVisible(True)
        except:
            QMessageBox.information(self, '提示框', '请先显示当前轧辊图像', QMessageBox.Ok)

    @pyqtSlot()
    def on_pushButton_IMR_clicked(self):
        """
        Slot documentation goes here.
        """
        try:
            try:
                self.textEdit_2.setVisible(False)
            except:
                pass
            self.imr_index = self.bur2imr[self.BUR].index(self.IMR)
            try:
                self.horizontalLayout_IMR.itemAt(1).widget().deleteLater()
                self.verticalLayout_2.itemAt(0).widget().deleteLater()
            except:
                pass
            F = self.fuyiqi_plot(self.IMR, 'IMR')
            self.horizontalLayout_IMR.addWidget(F)
            mpl_ntb = NavigationToolbar(F, self)
            self.verticalLayout_2.addWidget(mpl_ntb)

            self.pushButton_IMR_xia.setEnabled(True)
            self.pushButton_IMR_shang.setEnabled(True)
        except Exception as e:
            print(e)
            QMessageBox.information(self, '提示框', '请先选择轧辊号', QMessageBox.Ok)

    @pyqtSlot()
    def on_pushButton_IMR_xia_clicked(self):
        """
        Slot documentation goes here.
        """
        try:
            self.imr_index = self.imr_index + 2
            try:
                self.textEdit_2.setVisible(False)
            except:
                pass
            try:
                self.horizontalLayout_IMR.itemAt(1).widget().deleteLater()
                self.verticalLayout_2.itemAt(0).widget().deleteLater()
            except:
                pass
            if self.imr_index <= len(self.bur2imr[self.BUR]):
                xiayige = self.bur2imr[self.BUR][self.imr_index]
                F = self.fuyiqi_plot(xiayige, 'IMR')
                self.horizontalLayout_IMR.addWidget(F)
                mpl_ntb = NavigationToolbar(F, self)
                self.verticalLayout_2.addWidget(mpl_ntb)
            else:
                QMessageBox.information(self, '提示框', '当前中间辊已是支撑辊服役期的最后一个', QMessageBox.Ok)
                self.textEdit_2.setVisible(True)
        except:
            QMessageBox.information(self, '提示框', '请先显示当前轧辊图像', QMessageBox.Ok)

    @pyqtSlot()
    def on_pushButton_WR_shang_clicked(self):
        """
        Slot documentation goes here.
        """
        try:
            self.wr_index -= 2
            try:
                self.textEdit_3.setVisible(False)
            except:
                pass
            try:
                self.horizontalLayout_WR.itemAt(1).widget().deleteLater()
                self.verticalLayout_3.itemAt(0).widget().deleteLater()
            except:
                pass
            if self.wr_index > -1:
                F = self.fuyiqi_plot(self.imr2wr[self.IMR][self.wr_index], 'WR')
                self.horizontalLayout_WR.addWidget(F)
                mpl_ntb = NavigationToolbar(F, self)
                self.verticalLayout_3.addWidget(mpl_ntb)
            else:
                QMessageBox.information(self, '提示框', '当前工作辊已是中间辊服役期的第一个', QMessageBox.Ok)
                self.textEdit_3.setVisible(True)
        except:
            QMessageBox.information(self, '提示框', '请先显示当前轧辊图像', QMessageBox.Ok)

    @pyqtSlot()
    def on_pushButton_WR_clicked(self):
        """
        Slot documentation goes here.
        """
        try:
            try:
                self.textEdit_3.setVisible(False)
            except:
                pass
            self.wr_index = self.imr2wr[self.IMR].index(self.WR)
            try:
                self.horizontalLayout_WR.itemAt(1).widget().deleteLater()
                self.verticalLayout_3.itemAt(0).widget().deleteLater()
            except:
                pass
            F = self.fuyiqi_plot(self.WR, 'WR')
            self.horizontalLayout_WR.addWidget(F)
            mpl_ntb = NavigationToolbar(F, self)
            self.verticalLayout_3.addWidget(mpl_ntb)

            self.pushButton_WR_xia.setEnabled(True)
            self.pushButton_WR_shang.setEnabled(True)
        except:
            QMessageBox.information(self, '提示框', '请先选择轧辊号', QMessageBox.Ok)

    @pyqtSlot()
    def on_pushButton_WR_xia_clicked(self):
        """
        Slot documentation goes here.
        """
        try:
            self.wr_index += 2
            try:
                self.textEdit_3.setVisible(False)
            except:
                pass
            try:
                self.horizontalLayout_WR.itemAt(1).widget().deleteLater()
                self.verticalLayout_3.itemAt(0).widget().deleteLater()
            except:
                pass
            if self.wr_index < len(self.imr2wr[self.IMR]):
                F = self.fuyiqi_plot(self.imr2wr[self.IMR][self.wr_index], 'WR')
                self.horizontalLayout_WR.addWidget(F)
                mpl_ntb = NavigationToolbar(F, self)
                self.verticalLayout_3.addWidget(mpl_ntb)
            else:
                QMessageBox.information(self, '提示框', '当前工作辊已是中间辊服役期的最后一个', QMessageBox.Ok)
                self.textEdit_3.setVisible(True)
        except:

            QMessageBox.information(self, '提示框', '请先显示当前轧辊图像', QMessageBox.Ok)

    def fuyiqi_plot(self, zhagunhao, zhagunleixing):

        wr_iu_dir_path = os.path.dirname(
            os.path.dirname(__file__)) + '\data\换辊记录匹配iu值\工作辊\%s机架' % self.jijia
        imr_iu_dir_path = os.path.dirname(
            os.path.dirname(__file__)) + '\data\换辊记录匹配iu值\中间辊\%s机架' % self.jijia
        bur_iu_dir_path = os.path.dirname(
            os.path.dirname(__file__)) + '\data\换辊记录匹配iu值\支撑辊\%s机架' % self.jijia

        imr2wr = self.imr2wr
        bur2imr = self.bur2imr

        if zhagunleixing == 'BUR':
            roll_dict = bur2imr
            child_zhagunhao = roll_dict[zhagunhao]
            df = pd.read_excel('%s\%s%s' % (bur_iu_dir_path, zhagunhao, '.xlsx'), header=0)

            if len(df['辊号']) != 0:
                start = df.loc[0, '上机时间']
                end = df.loc[len(df) - 1, '下机时间']
                xtickslabel = []
                for i_str in range(len(df)):
                    xtickslabel.append('')
                xtickslabel[0] = start
                xtickslabel[-1] = end
                iu_mean = df['均值']
                weight = df['轧制重量(t)']
                days_ = (df['下机时间'] - df['上机时间']).map(lambda x: x / np.timedelta64(1, 'h')).abs()
            else:
                iu_mean = 0
                child_zhagunhao = []

        if zhagunleixing == 'IMR':
            roll_dict = imr2wr
            child_zhagunhao = roll_dict[zhagunhao]
            df = pd.read_excel('%s\%s%s' % (imr_iu_dir_path, zhagunhao, '.xlsx'), header=0)
            if len(df['辊号']) != 0:
                start = df.loc[0, '上机时间']
                end = df.loc[len(df) - 1, '下机时间']
                xtickslabel = []
                for i_str in range(len(df)):
                    xtickslabel.append('')
                xtickslabel[0] = start
                xtickslabel[-1] = end
                iu_mean = df['均值']
                weight = df['轧制重量(t)']
                days_ = (df['下机时间'] - df['上机时间']).map(lambda x: x / np.timedelta64(1, 'h')).abs()

            else:
                iu_mean = 0
                child_zhagunhao = []

        if zhagunleixing == 'WR':
            df = pd.read_excel('%s\%s%s' % (wr_iu_dir_path, zhagunhao, '.xlsx'), header=0)
            df = df.fillna(0)
            if len(df['入口材料号']) != 0:
                start = df.loc[0, '开始生产时刻']
                end = df.loc[len(df) - 1, '结束生产时刻']
                xtickslabel = []
                for i_str in range(len(df)):
                    xtickslabel.append('')
                xtickslabel[0] = start
                xtickslabel[-1] = end
                child_zhagunhao = df['入口材料号']
                iu_mean = df['均值']
                weight = df['出口材料实际重量']
                days_ = (df['结束生产时刻'] - df['开始生产时刻']).map(lambda x: x / np.timedelta64(1, 'h')).abs()

            else:
                child_zhagunhao = []
                iu_mean = 0

        x_name = child_zhagunhao
        x_name = xtickslabel

        # print(x_name)
        # x_name=
        x = range(len(days_))
        plt.rcParams['font.family'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        F = MyFigure(width=8, height=10, dpi=100)
        # axes=F.figure.subplots(1,1)
        axes = F.fig.add_subplot(111)
        axes.bar(x, days_, label='服役时间')
        axes.set_title(zhagunleixing + '：' + zhagunhao)
        axes.set_xticks(x)
        axes.set_xticklabels(x_name, rotation=0, ha='center')
        # axes.set_xlabel('轧辊先后顺序', size=15)
        axes.set_ylabel('服役时间/小时')
        axes.legend(loc='upper left')
        # F.fig.set_tight_layout()
        axes_1 = axes.twinx()
        axes_1.plot(weight, label='轧制重量', c='r', marker='.', markeredgecolor='b', markerfacecolor='b')
        axes_1.set_ylabel('轧制重量/t')
        axes_1.legend(loc='upper right')

        return F


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QMainWindow, QApplication

    app = QApplication(sys.argv)
    ui = RollingInfo()
    ui.show()
    sys.exit(app.exec_())
