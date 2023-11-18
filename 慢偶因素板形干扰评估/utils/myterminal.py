import sys

from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from Ui_terminal import Ui_MyTerminal


# 重定向信号
class Stream(QObject):
    newText = pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))
        QApplication.processEvents()


class MyTerminal(Ui_MyTerminal, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 将窗口移动到左上角
        self.move(0, 0)
        # 下面将输出重定向到textEdit中
        sys.stdout = Stream(newText=self.onUpdateText)

    def onUpdateText(self, text):
        """Write console output to text widget."""
        cursor = self.terminal.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.terminal.setTextCursor(cursor)
        self.terminal.ensureCursorVisible()