import sys
from enum import Enum

from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, QUrl, QSize, Qt
from PyQt5.QtGui import QDesktopServices, QFont, QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget
from qfluentwidgets import NavigationItemPosition, FluentIconBase, Theme, getIconColor, MessageBox, Icon
from qfluentwidgets import FluentIcon as FIF
from qtResource.MyIcon import MyIcon

from .Ui_板形控制数模优化Main import Ui_banxingkongzhishumo


class 板形控制数模优化(Ui_banxingkongzhishumo, QWidget):
    currentChanged = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initNavigation()
        # self.resize(1000, 800)

    def initNavigation(self):
        # self.stackedWidget.
        self.addSubInterfaceNavigation(self.tablePage, MyIcon.预设定表格, '表格自学习')
        self.addSubInterfaceNavigation(self.mechanismPage, MyIcon.预设定机理, '机理在线优化')
        self.addSubInterfaceNavigation(self.feedbackControlPage, MyIcon.反馈控制, '反馈控制')
        self.addSubInterfaceNavigation(self.designPage, MyIcon.设计, '辊形设计')

        self.NavigationBar.addItem(routeKey='Help',
                                   icon=FIF.HELP,
                                   text='帮助',
                                   onClick=self.showMessageBox,
                                   selectable=False,
                                   position=NavigationItemPosition.BOTTOM, )
        # self.NavigationBar.setFixedSize(50,50)

        self.stackedWidget.currentChanged.connect(self.onCurrentInterfaceChanged)
        self.NavigationBar.setCurrentItem(self.tablePage.objectName())

    def addSubInterfaceNavigation(self, interface, icon, text: str, position=NavigationItemPosition.TOP,
                                  selectedIcon=None):
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
            '联系方式',
            '北京市海淀区学院路30号北京科技大学机械工程学院周晓敏组，联系电话：010-62334963',
            self
        )
        w.yesButton.setText('ok')
        w.cancelButton.setText('close')

        w.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = 板形控制数模优化()
    win.show()
    sys.exit(app.exec_())
