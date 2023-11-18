# -*- coding: utf-8 -*-

"""
Module implementing MainWindowC2.
"""
import os

import joblib
import numpy as np
import pandas as pd
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from sklearn.metrics import confusion_matrix
from .myplot import MyFigure
from .Ui_板形缺陷有无预测 import Ui_MainWindowC2
import sys


class MainWindowC2(QMainWindow, Ui_MainWindowC2):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (defaults to None)
        @type QWidget (optional)
        """
        super(MainWindowC2, self).__init__(parent)
        self.setupUi(self)

        self.lineEdit.setReadOnly(True)
        self.textEdit.setReadOnly(True)
        self.textEdit_2.setReadOnly(True)
        self.comboBox_2.setVisible(False)

    @pyqtSlot()
    def on_help_triggered(self):
        from .帮助文档 import MainWindow
        self.help_ui = MainWindow()
        self.help_ui.show()

    @pyqtSlot(str)
    def on_comboBox_activated(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type str
        """
        try:
            self.textEdit.setText('您选择的模型为“%s”' % p0)

        except:
            QMessageBox.information(self, '提示信息', '模型选择出错', QMessageBox.Ok)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        数据
        """

        # 生成资源文件目录访问路径 相对路径
        def resource_path(relative_path):
            if getattr(sys, 'frozen', False):  # 是否Bundle Resource 捆绑资源
                base_path = sys._MEIPASS
            else:
                base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)

        # try:
        #     self.data_path = \
        #         QFileDialog.getOpenFileNames(self, "ADD", os.getcwd(), "CSV Files(*.csv);;XLSX Files(*.xlsx)")[0]
        #     self.data = pd.read_csv(self.data_path, encoding='gbk').dropna().reset_index(drop=True)
        #     feature = ['RCH2: Wedge passline deviation', 'RCH3: Wedge passline deviation', 'RCH4: Wedge passline deviation',
        #          'RCH5: Wedge passline deviation', 'F5 ref tension after stand 5',
        #          'F5 actual value after stand 5 smoothed', 'F5 flatness error tilt', 'F5  flatness error WR-bend',
        #          'F5  flatness error IR-bend', 'F5 flatness error','F5  flatness error IR-shift', 'F5 add tilt', 'F5 add WR-bend',
        #          'F5 add IR-bend', 'F5 add IR-shift', 'F5 strip length', 'F5 emulsion flow',
        #          'F5 release tilt control', 'F5 tilt control active', 'F5 release WR-bend control',
        #          'F5 WR-bend control active', 'F5 release IR-bend control', 'F5 IR-bend control active',
        #          'F5 release IR-shifting control', 'F5 IR-shifting control active', 'F5 IR-bending control active MONI',
        #          'F5 IR-shifting control active MONI', 'STAND_01_reduction', 'STAND_02_reduction', 'STAND_03_reduction',
        #          'STAND_04_reduction', 'STAND_05_reduction', 'THC: h ref. S1 entry(ims)', 'THC: h ref. S1 exit(ims)',
        #          'THC: act. thickness S1 entry', 'THC: act. thickness S1 exit', 'THX: h ref S5 exit',
        #          'THX: h act S5 exit', 'SLC laser speed behind S1', 'SLC laser speed behind S4',
        #          'SLC laser speed behind S5', 'SLC act. speed exit flatness roll', 'SLC act. speed stand 1',
        #          'SLC act. speed stand 2', 'SLC act. speed stand 3', 'SLC act speed stand 4', 'SLC act.speed stand 5',
        #          'SLC strip speed S1 - S2', 'SLC strip speed S2 - S3', 'SLC strip speed S3 - S4',
        #          'SLC strip speed S4 - S5', 'SLC strip speed after S5', 'SLC Slip factor stand 1',
        #          'SLC Slip factor stand 2', 'SLC Slip factor stand 3', 'SLC Slip factor stand 4',
        #          'SLC Slip factor stand 5', 'N1 ITC tension ref value', 'N1 ITC tension actual value DS',
        #          'N1 ITC tension actual value OS', 'N1 ITC tension actual value at ctrl', 'N1 ITC diff.tension at ctrl',
        #          'N2 ITC tension ref value', 'N2 ITC tension actual value DS', 'N2 ITC tension actual value OS',
        #          'N2 ITC tension actual value at ctrl', 'N2 ITC diff.tension at ctrl', 'N3 ITC tension ref value',
        #          'N3 ITC tension actual value DS', 'N3 ITC tension actual value OS',
        #          'N3 ITC tension actual value at ctrl', 'N3 ITC diff.tension at ctrl', 'N4 ITC tension ref value',
        #          'N4 ITC tension actual value DS', 'N4 ITC tension actual value OS',
        #          'N4 ITC tension actual value at ctrl', 'N4 ITC diff.tension at ctrl', 'N5 ITC tension ref value',
        #          'N5 ITC tension actual value DS', 'N5 ITC tension actual value OS',
        #          'N5 ITC tension actual value at ctrl', 'N5 ITC diff.tension at ctrl',
        #          'N5 tension actual value DS after S5', 'N5 tension actual value OS after S5',
        #          'D1 XSS position actual value', 'D1 WSS position ref value', 'D1 XFR roll force actual value',
        #          'D1 WFR roll force ref value', 'D1 XSSd tilting actual value', 'D1 WSSd tilting ref value',
        #          'D1 DIFF RF CTRL act value (DS-OS)', 'D2 XSS position actual value', 'D2 WSS position ref value',
        #          'D2 XFR roll force actual value', 'D2 WFR roll force ref value', 'D2 XSSd tilting actual value',
        #          'D2 WSSd tilting ref value', 'D2 DIFF RF CTRL act value (DS-OS)', 'D3 XSS position actual value',
        #          'D3 WSS position ref value', 'D3 XFR roll force actual value', 'D3 WFR roll force ref value',
        #          'D3 XSSd tilting actual value', 'D3 WSSd tilting ref value', 'D3 DIFF RF CTRL act value (DS-OS)',
        #          'D4 XSS position actual value', 'D4 WSS position ref value', 'D4 XFR roll force actual value',
        #          'D4 WFR roll force ref value', 'D4 XSSd tilting actual value', 'D4 WSSd tilting ref value',
        #          'D4 DIFF RF CTRL act value (DS-OS)', 'D5 XSS position actual value', 'D5 WSS position ref value',
        #          'D5 XFR roll force actual value', 'D5 WFR roll force ref value', 'D5 XSSd tilting actual value',
        #          'D5 WSSd tilting ref value', 'D5 DIFF RF CTRL act value (DS-OS)', 'B1 BURB actual value',
        #          'B1 BURB ref value', 'B1 WRB actual value', 'B1 WRB ref value', 'B1 IRB ref value',
        #          'B1 IRB ref value ctrl1', 'B1 IRB actual value ctrl1', 'B1 IRB ref value ctrl2',
        #          'B1 IRB actual value ctrl2', 'B2 BURB actual value', 'B2 BURB ref value', 'B2 WRB actual value',
        #          'B2 WRB ref value', 'B2 IRB ref value', 'B2 IRB ref value ctrl1', 'B2 IRB actual value ctrl1',
        #          'B2 IRB ref value ctrl2', 'B2 IRB actual value ctrl2', 'B3 BURB actual value', 'B3 BURB ref value',
        #          'B3 WRB actual value', 'B3 WRB ref value', 'B3 IRB ref value', 'B3 IRB ref value ctrl1',
        #          'B3 IRB actual value ctrl1', 'B3 IRB ref value ctrl2', 'B3 IRB actual value ctrl2',
        #          'WR bending actual value', 'B4 IRB ref value', 'B4 IRB ref value ctrl1', 'B4 IRB actual value ctrl1',
        #          'B4 IRB ref value ctrl2', 'B4 IRB actual value ctrl2', 'B5 BURB actual value', 'B5 WRB actual value',
        #          'B5 WRB ref value', 'B5 IRB ref value', 'B5 IRB ref value ctrl1', 'B5 IRB actual value ctrl1',
        #          'B5 IRB ref value ctrl2', 'B5 IRB actual value ctrl2', 'S1 top IR shfiting ref value',
        #          'S1 top IR shfitingl actual value', 'S1 bot IR shfiting ref value', 'S1 bot IR shfitingl actual value',
        #          'S1 ref value level 2', 'S2 top IR shfiting ref value', 'S2 top IR shfiting actual value',
        #          'S2 bot IR shfiting ref value', 'S2 bot IR shfiting actual value', 'S2 ref value level 2',
        #          'S3 top IR shfitingl ref value', 'S3 top IR shfiting actual value', 'S3 bot IR shfiting ref value',
        #          'S3 bot IR shfiting actual value', 'S3 ref value level 2', 'S4 top  IR shfiting  ref value',
        #          'S4 top  IR shfiting actual value', 'S4 bot IR shfiting ref value', 'S4 bot IR shfiting actual value',
        #          'S4 ref value level 2', 'S5 top IR shfiting ref value', 'S5 top IR shfiting actual value',
        #          'S5 bot IR shfiting ref value', 'S5 bot IR shfiting actual value', 'S5 ref value level 2', 'S2 FLOW',
        #          'S3 FLOW', 'T3 TEMP.', 'T3 LEV.', 'RCH1: Wedge passline deviation', 'POS', 'deg0', 'deg1', 'deg2',
        #          'deg3', 'deg4']
        #
        #     self.xtest = self.data[feature]
        #
        #     self.textEdit.setText('选择的数据路径为“%s”，\n数据已成功导入！' % self.data_path)
        # except:
        #     QMessageBox.information(self, '提示信息', '数据选择出错，请重新选择数据', QMessageBox.Ok)
        try:
            self.comboBox_2.clear()
            self.comboBox_2.setVisible(False)
        except:
            pass
        try:
            tmp = os.path.abspath(__file__)
            self.data_path = \
                QFileDialog.getOpenFileNames(self, "ADD", tmp, "CSV Files(*.csv);;XLSX Files(*.xlsx)")[0]
            if len(self.data_path) == 0:
                QMessageBox.information(self, '提示框', '您未选择任何文件，请重新导入数据', QMessageBox.Ok)
            else:
                self.juan_hao = [os.path.splitext(os.path.basename(file))[0] for file in self.data_path]
                self.data = [pd.read_csv(file, encoding='gbk').dropna().reset_index(drop=True) for file in
                             self.data_path]
                feature = ['RCH2: Wedge passline deviation', 'RCH3: Wedge passline deviation',
                           'RCH4: Wedge passline deviation',
                           'RCH5: Wedge passline deviation', 'F5 ref tension after stand 5',
                           'F5 actual value after stand 5 smoothed', 'F5 flatness error tilt',
                           'F5  flatness error WR-bend',
                           'F5  flatness error IR-bend', 'F5 flatness error', 'F5  flatness error IR-shift',
                           'F5 add tilt', 'F5 add WR-bend',
                           'F5 add IR-bend', 'F5 add IR-shift', 'F5 strip length', 'F5 emulsion flow',
                           'F5 release tilt control', 'F5 tilt control active', 'F5 release WR-bend control',
                           'F5 WR-bend control active', 'F5 release IR-bend control', 'F5 IR-bend control active',
                           'F5 release IR-shifting control', 'F5 IR-shifting control active',
                           'F5 IR-bending control active MONI',
                           'F5 IR-shifting control active MONI', 'STAND_01_reduction', 'STAND_02_reduction',
                           'STAND_03_reduction',
                           'STAND_04_reduction', 'STAND_05_reduction', 'THC: h ref. S1 entry(ims)',
                           'THC: h ref. S1 exit(ims)',
                           'THC: act. thickness S1 entry', 'THC: act. thickness S1 exit', 'THX: h ref S5 exit',
                           'THX: h act S5 exit', 'SLC laser speed behind S1', 'SLC laser speed behind S4',
                           'SLC laser speed behind S5', 'SLC act. speed exit flatness roll',
                           'SLC act. speed stand 1',
                           'SLC act. speed stand 2', 'SLC act. speed stand 3', 'SLC act speed stand 4',
                           'SLC act.speed stand 5',
                           'SLC strip speed S1 - S2', 'SLC strip speed S2 - S3', 'SLC strip speed S3 - S4',
                           'SLC strip speed S4 - S5', 'SLC strip speed after S5', 'SLC Slip factor stand 1',
                           'SLC Slip factor stand 2', 'SLC Slip factor stand 3', 'SLC Slip factor stand 4',
                           'SLC Slip factor stand 5', 'N1 ITC tension ref value', 'N1 ITC tension actual value DS',
                           'N1 ITC tension actual value OS', 'N1 ITC tension actual value at ctrl',
                           'N1 ITC diff.tension at ctrl',
                           'N2 ITC tension ref value', 'N2 ITC tension actual value DS',
                           'N2 ITC tension actual value OS',
                           'N2 ITC tension actual value at ctrl', 'N2 ITC diff.tension at ctrl',
                           'N3 ITC tension ref value',
                           'N3 ITC tension actual value DS', 'N3 ITC tension actual value OS',
                           'N3 ITC tension actual value at ctrl', 'N3 ITC diff.tension at ctrl',
                           'N4 ITC tension ref value',
                           'N4 ITC tension actual value DS', 'N4 ITC tension actual value OS',
                           'N4 ITC tension actual value at ctrl', 'N4 ITC diff.tension at ctrl',
                           'N5 ITC tension ref value',
                           'N5 ITC tension actual value DS', 'N5 ITC tension actual value OS',
                           'N5 ITC tension actual value at ctrl', 'N5 ITC diff.tension at ctrl',
                           'N5 tension actual value DS after S5', 'N5 tension actual value OS after S5',
                           'D1 XSS position actual value', 'D1 WSS position ref value',
                           'D1 XFR roll force actual value',
                           'D1 WFR roll force ref value', 'D1 XSSd tilting actual value',
                           'D1 WSSd tilting ref value',
                           'D1 DIFF RF CTRL act value (DS-OS)', 'D2 XSS position actual value',
                           'D2 WSS position ref value',
                           'D2 XFR roll force actual value', 'D2 WFR roll force ref value',
                           'D2 XSSd tilting actual value',
                           'D2 WSSd tilting ref value', 'D2 DIFF RF CTRL act value (DS-OS)',
                           'D3 XSS position actual value',
                           'D3 WSS position ref value', 'D3 XFR roll force actual value',
                           'D3 WFR roll force ref value',
                           'D3 XSSd tilting actual value', 'D3 WSSd tilting ref value',
                           'D3 DIFF RF CTRL act value (DS-OS)',
                           'D4 XSS position actual value', 'D4 WSS position ref value',
                           'D4 XFR roll force actual value',
                           'D4 WFR roll force ref value', 'D4 XSSd tilting actual value',
                           'D4 WSSd tilting ref value',
                           'D4 DIFF RF CTRL act value (DS-OS)', 'D5 XSS position actual value',
                           'D5 WSS position ref value',
                           'D5 XFR roll force actual value', 'D5 WFR roll force ref value',
                           'D5 XSSd tilting actual value',
                           'D5 WSSd tilting ref value', 'D5 DIFF RF CTRL act value (DS-OS)', 'B1 BURB actual value',
                           'B1 BURB ref value', 'B1 WRB actual value', 'B1 WRB ref value', 'B1 IRB ref value',
                           'B1 IRB ref value ctrl1', 'B1 IRB actual value ctrl1', 'B1 IRB ref value ctrl2',
                           'B1 IRB actual value ctrl2', 'B2 BURB actual value', 'B2 BURB ref value',
                           'B2 WRB actual value',
                           'B2 WRB ref value', 'B2 IRB ref value', 'B2 IRB ref value ctrl1',
                           'B2 IRB actual value ctrl1',
                           'B2 IRB ref value ctrl2', 'B2 IRB actual value ctrl2', 'B3 BURB actual value',
                           'B3 BURB ref value',
                           'B3 WRB actual value', 'B3 WRB ref value', 'B3 IRB ref value', 'B3 IRB ref value ctrl1',
                           'B3 IRB actual value ctrl1', 'B3 IRB ref value ctrl2', 'B3 IRB actual value ctrl2',
                           'WR bending actual value', 'B4 IRB ref value', 'B4 IRB ref value ctrl1',
                           'B4 IRB actual value ctrl1',
                           'B4 IRB ref value ctrl2', 'B4 IRB actual value ctrl2', 'B5 BURB actual value',
                           'B5 WRB actual value',
                           'B5 WRB ref value', 'B5 IRB ref value', 'B5 IRB ref value ctrl1',
                           'B5 IRB actual value ctrl1',
                           'B5 IRB ref value ctrl2', 'B5 IRB actual value ctrl2', 'S1 top IR shfiting ref value',
                           'S1 top IR shfitingl actual value', 'S1 bot IR shfiting ref value',
                           'S1 bot IR shfitingl actual value',
                           'S1 ref value level 2', 'S2 top IR shfiting ref value',
                           'S2 top IR shfiting actual value',
                           'S2 bot IR shfiting ref value', 'S2 bot IR shfiting actual value',
                           'S2 ref value level 2',
                           'S3 top IR shfitingl ref value', 'S3 top IR shfiting actual value',
                           'S3 bot IR shfiting ref value',
                           'S3 bot IR shfiting actual value', 'S3 ref value level 2',
                           'S4 top  IR shfiting  ref value',
                           'S4 top  IR shfiting actual value', 'S4 bot IR shfiting ref value',
                           'S4 bot IR shfiting actual value',
                           'S4 ref value level 2', 'S5 top IR shfiting ref value',
                           'S5 top IR shfiting actual value',
                           'S5 bot IR shfiting ref value', 'S5 bot IR shfiting actual value',
                           'S5 ref value level 2', 'S2 FLOW',
                           'S3 FLOW', 'T3 TEMP.', 'T3 LEV.', 'RCH1: Wedge passline deviation', 'POS', 'deg0',
                           'deg1', 'deg2',
                           'deg3', 'deg4']
                self.xtest = [one[feature] for one in self.data]

            self.textEdit.setText('选择的钢卷号为\n“%s”\n数据已成功导入！' % self.juan_hao)
        except:
            QMessageBox.information(self, '提示信息', '数据选择出错，请重新选择数据', QMessageBox.Ok)

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        预测
        """

        # 生成资源文件目录访问路径 相对路径
        def resource_path(relative_path):
            if getattr(sys, 'frozen', False):  # 是否Bundle Resource 捆绑资源
                base_path = sys._MEIPASS
            else:
                base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)

        try:
            try:
                self.comboBox_2.setVisible(True)
            except:
                pass
            self.comboBox_2.clear()
            self.comboBox_2.addItem('请选择想要评估的钢卷号')
            self.comboBox_2.addItems(self.juan_hao)
            model = joblib.load(
                resource_path('板形生成数据建模/板形缺陷模式有无预测\\二分类模型\erfenlei_%s.m' % self.comboBox.currentText()))
            self.C_pre = [model.predict(one) for one in self.xtest]
            self.textEdit.setText('已完成预测！')

        except Exception as e:
            print(e)
            QMessageBox.information(self, '提示框', '预测出错', QMessageBox.Ok)

    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        """
        评估
        """

        def accuracy(ytest, pre):
            acc_sum = 0
            for i in range(len(pre)):
                if pre[i] == ytest[i]:
                    acc_sum += 1
            acc = acc_sum / len(pre)
            # print('acc:', acc)
            return acc * 100

        try:
            if self.comboBox_2.currentText() != '请选择想要评估的钢卷号':
                acc = [accuracy(self.data[one].loc[:, 'y二分类'], self.C_pre[one]) for one in range(len(self.data))]
                self.lineEdit.setText('正确率：%.2f%%' % acc[self.juan_hao_index])
            else:
                QMessageBox.information(self, '提示框', '您未选择想要评估的钢卷号，请在上一个下拉框选择相应钢卷号',
                                        QMessageBox.Ok)
        except:
            QMessageBox.information(self, '提示框', '计算出错', QMessageBox.Ok)

    @pyqtSlot(str)
    def on_comboBox_2_activated(self, p0):
        try:
            if p0 != '请选择想要评估的钢卷号':
                self.juan_hao_index = self.juan_hao.index(p0)
            else:
                QMessageBox.information(self, '提示框', '请正确选择钢卷号', QMessageBox.Ok)
        except:
            QMessageBox.information(self, '提示框', '数据出错，请重新选择数据进行预测', QMessageBox.Ok)

    @pyqtSlot()
    def on_pushButton_7_clicked(self):
        """
        图像
        """
        try:
            if self.comboBox_2.currentText() != '请选择想要评估的钢卷号':
                self.textEdit_2.setVisible(False)
            else:
                QMessageBox.information(self, '提示框', '您未选择想要评估的钢卷号，请在上一个下拉框选择相应钢卷号',
                                        QMessageBox.Ok)
        except:
            pass

        try:
            self.verticalLayout_4.itemAt(1).widget().deleteLater()
            self.verticalLayout_5.itemAt(0).widget().deleteLater()
        except:
            pass
        try:
            self.C_plot(self.data[self.juan_hao_index].loc[:, 'y二分类'], self.C_pre[self.juan_hao_index])
        except:
            QMessageBox.information(self, '提示框', '图像显示出错', QMessageBox.Ok)

    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        """
        多卷保存
        """
        try:
            save_path = QFileDialog.getExistingDirectory(self, "预测结果保存", os.getcwd())
            houzhui = save_path.split('/')[-1].split('.')[-1]
            for i in range(len(self.juan_hao)):
                pd.DataFrame(self.C_pre[i]).iloc[:, :].to_csv('%s\\%s.csv' % (save_path, self.juan_hao[i]),
                                                              encoding='gbk', index=False)
            self.textEdit.setText('文件已保存完毕')
            # if houzhui == 'csv':
            #     pd.DataFrame(self.C_pre).to_csv(save_path, encoding='gbk', index=False)
            #
            # elif houzhui == 'xlsx':
            #     pd.DataFrame(self.C_pre).to_excel(save_path, encoding='gbk', index=False)
            # else:
            #     QMessageBox.information(self, '提示框', '文件格式错误', QMessageBox.Ok)
        except:
            QMessageBox.information(self, '提示框', '出错，保存失败', QMessageBox.Ok)

    @pyqtSlot()
    def on_pushButton_6_clicked(self):
        """
        单卷保存
        """
        try:
            save_path = QFileDialog.getExistingDirectory(self, "预测结果保存", os.getcwd())
            houzhui = save_path.split('/')[-1].split('.')[-1]
            pd.DataFrame(self.C_pre[self.juan_hao_index]).iloc[:, :].to_csv(
                '%s\\%s.csv' % (save_path, self.juan_hao[self.juan_hao_index]), encoding='gbk', index=False)
            self.textEdit.setText('文件已保存完毕')
            # if houzhui == 'csv':
            #     pd.DataFrame(self.C_pre).to_csv(save_path, encoding='gbk', index=False)
            #
            # elif houzhui == 'xlsx':
            #     pd.DataFrame(self.C_pre).to_excel(save_path, encoding='gbk', index=False)
            # else:
            #     QMessageBox.information(self, '提示框', '文件格式错误', QMessageBox.Ok)
        except:
            QMessageBox.information(self, '提示框', '出错，保存失败', QMessageBox.Ok)

    def C_plot(self, true, pre):
        labels = sorted(list(set(true)))
        labels = list(map(int, labels[:]))
        matrix_0 = confusion_matrix(true, pre, labels=labels)
        matrix = pd.DataFrame(matrix_0, columns=labels, index=labels)

        F = MyFigure(width=8, height=10, dpi=100)
        axes = F.fig.add_subplot(1, 1, 1)
        axes.imshow(matrix, alpha=0.4)
        # axes.imshow(matrix, cmap="Blues", alpha = 0.5)
        axes.set_xticks(range(len(labels)))
        axes.set_xticklabels(labels)
        axes.set_yticks(range(len(labels)))
        axes.set_yticklabels(labels)
        axes.set_xlabel('预测结果')
        axes.set_ylabel('实际结果')
        axes.set_title('%s二分类混淆矩阵' % self.juan_hao[self.juan_hao_index])
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                axes.text(j, i, matrix.iloc[i, j]
                          , ha='center', va='center', color='black', fontsize=15
                          )
        # F.fig.colorbar()
        self.verticalLayout_4.addWidget(F)
        mpl_ntb = NavigationToolbar(F, self)
        self.verticalLayout_5.addWidget(mpl_ntb)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QMainWindow, QApplication

    app = QApplication(sys.argv)
    ui = MainWindowC2()
    ui.show()
    sys.exit(app.exec_())
