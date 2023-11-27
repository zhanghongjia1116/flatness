import os.path

import numpy as np
import pandas as pd
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget
from 板形控制能力评价.预设定值评价.Ui_预设定值评价 import Ui_PresetEvaluate
from my_utils.prompt import showMessageBox
import sys
from PyQt5.QtWidgets import QApplication
from my_utils.display import PandasModel


def softmax(vector):
    """
    Implements the softmax function
    Args:
        vector: (np.array,list,tuple): A  numpy array of shape (1,n)
                consisting of real values or a similar list,tuple
    Returns:
        softmax_vec (np.array): The input numpy array  after applying
        softmax.
        The softmax vector adds up to one. We need to ceil to mitigate for
        precision
    """
    exponent_vector = np.exp(-1 * vector)  # 算向量中每个x的e^x，其中e是自然对数的底数（约2.718）
    # 把所有的指数加起来
    sum_of_exponents = np.sum(exponent_vector)
    # 将每个指数除以所有指数之和
    softmax_vector = exponent_vector / sum_of_exponents
    return softmax_vector


class PresetEvaluate(QWidget, Ui_PresetEvaluate):
    def __init__(self, parent=None):
        super(PresetEvaluate, self).__init__(parent)
        self.setupUi(self)
        self.data = pd.read_pickle(f"{os.path.dirname(__file__)}/data/预设定值初值表.pkl")
        self.CalendarPicker.dateChanged.connect(self.display_data)
        self.columns = ['B1 WRB ref value start',
                        'B1 IRB ref value start',
                        'S1 top IR shfiting ref value start',

                        'B2 WRB ref value start',
                        'B2 IRB ref value start',
                        'S2 top IR shfiting ref value start',

                        'B3 WRB ref value start',
                        'B3 IRB ref value start',
                        'S3 top IR shfitingl ref value start',

                        'WR bending actual value start',
                        'B4 IRB ref value start',
                        'S4 top  IR shfiting  ref value start',

                        'B5 WRB ref value start',
                        'B5 IRB ref value start',
                        'S5 top IR shfiting ref value start']

    @pyqtSlot()
    def on_calculatePushButton_clicked(self):
        strip_num = self.stripLineEdit.text()
        proportion1 = float(self.proportion_1.text())
        proportion3 = float(self.proportion_3.text())
        if proportion1 > 1 or proportion1 < 0 or proportion3 > 1 or proportion3 < 0:
            showMessageBox("权重值应在0-1之间", self)
            return
        if strip_num not in self.data['入口材料号'].values:
            showMessageBox("钢卷号不存在", self)
            return
        s1 = self.coefficient_1(strip_num, proportion1)
        s2 = self.coefficient_2(strip_num)
        s3 = self.coefficient_3(strip_num, proportion3)
        self.coefficientLineEdit_1.setText(str(s1))
        self.coefficientLineEdit_3.setText(str(s3))

    def coefficient_1(self, strip: str, proportion=0.5):
        policyNo = self.data[self.data['入口材料号'] == strip]['policyNo'].values[0]
        index = self.data[self.data['入口材料号'] == strip].index[0]
        singlePolicyData = self.data[self.data['policyNo'] == policyNo]
        good_strip = singlePolicyData[singlePolicyData['50米均值'] < 3]
        preset = singlePolicyData.loc[:, self.columns]
        good_preset = good_strip.loc[:, self.columns]
        IU = singlePolicyData.loc[:, '50米均值']
        normIU = softmax(IU)
        presetValueMean = good_preset.mean()
        distance = np.sqrt(np.square(preset - presetValueMean).sum(axis=1))
        normPrest = softmax(distance)
        # 计算欧氏距离
        s1 = proportion * normPrest + (1 - proportion) * normIU

        return np.round(s1[index], 8)

    def coefficient_2(self, strip: str, proportion=0.5):
        self.coefficientLineEdit_2.setText('亟待开发')
        return 0

    def coefficient_3(self, strip: str, proportion=0.5):
        L = []
        S = []
        row_data = self.data[self.data['入口材料号'] == strip]
        for i in range(1, 6):
            if i == 4:
                l = ((row_data['WR bending actual value start'] + row_data['B4 IRB ref value start']) /
                     2 * row_data['S4 top  IR shfiting  ref value start']).values[0]
                s = (row_data['WR bending actual value start'] + row_data['B4 IRB ref value start'] +
                     row_data['S4 top  IR shfiting  ref value start'])
            elif i == 3:
                l = ((row_data['B3 WRB ref value start'] + row_data['B3 IRB ref value start']) /
                     2 * row_data['S3 top IR shfitingl ref value start']).values[0]
                s = (row_data['B3 WRB ref value start'] + row_data['B3 IRB ref value start'] +
                     row_data['S3 top IR shfitingl ref value start'])
            else:
                l = ((row_data[f'B{i} WRB ref value start'] + row_data[f'B{i} IRB ref value start']) /
                     2 * row_data[f'S{i} top IR shfiting ref value start']).values[0]
                s = (row_data[f'B{i} WRB ref value start'] + row_data[f'B{i} IRB ref value start'] +
                     row_data[f'S{i} top IR shfiting ref value start'])
            L.append(l)
            S.append(s)
        K1 = np.exp(-1 * np.mean(L))
        K2 = np.exp(-1 * np.mean(S))
        res = proportion * K1 + (1 - proportion) * K2
        return np.round(res, 8)

    def display_data(self):
        date = self.CalendarPicker.getDate().toPyDate()
        data = self.data
        # 只保留结束生产时刻的日期
        display_data = data[data['结束生产时刻'].dt.date == date]
        model = PandasModel(display_data.iloc[:50, :])
        self.TableView.setModel(model)
        self.TableView.resizeColumnsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = PresetEvaluate()
    ui.show()
    sys.exit(app.exec_())
