# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DynamicControl.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DynamicControl(object):
    def setupUi(self, DynamicControl):
        DynamicControl.setObjectName("DynamicControl")
        DynamicControl.resize(1064, 686)
        self.centralwidget = QtWidgets.QWidget(DynamicControl)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_xuanzeshuju = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_xuanzeshuju.setObjectName("pushButton_xuanzeshuju")
        self.verticalLayout.addWidget(self.pushButton_xuanzeshuju)
        self.pushButton_fenxi = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_fenxi.setObjectName("pushButton_fenxi")
        self.verticalLayout.addWidget(self.pushButton_fenxi)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.textEdit_1 = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit_1.setObjectName("textEdit_1")
        self.horizontalLayout_2.addWidget(self.textEdit_1)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout.addWidget(self.label_9)
        self.lineEdit_xiajingzhi = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_xiajingzhi.setObjectName("lineEdit_xiajingzhi")
        self.horizontalLayout.addWidget(self.lineEdit_xiajingzhi)
        self.label_11 = QtWidgets.QLabel(self.groupBox)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout.addWidget(self.label_11)
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout.addWidget(self.label_10)
        self.lineEdit_xiajianglv = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_xiajianglv.setObjectName("lineEdit_xiajianglv")
        self.horizontalLayout.addWidget(self.lineEdit_xiajianglv)
        self.label_12 = QtWidgets.QLabel(self.groupBox)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout.addWidget(self.label_12)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.graphicsView_tuxing = QtWidgets.QGraphicsView(self.groupBox)
        self.graphicsView_tuxing.setObjectName("graphicsView_tuxing")
        self.gridLayout_2.addWidget(self.graphicsView_tuxing, 0, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_qingkonghuabu = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_qingkonghuabu.setObjectName("pushButton_qingkonghuabu")
        self.horizontalLayout_3.addWidget(self.pushButton_qingkonghuabu)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.setStretch(0, 6)
        self.verticalLayout_2.setStretch(1, 1)
        self.gridLayout.addLayout(self.verticalLayout_2, 2, 0, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.graphicsView_tuxing_2 = QtWidgets.QGraphicsView(self.groupBox)
        self.graphicsView_tuxing_2.setObjectName("graphicsView_tuxing_2")
        self.gridLayout_3.addWidget(self.graphicsView_tuxing_2, 0, 0, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButton_qingkonghuabu_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_qingkonghuabu_2.setObjectName("pushButton_qingkonghuabu_2")
        self.horizontalLayout_4.addWidget(self.pushButton_qingkonghuabu_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.verticalLayout_3.setStretch(0, 6)
        self.verticalLayout_3.setStretch(1, 1)
        self.gridLayout.addLayout(self.verticalLayout_3, 2, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setRowStretch(2, 8)
        self.horizontalLayout_5.addWidget(self.groupBox)
        DynamicControl.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(DynamicControl)
        self.statusbar.setObjectName("statusbar")
        DynamicControl.setStatusBar(self.statusbar)

        self.retranslateUi(DynamicControl)
        QtCore.QMetaObject.connectSlotsByName(DynamicControl)

    def retranslateUi(self, DynamicControl):
        _translate = QtCore.QCoreApplication.translate
        DynamicControl.setWindowTitle(_translate("DynamicControl", "FullLengthQuality"))
        self.pushButton_xuanzeshuju.setText(_translate("DynamicControl", "选择数据"))
        self.pushButton_fenxi.setText(_translate("DynamicControl", "动态分析"))
        self.label_9.setText(_translate("DynamicControl", "板形IU下降值："))
        self.label_11.setText(_translate("DynamicControl", "IU"))
        self.label_10.setText(_translate("DynamicControl", "板形IU下降率："))
        self.label_12.setText(_translate("DynamicControl", "%"))
        self.pushButton_qingkonghuabu.setText(_translate("DynamicControl", "清空画布"))
        self.pushButton_qingkonghuabu_2.setText(_translate("DynamicControl", "清空画布"))
