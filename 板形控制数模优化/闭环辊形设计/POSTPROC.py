import math

import numpy as np

import DATA_FORC
import DATA_MESH
import DATA_SHAP
from DATA_ROLL import DataRoll


def REGR(IK):
    NL = DATA_MESH.NL
    A = np.zeros((NL+1, NL+1))
    DTY = np.zeros(NL+1)
    DTX = np.zeros(NL+1)
    for I in range(1, NL+1):
        for J in range(1, NL+1):
            A[I, J] = 0.0e0
    for I in range(1, NL+1):
        A[I, I] = 1.0e0

    KDEG = 4
    N = KDEG + 1
    A[1, 1] = NL * 1.0e0
    PRFL = DATA_MESH.PRFL
    SP = DATA_MESH.SP
    BW = DATA_FORC.BW
    for I in range(1, NL+1):
        DTY[I] = -PRFL[IK + I, 5]
        DTX[I] = (I - 1) * SP - 0.5e0 * BW

    for J in range(2, N+1):
        for I in range(1, NL+1):
            A[1, J] = A[1, J] + DTX[I] ** (J - 1)
            A[J, N] = A[J, N] + DTX[I] ** (N + J - 2)

    for J in range(1, NL+1):
        A[1, N + 1] = A[1, N + 1] + DTY[J]

    for I in range(2, N+1):
        for J in range(1, NL+1):
            A[I, N + 1] = A[I, N + 1] + DTY[J] * (DTX[J] ** (I - 1))

    for I in range(2, N+1):
        for J in range(1, I - 1+1):
            A[J + 1, I - J] = A[1, I]
            A[N + 1 - I + J, N - J] = A[N + 1 - I, N]

    for I in range(1, N+1):
        if I != N:
            MAX = abs(A[I, I])
            IMAX = I
            for J in range(I+1, N+1):
                AA = abs(A[J, I])
                if MAX < AA: MAX = AA
                if MAX < AA: IMAX = J
            if IMAX != I:
                for J in range(1, N+1+1):
                    AA = A[I, J]
                    A[I, J] = A[IMAX, J]
                    A[IMAX, J] = AA

        P = A[I, I]
        for J in range(I+1, N + 1+1):
            A[I, J] = A[I, J] / P

        for J in range(1, N+1):
            if A[J, I] == 0.0e0 and J == I: continue
            if A[J, I] != 0.0e0 and J == I: continue
            if A[J, I] == 0.0e0 and J != I: continue

            P = A[J, I]
            for K in range(I+1, N + 1+1):
                A[J, K] = A[J, K] - P * A[I, K]

    DATA_SHAP.PHCW = 0.25e0 * A[3, KDEG + 2] * BW * BW
    DATA_SHAP.PHCQ = 3.0e0 * A[5, KDEG + 2] * (BW ** 4) / 256.0e0


