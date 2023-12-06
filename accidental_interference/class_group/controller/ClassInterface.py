# Philxt
# TIME: 2022/6/2 21:58
# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
import matplotlib
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QProgressBar, QLabel

from .Figure_Canvas import MyFigure
from .classSearch import inquiryClass, connect
from .dialog import Dialog
from ..view.Ui_ClassInterface import Ui_MainWindow

matplotlib.use("Qt5Agg")

global reg
reg = ('', '', '', '', '', '')  # 防止reg未定义，connect()报错


class MainWindow(QMainWindow, Ui_MainWindow):
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
        # 实例化子线程
        self.work = WorkThread()
        self.work_2 = WorkThread_2()
        self.pushButton.clicked.connect(self.excute)
        self.pushButton.clicked.connect(self.excute_2)
        self.flag = 0

    def excute(self):
        year_s = int(self.dateEdit.text().split('/')[0])
        month_s = int(self.dateEdit.text().split('/')[1])
        year_e = int(self.dateEdit_2.text().split('/')[0])
        month_e = int(self.dateEdit_2.text().split('/')[1])
        if year_s - year_e > 0 or (year_s - year_e == 0 and month_s - month_e > 0):
            QMessageBox.information(self, '提示信息', '请修改开始与结束时间范围')
        else:
            if reg[2] != '' and reg[3] != '' and self.flag == 3:  # 密码正确后不用进行弹窗
                pass
            else:
                # 实例化弹窗
                self.my_dialog = Dialog(self)
                # 连接主窗口 信号与槽函数
                self.my_dialog.signal.connect(self.information)
                self.my_dialog.exec_()

            global startTime, endTime
            startTime = self.dateEdit.text()
            endTime = self.dateEdit_2.text()

            startTime = startTime.replace('/', '-') + '-01 00:00:00'  # shijian_shang #开始结束时间
            endTime = endTime.replace('/', '-') + '-01 00:00:00'  # shijian_xia
            print(startTime, endTime)

            self.work.start()
            self.work.trigger.connect(self.drawp)
            self.work.error.connect(self.error)
            self.work.progressBarValue.connect(self.callback)
            self.work.signal_done.connect(self.callback_done)

    def excute_2(self):
        self.work_2.start()
        self.work_2.prompt.connect(self.prompt)
        self.work_2.progressBarValue.connect(self.callback)
        self.work_2.signal_done.connect(self.callback_done)

    # 正在加载提示
    def prompt(self, flag):
        self.work_2.disconnect()
        self.flag = flag
        if self.flag == 2:
            QMessageBox.information(self, '提示信息', '数据正在加载中,请稍后')

    # 获取弹窗输入信息，定义全局变量，在子线程调用
    def information(self, my_reg):
        global reg
        reg = my_reg
        self.my_dialog.close()
        print(my_reg)
        return my_reg

    # 回传进度条参数
    def callback(self, i):
        if i != 100:
            if self.flag == 1:
                self.statusLabel.setText('数据加载失败！')
            else:
                self.statusLabel.setText('数据正在加载中')
                self.pb.setValue(i)
        else:
            self.pb.setValue(i)
            self.statusLabel.setText('数据加载成功！')

    # 回传结束信号
    def callback_done(self, i):
        self.is_done = i
        if self.is_done == 1:
            self.statusLabel.setText('数据加载成功！')
        elif self.is_done == 2 or self.flag == 1:
            self.statusLabel.setText('数据加载失败！')

    # 连接提示
    def error(self, flag):
        self.work.disconnect()
        self.flag = flag
        if self.flag == 1:
            QMessageBox.information(self, '提示信息', '数据库连接失败，请重试')

    # 绘图
    def drawp(self, shuju):
        self.work.disconnect()
        global everyclassIUlist, jiaClassIUList, yiClassIUList, bingClassIUList, dingClassIUList, timelist, jiaClassIUListZhaGun, jiaClassIUListIU, yiClassIUListZhaGun, \
            yiClassIUListIU, bingClassIUListZhaGun, bingClassIUListIU, dingClassIUListZhaGun, dingClassIUListIU
        everyclassIUlist, jiaClassIUList, yiClassIUList, bingClassIUList, dingClassIUList, timelist, jiaClassIUListZhaGun, jiaClassIUListIU, yiClassIUListZhaGun, \
            yiClassIUListIU, bingClassIUListZhaGun, bingClassIUListIU, dingClassIUListZhaGun, dingClassIUListIU = shuju
        self.flag = 3

        # 清除内容
        self.comboBox.clear()
        self.comboBox_2.clear()
        global _class  # 用于设置班组下拉框选项
        _class = ['甲', '乙', '丙', '丁']
        self.comboBox.addItems(_class)

        print(timelist)
        month = []  # 用于设置月份下拉框选项
        for i in timelist:
            j = i[0] + '-' + i[1]
            month.append(j)
        self.comboBox_2.addItems(month)
        QMessageBox.information(self, '提示信息', '数据加载成功')

    @pyqtSlot()
    def on_pushButton_2_clicked(self):  # 显示图像
        """
        Slot documentation goes here.
        """
        # 绘图
        # 删除布局所有控件
        if self.flag == 0:
            QMessageBox.information(self, '提示信息', '请先加载数据')
        elif self.flag == 1:
            QMessageBox.information(self, '提示信息', '数据库连接失败，请重试')
        elif self.flag == 2:
            QMessageBox.information(self, '提示信息', '数据正在加载中,请稍后')
        else:
            for i in range(0, self.gridLayout.count()):
                self.gridLayout.itemAt(i).widget().deleteLater()
            banzu_fig = MyFigure()
            banzu_fig.inquiryClass(everyclassIUlist)
            self.banzu = banzu_fig.canvas
            # self.zong_fig.inquiryClass(everyclassIUlist)
            self.gridLayout.addWidget(self.banzu)

            zhazhiclass = self.comboBox.currentText()

            if self.comboBox.currentText() == '甲':
                y = jiaClassIUList
            elif self.comboBox.currentText() == '乙':
                y = yiClassIUList
            elif self.comboBox.currentText() == '丙':
                y = bingClassIUList
            elif self.comboBox.currentText() == '丁':
                y = dingClassIUList
            print('++++++++++++++++++++++++++++++++++++++++++++')
            print(y)
            x = timelist
            for i in range(0, self.gridLayout_2.count()):
                self.gridLayout_2.itemAt(i).widget().deleteLater()

            month_fig = MyFigure()
            month_fig.inquiryClassEachMonth(x, y, zhazhiclass)
            self.month = month_fig.canvas
            self.gridLayout_2.addWidget(self.month)

            # #判断列表中是否存在0值，返回索引，删掉即可
            # index_list=[]
            # for i in range(0,len(y)):
            #      if y[i]==0:
            #          index_list.append(i)
            # print()
            # for j  in index_list:
            #     self.comboBox_2.removeItem(j)

            index = self.comboBox_2.currentIndex()
            if self.comboBox.currentText() == '甲':
                x = jiaClassIUListZhaGun[index]
                y = jiaClassIUListIU[index]
                t = timelist[index][0] + '—' + timelist[index][1]
            elif self.comboBox.currentText() == '乙':
                x = yiClassIUListZhaGun[index]
                y = yiClassIUListIU[index]
                t = timelist[index][0] + '—' + timelist[index][1]
            elif self.comboBox.currentText() == '丙':
                x = bingClassIUListZhaGun[index]
                y = bingClassIUListIU[index]
                t = timelist[index][0] + '—' + timelist[index][1]
            elif self.comboBox.currentText() == '丁':
                x = dingClassIUListZhaGun[index]
                y = dingClassIUListIU[index]
                t = timelist[index][0] + '—' + timelist[index][1]

            if y != 0:
                for i in range(0, self.gridLayout_3.count()):
                    self.gridLayout_3.itemAt(i).widget().deleteLater()

                zhagun_fig = MyFigure()
                zhagun_fig.inquiryClassEachZhaGun(x, y, t, zhazhiclass)
                self.zhagun = zhagun_fig.canvas
                self.gridLayout_3.addWidget(self.zhagun)
            else:
                for i in range(0, self.gridLayout_3.count()):
                    self.gridLayout_3.itemAt(i).widget().deleteLater()

                QMessageBox.information(self, '提示信息', '暂无工作辊生产数据')


# 子线程1 用于处理数据
class WorkThread(QThread):
    trigger = pyqtSignal(tuple)
    error = pyqtSignal(int)
    load = pyqtSignal(int)
    progressBarValue = pyqtSignal(int)  # 更新进度条
    signal_done = pyqtSignal(int)  # 是否结束信号

    def __init__(self):
        super(WorkThread, self).__init__()

    def run(self):
        try:
            self.progressBarValue.emit(20)
            shuju = inquiryClass(startTime, endTime, reg)
            self.progressBarValue.emit(80)
            self.progressBarValue.emit(100)
            self.signal_done.emit(1)
            self.trigger.emit(shuju)
        except:
            flag = 1
            self.progressBarValue.emit(0)
            self.signal_done.emit(2)
            self.error.emit(flag)


# 子线程2 用于提示数据库是否连接成功
class WorkThread_2(QThread):
    prompt = pyqtSignal(int)
    progressBarValue = pyqtSignal(int)  # 更新进度条
    signal_done = pyqtSignal(int)  # 是否结束信号

    def __init__(self):
        super(WorkThread_2, self).__init__()

    def run(self):
        flag = connect(reg)[1]
        self.progressBarValue.emit(10)
        self.prompt.emit(flag)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
