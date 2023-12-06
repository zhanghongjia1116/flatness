import os

import pandas as pd
from PyQt5.QtCore import pyqtSlot, QEvent, Qt
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QWidget
from my_utils.display import PandasModel
from my_utils.prompt import showMessageBox
from qfluentwidgets import MessageBox

from flatness_control_capability_evaluation.BUR_roller_shape_evaluate.Ui_BUR_evaluate import Ui_BUREvaluate
from flatness_control_capability_evaluation.data_process import BURdata


# from 详细信息 import MatplotlibWidget, MplCanvas


class BUREvaluate(Ui_BUREvaluate, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pageBUR_data = None
        self.pageBUR_filtered_df = None
        self.pageBURframe1 = None
        self.pageBURframe2 = None
        self.pageBURframe3 = None
        self.pageBURframe4 = None
        self.pageBURframe5 = None
        self.initUI()

    def initUI(self):
        # SharePlatformData = BURdata()
        self.ComboBoxBUR.addItem('1号机架')
        self.ComboBoxBUR.addItem('2号机架')
        self.ComboBoxBUR.addItem('3号机架')
        self.ComboBoxBUR.addItem('4号机架')
        self.ComboBoxBUR.addItem('5号机架')
        if self.pageBUR_data is None:
            local_path = os.path.abspath(__file__)
            tmp = os.path.dirname(local_path)
            self.pageBUR_data = pd.read_pickle(f'{tmp}/data/BURdata.pkl')
            data = BURdata(data=self.pageBUR_data)
            self.pageBURframe1 = data.bur1
            self.pageBURframe2 = data.bur2
            self.pageBURframe3 = data.bur3
            self.pageBURframe4 = data.bur4
            self.pageBURframe5 = data.bur5

        self.LineEditBUR.installEventFilter(self)
        self.SliderBUR.valueChanged.connect(lambda value: self.LineEditBUR.setText(str(value)))
        self.LineEditBUR.textChanged.connect(self.updateSliderBUR)

    def eventFilter(self, obj, event):
        # 禁止lineEdit输入非数字
        if obj in {self.LineEditBUR} and event.type() == QEvent.KeyPress:
            # 获取按键的文本
            key = event.text()

            # 检查按键是否为数字或删除键
            if not key.isnumeric() and key not in {'\b', Qt.Key_Backspace}:
                return True  # 忽略非数字输入

        return super().eventFilter(obj, event)

    def updateSliderBUR(self, text):
        try:
            value = int(float(text))
            if value > 99:
                value = 99
                self.LineEditBUR.setText(str(value))
            self.SliderBUR.setValue(value)
        except Exception as e:
            print(f"An error occurred: {e}")
            w = MessageBox('错误',
                           '请输入正确百分比',
                           self)
            w.yesButton.setText('ok')
            w.cancelButton.setText('close')
            w.exec()

    @pyqtSlot()
    def on_importPushButtonBUR_clicked(self):
        # BUR辊形评价界面导入按钮
        self.importPushButtonBUR.setEnabled(False)  # 点击后禁用按钮
        self.displayPushButtonBUR.setEnabled(False)
        data = self.pageBUR_data
        try:
            start_date = self.CalendarPicker_3.getDate()
            end_date = self.CalendarPicker_4.getDate()
            if start_date > end_date:
                showMessageBox("错误", "开始时间大于结束时间", self)
                return

            startTimeBUR = pd.to_datetime(start_date.toPyDate())
            endTimeBUR = pd.to_datetime(end_date.toPyDate())

            # 使用布尔索引来筛选在指定时间段内的数据
            self.pageBUR_filtered_df: pd.DataFrame = data[
                (data['生产结束时刻(S11_0)'] >= startTimeBUR) & (data['生产结束时刻(S11_0)'] <= endTimeBUR)]
            display_data = self.pageBUR_filtered_df.copy()
            display_data.columns = ['策略号', '入口材料号', '生产结束时刻',
                                    '1#中间辊弯辊', '1#中间辊窜辊', '1#工作辊弯辊',
                                    '2#中间辊弯辊', '2#中间辊窜辊', '2#工作辊弯辊',
                                    '3#中间辊弯辊', '3#中间辊窜辊', '3#工作辊弯辊',
                                    '4#中间辊弯辊', '4#中间辊窜辊', '4#工作辊弯辊',
                                    '5#中间辊弯辊', '5#中间辊窜辊', '5#工作辊弯辊']
            # 为数据帧添加行号
            # display_data.insert(0, '序号', range(1, display_data.shape[0] + 1))
            if display_data.shape[0] > 100:
                df = display_data.iloc[:100, :]
            else:
                df = display_data
            pdModel = PandasModel(df)
            self.preViewTableBUR.setModel(pdModel)
            # 设置表头
            self.preViewTableBUR.resizeColumnsToContents()
            self.importPushButtonBUR.setEnabled(True)
            self.displayPushButtonBUR.setEnabled(True)

        except Exception as e:
            print(f"An error occurred: {e}")
            showMessageBox("错误", "未选择时间", self)
            self.importPushButtonBUR.setEnabled(True)
            self.displayPushButtonBUR.setEnabled(True)

    def getPresetValue(self, frame, singleFrameData: pd.DataFrame = None, rate=0.95):
        """筛选对应时间单机架的数据，不选择时间，则取3年的数据"""
        start_date = self.CalendarPicker_3.getDate()
        end_date = self.CalendarPicker_4.getDate()
        if frame == '1号机架':
            singleFrameData = self.pageBURframe1
        elif frame == '2号机架':
            singleFrameData = self.pageBURframe2
        elif frame == '3号机架':
            singleFrameData = self.pageBURframe3
        elif frame == '4号机架':
            singleFrameData = self.pageBURframe4
        elif frame == '5号机架':
            singleFrameData = self.pageBURframe5

        if start_date and end_date:
            startTimeBUR = pd.to_datetime(start_date.toPyDate())
            endTimeBUR = pd.to_datetime(end_date.toPyDate())
            singleFrameData = singleFrameData[
                (singleFrameData['生产结束时刻(S11_0)'] >= startTimeBUR) &
                (singleFrameData['生产结束时刻(S11_0)'] <= endTimeBUR)
                ]

        # 设置筛选的条件
        condition = (
                (abs(singleFrameData[f'{frame}中间上辊窜辊实际值(S11_0)']) >= 142.5 * rate) &
                (singleFrameData[f'{frame}中间辊弯辊实际值(S11_0)'] >= 2600 * rate) &
                ((singleFrameData[f'{frame}工作辊弯辊实际值(S11_0)'] >= 1000 * rate) |
                 (singleFrameData[f'{frame}工作辊弯辊实际值(S11_0)'] <= -700 * rate))
        )
        presetValue = singleFrameData[condition]
        return presetValue

    @pyqtSlot()
    def on_displayPushButtonBUR_clicked(self):
        # BUR辊形评价界面"打满显示"按钮
        # 清空tableview内容
        self.highValueTableBUR.setModel(QStandardItemModel())
        try:
            frameText = self.ComboBoxBUR.currentText()
            tmp = self.LineEditBUR.text()
            if not tmp:
                w = MessageBox('警告',
                               '未选择打满百分比，设置默认值为95%。',
                               self)
                w.yesButton.setText('ok')
                w.cancelButton.setText('close')
                w.exec()
                self.LineEditBUR.setText('95')
                percent = 0.95
            else:
                percent = int(float(self.LineEditBUR.text())) * 0.01
            presetValue = self.getPresetValue(frameText, rate=percent)

            if presetValue.shape[0] == 0:
                showMessageBox("提示", "未找到符合条件的数据", self)
                self.SpecificLabelBUR.setText('')
                return
            else:
                # 为数据帧添加行号
                presetValue.insert(0, '序号', range(1, presetValue.shape[0] + 1))
                if presetValue.shape[0] > 100:
                    df = presetValue.iloc[:100, :]
                else:
                    df = presetValue
                pdModel = PandasModel(df)
                self.highValueTableBUR.setModel(pdModel)
                self.highValueTableBUR.resizeColumnsToContents()
                self.displayPushButtonBUR.setEnabled(True)

            if self.pageBUR_filtered_df is not None:
                info = f"选择时间段内共{self.pageBUR_filtered_df.shape[0]}卷, 当前机架设定值打满共{presetValue.shape[0]}卷"
                self.SpecificLabelBUR.setText(info)
                decimal_number = (presetValue.shape[0] / self.pageBUR_filtered_df.shape[0])
                percentage = "{:.2%}".format(decimal_number)
                self.PercentLabelBUR.setText(percentage)
            else:
                showMessageBox('提示',
                               '未选择时间段, 显示3年数据中打满情况',
                               self)
                info = f"当前机架设定值打满共{presetValue.shape[0]}卷"
                self.SpecificLabelBUR.setText(info)
                self.PercentLabelBUR.setText('')

        except Exception as e:
            print(e)
            showMessageBox('错误',
                           '未选择时间段, 显示3年数据中打满情况',
                           self)

    def on_moreInfoPushButtonBUR_clicked(self):
        showMessageBox("提示", "正在开发", self)

    def update_highValueTable_view(self, model):
        self.highValueTableBUR.setModel(model)
        self.highValueTableBUR.resizeColumnsToContents()


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    ui = BUREvaluate()
    ui.show()
    sys.exit(app.exec_())
