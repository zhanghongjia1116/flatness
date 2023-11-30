import os
import numpy as np
import pandas as pd
from my_utils.prompt import showMessageBox
from ..view.Ui_HotRollingInterface import Ui_HotRollingInterface
from .draw_pic import MplCanvas
from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog
from PyQt5.QtCore import pyqtSlot
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT


class HotRollingInterface(QWidget, Ui_HotRollingInterface):
    def __init__(self):
        super().__init__()
        self.hot_rolling_data = None
        self.setupUi(self)
        self.displayPushButton.setEnabled(False)
        self.init_combox()

    def init_combox(self):
        self.ComboBox.clear()
        self.ComboBox.addItems(
            ["请选择变量", "卷取温度均值", "厚度均值", "宽度均值", "平直度均值", "凸度C25", "凸度C40",
             "楔形W40绝对值均值"])

    def cal_bar(self, x, lins, data, x_target, y_target):
        lins = float(lins)
        max_val = ((max(x) // lins) + 1) * lins
        min_val = (min(x) // lins) * lins
        lis = np.arange(min_val, max_val + 0.01, lins)
        all_num = []
        mean_val = []
        x_lis = []
        for i in range(len(lis) - 1):
            temp = data[(data[x_target] >= lis[i]) & (data[x_target] < lis[i + 1])]
            all_num.append(temp.shape[0])
            mean_val.append(np.mean(temp[y_target]))
            x_lis.append('%.1f-%.1f' % (lis[i], lis[i + 1]))
        return all_num, mean_val, x_lis

    @pyqtSlot()
    def on_importPushButton_clicked(self):
        tmp = os.path.dirname(os.path.dirname(__file__))
        data_dir = f"{tmp}/data/"
        file_name, file_type = QFileDialog.getOpenFileName(self, "选取文件", data_dir,
                                                           "Data Files (*.xlsx *.csv *.xls *.pkl)")
        if file_name == "":
            showMessageBox("提示", "未选择文件！", self)
            return
        self.LineEdit.setText(os.path.basename(file_name))
        self.hot_rolling_data = pd.read_csv(file_name)
        self.displayPushButton.setEnabled(True)

    @pyqtSlot()
    def on_displayPushButton_clicked(self):
        # 删除之前的画布
        for i in range(self.leftLayout.count()):
            self.leftLayout.itemAt(i).widget().deleteLater()
        for i in range(self.rightLayout.count()):
            self.rightLayout.itemAt(i).widget().deleteLater()
        # 获取Combox中的值
        var = self.ComboBox.currentText()
        lin_num = 0
        if var == "请选择变量":
            return
        elif var == '卷取温度均值':
            lin_num = 30.0
        elif var == '厚度均值':
            lin_num = 0.2
        elif var == '宽度均值':
            lin_num = 30.0
        elif var == '平直度均值':
            lin_num = 10.0
        elif var == '凸度C25':
            lin_num = 10.0
        elif var == '凸度C40':
            lin_num = 10.0
        elif var == '楔形W40绝对值均值':
            lin_num = 10.0
        all_num, mean_val, x_lis = self.cal_bar(x=self.hot_rolling_data[var],
                                                lins=lin_num, data=self.hot_rolling_data,
                                                x_target=var,
                                                y_target='冷轧平均板形偏差(IU)')
        leftCanvas = MplCanvas()
        leftCanvas.plot_bar(all_num, mean_val, x_lis, var, '冷轧平均板形偏差(IU)')
        leftCanvas.toolbar = NavigationToolbar2QT(leftCanvas, self)  # 添加toolbar

        rightCanvas = MplCanvas()
        rightCanvas.scatter_iu(var, '冷轧平均板形偏差(IU)', self.hot_rolling_data)
        rightCanvas.toolbar = NavigationToolbar2QT(rightCanvas, self)  # 添加toolbar

        self.leftLayout.addWidget(leftCanvas)
        self.leftLayout.addWidget(leftCanvas.toolbar)
        self.rightLayout.addWidget(rightCanvas)
        self.rightLayout.addWidget(rightCanvas.toolbar)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ui = HotRollingInterface()
    ui.show()
    sys.exit(app.exec_())
