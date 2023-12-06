from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication
from qfluentwidgets import LargeTitleLabel


class 辊形设计(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.centralLayout = QVBoxLayout(self)
        self.label = LargeTitleLabel(text='辊形设计相关功能正在等待有限元优化，正在开发中。')
        self.label.setWordWrap(True)
        self.centralLayout.addWidget(self.label)
        self.setLayout(self.centralLayout)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = 辊形设计()
    win.show()
    sys.exit(app.exec_())