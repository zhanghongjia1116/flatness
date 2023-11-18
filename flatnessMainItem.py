# coding:utf-8
import sys

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget, QVBoxLayout, QLabel, QSizePolicy

from qfluentwidgets import Pivot, setTheme, Theme, SegmentedWidget, FluentIcon
# from 慢偶因素板形干扰评估.慢偶因素Main import AccidentalFactor
from 慢偶因素板形干扰评估.慢偶因素Main import 慢偶因素
from 异常板形监测溯源.异常板形监测溯源Main import 异常板形监测溯源
from 板形质量评价.板形质量评价Main import 板形质量评价
from 板形调控功效挖掘.板形调控功效挖掘py import 板形调控功效挖掘
from 板形生成数据建模.板形生成数据建模Main import 板形生成数据建模
from 板形控制能力评价.板形控制能力评价Main import 板形控制能力评价
from 板形控制数模优化.板形控制数模优化Main import 板形控制数模优化


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1200, 900)
        self.setWindowTitle('灯塔工厂上线')
        # icon = QtGui.QIcon()
        # icon.addPixmap(QtGui.QPixmap(":/icons/images/SY-pic.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # 创建 QIcon 对象并设置图标路径
        icon = QIcon("D:/zhhj_work/zhhj_GUI/flatness/qtResource/images/SY-pic.jpg")
        self.setWindowIcon(icon)

        self.pivot = SegmentedWidget(self)
        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self)

        self.板形质量评价 = 板形质量评价()
        self.异常板形监测溯源 = 异常板形监测溯源()
        self.慢偶因素板形干扰评估 = 慢偶因素()
        self.板形调控功效挖掘 = 板形调控功效挖掘()
        self.板形生成数据建模 = 板形生成数据建模()
        self.板形控制能力评价 = 板形控制能力评价()
        self.板形控制数模优化 = 板形控制数模优化()

        self.addSubInterface(self.板形质量评价, '板形质量评价', '板形质量评价')
        self.addSubInterface(self.异常板形监测溯源, '异常板形监测溯源', '异常板形监测溯源')
        self.addSubInterface(self.慢偶因素板形干扰评估, '慢偶因素板形干扰评估', '慢偶因素板形干扰评估')
        self.addSubInterface(self.板形调控功效挖掘, '板形调控功效挖掘', '板形调控功效挖掘')
        self.addSubInterface(self.板形生成数据建模, '板形生成数据建模', '板形生成数据建模')
        self.addSubInterface(self.板形控制能力评价, '板形控制能力评价', '板形控制能力评价')
        self.addSubInterface(self.板形控制数模优化, '板形控制数模优化', '板形控制数模优化')

        self.vBoxLayout.addWidget(self.pivot)
        self.vBoxLayout.addWidget(self.stackedWidget)
        # self.vBoxLayout.setContentsMargins(30, 10, 30, 30)

        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.板形质量评价)
        self.pivot.setCurrentItem(self.板形质量评价.objectName())

    def addSubInterface(self, widget, objectName, text):
        widget.setObjectName(objectName)
        # widget.setAlignment(Qt.AlignCenter)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget),
        )
        self.pivot.setItemFontSize(18)

    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()
