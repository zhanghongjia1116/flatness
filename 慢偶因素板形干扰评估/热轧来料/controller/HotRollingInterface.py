from ..view.Ui_HotRollingInterface import Ui_HotRollingInterface
from PyQt5.QtWidgets import QWidget, QApplication


class HotRollingInterface(QWidget, Ui_HotRollingInterface):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ui = HotRollingInterface()
    ui.show()
    sys.exit(app.exec_())