def POSTPROC():
    INB = DATA_MESH.INB
    INI = DATA_MESH.INI
    INC = DATA_MESH.INC
    for I in range(1, INI+1):
        for J in range(1, 10+1):
            DATA_MESH.RDT[I, J] = 0.0e0

    DATA_MESH.RDT[1, 1] = DATA_MESH.RDS[INC[1], 1]
    DATA_MESH.RDT[INI, 1] = DATA_MESH.RDS[INC[2], 1]

    DATA_MESH.RDT[1, 2] = DATA_MESH.RDS[INC[3], 2]
    DATA_MESH.RDT[int((INI - 1) / 2), 2] = DATA_MESH.RDS[INC[4], 2]
    DATA_MESH.RDT[INI, 2] = DATA_MESH.RDS[INC[5], 2]

    NSBRD = DATA_MESH.NSBRD
    for I in range(1, INB+1):
        DATA_MESH.RDT[I, 3] = DATA_MESH.RDS[NSBRD + I - 1, 1]

    NSIRT = DATA_MESH.NSIRT
    NSIRD = DATA_MESH.NSIRD
    for I in range(1, INI+1):
        DATA_MESH.RDT[I, 4] = DATA_MESH.RDS[NSIRT + I - 1, 1]
        DATA_MESH.RDT[I, 5] = DATA_MESH.RDS[NSIRD + I - 1, 1]

    INW = DATA_MESH.INW
    NSWRT = DATA_MESH.NSWRT
    NSWRD = DATA_MESH.NSWRD
    for I in range(1, INW+1):
        DATA_MESH.RDT[I, 6] = DATA_MESH.RDS[NSWRT + I - 1, 1]
        DATA_MESH.RDT[I, 7] = DATA_MESH.RDS[NSWRD + I - 1, 1]

    SP = DATA_MESH.SP
    for I in range(1, INB+1):
        DATA_MESH.RDT[I, 8] = DATA_MESH.RDT[I, 3] / SP

    DATA_SHAP.QBI = -1000.0

    for I in range(1, INB+1):
        if DATA_SHAP.QBI < DATA_MESH.RDT[I, 8]:
            DATA_SHAP.QBI = DATA_MESH.RDT[I, 8]
            DATA_MESH.NYBI = I

    SUM = 0.0
    for I in range(1, INB+1):
        SUM = SUM + DATA_MESH.RDT[I, 8]

    CNBI = DATA_MESH.CNBI
    SUM = SUM / CNBI
    DATA_SHAP.QBI = DATA_SHAP.QBI / SUM

    for I in range(1, INI+1):
        DATA_MESH.RDT[I, 9] = DATA_MESH.RDT[I, 5] / SP

    DATA_SHAP.QIW = -1000.0
    for I in range(1, INI+1):
        if DATA_SHAP.QIW < DATA_MESH.RDT[I, 9]:
            DATA_SHAP.QIW = DATA_MESH.RDT[I, 9]
            DATA_MESH.NYIW = I

    SUM = 0.0
    for I in range(1, INI+1):
        SUM = SUM + DATA_MESH.RDT[I, 9]

    CNIW = DATA_MESH.CNIW
    SUM = SUM / CNIW
    DATA_SHAP.QIW = DATA_SHAP.QIW / SUM

    for I in range(1, INW+1):
        DATA_MESH.RDT[I, 10] = DATA_MESH.RDT[I, 7] / SP

    for I in range(1, 9+1):
        DATA_MESH.RSX[I] = 0.0

    for I in range(1, 7+1):
        for J in range(1, INI+1):
            DATA_MESH.RSX[I] = DATA_MESH.RSX[I] + DATA_MESH.RDT[J, I]

    NP = DATA_MESH.NP
    for I in range(1, NP+1):
        DATA_MESH.RSX[8] = DATA_MESH.RSX[8] + DATA_MESH.RDS[I, 1]
        DATA_MESH.RSX[9] = DATA_MESH.RSX[9] + DATA_MESH.RDS[I, 2]

    for I in range(1, INI+1):
        for J in range(1, 7+1):
            DATA_MESH.PRFL[I, J] = 0.0e0

    DP = DATA_MESH.DP
    DW = DATA_ROLL.DW
    DI = DATA_ROLL.DI
    X = DATA_MESH.X
    for I in range(1, INB+1):
        DATA_MESH.PRFL[I, 1] = X[NSBRD + I - 1] + DP[NSBRD + I - 1, 1] - DW - DI

    for I in range(1, INI+1):
        DATA_MESH.PRFL[I, 8] = X[NSIRT + I - 1] + DP[NSIRT + I - 1, 1] - DW - DI

    for I in range(1, INI+1):
        DATA_MESH.PRFL[I, 9] = X[NSIRD + I - 1] + DP[NSIRD + I - 1, 1] - DW

    for I in range(1, INW+1):
        DATA_MESH.PRFL[I, 2] = X[NSWRT + I - 1] + DP[NSWRT + I - 1, 1] - DW

    for I in range(1, INW+1):
        DATA_MESH.PRFL[I, 3] = X[NSWRD + I - 1] + DP[NSWRD + I - 1, 1]

    KSFTW = DATA_MESH.KSFTW
    KOFF = DATA_MESH.KOFF
    NCTR = int((INW + 1) / 2) + KSFTW - KOFF
    CWC = DATA_MESH.PRFL[NCTR, 3]
    for I in range(1, INW+1):
        DATA_MESH.PRFL[I, 4] = -(CWC - DATA_MESH.PRFL[I, 3]) * 1000.0e0

    for I in range(1, INW+1):
        DATA_MESH.PRFL[I, 7] = -DATA_MESH.PRFL[INW + 1 - I, 4]

    NL = DATA_MESH.NL
    IK = NCTR - int((NL + 1) / 2)
    for I in range(1, NL+1):
        DATA_MESH.PRFL[IK + I, 5] = DATA_MESH.PRFL[IK + I, 4] + DATA_MESH.PRFL[IK + NL + 1 - I, 4]

    COEF = (2 * SP - 25) / SP
    DATA_SHAP.CW = -(COEF * DATA_MESH.PRFL[IK + 2, 5] + (1 - COEF) * DATA_MESH.PRFL[IK + 3, 5])
    DATA_SHAP.WDG = DATA_MESH.PRFL[IK + 2, 5] - DATA_MESH.PRFL[IK + NL - 1, 5]

    COEF = (6 * SP - 100) / SP

    DATA_SHAP.EDG = COEF * DATA_MESH.PRFL[IK + 5, 5] + (1 - COEF) * DATA_MESH.PRFL[IK + 6, 5] - DATA_MESH.PRFL[IK + 1, 5]

    BW = DATA_FORC.BW
    DATA_FORC.TPG = DATA_SHAP.WDG / BW

    TF1 = DATA_MESH.PRFL[1, 4]
    TF2 = DATA_MESH.PRFL[1, 7]
    for I in range(1, INW+1):
        DATA_MESH.PRFL[I, 4] = DATA_MESH.PRFL[I, 4] - TF1
        DATA_MESH.PRFL[I, 7] = DATA_MESH.PRFL[I, 7] - TF2
    REGR(IK)

    J = int((INW + 1) / 2) - int((NL + 1) / 2)
    for I in range(1, NL+1):
        DATA_MESH.PRFL[J + I, 6] = DATA_MESH.PRFL[IK + I, 5]

