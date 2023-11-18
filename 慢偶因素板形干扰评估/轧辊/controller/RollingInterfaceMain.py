import math
import os
import re
import sys

import pandas as pd
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal, Qt, QMutex, QEvent, QAbstractTableModel, QEventLoop, QTimer, \
    QObject
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QTextCursor
from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox, QTableWidgetItem, QFileDialog, QApplication
from prompt import showMessageBox
from my_utils.zhhj_data import 轧辊数据
from ..view.Ui_RollingInterfaceMain import Ui_RollingInterfaceMain
from ..controller.辊类选择界面 import RollingChoose
from ..controller.选择轧辊类型警告界面 import WarningDialog
from ..controller.轧辊带钢索引查询界面 import RollingSearch


class RollingInterfaceMain(QWidget, Ui_RollingInterfaceMain):
    def __init__(self):
        super().__init__()
        self.displayData = None
        self.rawdataDict = None
        self.rawdata_path = None
        self.setupUi(self)

        self.ComboBox.setEnabled(False)
        self.exportPushButton.setEnabled(False)
        self.ComboBox.currentTextChanged.connect(self.tableDisplayData)
        rollType = ['请选择轧辊类型', 'BUR', 'IMR', 'TCM1-4', 'TCM5']
        for i in range(5):
            self.ComboBox.addItem(rollType[i])

    def getRawData(self, pathList, sheetNameList):
        """获取原始数据并储存进相应的字典中"""
        rawdataDict = {'BUR': [],
                       'IMR': [],
                       'TCM1-4': [],
                       'TCM5': []}
        for path in pathList:
            for sheetName in sheetNameList:
                single_sheet_data = 轧辊数据(path=path, sheetname=sheetName).format_table()
                if sheetName == 'TCM-BUR':
                    rawdataDict['BUR'].append(single_sheet_data)
                elif sheetName == 'TCM-IMR':
                    rawdataDict['IMR'].append(single_sheet_data)
                elif sheetName == 'TCM 1-4架':
                    rawdataDict['TCM1-4'].append(single_sheet_data)
                elif sheetName == 'TCM-5架':
                    rawdataDict['TCM5'].append(single_sheet_data)
        self.rawdataDict = rawdataDict

    @pyqtSlot()
    def on_importPushButton_clicked(self):
        """选择目录中的原始数据文件"""
        self.importPushButton.setEnabled(False)
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setWindowTitle("选择原始数据excel文件")
        file_dialog.setNameFilter("Excel files (*.xlsx *.xls)")
        data_path = os.path.dirname(os.path.dirname(__file__)) + '/data/raw'
        fileNames = QFileDialog.getOpenFileNames(self, 'Open file', data_path, "Excel files (*.xlsx *.xls)")[0]
        self.rawdata_path = fileNames  # 获取原始数据文件路径
        if self.rawdata_path:
            showMessageBox("提示", "正在处理数据, 减少操作界面", self)
            # 选择了原始数据的路径，接着选择轧辊类型
            choose_dialog = RollingChoose()
            choose_dialog.exec_()
            if not choose_dialog.selected_checkboxes:
                # 未选择轧辊类型，弹出警告框
                warning_dialog = WarningDialog()
                warning_dialog.exec_()
            self.getRawData(self.rawdata_path, choose_dialog.selected_checkboxes)
            # self.rawdata =
            if self.rawdataDict:
                QMessageBox.information(self, "提示", "原始数据选择成功")
                # self.plainTextEdit.clear()
                self.ComboBox.setEnabled(True)
        else:
            QMessageBox.warning(self, "警告", "未选择原始数据文件")
            self.importPushButton.setEnabled(True)

    @pyqtSlot()
    def tableDisplayData(self):
        """将DataFrame显示在TableView中"""
        try:
            rollingType = self.ComboBox.currentText()
            if rollingType != '请选择轧辊类型':
                df = pd.concat(self.rawdataDict[rollingType])
                from display import PandasModel
                pdModel = PandasModel(df)
                self.TableView.setModel(pdModel)
                self.TableView.resizeColumnsToContents()
                self.displayData = df
                self.importPushButton.setEnabled(True)
                self.exportPushButton.setEnabled(True)
            else:
                self.exportPushButton.setEnabled(False)
        except Exception as e:
            print(e)

    @pyqtSlot()
    def on_exportPushButton_clicked(self):
        # 弹出文件对话框以选择保存位置和文件名
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Data", "", "CSV Files (*.csv);;PKL Files (*.pkl)",
                                                   options=options)

        if file_name:
            if file_name.endswith(".csv"):
                # 选择了保存为 CSV 文件
                self.save_data_to_csv(file_name)
            elif file_name.endswith(".pkl"):
                # 选择了保存为 PKL 文件
                self.save_data_to_pkl(file_name)
            else:
                # 未选择有效文件格式
                print("无效的文件格式。请选择CSV或PKL。")

    def save_data_to_csv(self, file_name):
        try:
            self.displayData.to_csv(file_name, index=False)
            print(f"数据保存到 {file_name}")
        except Exception as e:
            print(f"将数据保存到CSV时出错: {str(e)}")

    def save_data_to_pkl(self, file_name):
        try:
            self.displayData.to_pickle(file_name)
            print(f"数据保存到 {file_name}")
        except Exception as e:
            print(f"将数据保存到PKL时出错: {str(e)}")

    @pyqtSlot()
    def on_mergePushButton_clicked(self):
        # 弹出文件对话框以选择多个CSV或PKL文件
        options = QFileDialog.Options()
        file_names, _ = QFileDialog.getOpenFileNames(self, "Select CSV or PKL Files", "",
                                                     "CSV Files (*.csv);;PKL Files (*.pkl)", options=options)

        if file_names:
            # 读取并连接CSV或PKL文件
            data_frames = []
            for file_name in file_names:
                if file_name.endswith(".csv"):
                    df = pd.read_csv(file_name)
                elif file_name.endswith(".pkl"):
                    df = pd.read_pickle(file_name)
                else:
                    print(f"Unsupported file format: {file_name}")
                    return
                data_frames.append(df)

            # 检查列名是否一致
            column_names = [df.columns.tolist() for df in data_frames]
            if all(column_names[i] == column_names[0] for i in range(1, len(column_names))):
                # 列名一致，进行列连接
                concatenated_df = pd.concat(data_frames, ignore_index=True)
                print("DataFrames merged successfully.")
                # 现在可以使用concatenated_df进行后续操作
                # 选择保存位置和文件名
                save_options = QFileDialog.Options()
                save_file_name, _ = QFileDialog.getSaveFileName(self, "Save Merged Data", "",
                                                                "CSV Files (*.csv);;PKL Files (*.pkl)",
                                                                options=save_options)
                if save_file_name:
                    if save_file_name.endswith(".csv"):
                        # 选择保存为 CSV 文件
                        concatenated_df.to_csv(save_file_name, index=False)
                        print(f"Data saved to {save_file_name}")
                    elif save_file_name.endswith(".pkl"):
                        # 选择保存为 PKL 文件
                        concatenated_df.to_pickle(save_file_name)
                        print(f"Data saved to {save_file_name}")
                    else:
                        # 未选择有效文件格式
                        print("Invalid file format. Please select either CSV or PKL.")
            else:
                # 列名不一致，给出错误提示
                print("Error: Column names in the selected CSV/PKL files are not consistent.")

    @pyqtSlot()
    def on_searchPushButton_clicked(self):
        self.searchWindow = RollingSearch()
        self.searchWindow.show()
