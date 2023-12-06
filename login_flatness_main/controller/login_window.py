from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtWidgets import QWidget
from loguru import logger
from playhouse.shortcuts import model_to_dict
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import Icon

from login_flatness_main.controller.flatnessMainNormal import MainWindow
from login_flatness_main.controller.mysql_form import mysql_form
from login_flatness_main.model.user import User
from login_flatness_main.view.Ui_login_window import Ui_LoginWindow


class LoginWindow(QWidget, Ui_LoginWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.drag_position = None
        self.setupUi(self)
        self.github_pushButton.setIcon(Icon(FIF.GITHUB))
        self.phone_pushButton.setIcon(Icon(FIF.PHONE))
        self.email_pushButton.setIcon(Icon(FIF.MAIL))
        self.root = parent
        self.click_count = 0

        # self.root.tray_icon.hide()  # 先隐藏托盘图标

        # 隐藏原始的框
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.login_pushButton.clicked.connect(self.login_pushButton_event)
        self.forget_password_pushButton.clicked.connect(self.forget_password_pushButton_event)
        self.register_pushButton.clicked.connect(self.register_pushButton_event)

        self.mysql_pushButton.clicked.connect(self.mysql_pushButton_event)
        # 底部按钮
        self.github_pushButton.clicked.connect(self.github_pushButton_event)
        self.phone_pushButton.clicked.connect(self.phone_pushButton_event)
        self.email_pushButton.clicked.connect(self.email_pushButton_event)

    def login_pushButton_event(self):
        logger.info("用户登录")
        # 登录的逻辑写在这里
        user_name = self.user_name_lineEdit.text()
        password = self.password_lineEdit.text()
        if user_name == "" or password == "":
            QMessageBox.information(self, "错误提示", "请输入用户名密码")
            return
        info = User.select_from_user_name_and_password(user_name, password)
        if info is not None:
            # 登录成功
            QMessageBox.information(self, "登录成功", "欢迎用户：\n" + str(info.user_name)
                                    + "\n" + str(model_to_dict(info)))
            self.root.show()  # 显示主窗体
            self.root.tray_icon.show()  # 显示托盘图标
            self.hide()
        else:
            QMessageBox.information(self, "错误提示", "用户名密码错误，请重试")

    def mysql_pushButton_event(self):
        self.click_count += 1
        if self.click_count == 4:
            logger.info("数据库窗口")
            self.mysql_form = mysql_form()
            self.mysql_form.show()
            self.click_count = 0

    def register_pushButton_event(self):
        logger.info("用户注册")
        QMessageBox.information(self, "注册", "请联系管理员admin")

    def forget_password_pushButton_event(self):
        logger.info("忘记密码")
        QMessageBox.information(self, "忘记密码", "请联系管理员admin")

    def github_pushButton_event(self):
        logger.info("跳转到github网站")
        QMessageBox.information(self, "GitHub", "zhhj1116")
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://github.com/zhanghongjia1116/flatness"))

    def phone_pushButton_event(self):
        logger.info("电话")
        QMessageBox.information(self, "电话", "手机号\n010-62334963")

    def email_pushButton_event(self):
        logger.info("邮箱")
        QMessageBox.information(self, "邮箱", "邮箱\nzhhj1116@outlook.com")

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
