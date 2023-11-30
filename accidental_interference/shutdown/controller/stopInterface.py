# coding:utf-8
import os
import re
import time
from datetime import datetime

import pandas as pd
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget, QFileDialog
from matplotlib.backends.backend_qt import NavigationToolbar2QT
from my_utils.display import NumberedTableModel, PandasModel
from my_utils.prompt import showMessageBox

# from Ui_StopInterface import Ui_StopInterface
from accidental_interference.shutdown.controller.draw_pic import MplCanvas
from accidental_interference.shutdown.view.Ui_StopInterface import Ui_StopInterface


def format_time(time_str):
    if '1900-01-01' in time_str:
        time_str = time_str.replace('1900-01-01', '')
    try:
        # 尝试解析成完整的时间格式
        a = datetime.strptime(time_str, "%Y.%m.%d %H:%M:%S").strftime("%Y.%m.%d-%H:%M:%S")
        return a
    except:
        # 解析失败，说明是不完整的时间格式，只有时分秒
        a = datetime.strptime(time_str, "%Y.%m.%d %H:%M").strftime("%Y.%m.%d-%H:%M:%S")
        return a


class StopInterface(Ui_StopInterface, QWidget):
    mergeOnlineSignal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.process_data = None
        self.setupUi(self)
        self.ComboBox.addItems(['选择年份', '2021', '2022', '2023'])
        self.ComboBox.currentIndexChanged.connect(self.on_ComboBox_currentIndexChanged)
        self.TableView.clicked.connect(self.cell_clicked)
        self.mergeOnlineSignal.connect(self.on_mergeOnlineTablePushButton_clicked)
        self.onlineData = None
        self.displayData = None

    @pyqtSlot()
    def on_importRawDataPushButton_clicked(self):
        # 打开文件对话框，选择文件
        file_dialog = QFileDialog()
        tmp = os.path.abspath(__file__)
        for i in range(2):
            tmp = os.path.dirname(tmp)
        path = f"{tmp}/data/raw"
        file_path, _ = file_dialog.getOpenFileNames(self, "选择文件", path, "Excel Files (*.xlsx *.xls)")
        cols = ['日期', '开始时间', '结束时间', '停机原因', '分类']
        stop_data = pd.DataFrame([])
        for file in file_path:
            print(f'正在处理---->{os.path.basename(file)}')
            df = pd.read_excel(file, header=4)[cols]

            ym = os.path.basename(file)[:7]
            start_t = ym + '.' + df['日期'].astype(str) + ' ' + df['开始时间'].astype(str)
            end_t = ym + '.' + df['日期'].astype(str) + ' ' + df['结束时间'].astype(str)
            df.insert(0, '停机开始时间', start_t)
            df.insert(1, '停机结束时间', end_t)

            df['停机开始时间'] = df['停机开始时间'].str.replace(r'24:00:00', '00:00:00')
            df['停机开始时间'] = df['停机开始时间'].str.replace(r'24:00', '00:00')
            df['停机结束时间'] = df['停机结束时间'].str.replace(r'24:00:00', '00:00:00')
            df['停机结束时间'] = df['停机结束时间'].str.replace(r'24:00', '00:00')

            # 将时间转换为datetime格式
            df['停机开始时间'] = df['停机开始时间'].apply(format_time)
            df['停机结束时间'] = df['停机结束时间'].apply(format_time)

            # 序列中包含24:00:00或24:00的数据的索引
            mask_end = df['停机结束时间'].str.contains(r'00:00:00')

            df['停机开始时间'] = pd.to_datetime(df['停机开始时间'])
            df['停机结束时间'] = pd.to_datetime(df['停机结束时间'])
            # 对于出现了 "24:00" 的日期，将日期加 1 天
            df.loc[mask_end, '停机结束时间'] = df.loc[mask_end, '停机结束时间'] + pd.Timedelta(days=1)

            df['停机时间(分钟)'] = (df['停机结束时间'] - df['停机开始时间']).dt.total_seconds() / 60

            df = df.loc[:, ['停机开始时间', '停机结束时间', '停机时间(分钟)', '停机原因', '分类']]
            stop_data = pd.concat([stop_data, df], axis=0)
            print(f'处理完成---->{os.path.basename(file)}')
            print('\n')
        self.displayData = stop_data
        pd_model = NumberedTableModel(stop_data)
        self.TableView.setModel(pd_model)
        self.TableView.resizeColumnsToContents()
        self.TableView.resizeRowsToContents()

    @pyqtSlot()
    def on_concatDataPushButton_clicked(self):
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
    def on_mergeOnlineTablePushButton_clicked(self):
        # 加载初值表
        tmp = os.path.abspath(__file__)
        for i in range(3):
            tmp = os.path.dirname(tmp)
        path = f"{tmp}/initial_value_table/初值表.pkl"
        data = pd.read_pickle(path)
        time.sleep(0.25)
        self.ProgressBar.setValue(25)
        time.sleep(0.25)
        self.ProgressBar.setValue(50)
        self.onlineData = data.loc[:, ['入口材料号', '结束生产时刻', '缺陷备注', 'policyNo', '板坯牌号',
                                       'IU均值', '50米均值', '100米均值']]
        time.sleep(0.25)
        self.ProgressBar.setValue(75)
        time.sleep(0.25)
        self.ProgressBar.setValue(100)

    def cell_clicked(self, index):
        # 清除画布上的所有内容
        while self.verticalLayout_7.count():
            item = self.verticalLayout_7.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        # 获取选中单元格的值
        value = index.data()
        # 判断value是否为时间格式'2020-01-01 00:30:00'
        if not re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', value):
            showMessageBox("提示", "未选中有效数据", self)
        else:
            # 将时间转换为datetime格式
            value = pd.to_datetime(value)

            if self.onlineData is None:
                self.mergeOnlineSignal.emit()
                # time.sleep(0.5)
                online_data: pd.DataFrame = self.onlineData
                # 选择data中结束生产时刻在value前的10条数据

            else:
                online_data: pd.DataFrame = self.onlineData
            data = online_data[online_data['结束生产时刻'] < value].tail(5)
            pd_model = PandasModel(data)
            # 设置显示颜色为红色
            self.TableView_2.setModel(pd_model)
            self.TableView_2.resizeColumnsToContents()
            self.TableView_2.resizeRowsToContents()

            # 选择data中结束生产时刻在value后的10条数据
            data2 = online_data[online_data['结束生产时刻'] > value].head(5)
            # 设置显示颜色为蓝色
            pd_model2 = PandasModel(data2)
            self.TableView_3.setModel(pd_model2)
            self.TableView_3.resizeColumnsToContents()
            self.TableView_3.resizeRowsToContents()

            if data.empty:
                IU_1 = [0] * 5
                name_1 = list(range(5))
            else:
                IU_1 = data['IU均值'].tolist()
                name_1 = data['入口材料号'].tolist()

            if data2.empty:
                IU_2 = [0] * 5
                name_2 = list(range(5))
            else:
                IU_2 = data2['IU均值'].tolist()
                name_2 = data2['入口材料号'].tolist()
            bar_canvas = MplCanvas()
            bar_canvas.barIU(IU_1, name_1, IU_2, name_2)
            bar_canvas.toolbar = NavigationToolbar2QT(bar_canvas)
            self.verticalLayout_7.addWidget(bar_canvas)
            self.verticalLayout_7.addWidget(bar_canvas.toolbar)
        print(f"选中的值: {value}")

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
    def on_importProcessDataPushButton_clicked(self):
        # 弹出文件对话框以选择多个CSV或PKL文件
        tmp = os.path.abspath(__file__)
        for i in range(2):
            tmp = os.path.dirname(tmp)
        path = f"{tmp}/data/process"
        options = QFileDialog.Options()
        filter_str = "CSV Files (*.csv);;PKL Files (*.pkl);;All Files (*)"
        file_name: str = QFileDialog.getOpenFileName(self, "Select CSV or PKL Files", path,
                                                     filter=filter_str, options=options)[0]
        if file_name:
            # 读取并连接CSV或PKL文件
            if file_name.endswith(".csv"):
                df = pd.read_csv(file_name)
            elif file_name.endswith(".pkl"):
                df = pd.read_pickle(file_name)
            else:
                print(f"Unsupported file format: {file_name}")
                return
            self.displayData = df

            pd_model = NumberedTableModel(df)
            self.TableView.setModel(pd_model)
            self.TableView.resizeColumnsToContents()
            self.TableView.resizeRowsToContents()

        try:
            min_year = self.displayData.iloc[0, 1].year
            max_year = self.displayData.iloc[-1, 1].year
            self.ComboBox.clear()
            self.ComboBox.addItem('选择年份')
            year_list = [i for i in range(min_year, max_year + 1)]
            self.ComboBox.addItems(map(str, year_list))
        except:
            showMessageBox("提示", "未导入数据", self)

    @pyqtSlot()
    def on_ComboBox_currentIndexChanged(self):
        print(self.ComboBox.currentText())
        # 清除画布上的所有内容
        while self.verticalLayout_6.count():
            item = self.verticalLayout_6.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        if self.process_data is None:
            tmp = os.path.abspath(__file__)
            for i in range(2):
                tmp = os.path.dirname(tmp)
            path = f"{tmp}/data/process"
            self.process_data = pd.read_pickle(f"{path}/example_data.pkl")
        current_text = self.ComboBox.currentText()
        if current_text != '选择年份':
            year = int(current_text)
            # 筛选self.process_data['shutdown']
            selected_year_data: pd.DataFrame = self.process_data[self.process_data['停机开始时间'].dt.year == year]
            total_minutes = selected_year_data['停机时间(分钟)'].sum()
            total_reason = selected_year_data.shape[0]
            self.displayData = selected_year_data

            # 显示当前ComboBox对应数据的一部分
            pd_model = PandasModel(selected_year_data)
            self.TableView.setModel(pd_model)
            self.TableView.resizeColumnsToContents()
            self.TableView.resizeRowsToContents()

            def countTheReasonsTime(reason):
                """统计某个停机原因下的停机时间、停机条数占总数的百分比"""
                index = selected_year_data['停机原因'].str.contains(reason)
                reasons = index.sum()
                minutes = selected_year_data['停机时间(分钟)'][index].sum()
                return reasons / total_reason, minutes / total_minutes

            # 计算绘图数据的代码
            # 初始化停机原因和停机时间的百分比数组
            reason_pie_list = []
            minutes_pie_list = []

            for i in ['变规格', '到产', '计划检修', '躲峰限电']:
                reason_pie, minutes_pie = countTheReasonsTime(reason=i)
                reason_pie_list.append(reason_pie)
                minutes_pie_list.append(minutes_pie)

            other_reasons = 1 - sum(reason_pie_list)
            other_minutes = 1 - sum(minutes_pie_list)
            reason_pie_list.append(other_reasons)
            minutes_pie_list.append(other_minutes)

            # 绘图
            pie_canvas = MplCanvas()
            pie_canvas.reasonAnnualShutdown(year=str(year),
                                            proportion_1=reason_pie_list,
                                            proportion_2=minutes_pie_list)
            pie_canvas.toolbar = NavigationToolbar2QT(pie_canvas)
            self.verticalLayout_6.addWidget(pie_canvas)
            self.verticalLayout_6.addWidget(pie_canvas.toolbar)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = StopInterface()
    w.show()
    sys.exit(app.exec_())
