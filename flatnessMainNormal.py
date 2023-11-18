# coding:utf-8
import sys

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget, QVBoxLayout, QLabel, QSizePolicy, QMainWindow
from Ui_flatnessMainNormal import Ui_MainWindow
from qfluentwidgets import Pivot, setTheme, Theme, SegmentedWidget, FluentIcon
# from 慢偶因素板形干扰评估.慢偶因素Main import AccidentalFactor
from 慢偶因素板形干扰评估.慢偶因素Main import 慢偶因素
from myterminal import MyTerminal
# from 异常板形监测溯源.异常板形监测溯源Main import 异常板形监测溯源
# from 板形质量评价.板形质量评价Main import 板形质量评价
# from 板形调控功效挖掘.板形调控功效挖掘 import 板形调控功效挖掘
# from 板形生成数据建模.板形生成数据建模Main import 板形生成数据建模
# from 板形控制能力评价.板形控制能力评价Main import 板形控制能力评价
# from 板形控制数模优化.板形控制数模优化Main import 板形控制数模优化


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.板形质量评价 = None
        self.异常板形监测溯源 = None
        self.慢偶因素板形干扰评估 = None
        self.板形调控功效挖掘 = None
        self.板形生成数据建模 = None
        self.板形控制能力评价 = None
        self.板形控制数模优化 = None

    @pyqtSlot()
    def on_PrimaryPushButton_clicked(self):
        self.板形质量评价 = 板形质量评价()
        self.板形质量评价.show()

    @pyqtSlot()
    def on_PrimaryPushButton_2_clicked(self):
        self.异常板形监测溯源 = 异常板形监测溯源()
        self.异常板形监测溯源.show()

    @pyqtSlot()
    def on_PrimaryPushButton_3_clicked(self):
        self.慢偶因素板形干扰评估 = 慢偶因素()
        self.慢偶因素板形干扰评估.show()
        self.terminal = MyTerminal()
        self.terminal.show()

    @pyqtSlot()
    def on_PrimaryPushButton_4_clicked(self):
        self.板形调控功效挖掘 = 板形调控功效挖掘()
        self.板形调控功效挖掘.show()

    @pyqtSlot()
    def on_PrimaryPushButton_5_clicked(self):
        self.板形生成数据建模 = 板形生成数据建模()
        self.板形生成数据建模.show()

    @pyqtSlot()
    def on_PrimaryPushButton_6_clicked(self):
        self.板形控制能力评价 = 板形控制能力评价()
        self.板形控制能力评价.show()

    @pyqtSlot()
    def on_PrimaryPushButton_7_clicked(self):
        self.板形控制数模优化 = 板形控制数模优化()
        self.板形控制数模优化.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
