import sys

from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from 登录及主界面.view.Ui_登录界面 import Ui_LoginWindow
from 登录及主界面.controller.flatnessMainNormal import MainWindow
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QPoint, pyqtSlot
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QFrame, QMainWindow, QApplication, QMessageBox
from loguru import logger
from playhouse.shortcuts import model_to_dict


class LoginWindow(QWidget, Ui_LoginWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.drag_position = None
        self.setupUi(self)
        self.root = parent
        # self.root.tray_icon.hide()  # 先隐藏托盘图标

        # 隐藏原始的框
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    @pyqtSlot()
    def on_close_pushButton_clicked(self):
        logger.info("关闭登录窗口")
        # 退出应用程序
        QApplication.instance().quit()

    @pyqtSlot()
    def on_min_pushButton_clicked(self):
        self.showMinimized()

    @pyqtSlot()
    def on_entry_pushButton_clicked(self):
        self.main_window = MainWindow()
        self.main_window.show()
        # splash.finish(self.main_window)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == QtCore.Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == QtCore.Qt.LeftButton:
            if self.drag_position is not None:
                self.move(event.globalPos() - self.drag_position)
                event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == QtCore.Qt.LeftButton:
            self.drag_position = None
            event.accept()
