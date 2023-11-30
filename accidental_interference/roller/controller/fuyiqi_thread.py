import os

import numpy as np
import pandas as pd
from PyQt5.QtCore import QObject, pyqtSignal, QEventLoop, QTimer, QThread, QTime, QMutex


# suo_1=QMutex()
class BUR_plot(QThread):
    sinOut = pyqtSignal(list, list)

    def __init__(self, zhagunhao):
        super(BUR_plot, self).__init__()
        self.zhagunhao = zhagunhao

    # 重写run()方法
    def run(self):
        # suo_1.lock()
        imr_iu_dir_path = os.getcwd() + '\data\换辊记录匹配iu值\中间辊'

        bur2imr = np.load('bur2imr.npy', allow_pickle=True).item()

        roll_dict = bur2imr
        child_zhagunhao = roll_dict[self.zhagunhao]
        iu_mean = []
        for value in child_zhagunhao:
            df = pd.read_excel('%s\%s%s' % (imr_iu_dir_path, value, '.xlsx'), header=0)
            df = df.fillna(0)
            if np.sum(df['个数']) != 0:
                iu = np.sum(df['均值'] * df['个数']) / np.sum(df['个数'])
                iu_mean.append(iu)
            else:
                iu_mean.append(0)
        x_name = child_zhagunhao
        x = range(len(child_zhagunhao))
        y = iu_mean
        # suo_1.unlock()
        self.sinOut.emit(x_name, y)
        # self.sinOut.emit(y)
