import sys

from PyQt5.QtCore import QProcess
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QHBoxLayout, QVBoxLayout
from flatness_control_data_model_optimization.roller_shape_design.Ui_rollerDesign import Ui_RollerDesign
from qfluentwidgets import LineEdit, PrimaryPushButton, SubtitleLabel


class 辊形设计(QWidget, Ui_RollerDesign):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.openButton.clicked.connect(self.openFile)
        self.terminateButton.clicked.connect(self.terminateProcess)

        self.process = None

    def openFile(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "选择exe文件", "", "Executable Files (*.exe);;All Files (*)",
                                                  options=options)

        if filePath:
            self.pathLineEdit.setText(filePath)
            self.startProcess(filePath)

    def startProcess(self, filePath):
        if self.process is not None and self.process.state() == QProcess.Running:
            self.process.terminate()
            self.process.waitForFinished()

        self.process = QProcess()
        self.process.start(filePath)

    def terminateProcess(self):
        if self.process is not None and self.process.state() == QProcess.Running:
            self.process.terminate()
            self.process.waitForFinished()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = 辊形设计()
    ui.show()
    sys.exit(app.exec_())

