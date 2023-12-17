import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QWidget
from matplotlib.backends.backend_qt import NavigationToolbar2QT

from accidental_interference.emulsion.controller.draw_pic import MplCanvas
from accidental_interference.emulsion.view.Ui_concentration_IU_scatter import Ui_AvgIUAndLiquid


class AvgIUAndLiquid(QWidget, Ui_AvgIUAndLiquid):
    def __init__(self, data):
        super().__init__()
        self.setupUi(self)
        self.data = data.loc[:, ['入口材料号', '结束生产时刻', 'policyNo', 'IU均值', '浓度', '电导率', 'PH值', '温度']]
        self.data = self.data.dropna(subset=['PH值', 'IU均值', 'policyNo'])
        self.data = self.data[(self.data['浓度'] != 'shutdown') & (self.data['浓度'] != '停机检修')]
        self.data['浓度'] = self.data['浓度'].astype(float)  # 转为浮点类型
        self.data['policyNo'] = self.data['policyNo'].astype(int)
        # 连接槽函数
        self.RadioButton2021.toggled.connect(self.init_left_canvas)
        self.RadioButton2022.toggled.connect(self.init_left_canvas)
        self.RadioButton2023.toggled.connect(self.init_left_canvas)

    def init_left_canvas(self):
        for i in range(1, self.gridLayoutLeft.count()):
            self.gridLayoutLeft.itemAt(i).widget().deleteLater()
        # 获取选中的单选按钮的文本
        data = None
        if self.RadioButton2021.isChecked():
            # 筛选2022年1月1日前的数据
            data = self.data[self.data['结束生产时刻'] < pd.to_datetime('2022-01-01')]
        elif self.RadioButton2022.isChecked():
            # 筛选2022年1月1日至2023年1月1日的数据
            data = self.data[(self.data['结束生产时刻'] >= pd.to_datetime('2022-01-01')) &
                             (self.data['结束生产时刻'] < pd.to_datetime('2023-01-01'))]
        elif self.RadioButton2023.isChecked():
            # 筛选2023年1月1日后的数据
            data = self.data[self.data['结束生产时刻'] >= pd.to_datetime('2023-01-01')]

        series1 = data['浓度']
        series2 = data['IU均值']
        count = series1.unique()
        avg_list = np.array([])
        length_list = np.array([])
        for i in count:
            length = series2[series1 == i].shape
            avg = series2[series1 == i].mean()
            avg_list = np.append(avg_list, avg)
            length_list = np.append(length_list, length)

        try:
            self.graphicsView.setVisible(False)
            leftCanvas = MplCanvas()
            leftCanvas.avgIUAndLiquid(count, avg_list, length_list)
            leftCanvas.toolbar = NavigationToolbar2QT(leftCanvas)
            self.gridLayoutLeft.addWidget(leftCanvas)
            self.gridLayoutLeft.addWidget(leftCanvas.toolbar)
        except Exception as e:
            print(e)