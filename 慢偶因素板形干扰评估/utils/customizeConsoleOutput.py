import sys
from PyQt5.QtCore import Qt, QTextCodec, pyqtSignal, QProcess
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPlainTextEdit, QLabel
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QTextCursor, QPalette, QColor, QFont


class ProcessOutputReader(QProcess):
    produce_output = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # merge stderr channel into stdout channel
        self.setProcessChannelMode(QProcess.MergedChannels)

        # prepare decoding process' output to Unicode
        codec = QTextCodec.codecForLocale()
        self._decoder_stdout = codec.makeDecoder()
        # only necessary when stderr channel isn't merged into stdout:
        # self._decoder_stderr = codec.makeDecoder()

        self.readyReadStandardOutput.connect(self._ready_read_standard_output)
        # only necessary when stderr channel isn't merged into stdout:
        # self.readyReadStandardError.connect(self._ready_read_standard_error)

    @pyqtSlot()
    def _ready_read_standard_output(self):
        raw_bytes = self.readAllStandardOutput()
        text = self._decoder_stdout.toUnicode(raw_bytes)
        self.produce_output.emit(text)

    # only necessary when stderr channel isn't merged into stdout:
    # @pyqtSlot()
    # def _ready_read_standard_error(self):
    #     raw_bytes = self.readAllStandardError()
    #     text = self._decoder_stderr.toUnicode(raw_bytes)
    #     self.produce_output.emit(text)


class MyConsole(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # 设置占位文本
        self.setPlaceholderText("console")

        # 创建字体并设置字体大小
        font = QFont("Times New Roman")
        font.setPointSize(14)  # 设置字体大小为 14
        self.setFont(font)  # 将字体应用到 MyConsole

        # 创建调色板
        palette = self.palette()
        palette.setColor(QPalette.Base, QColor(0, 0, 0))  # 设置背景颜色为黑色
        palette.setColor(QPalette.Text, QColor(255, 255, 255))  # 设置文本颜色为白色
        self.setPalette(palette)
        self.setReadOnly(True)
        self.setMaximumBlockCount(10000)  # limit console to 10000 lines

        self._cursor_output = self.textCursor()

    @pyqtSlot(str)
    def append_output(self, text):
        self._cursor_output.insertText(text)
        self.scroll_to_last_line()

    def scroll_to_last_line(self):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.movePosition(QTextCursor.Up if cursor.atBlockStart() else QTextCursor.StartOfLine)
        self.setTextCursor(cursor)


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 创建 ProcessOutputReader 实例
        self.process_reader = ProcessOutputReader()

        # 创建 MyConsole 实例
        self.console = MyConsole()
        layout.addWidget(self.console)

        # 将 ProcessOutputReader 的 produce_output 信号连接到 MyConsole 的 append_output 槽
        self.process_reader.produce_output.connect(self.console.append_output)

        # 启动外部进程，这里用一个简单的示例命令，你可以根据需要更改
        self.process_reader.start('echo "Hello, World!"')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MyWindow()
    mainWin.show()
    sys.exit(app.exec_())
