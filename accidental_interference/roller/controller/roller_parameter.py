# -*- coding: utf-8 -*-

"""
轧辊信息跟踪界面, 主要显示直径, 粗糙度, 轧制长度, 轧制重量的跟踪信息.
"""
import os

import numpy as np
import pandas as pd
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QMessageBox
from accidental_interference.roller.controller.myplot import MyFigure
from accidental_interference.roller.view.Ui_roller_parameter import Ui_RollerInfo


class RollerInfo(QDialog, Ui_RollerInfo):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (defaults to None)
        @type QWidget (optional)
        """
        super(RollerInfo, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(
            QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.radioButton_D.setEnabled(False)
        self.radioButton_Ra.setEnabled(False)
        self.radioButton_Length.setEnabled(False)
        self.radioButton_Weight.setEnabled(False)
        self.pushButton_show.setEnabled(False)
        # self.bur=np.load('bur_gunhao.npy')
        # self.imr = np.load('imr_gunhao.npy')
        # self.wr = np.load('wr_gunhao.npy')

    @pyqtSlot(str)
    def on_comboBox_leixing_activated(self, p0):
        """
        轧辊类型选择.
        Args:
            p0: comboBox选择的内容.
        Return:
            None.
        """
        try:
            self.comboBox_gunhao.clear()
            辊号: list = np.load(os.path.dirname(os.path.dirname(__file__)) + '\\data\\npy\\'+'%s_gunhao.npy' % p0).tolist()
            # 将列表内的元素转换为字符串
            for i in range(len(辊号)):
                辊号[i] = str(辊号[i])

            self.comboBox_gunhao.addItems(辊号)  # 将"辊号"列表中的元素添加到下拉框中
            if 'BUR' in p0:
                self.df = pd.read_excel(os.path.dirname(os.path.dirname(__file__)) + '\data\轧辊记录提取数据\支撑辊_all.xlsx', header=0)
                self.df['辊号'] = self.df['辊号'].astype(str)
            if 'IMR' in p0:
                self.df = pd.read_excel(os.path.dirname(os.path.dirname(__file__)) + '\data\轧辊记录提取数据\中间辊_all.xlsx')
                self.df['辊号'] = self.df['辊号'].astype(str)

            if 'WR' in p0:
                concatlist = []
                for i in range(1, 6):
                    df = pd.read_excel(os.path.dirname(os.path.dirname(__file__)) + '\data\轧辊记录提取数据\工作辊_%s_all.xlsx' % i, header=0)
                    concatlist.append(df)
                self.df = pd.concat(concatlist, axis=0)
                self.df['辊号'] = self.df['辊号'].astype(str)
        except:
            # 打印报错信息
            import traceback
            traceback.print_exc()
            QMessageBox.information(self, '提示框', '支带钢类型选择出错', QMessageBox.Ok)

    @pyqtSlot(str)
    def on_comboBox_gunhao_activated(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type str
        """
        try:
            self.radioButton_D.setEnabled(True)
            self.radioButton_Ra.setEnabled(True)
            self.radioButton_Length.setEnabled(True)
            self.radioButton_Weight.setEnabled(True)
            self.pushButton_show.setEnabled(True)
            self.辊号 = p0
            self.data = self.df[self.df['辊号'] == p0].sort_values('上机时间').reset_index(drop=True)
            self.D = self.data['直径']
            self.Ra = self.data['粗糙度']
            self.Length = self.data['轧制长度(km)']
            self.Weight = self.data['轧制重量(t)']
            self.start = self.data.loc[0, '上机时间']
            self.end = self.data.loc[len(self.data) - 1, '下机时间']
            self.xtickslabel = []
            for i in range(len(self.data)):
                self.xtickslabel.append('')
            self.xtickslabel[0] = self.start
            self.xtickslabel[-1] = self.end
        except:
            QMessageBox.information(self, '提示框', '辊号选择出错', QMessageBox.Ok)

    @pyqtSlot()
    def on_pushButton_show_clicked(self):
        """
        Slot documentation goes here.
        """

        from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
        try:
            F = MyFigure(width=8, height=10, dpi=100)
            axes = F.fig.add_subplot(111)
            # axes.set_xlabel('服役先后顺序')
            axes.set_title('%s在不同直径下的轧辊信息' % (self.辊号))

            if self.radioButton_D.isChecked():
                y = self.D
                axes.plot(range(len(y)), y, c='r', marker='.', markeredgecolor='b', markerfacecolor='b')
                axes.set_ylabel('直径/mm')

            if self.radioButton_Ra.isChecked():
                y = self.Ra
                axes.plot(range(len(y)), y, c='r', marker='.', markeredgecolor='b', markerfacecolor='b')
                axes.set_ylabel('粗糙度')

            if self.radioButton_Length.isChecked():
                y = self.Length
                axes.bar(range(len(y)), y)
                axes.set_ylabel('轧制长度/km')

            if self.radioButton_Weight.isChecked():
                y = self.Weight
                axes.bar(range(len(y)), y)
                axes.set_ylabel('轧制重量/t')

            # x = 0
            # for i in y:
            #     axes.text(x, i, i, rotation=25, ha='left', color='r')
            #     x += 1

            axes.set_xticks(range(len(y)))
            axes.set_xticklabels(self.xtickslabel, rotation=0, ha='center')
            axes.set_xlabel('轧辊先后顺序')

            try:
                self.textEdit.setVisible(False)
            except:
                pass
            try:
                self.horizontalLayout_pic.itemAt(1).widget().deleteLater()
                self.verticalLayout_bar.itemAt(0).widget().deleteLater()
            except:
                pass
            self.horizontalLayout_pic.addWidget(F)
            bar = NavigationToolbar(F, self)
            self.verticalLayout_bar.addWidget(bar)
        except Exception as e:
            print(e)
            QMessageBox.information(self, '提示框', '请先选择跟踪信息', QMessageBox.Ok)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QMainWindow, QApplication

    app = QApplication(sys.argv)
    ui = RollerInfo()
    ui.show()
    sys.exit(app.exec_())
