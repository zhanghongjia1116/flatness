"""
Module implementing FullLengthQuality.
"""

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QMessageBox
from PyQt5.QtWidgets import *
import matplotlib
# from PCA import run_pca, get_top_indexes
from ..utils.PCA import run_pca, get_top_indexes
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

matplotlib.use("Qt5Agg")
from matplotlib import pyplot
# import Figure_Canvas
from ..utils import Figure_Canvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

pyplot.rcParams['font.sans-serif'] = ['SimHei']
pyplot.rcParams['axes.unicode_minus'] = False

from .Ui_PCA_GUI import Ui_MainWindow
import os
import warnings

# 忽略所有RuntimeWarning
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=UserWarning)


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # self.t_total = None
        # self.q_total = None
        # self.t_limit = None
        # self.spe_limit = None
        # self.t_total_contribution = None
        # self.q_con_list = None
        # self.feature = None
        # self.canshu = None
        # self.id_err = None
        # self.sum_TC = None
        # self.sum_QC = None
        # self.IU = None

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        try:
            local_path = os.path.abspath(os.path.dirname(__file__))
            parent_path = os.path.dirname(local_path)
            self.train_path = \
            QFileDialog.getOpenFileName(self, "ADD", parent_path, "CSV Files(*.csv);;XLSX Files(*.xlsx)")[0]
            self.textBrowser_2.setText(self.train_path)
        except:
            QMessageBox.information(self, '提示信息', '选择数据集发生错误')
            return None

    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        # self.t_total = None
        # self.q_total = None
        # self.t_limit = None
        # self.spe_limit = None
        # self.t_total_contribution = None
        # self.q_con_list = None
        # self.feature = None
        # self.canshu = None
        # self.id_err = None
        # self.sum_TC = None
        # self.sum_QC = None
        # self.IU = None

        QMessageBox.information(self, '提示信息', '程序已启动，请等待运行完成。')

        try:
            # 清除画布上的所有内容
            while self.gridLayout.count():
                item = self.gridLayout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
        except:
            pass

        try:
            if self.textBrowser_2.toPlainText() != '数据路径':
                path2 = self.textBrowser_2.toPlainText()

            else:
                QMessageBox.information(self, '提示信息', '请先选择数据')
                # QMessageBox.information(self, '提示信息', '选择默认训练集和测试集')
                # path1 = 'D:\A_My_file\DATA\DX51D+Z\DX51D_all.csv'
                # path2 = 'D:\A_My_file\DATA\DX51D+Z\DX51D_ALL\H219C34305000_1.csv'

            # QMessageBox.information(self, '提示信息', '程序已启动...')
            model = self.lineEdit_2.text()
            if model == '无':
                QMessageBox.information(self, '提示信息', '请先选择钢种')
            else:
                local_path = os.path.abspath(os.path.dirname(__file__))
                parent_path = os.path.dirname(local_path)
                model_path = parent_path + '\\utils' + '\\model\\' + model + '.pkl'
                print(model_path)

            self.t_total, self.q_total, self.t_limit, self.spe_limit, self.t_total_contribution, self.q_con_list, self.feature, self.canshu, self.id_err, self.sum_TC, self.sum_QC, self.IU = run_pca(
                path2, path2, model_path)
            self.comboBox.clear()
            self.comboBox.addItems(map(str, self.id_err))
            self.comboBox.insertItem(0, "全长")
            self.comboBox.insertItem(0, "请选择")
            self.comboBox.setCurrentText("请选择")

            kk = Figure_Canvas.MyFigure()
            kk.visualization4(self. t_total, self.q_total, self.t_limit, self.spe_limit, name='PCA监测图')
            toolbar = NavigationToolbar2QT(kk.canvas, self)
            self.gridLayout.addWidget(kk.canvas)
            self.gridLayout.addWidget(toolbar)

            QMessageBox.information(self, '提示信息', '程序运行完成')



        except Exception as e:
            my_button = QMessageBox.information(self, '警告信息', '文件选择出错')
            print("erorr", e)

    @pyqtSlot(str)
    def on_comboBox_activated(self, p0):
        """
        Slot documentation goes here.

        @param p0 DESCRIPTION
        @type str
        """

        def on_bar_clicked(event):
            try:
                # 清除画布上的所有内容
                while self.gridLayout_4.count():
                    item = self.gridLayout_4.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.deleteLater()
            except:
                pass
            # 获取点击事件的坐标
            x = event.xdata
            y = event.ydata

            # 根据点击事件的坐标计算柱子的索引
            index = int(x + 0.5)
            if index >= 0 and index < 99:
                kk3 = Figure_Canvas.MyFigure()
                kk3.feature_IU(self.feature, index, self.canshu, self.IU)
                toolbar = NavigationToolbar2QT(kk3.canvas, self)
                self.gridLayout_4.addWidget(kk3.canvas)
                self.gridLayout_4.addWidget(toolbar)
            else:
                pass

            # 获取对应柱子的横坐标值
            # x_value = t_total_contribution[index]

            # 打印柱子的横坐标值
            print(f"点击了柱子，横坐标值为：{index}")

        try:
            # 清除画布上的所有内容
            while self.gridLayout_6.count():
                item = self.gridLayout_6.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            self.textBrowser_3.clear()
            if p0 != '全长':
                kk2 = Figure_Canvas.MyFigure()
                kk2.contribution(self.t_total_contribution, self.q_con_list, nu=int(p0))
                kk2.canvas.mpl_connect('button_press_event', on_bar_clicked)

                toolbar2 = NavigationToolbar2QT(kk2.canvas, self)
                self.gridLayout_6.addWidget(kk2.canvas)
                self.gridLayout_6.addWidget(toolbar2)

                def get_top_indexes2(values):
                    indexed_values = {index: value for index, value in enumerate(values)}
                    sorted_values = sorted(indexed_values.items(), key=lambda x: x[1], reverse=True)
                    top_three_indexes = [index for index, _ in sorted_values[:3]]
                    return top_three_indexes

                max_T_ind = get_top_indexes2(self.t_total_contribution[int(p0)])
                max_Q_ind = get_top_indexes2(self.q_con_list[int(p0)])
                # self.textBrowser_3.setText('')
                merged_string1 = set(max_T_ind + max_Q_ind)
                merged_string1 = sorted(merged_string1)
                merged_string2 = ''.join(f"第{idx}个特征{self.canshu[idx]}, " for i, idx in enumerate(merged_string1))
                merged_string = f"请重点关注：{merged_string2[:-2]}"
                self.textBrowser_3.append(merged_string)

            if p0 == '全长':
                kk2 = Figure_Canvas.MyFigure()
                kk2.contribution(self.sum_TC, self.sum_QC, nu=-1)
                kk2.canvas.mpl_connect('button_press_event', on_bar_clicked)
                toolbar2 = NavigationToolbar2QT(kk2.canvas, self)
                self.gridLayout_6.addWidget(kk2.canvas)
                self.gridLayout_6.addWidget(toolbar2)
                max_T_ind = get_top_indexes(self.sum_TC)
                max_Q_ind = get_top_indexes(self.sum_QC)

                merged_string1 = set(max_T_ind + max_Q_ind)
                merged_string1 = sorted(merged_string1)
                merged_string2 = ''.join(f"第{idx}个特征{self.canshu[idx]}, " for i, idx in enumerate(merged_string1))
                merged_string = f"请重点关注：{merged_string2[:-2]}"
                self.textBrowser_3.append(merged_string)



        except Exception as e:
            print(e)

    @pyqtSlot(str)
    def on_comboBox_2_activated(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type str
        """
        try:
            if p0 == '--请选择钢种--':
                self.lineEdit.setReadOnly(True)
                self.lineEdit_2.setReadOnly(True)
                self.lineEdit_2.setText('无')
                pass
            else:
                self.lineEdit.setReadOnly(True)
                self.lineEdit_2.setReadOnly(True)
                self.lineEdit_2.setText(p0)
                # validator = QIntValidator()  # 示例：仅允许输入整数
                # line_edit.setValidator(validator)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec())
