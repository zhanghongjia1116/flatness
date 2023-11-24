import sys
import os
from PyQt5.QtWidgets import QApplication
from loguru import logger

os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from 登录及主界面.controller.登录界面 import LoginWindow
# from 登录及主界面.controller.flatnessMainNormal import MainWindow
from 登录及主界面.controller.splash import SplashScreen


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
