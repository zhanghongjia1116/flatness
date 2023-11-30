import sys
import os
from PyQt5.QtWidgets import QApplication
from loguru import logger
from login_flatness_main.controller.login_window import LoginWindow
from login_flatness_main.controller.splash import SplashScreen


# from login_flatness_main.controller.flatnessMainNormal import MainWindow


class App(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.windows = {}

    def run(self, pytest=False):
        logger.info("程序启动 ...")

        splash = SplashScreen()  # 启动界面
        splash.loadProgress()  # 启动界面

        self.windows["login"] = LoginWindow()
        # self.windows["main"] = MainWindow()
        self.windows["login"].show()

        # splash.finish(self.windows['main'])

        if not pytest:
            sys.exit(self.exec_())


if __name__ == '__main__':
    App().run()
