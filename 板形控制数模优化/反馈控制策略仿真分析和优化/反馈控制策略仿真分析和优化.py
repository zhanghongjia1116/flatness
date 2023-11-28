from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel
from qfluentwidgets import PrimaryPushButton

from 板形控制数模优化.反馈控制策略仿真分析和优化.Ui_反馈控制策略仿真分析和优化 import Ui_Form


class 反馈控制策略(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initSegmentedWidget()

    def initSegmentedWidget(self):
        self.addSubInterfacePivot(self.singlePolicySubPage, self.singlePolicySubPage.objectName(), '单策略对比')
        self.addSubInterfacePivot(self.multiPolicySubPage, self.multiPolicySubPage.objectName(), '多策略对比')
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.singlePolicySubPage)
        self.pivot.setCurrentItem(self.singlePolicySubPage.objectName())

    def addSubInterfacePivot(self, widget, objectName, text):
        widget.setObjectName(objectName)
        # widget.setAlignment(Qt.AlignCenter)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget),
        )

    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    mainWindow = 反馈控制策略()
    mainWindow.show()
    sys.exit(app.exec_())
