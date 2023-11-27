import pandas as pd

df = pd.read_csv(
    r'D:\code\python\flatness\慢偶因素板形干扰评估\热轧来料\data\（热轧数据）H11.20210601-20220501（已匹配）.csv')
# 去除冷轧平均板形偏差(IU)为0的行
df_new = df[df['冷轧平均板形偏差(IU)'] != 0]
df_new.to_csv(
    r'D:\code\python\flatness\慢偶因素板形干扰评估\热轧来料\data\（热轧数据）H11.20210601-20220501（已匹配）.csv',
    index=False)