from my_utils.zhhj_data import 乳化液数据
import pandas as pd
import argparse

# parser添加args
parser = argparse.ArgumentParser()
parser.add_argument('--path_2022', type=str, default=r'./2022/raw/乳化液指标记录表2021.xls', help='2022乳化液数据路径')
parser.add_argument('--path_2023', type=str, default=r'./2023/raw/乳化液指标记录表2023.xls', help='2023乳化液数据路径')
parser.add_argument('--save_path_2022', type=str, default=r'./process/乳化液数据.xlsx', help='乳化液数据保存路径')
parser.add_argument('--save_path_2023', type=str, default=r'./process/乳化液数据.xlsx', help='乳化液数据保存路径')

args = parser.parse_args()

# 读取数据
data = 乳化液数据(args.path_2022)
time_format = data.format_time(box=3)
