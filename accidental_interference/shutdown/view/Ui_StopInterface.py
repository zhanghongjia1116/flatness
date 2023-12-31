# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'StopInterface.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_StopInterface(object):
    def setupUi(self, StopInterface):
        StopInterface.setObjectName("StopInterface")
        StopInterface.resize(1400, 800)
        self.gridLayout = QtWidgets.QGridLayout(StopInterface)
        self.gridLayout.setObjectName("gridLayout")
        self.CardWidget_2 = CardWidget(StopInterface)
        self.CardWidget_2.setObjectName("CardWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.CardWidget_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.SubtitleLabel_4 = SubtitleLabel(self.CardWidget_2)
        self.SubtitleLabel_4.setObjectName("SubtitleLabel_4")
        self.verticalLayout_2.addWidget(self.SubtitleLabel_4)
        self.TableView_2 = TableView(self.CardWidget_2)
        self.TableView_2.setObjectName("TableView_2")
        self.verticalLayout_2.addWidget(self.TableView_2)
        self.SubtitleLabel_5 = SubtitleLabel(self.CardWidget_2)
        self.SubtitleLabel_5.setObjectName("SubtitleLabel_5")
        self.verticalLayout_2.addWidget(self.SubtitleLabel_5)
        self.TableView_3 = TableView(self.CardWidget_2)
        self.TableView_3.setObjectName("TableView_3")
        self.verticalLayout_2.addWidget(self.TableView_3)
        self.mergeOnlineTablePushButton = PushButton(self.CardWidget_2)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/format.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mergeOnlineTablePushButton.setIcon(icon)
        self.mergeOnlineTablePushButton.setObjectName("mergeOnlineTablePushButton")
        self.verticalLayout_2.addWidget(self.mergeOnlineTablePushButton, 0, QtCore.Qt.AlignHCenter)
        self.ProgressBar = QtWidgets.QProgressBar(self.CardWidget_2)
        self.ProgressBar.setProperty("value", 0)
        self.ProgressBar.setObjectName("ProgressBar")
        self.verticalLayout_2.addWidget(self.ProgressBar)
        self.gridLayout.addWidget(self.CardWidget_2, 0, 2, 1, 1)
        self.CardWidget = CardWidget(StopInterface)
        self.CardWidget.setObjectName("CardWidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.CardWidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.SubtitleLabel = SubtitleLabel(self.CardWidget)
        self.SubtitleLabel.setObjectName("SubtitleLabel")
        self.horizontalLayout_3.addWidget(self.SubtitleLabel)
        spacerItem = QtWidgets.QSpacerItem(300, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.TableView = TableView(self.CardWidget)
        self.TableView.setObjectName("TableView")
        self.verticalLayout_5.addWidget(self.TableView)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.importRawDataPushButton = PushButton(self.CardWidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/导入.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.importRawDataPushButton.setIcon(icon1)
        self.importRawDataPushButton.setObjectName("importRawDataPushButton")
        self.horizontalLayout_2.addWidget(self.importRawDataPushButton)
        self.concatDataPushButton = PushButton(self.CardWidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/数据集合并.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.concatDataPushButton.setIcon(icon2)
        self.concatDataPushButton.setObjectName("concatDataPushButton")
        self.horizontalLayout_2.addWidget(self.concatDataPushButton)
        self.exportPushButton = PushButton(self.CardWidget)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/icons/导出.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exportPushButton.setIcon(icon3)
        self.exportPushButton.setObjectName("exportPushButton")
        self.horizontalLayout_2.addWidget(self.exportPushButton)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.gridLayout.addWidget(self.CardWidget, 0, 0, 1, 1)
        self.CardWidget_3 = CardWidget(StopInterface)
        self.CardWidget_3.setObjectName("CardWidget_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.CardWidget_3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame = QtWidgets.QFrame(self.CardWidget_3)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.SubtitleLabel_2 = SubtitleLabel(self.frame)
        self.SubtitleLabel_2.setObjectName("SubtitleLabel_2")
        self.gridLayout_2.addWidget(self.SubtitleLabel_2, 0, 0, 1, 1)
        self.ComboBox = ComboBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ComboBox.sizePolicy().hasHeightForWidth())
        self.ComboBox.setSizePolicy(sizePolicy)
        self.ComboBox.setMaximumSize(QtCore.QSize(100, 16777215))
        self.ComboBox.setObjectName("ComboBox")
        self.gridLayout_2.addWidget(self.ComboBox, 0, 1, 1, 1)
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout.addLayout(self.verticalLayout_6)
        self.gridLayout_2.addWidget(self.frame_3, 1, 0, 1, 2)
        self.verticalLayout_4.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(self.CardWidget_3)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.SubtitleLabel_3 = SubtitleLabel(self.frame_2)
        self.SubtitleLabel_3.setObjectName("SubtitleLabel_3")
        self.verticalLayout.addWidget(self.SubtitleLabel_3)
        self.frame_4 = QtWidgets.QFrame(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_3.addLayout(self.verticalLayout_7)
        self.verticalLayout.addWidget(self.frame_4)
        self.verticalLayout_4.addWidget(self.frame_2)
        self.importProcessDataPushButton = PushButton(self.CardWidget_3)
        self.importProcessDataPushButton.setIcon(icon1)
        self.importProcessDataPushButton.setObjectName("importProcessDataPushButton")
        self.verticalLayout_4.addWidget(self.importProcessDataPushButton, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_4.setStretch(0, 1)
        self.verticalLayout_4.setStretch(1, 1)
        self.gridLayout.addWidget(self.CardWidget_3, 0, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 2)
        self.gridLayout.setColumnStretch(1, 2)
        self.gridLayout.setColumnStretch(2, 2)

        self.retranslateUi(StopInterface)
        QtCore.QMetaObject.connectSlotsByName(StopInterface)

    def retranslateUi(self, StopInterface):
        _translate = QtCore.QCoreApplication.translate
        StopInterface.setWindowTitle(_translate("StopInterface", "停机数据分析"))
        self.SubtitleLabel_4.setText(_translate("StopInterface", "停机前钢卷信息"))
        self.SubtitleLabel_5.setText(_translate("StopInterface", "停机后钢卷信息"))
        self.mergeOnlineTablePushButton.setText(_translate("StopInterface", "合并酸轧判定"))
        self.SubtitleLabel.setText(_translate("StopInterface", "数据预览窗口"))
        self.importRawDataPushButton.setText(_translate("StopInterface", "导入并格式化"))
        self.concatDataPushButton.setText(_translate("StopInterface", "合并"))
        self.exportPushButton.setText(_translate("StopInterface", "导出"))
        self.SubtitleLabel_2.setText(_translate("StopInterface", "整年停机原因统计"))
        self.ComboBox.setText(_translate("StopInterface", "年份"))
        self.SubtitleLabel_3.setText(_translate("StopInterface", "停机前后IU均值"))
        self.importProcessDataPushButton.setText(_translate("StopInterface", "导入处理数据"))


from qfluentwidgets import CardWidget, ComboBox, PushButton, SubtitleLabel, TableView
from qtResource import resource_rc
