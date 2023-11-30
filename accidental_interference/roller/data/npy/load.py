import numpy as np


def load_npy(path):
    """
    读取npy文件
    """
    return np.load(path, allow_pickle=True)


if __name__ == '__main__':
    path = r'D:\zhhj_work\zhhj_GUI\轧辊服役期\npy\bur2imr_1.npy'
    data = load_npy(path)
    print(data)
