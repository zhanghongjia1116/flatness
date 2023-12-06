import os.path
import sys

import numpy as np
import pandas as pd
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from my_utils.display import PandasModel
from my_utils.prompt import showMessageBox

from flatness_control_capability_evaluation.preset_evaluate.Ui_preset_evaluate import Ui_PresetEvaluate
from flatness_control_capability_evaluation.preset_evaluate.coefficient_2.coefficient import get_K


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


def sigmoid_scaling(data):
    max_val = max(data)
    scaled_data = 1 / (1 + np.exp(-np.array(data) / max_val))
    return scaled_data


def min_max_scaling(data):
    min_val = min(data)
    max_val = max(data)

    scaled_data = [(x - min_val) / (max_val - min_val) for x in data]

    return scaled_data


class PresetEvaluate(QWidget, Ui_PresetEvaluate):
    def __init__(self, parent=None):
        super(PresetEvaluate, self).__init__(parent)
        self.setupUi(self)
        self.data = pd.read_pickle(f"{os.path.dirname(__file__)}/data/预设定值初值表.pkl")
        self.系数2_data = pd.read_excel(f"{os.path.dirname(__file__)}/data/待评价工况.xlsx")
        self.data_CPL = pd.read_excel(f"{os.path.dirname(__file__)}/data/CPL.xlsx", header=None)
        self.data_CPB = pd.read_excel(f"{os.path.dirname(__file__)}/data/CPB.xlsx", header=None)
        self.standard = pd.read_pickle(f"{os.path.dirname(__file__)}/data/standard_value_scaled.pkl")
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
            showMessageBox("提示", "权重值应在0-1之间", self)
            return
        if strip_num not in self.data['入口材料号'].values:
            showMessageBox("提示", "钢卷号不存在", self)
            return
        s1 = self.coefficient_1(strip_num, proportion1)
        s2 = self.coefficient_2(strip_num)
        s3 = self.coefficient_3(strip_num, proportion3)
        self.coefficientLineEdit_1.setText(str(s1))
        self.coefficientLineEdit_2.setText(str(s2))
        self.coefficientLineEdit_3.setText(str(s3))

    def coefficient_1(self, strip: str, proportion=0.5):
        index = self.data[self.data['入口材料号'] == strip].index[0]
        IU_series = self.data['50米均值']
        scaledIU = IU_series.apply(lambda x: 1 / (1 + np.exp((x - 10))))

        policyNo = self.data.loc[index, 'policyNo']
        singlePolicyData = self.data[self.data['policyNo'] == policyNo].reset_index()
        index_single = singlePolicyData[singlePolicyData['入口材料号'] == strip].index[0]
        standardValue = self.standard[self.standard['ADIRNO_AI'] == policyNo].iloc[0, 1:].to_numpy()
        preset: pd.DataFrame = singlePolicyData.loc[:, self.columns].to_numpy()
        distance = np.sqrt(np.square(preset - standardValue).sum(axis=1))

        # 计算欧氏距离
        s1 = proportion * scaledIU[index] + (1 - proportion) * distance[index_single]

        return np.round(s1, 8)

    def coefficient_2(self, strip: str):
        index = self.data[self.data['入口材料号'] == strip].index[0]
        policyNo = self.data.loc[index, 'policyNo']

        try:
            K = get_K(policyNo, self.系数2_data, self.data_CPB, self.data_CPL)
            return np.round(K, 8)
        except Exception as e:
            print(e)
            showMessageBox("提示", f"计算系数2时发生错误：表中不包含该钢卷的策略号", self)
            return

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
