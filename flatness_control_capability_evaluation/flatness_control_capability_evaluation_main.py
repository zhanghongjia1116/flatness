import sys

from PyQt5.QtWidgets import QApplication, QWidget
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import NavigationItemPosition, MessageBox
from qtResource.MyIcon import MyIcon

from flatness_control_capability_evaluation.Ui_flatness_control_capability_evaluation_main import Ui_FlatnessControlAbility


class 板形控制能力评价(Ui_FlatnessControlAbility, QWidget):
    def __init__(self):
        super().__init__()
        # self.stackedWidget = self.stackedWidget
        self.pageBUR_filtered_df = None
        self.pageBURframe1 = None
        self.pageBURframe2 = None
        self.pageBURframe3 = None
        self.pageBURframe4 = None
        self.pageBURframe5 = None
        self.pageBUR_data = None
        self.setupUi(self)
        self.initNavigation()

    def initNavigation(self):
        # self.stackedWidget.
        self.addSubInterface(self.preSetPage, MyIcon.预设定值, '预设定值')
        self.addSubInterface(self.dynamicControlPage, MyIcon.动态控制, '动态控制能力')
        self.addSubInterface(self.CVCPage, MyIcon.CVC, 'CVC辊型')
        self.addSubInterface(self.BURPage, MyIcon.支撑辊, '支撑辊辊型')

        self.NavigationBar.addItem(routeKey='Help',
                                   icon=FIF.HELP,
                                   text='帮助',
                                   onClick=self.showMessageBox,
                                   selectable=False,
                                   position=NavigationItemPosition.BOTTOM, )
        # self.NavigationBar.setFixedSize(50,50)

        self.stackedWidget.currentChanged.connect(self.onCurrentInterfaceChanged)  # 切换子界面
        self.NavigationBar.setCurrentItem(self.preSetPage.objectName())  # 在导航栏设置当前子界面

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
        # if widget.objectName() == 'CVCPage':
        #     self.initPageCVC()
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
    win = 板形控制能力评价()
    win.show()
    sys.exit(app.exec_())
