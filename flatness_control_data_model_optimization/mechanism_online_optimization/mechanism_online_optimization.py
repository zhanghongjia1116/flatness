from PyQt5.QtWidgets import QApplication, QWidget

from flatness_control_data_model_optimization.mechanism_online_optimization.Ui_mechanism_online_optimization import \
    Ui_Instruction


class 机理在线优化(QWidget, Ui_Instruction):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = 机理在线优化()
    w.show()
    sys.exit(app.exec_())
