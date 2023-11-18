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

print(res)
# res.to_pickle('./酸轧在线判定.pkl')
