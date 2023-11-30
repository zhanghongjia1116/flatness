import os

import pandas as pd
from PyQt5.QtCore import pyqtSlot, Qt, QEvent
from PyQt5.QtWidgets import QWidget
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from my_utils.display import PandasModel
from qfluentwidgets import MessageBox

from flatness_control_capability_evaluation.CVC_roller_shape_evaluate.Ui_CVC_evaluate import Ui_CVCEvaluate
from flatness_control_capability_evaluation.CVC_roller_shape_evaluate.more_info import MatplotlibWidget, MplCanvas


# class PlotCVCThread(QThread):
#     """绘图线程"""
#     canvasSignal = pyqtSignal(object, object)
#
#     def __init__(self, filter_data, high_value_data):
#         super().__init__()
#         self.filter_data = filter_data
#         self.high_value_data = high_value_data
#
#     def run(self):
#         leftCanvas = MplCanvas()
#         leftCanvas.plotBarCVC(self.filter_data, self.high_value_data)
#         leftCanvas.toolbar = NavigationToolbar2QT(leftCanvas)  # 添加toolbar
#
#         rightCanvas = MplCanvas()
#         rightCanvas.plotPieCVC(self.high_value_data)
#         rightCanvas.toolbar = NavigationToolbar2QT(rightCanvas)  # 添加toolbar
#
#         self.canvasSignal.emit(leftCanvas, rightCanvas)


