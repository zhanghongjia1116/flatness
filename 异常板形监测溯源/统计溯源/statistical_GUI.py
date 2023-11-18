"""
Module implementing FullLengthQuality.
"""
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QValidator
from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QMessageBox
from PyQt5.QtWidgets import *
# from statistical_method import *
from ..utils.statistical_method import *
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

matplotlib.use("Qt5Agg")
from matplotlib import pyplot
# import Figure_Canvas
from ..utils import Figure_Canvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from scipy.stats import spearmanr
# from MXL_Support import *
from ..utils.MXL_Support import *

pyplot.rcParams['font.sans-serif'] = ['SimHei']
pyplot.rcParams['axes.unicode_minus'] = False

from .Ui_statistical_GUI import Ui_mainWindow
import os
import warnings

# 忽略所有RuntimeWarning
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=UserWarning)


class MainWindow(QMainWindow, Ui_mainWindow):
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
        # self.clik = 1
        # self.dataSignal=None

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        try:
            self.cwd = os.getcwd()  # 获取当前程序文件位置
            local_path = os.path.abspath(os.path.dirname(__file__))  # 获取本文件所在位置
            parent_path = os.path.dirname(local_path)  # 获取本文件的上级目录
            self.train_path = \
                QFileDialog.getOpenFileName(self, "ADD", parent_path, "CSV Files(*.csv);;XLSX Files(*.xlsx)")[0]
            self.textBrowser_2.setText(self.train_path)
        except:
            QMessageBox.information(self, '提示信息', '选择数据集发生错误')
            return None

    @pyqtSlot()
    def on_pushButton_3_clicked(self):

        # QMessageBox.information(self, '提示信息', '程序已启动，请等待运行完成。')

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
                path = self.textBrowser_2.toPlainText()

            else:
                QMessageBox.information(self, '提示信息', '请先选择数据')

            threshold = float(self.lineEdit_2.text())
            threshold2 = threshold

            self.data = pd.read_csv(path, header=0, encoding='gbk').dropna()

            self.canshu = get_canshu2()
            # 检查参数是否都在self.data的列中，并创建符合条件的参数列表
            filtered_canshu = [c for c in self.canshu if c in self.data.columns]

            if filtered_canshu:
                self.df0 = self.data[filtered_canshu]
            else:
                self.df0 = self.data
            # self.df0 = self.dataSignal[self.canshu]
            self.canshu = self.canshu[:-1]
            self.feature = self.df0.values
            self.IU = self.data['F5 flatness error']
            # name_all = path.split('\\')[-1].split('.')[0]
            # name = name_all[:13]
            # print('file_name:', name)

            # if self.lineEdit_2.text()[:3] == '999':
            if True:
                self.pda = 1
                # QMessageBox.information(self, '提示信息', 'PDA数据模式')
                iu_mean = self.IU
                # threshold2 = int(self.lineEdit_2.text()[3:])
                # print(threshold2)
            else:
                self.pda = 0
                flat = self.dataSignal.values[:, -62:] / -2100000
                pot1, pot2, row_pot2 = jugde_row_col(flat)
                row_pot = flat.shape[0]
                data_n = self.dataSignal.iloc[:row_pot, :]
                useflat = flat[:row_pot, pot1:pot2]
                flatness = []
                iu_mean = []
                iu_rms = []
                iu_max = []
                iu_max_min = []
                for j in range(row_pot):
                    flatness1 = free_chazhi(useflat[j])[0]
                    flatness1 = flatness1 - np.mean(flatness1)  # 0均值处理
                    flatness.append(flatness1)

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

            kk = Figure_Canvas.MyFigure()
            kk.visualization2(iu_mean, threshold2)
            toolbar = NavigationToolbar2QT(kk.canvas, self)
            self.gridLayout.addWidget(kk.canvas)
            self.gridLayout.addWidget(toolbar)

            # QMessageBox.information(self, '提示信息', '程序运行完成')


        except Exception as e:
            my_button = QMessageBox.information(self, '警告信息', '文件选择出错')
            print("erorr", e)

    @pyqtSlot(int)
    def on_comboBox_2_activated(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type int
        """
        """
        Slot documentation goes here.

        @param p0 DESCRIPTION
        @type str
        """
        try:
            if index == 0:
                # self.lineEdit.setReadOnly(True)
                # self.lineEdit_2.setReadOnly(True)
                self.lineEdit_2.setText('无')
                pass
            else:

                validator = QDoubleValidator()  # 示例：允许输入整数和小数
                self.lineEdit_2.setValidator(validator)

                # lim = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
                lim = [4.64, 3.55, 3.92, 4.07, 8.22, 3.33, 2.38, 3.05, 4.17, 2.19, 3.40, 3.30, 2.28]
                # self.lineEdit.setReadOnly(True)
                # self.lineEdit_2.setReadOnly(True)
                self.lineEdit_2.setText(str(lim[index - 1]))

        except Exception as e:
            print(e)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
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

            df_scaled = normalize(np.array(self.df0))
            # 创建新的DataFrame来存储处理后的数据
            df = pd.DataFrame(df_scaled, columns=self.df0.columns)

            correlation = df.corr()['F5 flatness error'][:-1]

            correlation2, _ = spearmanr(df)
            correlation2 = pd.DataFrame(correlation2, columns=df.columns, index=df.columns)
            top_features = correlation2['F5 flatness error'][:-1]

            kk2 = Figure_Canvas.MyFigure()
            kk2.relate(correlation, top_features)
            kk2.canvas.mpl_connect('button_press_event', on_bar_clicked)

            toolbar2 = NavigationToolbar2QT(kk2.canvas, self)
            self.gridLayout_6.addWidget(kk2.canvas)
            self.gridLayout_6.addWidget(toolbar2)

            # def get_top_indexes2(values):
            #     indexed_values = {index: value for index, value in enumerate(values)}
            #     sorted_values = sorted(indexed_values.items(), key=lambda x: x[1], reverse=True)
            #     top_three_indexes = [index for index, _ in sorted_values[:3]]
            #     return top_three_indexes

            def get_top_indexes2(values):
                indexed_values = {index: abs(value) for index, value in enumerate(values)}
                sorted_values = sorted(indexed_values.items(), key=lambda x: x[1], reverse=True)
                top_three_indexes = [index for index, _ in sorted_values[:3]]
                return top_three_indexes

            max_T_ind = get_top_indexes2(correlation)
            max_Q_ind = get_top_indexes2(top_features)
            merged_string1 = set(max_T_ind + max_Q_ind)
            merged_string1 = sorted(merged_string1)
            merged_string2 = ''.join(f"第{idx}个特征{self.canshu[idx]}, " for i, idx in enumerate(merged_string1))
            merged_string = f"请重点关注：{merged_string2[:-2]}"
            self.textBrowser_3.append(merged_string)

            # # 拼接max_T_ind对应的字符串及信息
            # max_T_string = ''.join(f"第{idx}个特征{self.canshu[idx]}, " for i, idx in enumerate(max_T_ind))
            # max_T_string = f"皮尔逊相关系数绝对值前三特征：{max_T_string[:-2]}"  # 去除最后的逗号和空格
            #
            # # 在textBrowser_3中显示max_T_ind对应的字符串及信息
            # self.textBrowser_3.append(max_T_string)
            #
            # # 拼接max_Q_ind对应的字符串及信息
            # max_Q_string = ''.join(f"第{idx}个特征{self.canshu[idx]}, " for i, idx in enumerate(max_Q_ind))
            # max_Q_string = f"斯皮尔曼相关系数绝对值前三特征：{max_Q_string[:-2]}"  # 去除最后的逗号和空格
            #
            # # 在textBrowser_3中显示max_Q_ind对应的字符串及信息
            # self.textBrowser_3.append(max_Q_string)
        except Exception as e:
            print(e)
            # pass


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec())
