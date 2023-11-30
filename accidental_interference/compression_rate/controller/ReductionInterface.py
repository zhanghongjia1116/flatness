# Philxt
# TIME: 2022/6/27 22:12
# -*- coding: utf-8 -*-

"""
Module implementing ReductionInterface.
"""
import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

from ..view.Ui_ReductionInterface import Ui_MainWindow
from .Figure_Canvas import MyFigure


class ReductionInterface(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget (defaults to None)
        @type QWidget (optional)
        """
        super(ReductionInterface, self).__init__(parent)
        self.flag = 0
        self.setupUi(self)
        width_sp = ['700-1200', '1200-1500', '1500-2000']
        thick_sp = ['0.2-0.6', '0.6-1.2', '1.2-5.0']
        self.comboBox_2.addItems(width_sp)
        self.comboBox_3.addItems(thick_sp)
        # 子线程
        self.work = WorkThread()
        self.pushButton.clicked.connect(self.excute)
        self.work_2 = WorkThread_2()
        self.pushButton_3.clicked.connect(self.excute_2)
        self.is_done = 0

    def excute(self):
        global path
        tmp = os.path.abspath(__file__)
        for i in range(2):
            tmp = os.path.dirname(tmp)
        path = f"{tmp}/data"
        path = QFileDialog.getOpenFileName(self, '选择文件', path, 'CSV Files(*.csv);;XLSX Files(*.xlsx)')[0]
        if path == '':
            QMessageBox.information(self, '警告信息', '请选择文件')
        else:
            self.flag = 1

            self.work.start()
            self.work.trigger.connect(self.shuju)
            self.work.progressBarValue.connect(self.callback)
            self.work.signal_done.connect(self.callback_done)

    def excute_2(self):
        if self.flag == 0:
            QMessageBox.information(self, '警告信息', '请选择文件')
        elif self.flag == 1:
            QMessageBox.information(self, '警告信息', '文件正在加载中')
        elif self.flag == 3:
            QMessageBox.information(self, '警告信息', '文件选择出错，请重新选择文件')


        else:
            global dir_path
            path_2 = os.getcwd()
            dir_path = QFileDialog.getExistingDirectory(self, '选择文件路径', path_2)
            if dir_path == '':
                print('子线程未执行')
            else:
                self.work_2.start()

    # 更新钢种类别
    def shuju(self, shuju, flag):
        self.flag = flag
        if self.flag == 2:
            try:
                self.work.disconnect()
                self.comboBox.clear()
                steel_name = sorted(set(data['钢种']))  # set()删除重复数据 sorted()默认升序排序
                self.comboBox.addItems(steel_name)
                QMessageBox.information(self, '提示信息', '文件加载成功！')
            except:
                # self.work.disconnect()
                QMessageBox.information(self, '警告信息', '文件选择出错，请重新选择文件')
        elif self.flag == 3:
            self.work.disconnect()
            QMessageBox.information(self, '警告信息', '文件选择出错，请重新选择文件')

    # 回传进度条参数
    def callback(self, i):
        if i != 100:
            self.statusLabel.setText('文件正在加载中')
            self.pb.setValue(i)
        else:
            self.pb.setValue(i)
            self.statusLabel.setText('文件加载成功！')

    # 回传结束信号
    def callback_done(self, i):
        self.is_done = i
        if self.is_done == 1:
            self.statusLabel.setText('文件加载成功！')
        elif self.is_done == 2:
            self.statusLabel.setText('文件加载失败！')
            # QMessageBox.information(self, '警告信息', '文件选择出错，请重新选择文件')

    # 显示图像
    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        try:
            thick = self.comboBox_3.currentText()
            index_t = self.comboBox_3.currentIndex()
            width = self.comboBox_2.currentText()
            index_w = self.comboBox_2.currentIndex()
            gangzhong = self.comboBox.currentText()
            width_guige = ['宽度规格1-(700-1200)', '宽度规格2-(1200-1500)', '宽度规格3-(1500-2000)']
            thick_guige = ['厚度规格1-(0.2-0.6)', '厚度规格2-(0.6-1.2)', '厚度规格3-(1.2-5.0)']
            self.lineEdit.setText(width_guige[index_w])
            self.lineEdit_2.setText(thick_guige[index_t])

            if self.flag == 0:
                QMessageBox.information(self, '警告信息', '请选择文件')
            elif self.flag == 1:
                QMessageBox.information(self, '警告信息', '文件正在加载中')
            elif self.flag == 3:
                QMessageBox.information(self, '警告信息', '文件选择出错，请重新选择文件')
            elif gangzhong == '':
                QMessageBox.information(self, '警告信息', '请选择钢种')
            else:
                data_gz = data[data['钢种'] == gangzhong]
                data_gz_w = data_gz[data_gz['宽度区间'] == width]
                data_gz_w_t = data_gz_w[data_gz_w['厚度区间'] == thick]
                if data_gz_w_t.shape[0] == 0:
                    QMessageBox.information(self, '提示信息', '未生产上述规格产品')
                else:
                    print(data_gz_w_t.shape)
                    x = np.linspace(1, len(data_gz_w_t['钢种']),
                                    len(data_gz_w_t['钢种']))  # linspace创建等差序列
                    print(x)

                    # 删除布局所有控件
                    for i in range(0, self.gridLayout_2.count()):
                        self.gridLayout_2.itemAt(i).widget().deleteLater()

                    # 绘图
                    yaxialv_iu = MyFigure()
                    yaxialv_iu.draw_yaxialv(data_gz_w_t, gangzhong, width, thick, x)
                    self.yaxialv_iu = yaxialv_iu.canvas
                    self.gridLayout_2.addWidget(self.yaxialv_iu)
                    line_v = []  # 添加的竖线对象
                    line_h = []  # 添加水平线对象
                    biaozhu = []  # 添加标注
                    for i in yaxialv_iu.fig.get_axes():
                        # i.axvline(x=-1, color='skyblue')
                        # i.axhline(-1,color='skyblue')
                        line_v.append(i.axvline(x=-1, color='skyblue'))
                        line_h.append(i.axhline(-1, color='skyblue'))
                        # 添加标签
                        # i.text(-1, 33, '32', size=12, family="Times new roman", color="black", style='italic',
                        #          weight="light", bbox=dict(facecolor="dimgray", alpha=0.5, boxstyle="round"))
                        biaozhu.append(
                            i.text(-1, 33, '32', size=12, family="Times new roman", color="black", style='italic',
                                   weight="light", bbox=dict(facecolor="dimgray", alpha=0.5, boxstyle="round")))
                    # 初始设置不可见
                    for i in biaozhu:
                        i.set_visible(False)
                    for i in line_h:
                        i.set_visible(False)
                    for i in line_v:
                        i.set_visible(False)

                varitions = ['STAND_01_reduction start', 'STAND_02_reduction start', 'STAND_03_reduction start',
                             'STAND_04_reduction start', 'STAND_05_reduction start', '板形均值IU']  # compression_rate

                def motion(event):
                    try:
                        if round(event.xdata) > 0:
                            for i, j in enumerate(line_v):  # 重新辅助线的值

                                y = data_gz_w_t[varitions[i]].values  # 压下率值 与 IU值

                                j.set_xdata(round(event.xdata))  # 绘制直线
                                line_h[i].set_ydata(y[round(event.xdata) - 1])  # 绘制水平线
                                # 数据标签
                                biaozhu[i].set_position((round(event.xdata), y[round(event.xdata) - 1]))
                                biaozhu[i].set_text(str(round(y[round(event.xdata) - 1], 2)))
                                j.set_visible(True)
                                line_h[i].set_visible(True)
                                biaozhu[i].set_visible(True)

                            yaxialv_iu.canvas.draw_idle()
                    except:
                        pass

                yaxialv_iu.canvas.mpl_connect('motion_notify_event', motion)

        except:
            pass


# 一键绘图参数
def draw_pic(reduce_data, n, w, t, dir_path):  # 一键绘图参数
    varitions = ['STAND_01_reduction start', 'STAND_02_reduction start', 'STAND_03_reduction start',
                 'STAND_04_reduction start', 'STAND_05_reduction start']  # 'compression_rate'

    # print(reduce_data, len(reduce_data['钢种']))
    x = np.linspace(1, len(reduce_data['钢种']), len(reduce_data['钢种']))  # linspace创建等差序列
    # print(x)

    # ymajorLocator = MultipleLocator(0.5)  # 将y轴主刻度标签设置为0.5的倍数
    ymajorFormatter = FormatStrFormatter('%1.2f')  # 设置y轴标签文本的格式
    # yminorLocator = MultipleLocator(0.1)  # 将此y轴次刻度标签设置为0.1的倍数

    plt.figure()
    plt.suptitle('钢种：' + n + '-宽度：' + w + '-厚度：' + t)
    for m, var in enumerate(varitions):  # enumerate既能获得索引，也能获得元素  #生成五个压下率的图
        # plt.subplots(6, m+1, sharex='col')
        plt.subplot(6, 1, m + 1)
        ax_m = plt.gca()  # 获取当前对象
        j = str(m + 1)
        r_m = reduce_data[var].values
        # print(var)
        plt.plot(x, r_m, 'bo', markersize='3')
        plt.ylabel('机架_' + j)
        if r_m.size == 0:
            plt.ylim(-30, 30)
        else:
            plt.ylim(np.min(r_m) - 1, np.max(r_m) + 1)  # 设置临界
        ax_m.yaxis.set_major_formatter(ymajorFormatter)  # 设置y坐标轴的格式
    plt.subplot(6, 1, 6)
    r_6 = reduce_data['板形均值IU'].values
    plt.plot(x, r_6, 'ro', markersize='3')
    plt.xlabel('钢卷样本')
    plt.ylabel('IU均值')
    if r_6.size == 0:
        plt.ylim(-30, 30)
    else:
        plt.ylim(np.min(r_6) - 1, np.max(r_6) + 1)  # 设置临界
    plt.tight_layout()
    if '/' in n:
        n = n.replace('/', '_')
    # plt.show()
    plt.savefig(dir_path + '/' + '钢种：' + n + '-宽度：' + w + '-厚度：' + t + 'compression_rate-IU图.jpg')


# 子线程
class WorkThread(QThread):
    trigger = pyqtSignal(pd.DataFrame, int)  # 用来传递参数 信号与槽函数的连接
    progressBarValue = pyqtSignal(int)  # 更新进度条
    signal_done = pyqtSignal(int)  # 是否结束信号

    def __init__(self):
        super(WorkThread, self).__init__()

    def run(self):
        # 读取数据
        def getData(path):
            if 'csv' in path:
                self.progressBarValue.emit(2)
                data1 = pd.read_csv(path, header=0, low_memory=False)  # 读取csv数据,head=None不确定表头（1，2，3...）
                print('读入csv数据！')
            elif 'xls' in path:
                self.progressBarValue.emit(2)
                data1 = pd.read_excel(path, header=0)  # 读取excel数据
                print('读入excel数据！')
            else:
                self.progressBarValue.emit(2)
                print('输入数据有误！')
            return data1

        global data
        try:
            data1 = getData(path)
            self.progressBarValue.emit(50)
            data = data1.iloc[:, 1:]
            self.progressBarValue.emit(89)
            flag = 2  # 代表文件加载成功
            self.signal_done.emit(0)
            self.progressBarValue.emit(100)
            self.signal_done.emit(1)
            self.trigger.emit(data, flag)

        except:
            flag = 3  # 文件加载失败
            data = pd.DataFrame()
            self.progressBarValue.emit(0)
            self.signal_done.emit(2)
            self.trigger.emit(data, flag)


# 一键保存图片线程
class WorkThread_2(QThread):
    def __init__(self):
        super(WorkThread_2, self).__init__()

    def run(self):
        try:
            steel_name = sorted(set(data['钢种']))  # set()删除重复数据 sorted()默认升序排序
            width_guige = ['宽度规格1-(700-1200)', '宽度规格2-(1200-1500)', '宽度规格3-(1500-2000)']
            thick_guige = ['厚度规格1-(0.2-0.6)', '厚度规格2-(0.6-1.2)', '厚度规格3-(1.2-5.0)']
            width_sp = ['700-1200', '1200-1500', '1500-2000']
            thick_sp = ['0.2-0.6', '0.6-1.2', '1.2-5.0']
            for a in steel_name:
                data_gangzhong = data[data['钢种'] == a]
                for b in width_sp:
                    data_gangzhong_width = data_gangzhong[data_gangzhong['宽度区间'] == b]
                    for c in thick_sp:
                        data_gangzhong_width_thick = data_gangzhong_width[data_gangzhong_width['厚度区间'] == c]
                        draw_pic(data_gangzhong_width_thick, a, b, c, dir_path)
        except:
            return None


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = ReductionInterface()
    ui.show()
    sys.exit(app.exec_())
