# -*- coding: utf-8 -*-

"""
Module implementing mainWindow.
"""
import os
import numpy as np
import joblib
import pandas as pd
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from keras.models import load_model
from sklearn.metrics import r2_score, mean_squared_error

from 板形生成数据建模.板形缺陷定量回归预测.Ui_板形缺陷定量回归预测 import Ui_mainWindow
from 板形生成数据建模.板形缺陷定量回归预测.myplot import MyFigure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class MainWindow(QMainWindow, Ui_mainWindow):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (defaults to None)
        @type QWidget (optional)
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.lineEdit.setReadOnly(True)
        self.lineEdit_2.setReadOnly(True)
        self.textEdit.setReadOnly(True)
        self.textEdit_2.setReadOnly(True)
        self.comboBox_3.setVisible(False)

    @pyqtSlot()
    def on_help_doc_triggered(self):
        from .帮助文档 import help
        self.help_ui = help()
        self.help_ui.show()
        # QMessageBox.information(self, '提示信息', '这是一个帮助文档', QMessageBox.Ok)

    @pyqtSlot(str)
    def on_comboBox_activated(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type str
        """

        # 生成资源文件目录访问路径 相对路径
        model_path = f"{os.path.dirname(__file__)}/定量回归模型"

        try:
            self.textEdit.setText('您选择的模型为“%s”' % p0)
            if p0 == 'BP':
                self.scalarX = joblib.load(rf'{model_path}\标准化X.m')
                self.scalarY = joblib.load(rf'{model_path}\标准化Y.m')
                self.x = [self.scalarX.transform(one) for one in self.xtest]
            if p0 == 'RNN':
                self.scalarX = joblib.load(rf'{model_path}\标准化X.m')
                self.scalarY = joblib.load(rf'{model_path}\标准化Y.m')
                x = [self.scalarX.transform(one) for one in self.xtest]
                self.x = [one.reshape(one.shape[0], 1, one.shape[1]).astype('float32') for one in x]

        except:
            QMessageBox.information(self, '提示信息', '模型选择出错', QMessageBox.Ok)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        数据导入
        """
        try:
            self.comboBox_3.clear()
        except:
            pass
        try:
            local_path = os.path.abspath(__file__)
            tmp = os.path.dirname(local_path) + '/定量回归数据/'
            self.data_path = QFileDialog.getOpenFileNames(self, "ADD", tmp, "CSV Files(*.csv);;XLSX Files(*.xlsx)")[0]
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
                           'F5  flatness error IR-bend', 'F5  flatness error IR-shift', 'F5 add tilt',
                           'F5 add WR-bend',
                           'F5 add IR-bend', 'F5 add IR-shift', 'F5 strip length', 'F5 flatness error',
                           'F5 emulsion flow',
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
                           'SLC laser speed behind S5', 'SLC act. speed exit flatness roll', 'SLC act. speed stand 1',
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
                           'D1 WFR roll force ref value', 'D1 XSSd tilting actual value', 'D1 WSSd tilting ref value',
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
                           'D4 WFR roll force ref value', 'D4 XSSd tilting actual value', 'D4 WSSd tilting ref value',
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
                           'S1 ref value level 2', 'S2 top IR shfiting ref value', 'S2 top IR shfiting actual value',
                           'S2 bot IR shfiting ref value', 'S2 bot IR shfiting actual value', 'S2 ref value level 2',
                           'S3 top IR shfitingl ref value', 'S3 top IR shfiting actual value',
                           'S3 bot IR shfiting ref value',
                           'S3 bot IR shfiting actual value', 'S3 ref value level 2',
                           'S4 top  IR shfiting  ref value',
                           'S4 top  IR shfiting actual value', 'S4 bot IR shfiting ref value',
                           'S4 bot IR shfiting actual value',
                           'S4 ref value level 2', 'S5 top IR shfiting ref value', 'S5 top IR shfiting actual value',
                           'S5 bot IR shfiting ref value', 'S5 bot IR shfiting actual value', 'S5 ref value level 2',
                           'S2 FLOW',
                           'S3 FLOW', 'T3 TEMP.', 'T3 LEV.', 'RCH1: Wedge passline deviation', 'POS', 'deg0', 'deg1',
                           'deg2',
                           'deg3', 'deg4']
                self.xtest = [one[feature] for one in self.data]

                self.textEdit.setText('选择的钢卷号为\n“%s”\n数据已成功导入！' % self.juan_hao)
        except:
            QMessageBox.information(self, '提示信息', '数据选择出错，请重新选择数据', QMessageBox.Ok)

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        模型预测
        """

        model_path = f"{os.path.dirname(__file__)}/定量回归模型"

        # try:
        try:
            self.comboBox_3.setVisible(True)
        except:
            pass
        self.comboBox_3.clear()
        self.comboBox_3.addItem('请选择想要评估的钢卷号')
        self.comboBox_3.addItems(self.juan_hao)
        if self.comboBox.currentText() == 'CatBoost':
            sum_pre = []
            sum_true = []
            for j in range(len(self.data)):
                test_pre = []
                test_true = []
                for i in range(5):
                    model = joblib.load(fr'{model_path}\{self.comboBox.currentText()}Deg{i}.m')

                    ytest_true = self.data[j].loc[:, 'ydeg%s' % i]
                    test_true.append(ytest_true)
                    ytest_pre = model.predict(self.xtest[j])
                    test_pre.append(ytest_pre)
                sum_pre.append(test_pre)
                sum_true.append(test_true)
            self.test_pre = [pd.DataFrame(sum_pre_i).T for sum_pre_i in sum_pre]
            print(self.test_pre)
            self.test_true = [pd.DataFrame(sum_true_i).T for sum_true_i in sum_true]

        elif self.comboBox.currentText() == 'BP' or 'RNN':
            import tensorflow as tf
            os.environ["CUDA_VISIBLE_DEVICES"] = "0"
            config = tf.compat.v1.ConfigProto()
            config.gpu_options.allow_growth = True
            session = tf.compat.v1.Session(config=config)
            model = load_model(fr'{model_path}\{self.comboBox.currentText()}.h5')
            y = [model.predict(one) for one in self.x]
            self.test_pre = [pd.DataFrame(self.scalarY.inverse_transform(one)) for one in y]
            self.test_true = [one[['ydeg0', 'ydeg1', 'ydeg2', 'ydeg3', 'ydeg4']] for one in self.data]

        else:
            QMessageBox.information(self, '提示框', 'BP、LSTM、RNN不如CatBoost，建议选择CatBoost', QMessageBox.Ok)
        self.textEdit.setText('已完成预测！')
        # except:
        #     QMessageBox.information(self, '提示框', 'BP、RNN所需环境不稳定，建议选择CatBoost', QMessageBox.Ok)

    @pyqtSlot(str)
    def on_comboBox_3_activated(self, p0):
        try:
            if p0 != '请选择想要评估的钢卷号':
                self.juan_hao_index = self.juan_hao.index(p0)
            else:
                QMessageBox.information(self, '提示框', '请正确选择钢卷号', QMessageBox.Ok)
        except:
            QMessageBox.information(self, '提示框', '数据出错，请重新选择数据进行预测', QMessageBox.Ok)

    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        """
        计算R2和MSE
        """
        try:
            if self.comboBox_3.currentText() != '请选择想要评估的钢卷号':
                if self.comboBox_2.currentText() != '选择系数':
                    i = int(list(self.comboBox_2.currentText())[-1])
                    r2 = [r2_score(self.test_true[yang_ben].iloc[:, i], self.test_pre[yang_ben].iloc[:, i]) for yang_ben
                          in range(len(self.test_true))]
                    mse = [mean_squared_error(self.test_true[yang_ben].iloc[:, i], self.test_pre[yang_ben].iloc[:, i])
                           for yang_ben in range(len(self.test_true))]
                    self.lineEdit.setText('%.2f' % r2[self.juan_hao_index])
                    self.lineEdit_2.setText('%.4f' % mse[self.juan_hao_index])
                else:
                    QMessageBox.information(self, '提示框', '请选择系数！', QMessageBox.Ok)
            else:
                QMessageBox.information(self, '提示框', '您未选择想要评估的钢卷号，请在上一个下拉框选择相应钢卷号',
                                        QMessageBox.Ok)
        except:
            QMessageBox.information(self, '提示框', '计算出错', QMessageBox.Ok)

    @pyqtSlot()
    def on_pushButton_7_clicked(self):
        """
        图像显示
        """

        try:
            self.textEdit_2.setVisible(False)
        except:
            pass

        try:
            self.verticalLayout_4.itemAt(1).widget().deleteLater()
            self.verticalLayout_5.itemAt(0).widget().deleteLater()
        except:
            pass
        try:
            pre = np.array(self.test_pre[self.juan_hao_index])
            true = np.array(self.test_true[self.juan_hao_index])
            self.deg_plot(pre, true)
        except:
            QMessageBox.information(self, '提示框', '图像显示出错', QMessageBox.Ok)

    @pyqtSlot()
    def on_pushButton_6_clicked(self):
        """
        保存结果
        """
        try:
            save_path = QFileDialog.getExistingDirectory(self, "预测结果保存", os.getcwd())
            # self.textEdit.setText(save_path)
            self.test_pre[self.juan_hao_index].iloc[:, :].to_csv(
                '%s\\%s.csv' % (save_path, self.juan_hao[self.juan_hao_index]), encoding='gbk', index=False)
            self.textEdit.setText('文件已保存完毕')
        except:
            QMessageBox.information(self, '提示框', '保存出错', QMessageBox.Ok)

    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        """多卷结果保存"""
        try:
            save_path = QFileDialog.getExistingDirectory(self, "指定保存的文件夹，文件名默认为钢卷号", os.getcwd())
            # self.textEdit.setText(save_path)
            for i in range(len(self.juan_hao)):
                self.test_pre[i].iloc[:, :].to_csv('%s\\%s.csv' % (save_path, self.juan_hao[i]), encoding='gbk',
                                                   index=False)
            self.textEdit.setText('文件已保存完毕')
        except:
            QMessageBox.information(self, '提示框', '保存出错', QMessageBox.Ok)

    def deg_plot(self, test_pre, test_act):
        F = MyFigure(width=8, height=10, dpi=100)
        # x=range(len(test_pre))
        axes = F.fig.subplots(4, 1, sharex=True)

        # ax1=F.fig.add_subplot(411)
        ax1 = axes[0]
        ax1.plot(test_pre[:, 1], 'r-', label='pre', linewidth=0.5, markersize=1)
        ax1.plot(test_act[:, 1], 'b-', label='act', linewidth=0.5, markersize=1)
        # ax1.legend(loc='best')
        ax1.set_ylabel('一次项系数')
        ax1.set_title('%s板形缺陷定量回归预测模型分析' % self.juan_hao[self.juan_hao_index], fontsize=15)

        # ax2=F.fig.add_subplot(412)
        ax2 = axes[1]
        ax2.plot(test_pre[:, 2], 'r-', label='pre', linewidth=0.5, markersize=1)
        ax2.plot(test_act[:, 2], 'b-', label='act', linewidth=0.5, markersize=1)
        # ax2.legend()
        ax2.set_ylabel('二次项系数')

        # ax3 = F.fig.add_subplot(413)
        ax3 = axes[2]
        ax3.plot(test_pre[:, 3], 'r-', label='pre', linewidth=0.5, markersize=1)
        ax3.plot(test_act[:, 3], 'b-', label='act', linewidth=0.5, markersize=1)
        # ax3.legend()
        ax3.set_ylabel('三次项系数')

        # ax4 = F.fig.add_subplot(414,sharex=True)
        ax4 = axes[3]
        ax4.plot(test_pre[:, 4], 'r-', label='pre', linewidth=0.5, markersize=1)
        ax4.plot(test_act[:, 4], 'b-', label='act', linewidth=0.5, markersize=1)
        # ax4.legend()
        ax4.set_ylabel('四次项系数')
        ax4.set_xlabel('采样点', fontsize=15)
        # F.fig.legend()
        lines, labels = axes[-1].get_legend_handles_labels()
        F.fig.legend(lines, labels, fontsize=15)
        # F.fig.suptitle('板形缺陷定量回归预测模型分析')

        # print(self.horizontalLayout_bar.count()==1)

        self.verticalLayout_4.addWidget(F)
        mpl_ntb = NavigationToolbar(F, self)
        self.verticalLayout_5.addWidget(mpl_ntb)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QMainWindow, QApplication

    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
