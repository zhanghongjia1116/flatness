from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from ..view.Ui_roller_type_choose import Ui_rollingChooseDialog


class RollingChoose(QDialog, Ui_rollingChooseDialog):
    """选择轧辊类型的界面逻辑"""

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    @pyqtSlot()
    def on_PrimaryPushButton_clicked(self):
        """确认选择"""
        # 返回checkbox的状态
        self.selected_checkboxes = []
        for checkbox in [self.CheckBox, self.CheckBox_2, self.CheckBox_3,
                         self.CheckBox_4]:
            if checkbox.isChecked():
                self.selected_checkboxes.append(checkbox.text())
        self.close()


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = RollingChoose()
    w.show()
    sys.exit(app.exec_())