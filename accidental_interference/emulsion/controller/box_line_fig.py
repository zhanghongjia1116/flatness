import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QWidget
from matplotlib.backends.backend_qt import NavigationToolbar2QT

from accidental_interference.emulsion.view.Ui_concentration_IU_scatter import Ui_AvgIUAndLiquid
from accidental_interference.emulsion.controller.draw_pic import MplCanvas


class BoxDiagram(QWidget, Ui_AvgIUAndLiquid):
    def __init__(self, data):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('箱线图')
        self.data = data
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

        # 删除含有空值的行
        data = data.dropna(subset=['PH值', '浓度', '电导率'])
        # 按月份进行分组
        data_grouped = data.groupby(data['结束生产时刻'].dt.to_period("M"))

        concentration = []
        ph = []
        conductivity = []
        x_labels = []

        for i in data_grouped.groups:
            concentration.append(data_grouped.get_group(i)['浓度'].tolist())
            ph.append(data_grouped.get_group(i)['PH值'].tolist())
            conductivity.append(data_grouped.get_group(i)['电导率'].tolist())
            x_labels.append(i)

        try:
            self.graphicsView.setVisible(False)
            leftCanvas = MplCanvas()
            leftCanvas.liquidBoxDiagram(concentration, ph, conductivity, x_labels)
            leftCanvas.toolbar = NavigationToolbar2QT(leftCanvas)
            self.gridLayoutLeft.addWidget(leftCanvas)
            self.gridLayoutLeft.addWidget(leftCanvas.toolbar)
        except Exception as e:
            print(e)
