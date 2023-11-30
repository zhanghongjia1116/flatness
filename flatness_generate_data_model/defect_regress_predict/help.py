# -*- coding: utf-8 -*-

"""
Module implementing help.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow

from flatness_generate_data_model.defect_regress_predict.Ui_help import Ui_help


class help(QMainWindow, Ui_help):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (defaults to None)
        @type QWidget (optional)
        """
        super(help, self).__init__(parent)
        self.setupUi(self)
