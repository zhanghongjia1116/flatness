# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QDialog
import PyQt5.QtWidgets

from ..view.Ui_dialog import Ui_Dialog


class Dialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    # 自定义信号
    signal = pyqtSignal(tuple)

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (defaults to None)
        @type QWidget (optional)
        """
        super(Dialog, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.get_reg)

    # global host,port,user,passwd,db,charset

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        self.close()

    def get_reg(self):
        host = self.lineEdit.text()
        port = self.lineEdit_2.text()
        user = self.lineEdit_3.text()
        passwd = self.lineEdit_4.text()
        db = self.lineEdit_5.text()
        charset = self.lineEdit_6.text()
        my_reg = (host, port, user, passwd, db, charset)
        self.signal.emit(my_reg)  # 发射信号


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = Dialog()
    ui.show()
    sys.exit(app.exec_())
