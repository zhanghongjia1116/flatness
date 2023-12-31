# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LiquidInterfaceMain.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1132, 821)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.CardWidget = CardWidget(Form)
        self.CardWidget.setObjectName("CardWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.CardWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.SubtitleLabel = SubtitleLabel(self.CardWidget)
        self.SubtitleLabel.setObjectName("SubtitleLabel")
        self.horizontalLayout_2.addWidget(self.SubtitleLabel)
        spacerItem = QtWidgets.QSpacerItem(300, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.ComboBox = ComboBox(self.CardWidget)
        self.ComboBox.setObjectName("ComboBox")
        self.horizontalLayout_2.addWidget(self.ComboBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.TableView = TableView(self.CardWidget)
        self.TableView.setObjectName("TableView")
        self.verticalLayout.addWidget(self.TableView)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(50)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.importRawDataPushButton = PushButton(self.CardWidget)
        self.importRawDataPushButton.setObjectName("importRawDataPushButton")
        self.horizontalLayout.addWidget(self.importRawDataPushButton)
        self.importProcessDataPushButton = PushButton(self.CardWidget)
        self.importProcessDataPushButton.setObjectName("importProcessDataPushButton")
        self.horizontalLayout.addWidget(self.importProcessDataPushButton)
        self.exportPushButton = PushButton(self.CardWidget)
        self.exportPushButton.setObjectName("exportPushButton")
        self.horizontalLayout.addWidget(self.exportPushButton)
        self.mergeOnlineTablePushButton = PushButton(self.CardWidget)
        self.mergeOnlineTablePushButton.setObjectName("mergeOnlineTablePushButton")
        self.horizontalLayout.addWidget(self.mergeOnlineTablePushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_4.addWidget(self.CardWidget)
        self.CardWidget_2 = CardWidget(Form)
        self.CardWidget_2.setObjectName("CardWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.CardWidget_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.TitleLabel_2 = TitleLabel(self.CardWidget_2)
        self.TitleLabel_2.setObjectName("TitleLabel_2")
        self.horizontalLayout_3.addWidget(self.TitleLabel_2)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        spacerItem3 = QtWidgets.QSpacerItem(20, 25, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem3)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem4 = QtWidgets.QSpacerItem(37, 17, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem4, 5, 2, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 80, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.gridLayout_3.addItem(spacerItem5, 1, 1, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(37, 17, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem6, 0, 2, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(20, 80, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.gridLayout_3.addItem(spacerItem7, 6, 1, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(20, 80, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.gridLayout_3.addItem(spacerItem8, 4, 1, 1, 1)
        self.BoxDiagramPushButton = PrimaryPushButton(self.CardWidget_2)
        self.BoxDiagramPushButton.setMinimumSize(QtCore.QSize(150, 50))
        self.BoxDiagramPushButton.setObjectName("BoxDiagramPushButton")
        self.gridLayout_3.addWidget(self.BoxDiagramPushButton, 2, 3, 1, 1)
        self.IconWidget_8 = IconWidget(self.CardWidget_2)
        self.IconWidget_8.setMinimumSize(QtCore.QSize(50, 50))
        self.IconWidget_8.setMaximumSize(QtCore.QSize(50, 16777215))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/箱线图.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.IconWidget_8.setIcon(icon)
        self.IconWidget_8.setObjectName("IconWidget_8")
        self.gridLayout_3.addWidget(self.IconWidget_8, 2, 1, 1, 1)
        self.IconWidget_7 = IconWidget(self.CardWidget_2)
        self.IconWidget_7.setMinimumSize(QtCore.QSize(50, 50))
        self.IconWidget_7.setMaximumSize(QtCore.QSize(50, 16777215))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/跟踪.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.IconWidget_7.setIcon(icon1)
        self.IconWidget_7.setObjectName("IconWidget_7")
        self.gridLayout_3.addWidget(self.IconWidget_7, 5, 1, 1, 1)
        self.IUScatterPushButton = PrimaryPushButton(self.CardWidget_2)
        self.IUScatterPushButton.setMinimumSize(QtCore.QSize(150, 50))
        self.IUScatterPushButton.setObjectName("IUScatterPushButton")
        self.gridLayout_3.addWidget(self.IUScatterPushButton, 0, 3, 1, 1)
        self.SpecificTimePushButton = PrimaryPushButton(self.CardWidget_2)
        self.SpecificTimePushButton.setMinimumSize(QtCore.QSize(150, 50))
        self.SpecificTimePushButton.setObjectName("SpecificTimePushButton")
        self.gridLayout_3.addWidget(self.SpecificTimePushButton, 5, 3, 1, 1)
        self.IconWidget_6 = IconWidget(self.CardWidget_2)
        self.IconWidget_6.setMinimumSize(QtCore.QSize(50, 50))
        self.IconWidget_6.setMaximumSize(QtCore.QSize(50, 16777215))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/散点图.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.IconWidget_6.setIcon(icon2)
        self.IconWidget_6.setObjectName("IconWidget_6")
        self.gridLayout_3.addWidget(self.IconWidget_6, 0, 1, 1, 1)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem9, 5, 0, 1, 1)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem10, 5, 4, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_3)
        spacerItem11 = QtWidgets.QSpacerItem(20, 47, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem11)
        self.horizontalLayout_4.addWidget(self.CardWidget_2)
        self.horizontalLayout_4.setStretch(0, 2)
        self.horizontalLayout_4.setStretch(1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "乳化液分析"))
        self.SubtitleLabel.setText(_translate("Form", "数据预览窗口"))
        self.ComboBox.setText(_translate("Form", "选择箱号"))
        self.importRawDataPushButton.setText(_translate("Form", "导入并格式化"))
        self.importProcessDataPushButton.setText(_translate("Form", "导入处理数据"))
        self.exportPushButton.setText(_translate("Form", "导出"))
        self.mergeOnlineTablePushButton.setText(_translate("Form", "合并酸轧判定"))
        self.TitleLabel_2.setText(_translate("Form", "数据分析"))
        self.BoxDiagramPushButton.setToolTip(_translate("Form", "导入单个酸轧在线判定表"))
        self.BoxDiagramPushButton.setText(_translate("Form", "乳化液箱线"))
        self.IUScatterPushButton.setToolTip(_translate("Form", "导入单个酸轧在线判定表"))
        self.IUScatterPushButton.setText(_translate("Form", "浓度与IU散点"))
        self.SpecificTimePushButton.setToolTip(_translate("Form", "导入单个酸轧在线判定表"))
        self.SpecificTimePushButton.setText(_translate("Form", "特定时间IU均值"))
from qfluentwidgets import CardWidget, ComboBox, IconWidget, PrimaryPushButton, PushButton, SubtitleLabel, TableView, TitleLabel
from qtResource import resource_rc
