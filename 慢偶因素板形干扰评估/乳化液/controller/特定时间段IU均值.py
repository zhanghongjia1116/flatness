import numpy as np
import pandas as pd
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget
from matplotlib.backends.backend_qt import NavigationToolbar2QT

from my_utils.prompt import showMessageBox
from .draw_pic import MplCanvas
from ..view.Ui_特定时间段IU均值 import Ui_SpecialNumIU


class SpecialNumIU(QWidget, Ui_SpecialNumIU):
    def __init__(self, data):
        super().__init__()
        self.setupUi(self)
        self.data = data

    @pyqtSlot()
    def on_PrimaryPushButton_clicked(self):
        """板坯牌号IU钢卷数变化散点图"""
        try:

            start_date = self.CalendarPicker.getDate()
            end_date = self.CalendarPicker_2.getDate()
            start_time = str(start_date.toPyDate()) + ' ' + str(self.TimeEdit.time().toPyTime())
            end_time = str(end_date.toPyDate()) + ' ' + str(self.TimeEdit_2.time().toPyTime())

            if start_date > end_date:
                showMessageBox('错误', '开始时间不能大于结束时间', self)

            start_time = pd.to_datetime(start_time)
            end_time = pd.to_datetime(end_time)
            timestamp_data = self.data[
                (self.data['结束生产时刻'] >= start_time) & (self.data['结束生产时刻'] <= end_time)]
            policy_count = timestamp_data['板坯牌号'].unique()
            x_range = range(len(policy_count))

            avg_list_sub = np.array([])
            volumes_list_sub = np.array([])  # 钢卷数
            for i in policy_count:
                filter_df = timestamp_data[timestamp_data['板坯牌号'] == i]
                volume_sub = filter_df.shape[0]
                avg_sub = filter_df['IU均值'].mean()
                avg_list_sub = np.append(avg_list_sub, avg_sub)
                volumes_list_sub = np.append(volumes_list_sub, volume_sub).astype(int)

            avg_list_all_time = np.array([])
            volumes_list_all_time = np.array([])  # 钢卷数
            for i in policy_count:
                filter_df = self.data[self.data['板坯牌号'] == i]
                volume_all_time = filter_df.shape[0]
                avg_all_time = filter_df['IU均值'].mean()
                avg_list_all_time = np.append(avg_list_all_time, avg_all_time)
                volumes_list_all_time = np.append(volumes_list_all_time, volume_all_time).astype(int)
            self.graphicsView_2.setVisible(False)
            rightCanvas = MplCanvas()
            rightCanvas.板坯牌号IU钢卷数变化散点(
                policy_count, avg_list_sub, volumes_list_sub, avg_list_all_time,
                volumes_list_all_time, x_range
            )
            rightCanvas.toolbar = NavigationToolbar2QT(rightCanvas, self)
            for i in range(1, self.gridLayoutRight.count()):
                self.gridLayoutRight.itemAt(i).widget().deleteLater()
            self.gridLayoutRight.addWidget(rightCanvas)
            self.gridLayoutRight.addWidget(rightCanvas.toolbar)

        except Exception as e:
            print(e)
