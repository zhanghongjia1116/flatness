import glob
import os
import re
from datetime import datetime
import pandas as pd
from icecream import ic


# from 信号分析.轧辊数据处理 import concat_huanGun_pda

# 定义一个函数来格式化时间
def format_time(time_str):
    if '1900-01-01' in time_str:
        time_str = time_str.replace('1900-01-01', '')
    try:
        # 尝试解析成完整的时间格式
        a = datetime.strptime(time_str, "%Y.%m.%d %H:%M:%S").strftime("%Y.%m.%d %H:%M:%S")
        return a
    except:
        # 解析失败，说明是不完整的时间格式，只有时分秒
        a = datetime.strptime(time_str, "%Y.%m.%d %H:%M").strftime("%Y.%m.%d %H:%M:%S")
        return a

def concat_stop_data(file_path_, is_save=False):
    """"""
    file_path = glob.glob(os.path.join(file_path_, "*.xls"))
    # ic(file_path)

    cols = ['日期', '开始时间', '结束时间', '停机时间(分钟)', '停机原因', '分类']
    stop_data = []
    for file in file_path:
        df = pd.read_excel(file, header=4)[cols]
        ym = os.path.basename(file)[:7]
        start_t = ym + '.' + df['日期'].astype(str) + ' ' + df['开始时间'].astype(str)
        end_t = ym + '.' + df['日期'].astype(str) + ' ' + df['结束时间'].astype(str)
        df.insert(0, 'start_time', start_t)
        df.insert(1, 'end_time', end_t)
        # 序列中包含24:00:00或24:00的数据的索引
        mask_start = df['start_time'].str.match(r'.*24:00(:00)?$')
        mask_end = df['end_time'].str.match(r'.*24:00(:00)?$')
        # 将mask中的数据替换为00:00:00
        df.loc[mask_start, 'start_time'] = df.loc[mask_start, 'start_time'].apply(
            lambda x: re.sub(r' 24:00(:00)?$', ' 00:00:00', x))

        df.loc[mask_end, 'end_time'] = df.loc[mask_end, 'end_time'].apply(
            lambda x: re.sub(r' 24:00(:00)?$', ' 00:00:00', x))

        # 将时间转换为datetime格式
        df['start_time'] = df['start_time'].apply(format_time)
        df['end_time'] = df['end_time'].apply(format_time)

        df['start_time'] = pd.to_datetime(df['start_time'], format='%Y.%m.%d %H:%M:%S')
        df['end_time'] = pd.to_datetime(df['end_time'], format='%Y.%m.%d %H:%M:%S')

        # 对于出现了 "24:00" 的日期，将日期加 1 天
        df.loc[mask_start, 'start_time'] = df.loc[mask_start, 'start_time'] + pd.Timedelta(days=1)
        df.loc[mask_end, 'end_time'] = df.loc[mask_end, 'end_time'] + pd.Timedelta(days=1)

        df = df.loc[:, ['start_time', 'end_time', '停机时间(分钟)', '停机原因', '分类']]
        # ic(df)
        stop_data.append(df)
        # t =
    stop_data = pd.concat(stop_data)
    if is_save:
        stop_data.to_csv(fr'{file_path_}\合并.csv', index=False)
    return stop_data.dropna(subset='end_time').sort_values(by='end_time').reset_index(drop=True)


if __name__ == '__main__':
    file_path = 'raw'
    df = concat_stop_data(file_path, is_save=False)
    pda_path = r'F:\my_objects\预设定相关工作的数据\数据与有限元协作分析\日志文件数据(添加w).csv'
    df_iu = pd.read_csv(pda_path)
    df_iu['time'] = pd.to_datetime(df_iu['time'])
    # df = concat_huanGun_pda(df, df_iu, name='end_time')
    print(df)
    df.to_csv('停机后开机第一卷数据.csv', index=False)
