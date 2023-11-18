import pandas as pd
import os


class CVCdata:
    def __init__(self, data=None):
        local_path = os.path.abspath(__file__)
        tmp = os.path.dirname(local_path)
        data_path = f'{tmp}/data'
        # 获取data_path文件夹下所有文件的路径
        file_path = [os.path.join(data_path, i) for i in os.listdir(data_path)]
        self.data_path = file_path
        if data is None:
            CVC2020 = self.getNeedData(0)
            CVC2021 = self.getNeedData(1)
            CVC2022 = self.getNeedData(2)
            CVC2023 = self.getNeedData(3)
            self.allData = pd.concat([CVC2020, CVC2021, CVC2022, CVC2023], ignore_index=True)
        else:
            self.allData = data

    def getNeedData(self, num):
        needData = pd.read_csv(self.data_path[num],
                               usecols=['aDirNoAi', '生产结束时刻(S11_0)', '入口卷号(S11_0)',
                                        '5号机架中间上辊窜辊实际值(S11_0)'])
        # 删除列5号机架中间上辊窜辊实际值(S11_0)中为空值的行
        needData.dropna(inplace=True)
        needData['生产结束时刻(S11_0)'] = pd.to_datetime(needData['生产结束时刻(S11_0)'])
        needData['5号机架中间上辊窜辊实际值(S11_0)'] = needData['5号机架中间上辊窜辊实际值(S11_0)'].astype(int)
        needData['aDirNoAi'] = needData['aDirNoAi'].astype(int)
        return needData


class BURdata:
    def __init__(self, data=None):
        # self.data_path = file_path
        self.frame1name = ['1号机架中间辊弯辊实际值(S11_0)', '1号机架中间上辊窜辊实际值(S11_0)',
                           '1号机架工作辊弯辊实际值(S11_0)']
        self.frame2name = ['2号机架中间辊弯辊实际值(S11_0)', '2号机架中间上辊窜辊实际值(S11_0)',
                           '2号机架工作辊弯辊实际值(S11_0)']
        self.frame3name = ['3号机架中间辊弯辊实际值(S11_0)', '3号机架中间上辊窜辊实际值(S11_0)',
                           '3号机架工作辊弯辊实际值(S11_0)']
        self.frame4name = ['4号机架中间辊弯辊实际值(S11_0)', '4号机架中间上辊窜辊实际值(S11_0)',
                           '4号机架工作辊弯辊实际值(S11_0)']
        self.frame5name = ['5号机架中间辊弯辊实际值(S11_0)', '5号机架中间上辊窜辊实际值(S11_0)',
                           '5号机架工作辊弯辊实际值(S11_0)']
        self.basicName = ['aDirNoAi', '生产结束时刻(S11_0)', '入口卷号(S11_0)']
        if data is None:
            BUR2020 = self.getNeedData(0)
            BUR2021 = self.getNeedData(1)
            BUR2022 = self.getNeedData(2)
            BUR2023 = self.getNeedData(3)
            self.allData = pd.concat([BUR2020, BUR2021, BUR2022, BUR2023], ignore_index=True)
        else:
            self.allData = data

    def getNeedData(self, num):
        allFrameName = self.frame1name + self.frame2name + self.frame3name + self.frame4name + self.frame5name
        needData = pd.read_csv(self.data_path[num], usecols=self.basicName + allFrameName)
        # 删除列5号机架中间上辊窜辊实际值(S11_0)中为空值的行
        needData.dropna(inplace=True)
        needData['生产结束时刻(S11_0)'] = pd.to_datetime(needData['生产结束时刻(S11_0)'])

        needData[allFrameName] = needData[allFrameName].astype(int)
        needData['aDirNoAi'] = needData['aDirNoAi'].astype(int)
        return needData

    @property
    def bur1(self):
        return self.allData[self.basicName + self.frame1name]

    @property
    def bur2(self):
        return self.allData[self.basicName + self.frame2name]

    @property
    def bur3(self):
        return self.allData[self.basicName + self.frame3name]

    @property
    def bur4(self):
        return self.allData[self.basicName + self.frame4name]

    @property
    def bur5(self):
        return self.allData[self.basicName + self.frame5name]


if __name__ == '__main__':
    df = BURdata().allData
    df.to_pickle('BURdata.pkl')
