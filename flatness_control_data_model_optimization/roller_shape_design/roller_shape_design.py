import os
import subprocess
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog

from flatness_control_data_model_optimization.roller_shape_design.Ui_rollerDesign import Ui_RollerDesign


class 辊形设计(QWidget, Ui_RollerDesign):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.openButton.clicked.connect(self.selectExecutable)

    def selectExecutable(self):
        # 打开文件对话框
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.Directory)

        # 获取用户选择的目录
        tmp = os.path.dirname(__file__)
        directory = f'{os.path.dirname(tmp)}/roller_shape_design/'

        if not directory:
            return

        # 构建要执行的命令
        command = f'cd {directory} && MAIN_OPTRC.exe'

        # 使用 subprocess 执行命令
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f'execute the exe failed: {e}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = 辊形设计()
    ui.show()
    sys.exit(app.exec_())
