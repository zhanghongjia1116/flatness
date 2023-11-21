import numpy as np


class DataMesh:
    INB: int = 81
    INI: int = 97
    INW: int = 81
    NP: int = 0
    NE: int = 0
    INC = np.zeros(5 + 1, dtype=np.int32)
    NSBRD: int = 0
    NSIRT: int = 0
    NSIRD: int = 0
    NSWRT: int = 0
    NSWRD: int = 0
    NPBR: int = 0
    NPIR: int = 0
    NPWR: int = 0
    NEBR: int = 0
    NEIR: int = 0
    NEWR: int = 0
    NL: int = 0
    NO_S = np.zeros(66 + 1, dtype=np.int32)
    CNBI: int = 0
    CNIW: int = 0
    KSFTI: int = 0
    KSFTW: int = 0
    KOFF: int = 0
    MS = np.zeros((4000 + 1, 3 + 1), dtype=np.int32)
    NYBI: int = 0
    NYIW: int = 0
    X = np.zeros(2500 + 1, dtype=np.float64)
    Y = np.zeros(2500 + 1, dtype=np.float64)
    TH = np.zeros(4000 + 1, dtype=np.float64)
    SP = 0.0
    DP = np.zeros((2500 + 1, 2 + 1), dtype=np.float64)
    RDS = np.zeros((2500 + 1, 2 + 1), dtype=np.float64)
    PRFL = np.zeros((100 + 1, 10 + 1), dtype=np.float64)
    RDT = np.zeros((100 + 1, 10 + 1), dtype=np.float64)
    TEQB = 13.0
    TEQI = 6.0
    TEQW = 5.0
    PROBR = np.zeros(100 + 1, dtype=np.float64)
    PROIR = np.zeros(100 + 1, dtype=np.float64)
    PROWR = np.zeros(100 + 1, dtype=np.float64)
    RSX = np.zeros(9 + 1, dtype=np.float64)


