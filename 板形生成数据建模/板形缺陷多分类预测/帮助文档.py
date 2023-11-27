# -*- coding: utf-8 -*-

"""
Module implementing SinglePolicyCompare.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow

from 板形生成数据建模.板形缺陷多分类预测.Ui_帮助文档 import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (defaults to None)
        @type QWidget (optional)
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
