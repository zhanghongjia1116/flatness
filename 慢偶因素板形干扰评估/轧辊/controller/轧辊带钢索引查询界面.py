import os
import sys
import pandas as pd
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox

from my_utils.display import PandasModel
from ..view.Ui_轧辊带钢索引查询界面 import Ui_RollingSearch


class RollingSearch(QWidget, Ui_RollingSearch):
    loading_finished = pyqtSignal()  # 自定义信号

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.get_data()
        self.initComboBox()

        self.CalendarPicker.dateChanged.connect(self.update_table)
        self.LineEdit.textChanged.connect(self.check_input_completion)
        self.PrimaryPushButton.clicked.connect(self.display_roll)

        # 在Search窗口初始化完成时发射自定义信号
        self.loading_finished.emit()

    def initComboBox(self):
        """初始化下拉框"""
        self.ComboBox.clear()
        self.ComboBox.addItems(['1', '2', '3', '4', '5'])

    def get_data(self):
        """获取数据"""
        local_path = os.path.abspath(__file__)
        tmp = local_path
        for i in range(3):
            tmp = os.path.dirname(tmp)
        real_path = f'{tmp}/酸轧在线判定/酸轧在线判定.pkl'

        self.酸轧在线判定 = pd.read_pickle(real_path)
        self.酸轧在线判定['结束生产时刻'] = pd.to_datetime(self.酸轧在线判定['结束生产时刻'])
        rolling_path = f'{tmp}/轧辊/data/process/合并酸轧在线判定/'
        roller_data = {'BUR': [], 'IMR': [], 'TCM': []}

        for key in roller_data.keys():
            for i in range(1, 6):
                roller_data[key].append(pd.read_pickle(f'{rolling_path}/{key}/{key}#{i}.pkl'))

        self.roller_data = roller_data

    def check_input_completion(self, text):
        # 以H开头，长度为13，才是正确的钢卷号
        if text and text[0] != 'H':
            self.LineEdit.setStyleSheet("background-color: red;")
        else:
            if len(text) != 13:
                self.LineEdit.setStyleSheet("background-color: red;")
            else:
                self.LineEdit.setStyleSheet("background-color: white;")

    def update_table(self):
        """连接日历控件的信号，更新日历下的表格"""
        selected_date = self.CalendarPicker.getDate().toPyDate()
        filtered_data = self.酸轧在线判定[self.酸轧在线判定['结束生产时刻'].dt.date == selected_date].copy()
        # filtered_data['结束生产时刻'] = filtered_data['结束生产时刻'].dt.strftime("%H:%M")

        pd_model = PandasModel(filtered_data)
        self.TableWidget.setModel(pd_model)
        self.TableWidget.resizeColumnsToContents()
        # self.TableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode)
        # self.TableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode)

    def display_roll(self):
        selected_value = self.ComboBox.currentText()
        roll_num = self.LineEdit.text()
        # print(str(roll_num))
        try:
            singleFrameBUR = self.roller_data['BUR'][int(selected_value) - 1]
            singleFrameIMR = self.roller_data['IMR'][int(selected_value) - 1]
            singleFrameTCM = self.roller_data['TCM'][int(selected_value) - 1]
            # 支撑辊, 中间辊, 工作辊 = self.roller_data['TCM'][int(self.ComboBox.currentText()) - 1]

            rowOfSingleFrameBUR = singleFrameBUR[singleFrameBUR['入口材料号'] == roll_num]
            rowOfSingleFrameIMR = singleFrameIMR[singleFrameIMR['入口材料号'] == roll_num]
            rowOfSingleFrameTCM = singleFrameTCM[singleFrameTCM['入口材料号'] == roll_num]

            # row_支撑辊 = 支撑辊[支撑辊['入口材料号'] == roll_num]
            # row_中间辊 = 中间辊[中间辊['入口材料号'] == roll_num]
            # row_工作辊 = 工作辊[工作辊['入口材料号'] == roll_num]

            def get_index(df: pd.DataFrame, row_df):
                """
                得到辊的上下辊号和在服役期内的索引，并且显示在界面上
                Args:
                    df (pd.DataFrame):
                    row_df (_type_): _description_

                Returns:
                    _type_: _description_
                """
                if not row_df.empty:
                    tmp = row_df.reset_index(drop=True)
                    index = tmp.iloc[0, 2]
                    up_roll = tmp.iloc[0, 3]
                    down_roll = tmp.iloc[0, 10]

                    filter_df = df[df.iloc[:, 3] == up_roll]
                    length = len(filter_df)
                    menu = str(index) + '/' + str(length)
                    return up_roll, down_roll, menu
                else:
                    return None, None, str(None)

            支撑辊_up, 支撑辊_down, 支撑辊_index = get_index(singleFrameBUR, rowOfSingleFrameBUR)
            self.LineEdit_2.setText(str(支撑辊_up))
            self.LineEdit_3.setText(str(支撑辊_down))
            self.LineEdit_4.setText(支撑辊_index)

            中间辊_up, 中间辊_down, 中间辊_index = get_index(singleFrameIMR, rowOfSingleFrameIMR)
            self.LineEdit_9.setText(str(中间辊_up))
            self.LineEdit_8.setText(str(中间辊_down))
            self.LineEdit_10.setText(中间辊_index)

            工作辊_up, 工作辊_down, 工作辊_index = get_index(singleFrameTCM, rowOfSingleFrameTCM)
            self.LineEdit_12.setText(str(工作辊_up))
            self.LineEdit_11.setText(str(工作辊_down))
            self.LineEdit_13.setText(工作辊_index)
        except Exception as e:
            print(e)
            QMessageBox.warning(self, '提示框', '钢卷号或机架号不正确!', QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RollingSearch()
    window.show()
    sys.exit(app.exec_())
