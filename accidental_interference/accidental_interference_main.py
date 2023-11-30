import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget
from my_utils.myterminal import MyTerminal
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import NavigationItemPosition, MessageBox
from qtResource.MyIcon import MyIcon

from accidental_interference.Ui_accidental_interference_main import Ui_AccidentalFactor


class 慢偶因素(Ui_AccidentalFactor, QWidget):
    currentChanged = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        # self.stackedWidget = self.stackedWidget
        self.setupUi(self)
        self.initNavigation()
        self.terminal = MyTerminal()
        self.terminal.show()

    def initNavigation(self):
        # self.stackedWidget.
        self.addSubInterface(self.LiquidPage, MyIcon.LIQUID, '乳化液')
        self.addSubInterface(self.ClassPage, MyIcon.CLASS, '班组')
        self.addSubInterface(self.ReductionPage, MyIcon.REDUCTION, '压下率')
        self.addSubInterface(self.StopPage, MyIcon.STOP, '停机')
        self.addSubInterface(self.MaterialPage, MyIcon.MATERIAL, '来料')
        self.addSubInterface(self.RollingPage, MyIcon.ROLLING, '轧辊服役')

        # self.addSubInterface(self.libraryInterface, FIF.BOOK_SHELF, '库', NavigationItemPosition.BOTTOM,
        #                      FIF.LIBRARY_FILL)
        self.NavigationBar.addItem(routeKey='Help',
                                   icon=FIF.HELP,
                                   text='帮助',
                                   onClick=self.showMessageBox,
                                   selectable=False,
                                   position=NavigationItemPosition.BOTTOM, )
        # self.NavigationBar.setFixedSize(50,50)

        self.stackedWidget.currentChanged.connect(self.onCurrentInterfaceChanged)
        self.NavigationBar.setCurrentItem(self.LiquidPage.objectName())

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

    def closeEvent(self, a0):
        self.terminal.close()
        super().closeEvent(a0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = 慢偶因素()
    win.show()
    sys.exit(app.exec_())
