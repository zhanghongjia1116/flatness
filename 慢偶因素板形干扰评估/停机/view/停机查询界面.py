from Ui_停机查询界面new import *
import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
import os
import re


class StopSearch(QWidget, Ui_StopRollSearch):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.CalendarPicker.dateChanged.connect(self.update_table)  # 连接日历控件的信号，更新表格
        # self.CalendarPicker.selectionChanged.connect(self.update_table)  # 连接日历控件的信号，更新表格

        self.TableWidget.itemSelectionChanged.connect(self.showSelectedContent)  # 连接表格的 itemSelectionChanged 事件到槽函数

        local_path = os.path.abspath(__file__)
        tmp = local_path
        for i in range(3):
            tmp = os.path.dirname(tmp)

        real_path = f'{tmp}/酸轧在线/data/酸轧表.csv'
        self.酸轧csv = self.load_csv(path=real_path,
                                     use_cols=['结束生产时刻', '入口材料号', 'policyNo', 'IU_error'])
        self.停机csv = self.load_stop_csv(f'{tmp}/停机/data/合并后的停机数据.csv')

    @staticmethod
    def load_csv(path, use_cols=None):
        df = pd.read_csv(path, usecols=use_cols)
        df['结束生产时刻'] = pd.to_datetime(df['结束生产时刻'])
        return df

    @staticmethod
    def load_stop_csv(path):
        df = pd.read_csv(path)
        # start_time_obj = pd.to_datetime(df['开始时间'])
        # df['开始时间'] = start_time_obj.dt.strftime("%H:%M")
        df['开始时间'] = pd.to_datetime(df['开始时间'])

        # end_time_obj = pd.to_datetime(df['结束时间'])
        # df['结束时间'] = end_time_obj.dt.strftime("%H:%M")
        df['结束时间'] = pd.to_datetime(df['结束时间'])
        return df

    @staticmethod
    def display_table(tableWidget, data: pd.DataFrame, columns: list = None, *args: int):
        """将表格展示在TableWidget中, 并且"""
        if columns is None:
            columns = data.columns
        row = data.shape[0]
        col = data.shape[1]

        tableWidget.setRowCount(row)
        tableWidget.setColumnCount(col)

        tableWidget.setHorizontalHeaderLabels(columns)
        # 在设置列数之后，再设置列标题左对齐
        header = tableWidget.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # 设置列标题左对齐

        tableWidget.setHorizontalHeaderLabels(columns)  # 设置列标签

        if args is None:
            args = [80] * col

        column_widths = args  # 这里设置三列的宽度比例
        for c, width in enumerate(column_widths):
            tableWidget.setColumnWidth(c, width)

        for i in range(row):
            for j in range(col):
                item = QTableWidgetItem(str(data.iloc[i, j]))
                tableWidget.setItem(i, j, item)

    def update_table(self):
        """连接日历控件的信号，更新表格"""
        # selected_date = self.calendarWidget.selectedDate().toPyDate()
        selected_date = self.CalendarPicker.getDate().toPyDate()
        filtered_data = self.停机csv[self.停机csv['开始时间'].dt.date == selected_date].iloc[:, 0:4]

        filtered_data['开始时间'] = filtered_data['开始时间'].dt.strftime("%H:%M")
        filtered_data['结束时间'] = filtered_data['结束时间'].dt.strftime("%H:%M")
        self.display_table(self.TableWidget, filtered_data,
                           ["开始时间", "结束时间", "停机时间", "原因"],
                           80, 80, 80, 500)

    def showSelectedContent(self):
        selected_date = self.CalendarPicker.getDate().toPyDate()
        # 获取选中的单元格内容
        selected_items = self.TableWidget.selectedItems()
        if selected_items:
            selected_text = selected_items[0].text()

            # 定义匹配 "00:00" 格式的正则表达式
            pattern = r'^[0-2][0-9]:[0-5][0-9]$'
            # 使用 re.match() 方法进行匹配
            match = re.match(pattern, selected_text)

            if match is not None:
                time_obj = pd.to_datetime(selected_text, format="%H:%M").time()

                # 开始停机的具体时间, 将日期对象和时间对象组合成一个 datetime.datetime 对象
                combined_datetime = pd.to_datetime(str(selected_date) + " " + str(time_obj))

                # 计算每行的时间与给定时间的差值
                diff_series = abs(self.酸轧csv['结束生产时刻'] - combined_datetime)

                # 酸轧表中距离停机时间最近的带钢的索引
                closest_index = diff_series.idxmin()
                if self.酸轧csv['结束生产时刻'][closest_index] > combined_datetime:  # 结束生产时刻必须要 < 停机开始的时间
                    closest_index = closest_index - 1
                if closest_index + 3 > self.酸轧csv.shape[0]:  # 如果最近的带钢索引 + 3 > 酸轧表的行数，那么就取最后一行
                    up_display_index = range(closest_index - 4, closest_index + 1)  # 停机前widget表格显示5个条目
                    down_display_index = range(closest_index + 1, self.酸轧csv.shape[0])
                else:
                    up_display_index = range(closest_index - 6, closest_index + 1)  # 停机前widget表格显示5个条目
                    down_display_index = range(closest_index + 1, closest_index + 8)  # 停机后widget表格显示5个条目

                up_display_data = self.酸轧csv.iloc[up_display_index, :].copy()
                down_display_data = self.酸轧csv.iloc[down_display_index, :].copy()

                up_display_data['结束生产时刻'] = pd.to_datetime(up_display_data['结束生产时刻'])
                up_display_data['结束生产时刻'] = up_display_data['结束生产时刻'].dt.strftime("%H:%M")
                up_display_data['policyNo'] = up_display_data['policyNo'].astype(int)
                up_display_data['IU_error'] = up_display_data['IU_error'].round(3)

                down_display_data['结束生产时刻'] = down_display_data['结束生产时刻'].dt.strftime("%H:%M")
                down_display_data['policyNo'] = down_display_data['policyNo'].astype(int)
                down_display_data['IU_error'] = down_display_data['IU_error'].round(3)  # 保留三位小数

                # 在TableWidget_2中显示up_display_data
                self.display_table(self.TableWidget_2,
                                   up_display_data,
                                   ["结束生产时刻", "入口材料号", "policyNo", "IU_error"],
                                   120, 150, 80, 80)

                # 在TableWidget_3中显示up_display_data
                self.display_table(self.TableWidget_3,
                                   down_display_data,
                                   ["结束生产时刻", "入口材料号", "policyNo", "IU_error"],
                                   120, 150, 80, 80)
            else:
                QMessageBox.warning(self, "警告", "请选择停机时间！")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StopSearch()
    window.show()
    sys.exit(app.exec_())
