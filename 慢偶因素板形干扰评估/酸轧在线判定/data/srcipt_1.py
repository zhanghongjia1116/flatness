from my_utils.zhhj_data import 酸轧在线判定

data = 酸轧在线判定.merge_single_data(
    folder_path=r'D:\zhhj_work\zhhj_GUI\flatness\慢偶因素板形干扰评估\酸轧在线判定\data',
    use_cols=['入口材料号', '结束生产时刻', '缺陷备注'])


data.to_pickle(r'.\酸轧在线判定.pkl')