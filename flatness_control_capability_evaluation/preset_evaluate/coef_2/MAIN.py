from coefficient import get_K
import numpy as np
import multiprocessing

if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=10)

    BW = np.double(1000)
    hout = [5.0,3.5,2.5,2.0,1.8]
    C40base = 54.1
    CPtarget = 18
    IRB = [87.4,75.9,74.2,67.4,72.4]
    WRB= [44.4,39.2,38.4,37.5,25.7]
    IRS= [128,128,121,111,-72]
    QSbase = [0.9,0.8,0.6,0.6,0.3]
    DB = [1300,1300,1300,1300,1300]
    DI = [560,560,560,560,560]
    DW = [480,480,480,480,480]
    Result = get_K(BW, hout, C40base, CPtarget, IRB, WRB, IRS, QSbase, DB, DI, DW, pool)
