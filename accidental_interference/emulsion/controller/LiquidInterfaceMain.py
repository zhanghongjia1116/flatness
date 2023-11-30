import os

import pandas as pd
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget, QFileDialog
from my_utils.display import PandasModel
from my_utils.prompt import showMessageBox
from my_utils.zhhj_data import 乳化液数据

from accidental_interference.emulsion.controller.concentration_IU_scatter import AvgIUAndLiquid
from accidental_interference.emulsion.controller.time_period_IU_average import SpecialNumIU
from accidental_interference.emulsion.controller.box_line_fig import BoxDiagram
from accidental_interference.emulsion.view.Ui_LiquidInterfaceMain import Ui_Form


class LiquidInterfaceMain(QWidget, Ui_Form):
    displaySignal = pyqtSignal(pd.DataFrame)

    def __init__(self):
        super().__init__()
        self.processData = None
        self.processDataPath = None
        self.box_2 = None
        self.box_3 = None
        self.displayData = None
        self.rawdata_path = None
        self.setupUi(self)
        self.initComboBox()
        self.exportPushButton.setEnabled(False)
        self.mergeOnlineTablePushButton.setEnabled(False)
        print("程序启动成功")

    def initComboBox(self):
        self.ComboBox.addItems(['选择乳化液箱号', '2', '3'])
        self.ComboBox.setEnabled(False)

    @pyqtSlot()
    def on_importRawDataPushButton_clicked(self):
        """选择目录中的原始数据文件"""
        self.importRawDataPushButton.setEnabled(False)
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setWindowTitle("选择原始数据excel文件")
        file_dialog.setNameFilter("Excel files (*.xlsx *.xls)")

        data_path = os.path.dirname(os.path.dirname(__file__)) + '/data/'
        fileNames = QFileDialog.getOpenFileNames(self, 'Open file', data_path, "Excel files (*.xlsx *.xls)")[0]
        self.rawdata_path = fileNames  # 获取原始数据文件路径
        try:
            name = os.path.basename(self.rawdata_path[0])

            if "乳化液" not in name:
                showMessageBox("警告", "请选择乳化液数据文件", self)
                self.importRawDataPushButton.setEnabled(True)
            else:
                showMessageBox("提示", "正在处理数据, 减少操作界面", self)
                liquid = 乳化液数据(xls_path=self.rawdata_path[0])
                self.box_2 = liquid.format_time(box=2)
                self.box_3 = liquid.format_time(box=3)
                self.ComboBox.currentIndexChanged.connect(self.updateTableView)
                self.ComboBox.setEnabled(True)

        except Exception as e:
            print(e)
            showMessageBox("警告", "请选择乳化液数据文件", self)
            self.importRawDataPushButton.setEnabled(True)

    @pyqtSlot()
    def updateTableView(self):
        box_num = self.ComboBox.currentText()
        df = None
        if box_num == '2':
            df = self.box_2
            self.mergeOnlineTablePushButton.setEnabled(True)
        elif box_num == '3':
            df = self.box_3
            self.mergeOnlineTablePushButton.setEnabled(True)
        elif box_num == '选择乳化液箱号':
            # 清空TableView
            df = pd.DataFrame()
        self.displayData = df
        # 设置展示数据的条数
        if df.shape[0] > 100:
            df = df.iloc[:100, :]
        else:
            df = df
        pdModel = PandasModel(df)
        self.TableView.setModel(pdModel)
        self.TableView.resizeColumnsToContents()
        self.importRawDataPushButton.setEnabled(True)
        self.exportPushButton.setEnabled(True)

    def updateTableViewMerge(self, res):
        self.displayData = res
        pdModel = PandasModel(res)
        self.TableView.setModel(pdModel)
        self.TableView.resizeColumnsToContents()
        self.importRawDataPushButton.setEnabled(True)
        self.exportPushButton.setEnabled(True)

    @pyqtSlot()
    def on_mergeOnlineTablePushButton_clicked(self):
        """合并在线判定表或初值表"""
        self.mergeOnlineTablePushButton.setEnabled(False)
        try:
            self.ComboBox.currentIndexChanged.disconnect(self.updateTableView)
            num = self.ComboBox.currentText()
            if num == '2':
                liquid = self.box_2
            elif num == '3':
                liquid = self.box_3
            else:
                showMessageBox("警告", "请选择乳化液箱号", self)
                return
            tmp = os.path.abspath(__file__)
            for i in range(3):
                tmp = os.path.dirname(tmp)
            online_data_path = f'{tmp}/initial_value_table/initial_value_table.pkl'
            online_data = pd.read_pickle(online_data_path)
            self.displayData = 乳化液数据.merge_liquid_rollTable(liquid, online_data)
            self.updateTableViewMerge(self.displayData.iloc[:100, :])
            self.ComboBox.currentIndexChanged.connect(self.updateTableView)
        except Exception as e:
            print(e)

    @pyqtSlot()
    def on_importProcessDataPushButton_clicked(self):
        """选择目录中的处理后数据文件"""
        self.importProcessDataPushButton.setEnabled(False)
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setWindowTitle("选择处理后数据文件")
        file_dialog.setNameFilter("Excel files (*.xlsx *.xls)")

        data_path = os.path.dirname(os.path.dirname(__file__)) + '/data/process/'
        fileNames = QFileDialog.getOpenFileNames(self, 'Open file',
                                                 data_path,
                                                 "processedLiquidData files (*.xlsx *.xls *.csv *.pkl)")[0]
        self.processDataPath = fileNames
        try:
            self.processData = pd.read_pickle(self.processDataPath[0])
            self.displayData = self.processData

            pdModel = PandasModel(self.displayData.iloc[:100, :])
            self.TableView.setModel(pdModel)
            self.TableView.resizeColumnsToContents()
            self.importRawDataPushButton.setEnabled(True)
            self.exportPushButton.setEnabled(True)
        except Exception as e:
            print(e)
            self.importProcessDataPushButton.setEnabled(True)

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

    @pyqtSlot()
    def on_IUScatterPushButton_clicked(self):
        """浓度与IU散点图"""
        if self.processData is None:
            data = pd.read_pickle(
                os.path.dirname(os.path.dirname(__file__)) + '/data/process/乳化液#3+初值表.pkl')
        else:
            data = self.processData
        # self.IuAndLiquidWindow = concentrationAndIUScatter(data)
        self.IuAndLiquidWindow = AvgIUAndLiquid(data)
        self.IuAndLiquidWindow.show()

    @pyqtSlot()
    def on_SpecificTimePushButton_clicked(self):
        """特定时间段IU均值"""
        if self.processData is None:
            data = pd.read_pickle(
                os.path.dirname(os.path.dirname(__file__)) + '/data/process/乳化液#3+初值表.pkl')
        else:
            data = self.processData
        self.SpecialNumIUWindow = SpecialNumIU(data)
        self.SpecialNumIUWindow.show()

    def save_data_to_csv(self, file_name):
        try:
            self.displayData.to_csv(file_name, index=False)
            print(f"数据保存到 {file_name}")
        except Exception as e:
            print(f"将数据保存到CSV时出错: {str(e)}")

    @pyqtSlot()
    def on_BoxDiagramPushButton_clicked(self):
        """箱形图"""
        if self.processData is None:
            data = pd.read_pickle(
                os.path.dirname(os.path.dirname(__file__)) + '/data/process/乳化液#3+初值表.pkl',
            )
        else:
            data = self.processData
        data = data.loc[:, ['结束生产时刻', '浓度', '电导率', 'PH值']]
        self.BoxDiagramWindow = BoxDiagram(data)
        self.BoxDiagramWindow.show()

    def save_data_to_pkl(self, file_name):
        try:
            self.displayData.to_pickle(file_name)
            print(f"数据保存到 {file_name}")
        except Exception as e:
            print(f"将数据保存到PKL时出错: {str(e)}")
