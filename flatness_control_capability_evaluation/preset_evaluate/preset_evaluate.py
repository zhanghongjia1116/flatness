import sys

import numpy as np
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal, QTime
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
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
    return exponent_vector / sum_of_exponents  # 将每个指数除以所有指数之和


def sigmoid_scaling(data):
    max_val = max(data)
    return 1 / (1 + np.exp(-np.array(data) / max_val))


def min_max_scaling(data):
    """
        对数据列表执行最小-最大缩放。
        Args:
            data: The list of data to be scaled.
        Returns:
            List[float]: The scaled data, where each value is transformed to the range [0, 1].
        Raises:
            None
        Examples:
            data = [1, 2, 3, 4, 5]
            min_max_scaling(data)  # Returns [0.0, 0.25, 0.5, 0.75, 1.0]
    """
    min_val = min(data)
    max_val = max(data)

    return [(x - min_val) / (max_val - min_val) for x in data]


class CoefficientThread(QThread):
    result_signal = pyqtSignal(float)
    runTime_signal = pyqtSignal(QTime)

    def __init__(self, BW, hout, C40base, CPtarget, IRB, WRB, IRS, QSbase, DB, DI, DW):
        super(CoefficientThread, self).__init__()
        self.is_running = True
        self.BW = BW
        self.hout = hout
        self.C40base = C40base
        self.CPtarget = CPtarget
        self.IRB = IRB
        self.WRB = WRB
        self.IRS = IRS
        self.QSbase = QSbase
        self.DB = DB
        self.DI = DI
        self.DW = DW

    def run(self):
        start_time = QTime.currentTime()  # 记录开始时间
        result = self.calculate()
        end_time = QTime.currentTime()  # 记录结束时间
        elapsed_time = start_time.secsTo(end_time)  # 计算时间差（秒）
        self.runTime_signal.emit(elapsed_time)
        self.result_signal.emit(result)

    def stop(self):
        self.is_running = False
        print('Stopping thread...')
        self.terminate()

    def calculate(self):
        return get_K(
            BW=self.BW,
            hout=self.hout,
            C40base=self.C40base,
            CPtarget=self.CPtarget,
            IRB=self.IRB,
            WRB=self.WRB,
            IRS=self.IRS,
            QSbase=self.QSbase,
            DB=self.DB,
            DI=self.DI,
            DW=self.DW,
        )


