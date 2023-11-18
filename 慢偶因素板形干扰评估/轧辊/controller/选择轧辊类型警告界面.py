from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from ..view.Ui_选择轧辊类型警告界面 import Ui_warningDialog
from ..controller.辊类选择界面 import RollingChoose


class WarningDialog(Ui_warningDialog, QDialog):
    """选择轧辊类型的界面逻辑"""

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    @pyqtSlot()
    def on_PrimaryPushButton_clicked(self):
        self.close()
        last_window = RollingChoose()
        last_window.exec_()

    @pyqtSlot()
    def on_PrimaryPushButton_2_clicked(self):
        self.close()


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication, QDialog

    app = QApplication(sys.argv)
    w = WarningDialog()
    w.show()
    sys.exit(app.exec_())