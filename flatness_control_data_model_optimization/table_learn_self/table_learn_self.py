from flatness_control_data_model_optimization.table_learn_self.Ui_table_learn_self import Ui_Instruction
from PyQt5.QtWidgets import QWidget, QApplication


class 表格自学习(QWidget, Ui_Instruction):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainWindow = 表格自学习()
    mainWindow.show()
    sys.exit(app.exec_())