class PresetEvaluate(QWidget, Ui_PresetEvaluate):
    def __init__(self, parent=None):
        super(PresetEvaluate, self).__init__(parent)
        self.thread = None
        self.setupUi(self)

    def get_row_data(self, row_index) -> list[float]:
        """
        从TableWidget的特定行检索并返回数据。

        Args:
            row_index（int）：从中检索数据的行的索引。

        Returns:
            list[float]：指定行中的数据作为浮点列表。
        Explanation:
           此函数从TableWidget的特定行中检索数据。它遍历指定行的列，并从每个项中检索文本。
           然后将文本转换为浮点值并添加到row_data列表中。如果在转换过程中发生任何错误，
           将使用showMessageBox函数显示一条错误消息。函数返回包含检索到的数据的row_data列表。
        """
        row_data = []
        for col in range(self.TableWidget.columnCount()):
            item = self.TableWidget.item(row_index, col)
            if item is not None:
                try:
                    text = item.text()
                    # 去除任意数量的空格
                    text = text.replace(' ', '')
                    row_data.append(float(text))
                except Exception as e:
                    print(e)
                    showMessageBox("提示", f"输入数据第{row_index + 1}行, 第{col + 1}列有误", self)
        return row_data

    def get_lineEdit_data(self, lineEdit):
        """
        从特定的行编辑小部件检索并返回数据。

        Args:
           lineEdit：从中检索数据的行编辑小部件。

        Returns:
            float：行编辑小部件中的数据作为float。

        Explanation:
            此函数用于从特定的行编辑小部件中检索数据。它首先检索行编辑小部件的对象名称。
            然后，它从行编辑小部件中检索文本并删除任何空白。然后将文本转换为浮点值并返回。
            如果在转换过程中发生任何错误，将使用showMessageBox函数显示一条错误消息。
        """

        name = lineEdit.objectName()
        try:
            text = lineEdit.text()
            # 去除任意数量的空格
            text = text.replace(' ', '')
            return float(text)
        except Exception as e:
            print(e)
            showMessageBox("提示", f"{name}输入数据有误", self)

    def stop_calculate_coefficient_2_worker(self, run_time):
        # 停止子线程
        self.thread.stop()
        self.calculatePushButton.setEnabled(True)
        showMessageBox("提示", f"计算结束, 计算时长{run_time}秒", self)

    def update_coefficient_2(self, result):
        K2 = np.round(result, 8)
        self.coefficientLineEdit_2.setText(str(K2))
        res = self.coefficient_1 * self.proportion1 + K2 * self.proportion2 + self.coefficient_3 * self.proportion3
        res = np.round(res, 8)
        self.coefficientLineEdit_final.setText(str(res))

    @pyqtSlot()
    def on_calculatePushButton_clicked(self):
        showMessageBox("提示", "开始计算, 系数二计算时间较长, 请减少操作界面", self)
        self.proportion1 = self.get_lineEdit_data(self.proportion_1)
        self.proportion2 = self.get_lineEdit_data(self.proportion_2)
        self.proportion3 = self.get_lineEdit_data(self.proportion_3)

        # 要求self.proportion1+self.proportion2+self.proportion3=1, 并且self.proportion1, self.proportion3在0-1之间
        if self.proportion1 + self.proportion2 + self.proportion3 != 1:
            showMessageBox("提示", "三个比例之和不为1", self)
            return
        if not (0 <= self.proportion1 <= 1 and 0 <= self.proportion2 <= 1 and 0 <= self.proportion3 <= 1):
            showMessageBox("提示", "比例应在0-1之间", self)
            return

        # 获取TableWidget各行的数据
        WRB = self.get_row_data(0)  # 第一行数据
        WRB_percent = [(wrb + 35) / 85 for wrb in WRB]
        IRB = self.get_row_data(1)  # 第二行数据
        IRB_percent = [irb / 130 for irb in IRB]
        IRS = self.get_row_data(2)  # 第三行数据
        IRS_percent = [(irs + 142.5) / 285 for irs in IRS]
        exitThickness = self.get_row_data(3)  # 第四行数据
        rollForce = self.get_row_data(4)  # 第五行数据
        BURDiameter = self.get_row_data(5)  # 第六行数据
        IRBDiameter = self.get_row_data(6)  # 第七行数据
        WRBDiameter = self.get_row_data(7)  # 第八行数据

        # 要求以上数据都是长度为5的列表
        if not (len(WRB) == len(IRB) == len(IRS) == len(exitThickness) == len(rollForce) == len(BURDiameter) == len(
                IRBDiameter) == len(WRBDiameter) == 5):
            return

        # 获取IULineEdit的数据, 计算系数1
        IU = self.get_lineEdit_data(self.IULineEdit)
        scaledIU = 1 / (1 + np.exp(IU - 10))
        self.coefficient_1 = np.round(scaledIU, 8)
        self.coefficientLineEdit_1.setText(str(self.coefficient_1))  # 设置系数1

        # 计算系数3
        coefficient_3_L = [(wrb + irb) / 2 * irs for wrb, irb, irs in zip(WRB_percent, IRB_percent, IRS_percent)]
        coefficient_3_S = [(wrb + irb + irs) for wrb, irb, irs in zip(WRB_percent, IRB_percent, IRS_percent)]
        coefficient_3_K1 = np.exp(-1 * np.mean(coefficient_3_L))
        coefficient_3_K2 = np.exp(-1 * np.mean(coefficient_3_S))
        self.coefficient_3 = 0.5 * coefficient_3_K1 + 0.5 * coefficient_3_K2
        self.coefficientLineEdit_3.setText(str(np.round(self.coefficient_3, 8)))  # 设置系数3

        # 读取带钢相关参数
        stripWidth = self.get_lineEdit_data(self.stripWidthLineEdit)
        materialConvexity = self.get_lineEdit_data(self.materialConvexityLineEdit)
        exitThickness_5 = self.get_lineEdit_data(self.exitThicknessLineEdit)
        targetConvexity = self.get_lineEdit_data(self.targetConvexityLineEdit)

        # 计算系数2
        self.thread = CoefficientThread(BW=stripWidth,
                                        hout=exitThickness,
                                        C40base=materialConvexity, CPtarget=targetConvexity,
                                        IRB=IRB, WRB=WRB, IRS=IRS,
                                        QSbase=[i / stripWidth for i in rollForce],
                                        DB=BURDiameter, DI=IRBDiameter, DW=WRBDiameter)
        self.thread.runTime_signal.connect(self.stop_calculate_coefficient_2_worker)
        self.thread.result_signal.connect(self.update_coefficient_2)
        self.thread.start()
        self.calculatePushButton.setEnabled(False)

    @pyqtSlot()
    def on_stopCalculatePushButton_clicked(self):
        # print("stop")
        if not self.thread:
            return
        showMessageBox(title="提示", content="停止计算...", parent=self)
        self.thread.stop()
        self.calculatePushButton.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = PresetEvaluate()
    ui.show()
    sys.exit(app.exec_())
