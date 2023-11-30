import sys
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget
from qfluentwidgets import FluentIcon as FIF
# from matplotlib.backends.backend_qt import NavigationToolbar2QT
from qfluentwidgets import NavigationItemPosition, MessageBox
from qtResource.MyIcon import MyIcon
from abnormal_flatness_monitoring.Ui_abnormal_flatness_monitoring_main import Ui_Monitor


class 异常板形监测溯源(Ui_Monitor, QWidget):
    currentChanged = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initNavigation()
        self.resize(1300, 1000)

    def initNavigation(self):
        # self.stackedWidget.
        self.addSubInterface(self.statisticsPage, MyIcon.贡献度分析, '统计溯源')
        self.addSubInterface(self.PCAPage, MyIcon.相关性分析, 'PCA监测')
        # self.addSubInterface(self.correlationAnalysisPage, MyIcon.相关性分析, '相关性分析')
        # self.addSubInterface(self.contributionAnalysisPage, MyIcon.贡献度分析, '贡献度分析')

        self.NavigationBar.addItem(routeKey='Help',
                                   icon=FIF.HELP,
                                   text='帮助',
                                   onClick=self.showMessageBox,
                                   selectable=False,
                                   position=NavigationItemPosition.BOTTOM, )
        # self.NavigationBar.setFixedSize(50,50)

        self.stackedWidget.currentChanged.connect(self.onCurrentInterfaceChanged)
        self.NavigationBar.setCurrentItem(self.statisticsPage.objectName())

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
    win = 异常板形监测溯源()
    win.show()
    sys.exit(app.exec_())
