# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'flatnessMainNormal.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("SinglePolicyCompare")
        MainWindow.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/images/首钢.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.CardWidget = CardWidget(self.centralwidget)
        self.CardWidget.setObjectName("CardWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.CardWidget)
        self.verticalLayout.setSpacing(100)
        self.verticalLayout.setObjectName("verticalLayout")
        self.PrimaryPushButton = PrimaryPushButton(self.CardWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PrimaryPushButton.sizePolicy().hasHeightForWidth())
        self.PrimaryPushButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.PrimaryPushButton.setFont(font)
        self.PrimaryPushButton.setObjectName("PrimaryPushButton")
        self.verticalLayout.addWidget(self.PrimaryPushButton)
        self.PrimaryPushButton_2 = PrimaryPushButton(self.CardWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PrimaryPushButton_2.sizePolicy().hasHeightForWidth())
        self.PrimaryPushButton_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.PrimaryPushButton_2.setFont(font)
        self.PrimaryPushButton_2.setObjectName("PrimaryPushButton_2")
        self.verticalLayout.addWidget(self.PrimaryPushButton_2)
        self.PrimaryPushButton_3 = PrimaryPushButton(self.CardWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PrimaryPushButton_3.sizePolicy().hasHeightForWidth())
        self.PrimaryPushButton_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.PrimaryPushButton_3.setFont(font)
        self.PrimaryPushButton_3.setObjectName("PrimaryPushButton_3")
        self.verticalLayout.addWidget(self.PrimaryPushButton_3)
        self.horizontalLayout.addWidget(self.CardWidget)
        self.CardWidget_2 = CardWidget(self.centralwidget)
        self.CardWidget_2.setObjectName("CardWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.CardWidget_2)
        self.verticalLayout_2.setSpacing(40)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.PrimaryPushButton_4 = PrimaryPushButton(self.CardWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PrimaryPushButton_4.sizePolicy().hasHeightForWidth())
        self.PrimaryPushButton_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.PrimaryPushButton_4.setFont(font)
        self.PrimaryPushButton_4.setObjectName("PrimaryPushButton_4")
        self.verticalLayout_2.addWidget(self.PrimaryPushButton_4)
        self.PrimaryPushButton_5 = PrimaryPushButton(self.CardWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PrimaryPushButton_5.sizePolicy().hasHeightForWidth())
        self.PrimaryPushButton_5.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.PrimaryPushButton_5.setFont(font)
        self.PrimaryPushButton_5.setObjectName("PrimaryPushButton_5")
        self.verticalLayout_2.addWidget(self.PrimaryPushButton_5)
        self.PrimaryPushButton_6 = PrimaryPushButton(self.CardWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PrimaryPushButton_6.sizePolicy().hasHeightForWidth())
        self.PrimaryPushButton_6.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.PrimaryPushButton_6.setFont(font)
        self.PrimaryPushButton_6.setObjectName("PrimaryPushButton_6")
        self.verticalLayout_2.addWidget(self.PrimaryPushButton_6)
        self.PrimaryPushButton_7 = PrimaryPushButton(self.CardWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PrimaryPushButton_7.sizePolicy().hasHeightForWidth())
        self.PrimaryPushButton_7.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.PrimaryPushButton_7.setFont(font)
        self.PrimaryPushButton_7.setObjectName("PrimaryPushButton_7")
        self.verticalLayout_2.addWidget(self.PrimaryPushButton_7)
        self.horizontalLayout.addWidget(self.CardWidget_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("SinglePolicyCompare", "灯塔工厂上线"))
        self.PrimaryPushButton.setText(_translate("SinglePolicyCompare", "板形质量评价"))
        self.PrimaryPushButton_2.setText(_translate("SinglePolicyCompare", "异常板形监测溯源"))
        self.PrimaryPushButton_3.setText(_translate("SinglePolicyCompare", "慢偶因素板形干扰评估"))
        self.PrimaryPushButton_4.setText(_translate("SinglePolicyCompare", "板形调控功效挖掘"))
        self.PrimaryPushButton_5.setText(_translate("SinglePolicyCompare", "板形生成数据建模"))
        self.PrimaryPushButton_6.setText(_translate("SinglePolicyCompare", "板形控制能力评价"))
        self.PrimaryPushButton_7.setText(_translate("SinglePolicyCompare", "板形控制数模优化"))
from qfluentwidgets import CardWidget, PrimaryPushButton
import resource_rc