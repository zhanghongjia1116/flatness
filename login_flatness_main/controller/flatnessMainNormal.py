# coding:utf-8
import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow
from my_utils.prompt import showMessageBox

from abnormal_flatness_monitoring.abnormal_flatness_monitoring_main import 异常板形监测溯源
# from accidental_interference.慢偶因素Main import AccidentalFactor
from accidental_interference.accidental_interference_main import 慢偶因素
from flatness_control_capability_evaluation.flatness_control_capability_evaluation_main import 板形控制能力评价
from flatness_control_data_model_optimization.flatness_control_data_model_optimization import 板形控制数模优化
from flatness_generate_data_model.flatness_generate_data_model_main import 板形生成数据建模
from flatness_quality_evaluate.flatness_quality_evaluate_main import 板形质量评价
from flatness_regulatory_efficacy.flatness_regulatory_efficacy import 板形调控功效挖掘
from login_flatness_main.view.Ui_flatnessMainNormal import Ui_FlatnessMain


class MainWindow(QMainWindow, Ui_FlatnessMain):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.板形质量评价 = None
        self.异常板形监测溯源 = None
        self.慢偶因素板形干扰评估 = None
        self.板形调控功效挖掘 = None
        self.板形生成数据建模 = None
        self.板形控制能力评价 = None
        self.板形控制数模优化 = None

    @pyqtSlot()
    def on_PrimaryPushButton_clicked(self):
        self.板形质量评价 = 板形质量评价()
        self.板形质量评价.show()

    @pyqtSlot()
    def on_PrimaryPushButton_2_clicked(self):
        self.异常板形监测溯源 = 异常板形监测溯源()
        self.异常板形监测溯源.show()

    @pyqtSlot()
    def on_PrimaryPushButton_3_clicked(self):
        self.慢偶因素板形干扰评估 = 慢偶因素()
        self.慢偶因素板形干扰评估.show()

    @pyqtSlot()
    def on_PrimaryPushButton_4_clicked(self):
        self.板形调控功效挖掘 = 板形调控功效挖掘()
        self.板形调控功效挖掘.show()

    @pyqtSlot()
    def on_PrimaryPushButton_5_clicked(self):
        self.板形生成数据建模 = 板形生成数据建模()
        self.板形生成数据建模.show()

    @pyqtSlot()
    def on_PrimaryPushButton_6_clicked(self):
        self.板形控制能力评价 = 板形控制能力评价()
        self.板形控制能力评价.show()

    @pyqtSlot()
    def on_PrimaryPushButton_7_clicked(self):
        self.板形控制数模优化 = 板形控制数模优化()
        self.板形控制数模优化.show()

    @pyqtSlot()
    def on_PrimaryPushButton_8_clicked(self):
        showMessageBox('提示', "数据服务内嵌于各功能模块中.", parent=self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
