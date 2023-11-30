import sys
from enum import Enum

from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, QUrl, QSize
from PyQt5.QtGui import QDesktopServices, QFont, QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from qfluentwidgets import NavigationItemPosition, FluentIconBase, Theme, getIconColor, MessageBox, Icon
from qfluentwidgets import FluentIcon as FIF
from qtResource.MyIcon import MyIcon

from flatness_generate_data_model.Ui_flatness_generate_data_model_main import Ui_板形生成数据建模


class 板形生成数据建模(Ui_板形生成数据建模, QWidget):
    currentChanged = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        # self.stackedWidget = self.stackedWidget
        self.setupUi(self)
        self.initNavigation()
        # self.centerWindow()

    def centerWindow(self):
        # 获取主屏幕的几何信息
        screenGeometry = QDesktopWidget().screenGeometry()

        # 计算窗口在屏幕上的中心坐标
        x = (screenGeometry.width() - self.width()) // 2
        y = (screenGeometry.height() - self.height()) // 2

        # 移动窗口到中心
        self.move(x, y)

    def initNavigation(self):
        # self.stackedWidget.
        self.addSubInterface(self.existPage, MyIcon.有无, '缺陷有无预测')
        self.addSubInterface(self.classificationPage, MyIcon.多分类, '多分类预测')
        self.addSubInterface(self.regressionPage, MyIcon.回归, '回归预测')

        self.NavigationBar.addItem(routeKey='Help',
                                   icon=FIF.HELP,
                                   text='帮助',
                                   onClick=self.showMessageBox,
                                   selectable=False,
                                   position=NavigationItemPosition.BOTTOM, )
        # self.NavigationBar.setFixedSize(50,50)

        self.stackedWidget.currentChanged.connect(self.onCurrentInterfaceChanged)
        self.NavigationBar.setCurrentItem(self.existPage.objectName())

    def addSubInterface(self, interface, icon, text: str, position=NavigationItemPosition.TOP, selectedIcon=None):
        """ add sub interface """
        self.stackedWidget.addWidget(interface)
        self.NavigationBar.addItem(routeKey=interface.objectName(),
                                   icon=icon,
                                   text=text,
                                   onClick=lambda: self.switchTo(interface),
                                   selectedIcon=selectedIcon,
                                   position=position, )
        # font = QFont()
        # font.setPointSize(50)  # 设置字体大小为16
        # self.NavigationBar.setFont(font)
        # self.NavigationBar.setFixedSize(80, 500)
        # self.NavigationBar.setMinimumSize(50, 50)

    def switchTo(self, widget):
        self.stackedWidget.setCurrentWidget(widget)

    def onCurrentInterfaceChanged(self, index):
        widget = self.stackedWidget.widget(index)
        self.NavigationBar.setCurrentItem(widget.objectName())

    def showMessageBox(self):
        w = MessageBox(
            '帮助',
            '冷轧板形控制智能化智能支撑系统软件所有权-北京科技大学&北京首钢自动化信息技术有限公司&首钢顺义冷轧薄板厂',
            self
        )
        w.yesButton.setText('ok')
        w.cancelButton.setText('close')

        w.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = 板形生成数据建模()
    win.show()
    sys.exit(app.exec_())
