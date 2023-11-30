import pandas as pd
from my_utils.zhhj_file import get_certain_file
import os

local_path = os.path.abspath(__file__)
folder = os.path.dirname(local_path)

csv_list = get_certain_file(folder, '.csv')
print(csv_list)

res = pd.DataFrame([])
for i in range(len(csv_list)):
    df = pd.read_csv(csv_list[i])
    # 按列concat
    res = pd.concat([res, df], axis=0)

res = res.loc[:, ['钢卷号', '板坯牌号', 'APSKEY', 'hEntryId', 'hExitId', 'wId', 'policyNo', 'IU均值', '50米均值', '100米均值',
                  'B1 WRB ref value start',
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
                  'S5 top IR shfiting ref value start'
                  ]]
res['钢卷号'] = res['钢卷号'].apply(lambda x: x.replace('_1', ''))
res.rename(columns={'钢卷号': '入口材料号'}, inplace=True)

res.drop_duplicates(subset=['入口材料号'], inplace=True)

onlineData = pd.read_pickle(r'D:\zhhj_work\zhhj_GUI\flatness\慢偶因素板形干扰评估\酸轧在线判定\酸轧在线判定.pkl')
res = pd.merge(onlineData, res, on='入口材料号')
res.to_pickle('./预设定值初值表.pkl')