class CVCEvaluate(Ui_CVCEvaluate, QWidget):
    def __init__(self):
        super().__init__()
        self.pageCVC_filtered_df = pd.DataFrame([])
        self.setupUi(self)
        self.pageCVC_data = None
        self.initUI()
        # self.plotThread = None

    def initUI(self):
        local_path = os.path.abspath(__file__)
        tmp = os.path.dirname(local_path)
        if self.pageCVC_data is None:
            self.pageCVC_data = pd.read_pickle(f'{tmp}/data/CVCdata.pkl')
        self.LineEditCVC.installEventFilter(self)
        self.SliderCVC.valueChanged.connect(lambda value: self.LineEditCVC.setText(str(value)))
        self.LineEditCVC.textChanged.connect(self.updateSliderCVC)

    def eventFilter(self, obj, event):
        if obj in {self.LineEditCVC} and event.type() == QEvent.KeyPress:
            # 获取按键的文本
            key = event.text()

            # 检查按键是否为数字或删除键
            if not key.isnumeric() and key not in {'\b', Qt.Key_Backspace}:
                return True  # 忽略非数字输入

        return super().eventFilter(obj, event)

    def updateSliderCVC(self, text):
        try:
            value = int(text)
            if value > 99:
                value = 99
                self.LineEditCVC.setText(str(value))
            self.SliderCVC.setValue(value)
        except Exception as e:
            print(f"An error occurred: {e}")
            w = MessageBox('错误',
                           '请输入正确百分比',
                           self)
            w.yesButton.setText('ok')
            w.cancelButton.setText('close')
            w.exec()

    @pyqtSlot()
    def on_importPushButtonCVC_clicked(self):
        """导入按钮"""
        try:
            self.importPushButtonCVC.setEnabled(False)  # 点击后禁用按钮
            self.displayPushButtonCVC.setEnabled(False)
            self.moreInfoPushButtonCVC.setEnabled(False)

            start_date = self.CalendarPicker.getDate()
            end_date = self.CalendarPicker_2.getDate()
            if start_date and end_date:
                if start_date > end_date:
                    w = MessageBox('错误',
                                   '开始时间不能大于结束时间',
                                   self)
                    w.yesButton.setText('ok')
                    w.cancelButton.setText('close')
                    w.exec()
                data = self.pageCVC_data
                start_time = pd.to_datetime(start_date.toPyDate())
                end_time = pd.to_datetime(end_date.toPyDate())
                self.pageCVC_filtered_df: pd.DataFrame = data[
                    (data['生产结束时刻(S11_0)'] >= start_time) & (data['生产结束时刻(S11_0)'] <= end_time)]
            else:
                self.pageCVC_filtered_df = self.pageCVC_data

            display_data = self.pageCVC_filtered_df.copy()
            display_data.columns = ['策略号', '入口卷号', '生产结束时刻', 'CVC窜辊']
            # 为数据帧添加行号
            display_data.insert(0, '序号', range(1, len(display_data) + 1))
            if display_data.shape[0] < 100:
                pdModel = PandasModel(display_data)
            else:
                pdModel = PandasModel(display_data.iloc[:100, :])
            self.preViewTableCVC.setModel(pdModel)
            self.preViewTableCVC.setColumnWidth(0, 80)
            self.preViewTableCVC.setColumnWidth(1, 80)
            self.preViewTableCVC.setColumnWidth(2, 150)
            self.preViewTableCVC.setColumnWidth(3, 180)
            self.preViewTableCVC.setColumnWidth(4, 80)
            self.importPushButtonCVC.setEnabled(True)
            self.displayPushButtonCVC.setEnabled(True)

        except Exception as e:
            print(f"An error occurred: {e}")
            w = MessageBox('错误',
                           '未选择时间',
                           self)
            w.yesButton.setText('ok')
            w.cancelButton.setText('close')
            self.importPushButtonCVC.setEnabled(True)
            self.displayPushButtonCVC.setEnabled(True)
            w.exec()

    @pyqtSlot()
    def on_displayPushButtonCVC_clicked(self):
        # CVC辊形评价界面"打满显示"按钮
        def getPercent():
            """获取打满百分比"""
            tmp = self.LineEditCVC.text()
            if not tmp:
                w = MessageBox('警告',
                               '未选择打满百分比，设置默认值为95%。',
                               self)
                w.yesButton.setText('ok')
                w.cancelButton.setText('close')
                w.exec()
                self.LineEditCVC.setText('95')
                res = 0.95
            else:
                res = int(float(self.LineEditCVC.text())) * 0.01
            return res

        self.displayPushButtonCVC.setEnabled(False)

        if self.pageCVC_filtered_df.empty:
            data = pd.DataFrame([])
        else:
            data = self.pageCVC_filtered_df.copy()

        if data.empty:
            w = MessageBox('警告',
                           '未导入数据, 将显示所有打满的钢卷',
                           self)
            w.yesButton.setText('ok')
            w.cancelButton.setText('close')
            w.exec()
            percent = getPercent()
            self.highValueDataCVC = self.pageCVC_data[
                abs(self.pageCVC_data['5号机架中间上辊窜辊实际值(S11_0)']) >= 142.5 * percent]
            self.displayPushButtonCVC.setEnabled(True)
        else:
            percent = getPercent()
            self.highValueDataCVC = data[abs(data['5号机架中间上辊窜辊实际值(S11_0)']) >= 142.5 * percent]
            info = f"选择时间段内共{data.shape[0]}卷, 设定值打满共{self.highValueDataCVC.shape[0]}"
            self.SpecificLabelCVC.setText(info)
            decimal_number = (self.highValueDataCVC.shape[0] / data.shape[0])
            percentage = "{:.2%}".format(decimal_number)
            self.PercentLabelCVC.setText(percentage)

        display_data = self.highValueDataCVC.copy()
        display_data.columns = ['策略号', '入口材料号', '生产结束时刻', 'CVC窜辊']
        # 为数据帧添加行号
        display_data.insert(0, '序号', range(1, len(self.highValueDataCVC) + 1))
        if display_data.shape[0] < 100:
            pdModel = PandasModel(display_data)
        else:
            pdModel = PandasModel(display_data.iloc[:100, :])
        self.highValueTableCVC.setModel(pdModel)
        self.highValueTableCVC.setColumnWidth(0, 80)
        self.highValueTableCVC.setColumnWidth(1, 80)
        self.highValueTableCVC.setColumnWidth(2, 150)
        self.highValueTableCVC.setColumnWidth(3, 180)
        self.highValueTableCVC.setColumnWidth(4, 80)

        self.importPushButtonCVC.setEnabled(True)
        self.displayPushButtonCVC.setEnabled(True)
        self.moreInfoPushButtonCVC.setEnabled(True)

        # except Exception as e:
        #     print(e)
        #     w = MessageBox('错误',
        #                    '未知的错误',
        #                    self)
        #     w.yesButton.setText('ok')
        #     w.cancelButton.setText('close')
        #     w.exec()
        #     self.displayPushButtonCVC.setEnabled(True)

    # def updateCanvas(self, leftCanvas, rightCanvas):
    #     leftCanvas.toolbar = NavigationToolbar2QT(leftCanvas, self)  # 添加toolbar
    #     rightCanvas.toolbar = NavigationToolbar2QT(rightCanvas, self)
    #     self.moreInfoWindow.leftLayout.addWidget(leftCanvas.canvas)
    #     self.moreInfoWindow.leftLayout.addWidget(leftCanvas.toolbar)
    #     self.moreInfoWindow.rightLayout.addWidget(rightCanvas.canvas)
    #     self.moreInfoWindow.rightLayout.addWidget(rightCanvas.toolbar)

    @pyqtSlot()
    def on_moreInfoPushButtonCVC_clicked(self):
        """CVC辊形评价界面"详细信息"按钮"""
        # # 清除 self.moreInfoWindow.leftLayout 中的所有子部件
        # self.removeAllWidget(self.moreInfoWindow.leftLayout)
        # self.removeAllWidget(self.moreInfoWindow.rightLayout)
        self.moreInfoPushButtonCVC.setEnabled(False)
        self.moreInfoWindow = MatplotlibWidget()
        # self.plotThread = PlotCVCThread(self.pageCVC_filtered_df, self.highValueDataCVC)
        # self.plotThread.canvasSignal.connect(self.updateCanvas)
        try:
            # self.plotThread.start()
            # if self.plotThread.finished:
            #     self.moreInfoWindow.show()
            # self.plotCVC()
            leftCanvas = MplCanvas()
            leftCanvas.plotBarCVC(self.pageCVC_filtered_df, self.highValueDataCVC)
            leftCanvas.toolbar = NavigationToolbar2QT(leftCanvas, self)  # 添加toolbar

            rightCanvas = MplCanvas()
            rightCanvas.plotPieCVC(self.highValueDataCVC)
            rightCanvas.toolbar = NavigationToolbar2QT(rightCanvas, self)  # 添加toolbar
            self.moreInfoWindow.leftLayout.addWidget(leftCanvas.canvas)
            self.moreInfoWindow.leftLayout.addWidget(leftCanvas.toolbar)
            self.moreInfoWindow.rightLayout.addWidget(rightCanvas.canvas)
            self.moreInfoWindow.rightLayout.addWidget(rightCanvas.toolbar)
            self.moreInfoWindow.show()
            self.moreInfoPushButtonCVC.setEnabled(True)

        except Exception as e:
            print(e)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = CVCEvaluate()
    w.show()
    sys.exit(app.exec_())
