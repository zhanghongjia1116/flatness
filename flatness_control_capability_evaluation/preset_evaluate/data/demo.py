import pandas as pd

df = pd.read_pickle('standard_value.pkl')

# 删除带有9999的行
drop_index = df[df['WRB_1'] == 9999].index
df.drop(drop_index, inplace=True)


def wrb_fuc(row):
    minValue = -700
    maxValue = 1000
    # 放缩到0-1之间
    return row / minValue if row < 0 else row / maxValue


def irb_fuc(row):
    minValue = -1800
    maxValue = 2600
    # 放缩到0-1之间
    return row / minValue if row < 0 else row / maxValue


def irs_fuc(row):
    # 放缩到0-1之间
    return row / 285


df['WRB_1'] = df['WRB_1'].apply(wrb_fuc)
df['WRB_2'] = df['WRB_2'].apply(wrb_fuc)
df['WRB_3'] = df['WRB_3'].apply(wrb_fuc)
df['WRB_4'] = df['WRB_4'].apply(wrb_fuc)
df['WRB_5'] = df['WRB_5'].apply(wrb_fuc)

df['IRB_1'] = df['IRB_1'].apply(irb_fuc)
df['IRB_2'] = df['IRB_2'].apply(irb_fuc)
df['IRB_3'] = df['IRB_3'].apply(irb_fuc)
df['IRB_4'] = df['IRB_4'].apply(irb_fuc)
df['IRB_5'] = df['IRB_5'].apply(irb_fuc)

df['IRS_1'] = df['IRS_1'].apply(irs_fuc)
df['IRS_2'] = df['IRS_2'].apply(irs_fuc)
df['IRS_3'] = df['IRS_3'].apply(irs_fuc)
df['IRS_4'] = df['IRS_4'].apply(irs_fuc)
df['IRS_5'] = df['IRS_5'].apply(irs_fuc)

df.to_pickle('./standard_value_scaled.pkl')

