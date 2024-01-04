import math

import numpy as np

from . import DATA_FORC
from . import DATA_MESH

ME = np.zeros(3 + 1, dtype=np.int32)
B = np.zeros(3 + 1, dtype=np.float64)
C = np.zeros(3 + 1, dtype=np.float64)
F = np.zeros(6000 + 1, dtype=np.float64)
QK = np.zeros(650000 + 1, dtype=np.float64)
S0: float = 0
IDX: int = 0


def DIV(N):
    global ME
    ME[1] = DATA_MESH.MS[N, 1]
    ME[2] = DATA_MESH.MS[N, 2]
    ME[3] = DATA_MESH.MS[N, 3]


def BCS():
    global IDX
    global ME
    global B
    global C
    global S0
    X = DATA_MESH.X
    Y = DATA_MESH.Y
    B = np.zeros(3 + 1)
    C = np.zeros(3 + 1)
    I = ME[1]
    J = ME[2]
    M = ME[3]
    B[1] = Y[J] - Y[M]
    B[2] = Y[M] - Y[I]
    B[3] = Y[I] - Y[J]
    C[1] = X[M] - X[J]
    C[2] = X[I] - X[M]
    C[3] = X[J] - X[I]
    S0 = (B[2] * C[3] - B[3] * C[2]) / 2
    if S0 < 0.0e0: IDX = -1


def RFS(N):
    global ME
    global B
    global C
    global S0
    HH = np.zeros((6 + 1, 6 + 1))
    Q = np.zeros(6 + 1)
    QH = np.zeros(6 + 1)

    DIV(N)
    BCS()

    E0 = 21.0e0
    V0 = 0.3e0
    ET1 = DATA_MESH.TH[N] * E0 / S0 / (1.0e0 - V0 * V0) / 4.0e0
    V1 = (1.0e0 - V0) / 2.0e0

    IR1 = 0
    for NIR in range(1, 3 + 1):
        IR1 = IR1 + 1
        IS1 = 0
        for NIS in range(1, 3 + 1):
            IS = ME[NIS]
            IS1 = IS1 + 1
            BRBS = B[IR1] * B[IS1]
            BRCS = B[IR1] * C[IS1]
            CRBS = C[IR1] * B[IS1]
            CRCS = C[IR1] * C[IS1]
            HH[2 * IR1 - 1, 2 * IS1 - 1] = ET1 * (BRBS + V1 * CRCS)
            HH[2 * IR1 - 1, 2 * IS1] = ET1 * (V0 * BRCS + V1 * CRBS)
            HH[2 * IR1, 2 * IS1 - 1] = ET1 * (V0 * CRBS + V1 * BRCS)
            HH[2 * IR1, 2 * IS1] = ET1 * (CRCS + V1 * BRBS)

    IP = ME[1]
    JP = ME[2]
    MP = ME[3]
    for KK in range(1, 6 + 1):
        QH[1] = HH[KK, 1] * DATA_MESH.DP[IP, 1]
        QH[2] = HH[KK, 2] * DATA_MESH.DP[IP, 2]
        QH[3] = HH[KK, 3] * DATA_MESH.DP[JP, 1]
        QH[4] = HH[KK, 4] * DATA_MESH.DP[JP, 2]
        QH[5] = HH[KK, 5] * DATA_MESH.DP[MP, 1]
        QH[6] = HH[KK, 6] * DATA_MESH.DP[MP, 2]
        Q[KK] = QH[1] + QH[2] + QH[3] + QH[4] + QH[5] + QH[6]
    DATA_MESH.RDS[IP, 1] = DATA_MESH.RDS[IP, 1] + Q[1]
    DATA_MESH.RDS[IP, 2] = DATA_MESH.RDS[IP, 2] + Q[2]
    DATA_MESH.RDS[JP, 1] = DATA_MESH.RDS[JP, 1] + Q[3]
    DATA_MESH.RDS[JP, 2] = DATA_MESH.RDS[JP, 2] + Q[4]
    DATA_MESH.RDS[MP, 1] = DATA_MESH.RDS[MP, 1] + Q[5]
    DATA_MESH.RDS[MP, 2] = DATA_MESH.RDS[MP, 2] + Q[6]


def QKS(N, NGB):
    global ME
    global B
    global C
    global S0
    global F
    global QK
    global GP
    global IGPN
    global ICP
    global IDGL

    H = np.zeros((2 + 1, 2 + 1))
    NP = DATA_MESH.NP
    DIV(N)
    BCS()
    E0 = 21.0e0
    V0 = 0.3e0
    TH = DATA_MESH.TH
    ET1 = TH[N] * E0 / S0 / (1.0e0 - V0 * V0) / 4.0e0
    V1 = (1.0e0 - V0) / 2.0e0
    IR1 = 0
    for NIR in range(1, 3 + 1):
        IR = ME[NIR]
        IR1 = IR1 + 1
        IS1 = 0
        for NIS in range(1, 3 + 1):
            IS = ME[NIS]
            IS1 = IS1 + 1
            BRBS = B[IR1] * B[IS1]
            BRCS = B[IR1] * C[IS1]
            CRBS = C[IR1] * B[IS1]
            CRCS = C[IR1] * C[IS1]
            H[1, 1] = ET1 * (BRBS + V1 * CRCS)
            H[1, 2] = ET1 * (V0 * BRCS + V1 * CRBS)
            H[2, 1] = ET1 * (V0 * CRBS + V1 * BRCS)
            H[2, 2] = ET1 * (CRCS + V1 * BRBS)
            ICPS = ICP[IS, 1]
            if ICPS < 0:
                for IG in range(1, NGB + 1):
                    if abs(IS - IGPN[IG]) > 0: continue
                    NGP = IG
                    break

                for KK in range(1, 2 + 1):
                    IBB = abs(ICP[IR, KK])
                    if IBB > 0: F[IBB] = F[IBB] + H[KK, 1] * GP[NGP]

            for KK in range(1, 2 + 1):
                ICPR = abs(ICP[IR, KK])
                if ICPR == 0: continue
                for JJ in range(1, 2 + 1):
                    NN = abs(ICP[IS, JJ])
                    if NN == 0: continue
                    if ICPR < NN: continue
                    NQ = IDGL[ICPR] - (ICPR - NN)
                    QK[NQ] = QK[NQ] + H[KK, JJ]


def EQS(NEQ, LMAX):
    global F
    global QK
    global IDGL
    for I in range(2, NEQ + 1):
        IS = IDGL[I] - I
        IR = IDGL[I - 1] - IS + 1
        for J in range(IR + 1, I + 1):
            IT = IDGL[J] - J
            IE = IDGL[J - 1] - IT + 1
            if IR > IE: IE = IR
            IG = IS + J
            if J - 1 < IE: continue
            for IP in range(IE, J - 1 + 1):
                IQ = IDGL[IP]
                QK[IG] = QK[IG] - QK[IS + IP] / QK[IQ] * QK[IT + IP]

    F[1] = F[1] / QK[1]
    for I in range(2, NEQ + 1):
        Q = F[I]
        IZ = IDGL[I]
        IS = IZ - I
        IE = IDGL[I - 1] - IS + 1
        if I - 1 >= IE:
            for IP in range(IE, I - 1 + 1):
                Q = Q - QK[IS + IP] * F[IP]
        F[I] = Q / QK[IZ]

    for KK in range(1, NEQ - 1 + 1):
        I = NEQ - KK
        IZ = IDGL[I]
        JT = I + LMAX - 1
        if JT > NEQ: JT = NEQ
        Q = 0.0e0
        for IP in range(I + 1, JT + 1):
            IG = IDGL[IP] - IP + I
            if IDGL[IP - 1] - IG < 0: Q = Q + QK[IG] * F[IP]
        F[I] = F[I] - Q / QK[IZ]


def XTM(AA, M, ID):
    if ID < 0:
        XMM = 1.0e10
        for I in range(1, M + 1):
            if AA[I] < XMM:
                XMM = AA[I]
    else:
        XMM = -1.0e10
        for I in range(1, M + 1):
            if AA[I] > XMM:
                XMM = AA[I]
    return XMM


ND = np.zeros(6 + 1, dtype=np.int32)

IDGL = np.zeros(5800 + 1, dtype=np.int32)
IGPN = np.zeros(200 + 1, dtype=np.int32)
KGPN = np.zeros(200 + 1, dtype=np.int32)
IHY = np.zeros(200 + 1, dtype=np.int32)
GP = np.zeros(200 + 1)
GGP = np.zeros(100 + 1)
FF = np.zeros(200 + 1)
IFJI = np.zeros(2 + 1, dtype=np.int32)
IFJW = np.zeros(2 + 1, dtype=np.int32)


def ROLLFEM():
    global ME
    global B
    global C
    global F
    global QK
    global S0
    global IDX
    global ND
    global ICP
    global IDGL
    global IGPN
    global KGPN
    global IHY
    global GP
    global GGP
    global FF
    global IFJI
    global IFJW

    NP = DATA_MESH.NP
    ICP = np.zeros((DATA_MESH.NP + 1 + 1, 2 + 1), dtype=np.int32)
    NB = 2
    INB = DATA_MESH.INB
    INI = DATA_MESH.INI
    INW = DATA_MESH.INW
    NPBR = DATA_MESH.NPBR
    SP = DATA_MESH.SP
    BW = DATA_FORC.BW
    KSFTI = DATA_MESH.KSFTI
    KSFTW = DATA_MESH.KSFTW
    NPIR = DATA_MESH.NPIR

    NPM = NP - int((INW - 1) / 2)
    IFJI[1] = NPBR + 4 * INI + 54
    IFJI[2] = NPBR + 4 * INI + int((INI - 1) / 4) + 62
    IFJW[1] = NPBR + NPIR + 4 * INW + 54
    IFJW[2] = NPBR + NPIR + 4 * INW + int((INW - 1) / 4) + 62

    KCHAMF = 0
    DATA_MESH.NL = int(BW / 2 / SP + 0.5) * 2 + 1
    DATA_FORC.BW = (DATA_MESH.NL - 1) * SP
    BW = DATA_FORC.BW
    DATA_FORC.PS = 1.0 - 1.0 / (DATA_MESH.NL * 1.0)

    NPBI = int((INI - INB) / 2)
    if (NPBI - abs(KSFTI)) < 0:
        DATA_MESH.CNBI = INB + NPBI - abs(KSFTI)
    else:
        DATA_MESH.CNBI = INB

    NPIW = int((INW - INI) / 2)
    if KSFTI * KSFTW < 0:
        if INI <= INW:
            if NPIW - abs(KSFTI) - abs(KSFTW) < 0:
                DATA_MESH.CNIW = INI + NPIW - abs(KSFTI) - abs(KSFTW)
            else:
                DATA_MESH.CNIW = INI
        else:
            if abs(NPIW) - abs(KSFTI) - abs(KSFTW) < 0:
                DATA_MESH.CNIW = INW + abs(NPIW) - abs(KSFTI) - abs(KSFTW)
            else:
                DATA_MESH.CNIW = INW
    else:
        if INI <= INW:
            if NPIW - abs(KSFTI - KSFTW) < 0:
                DATA_MESH.CNIW = INI + NPIW - abs(KSFTI - KSFTW)
            else:
                DATA_MESH.CNIW = INI
        else:
            if abs(NPIW) - abs(KSFTI - KSFTW) < 0:
                DATA_MESH.CNIW = INW + abs(NPIW) - abs(KSFTI - KSFTW)
            else:
                DATA_MESH.CNIW = INW

    NSBRD = DATA_MESH.NSBRD
    CNBI = DATA_MESH.CNBI
    NSIRT = DATA_MESH.NSIRT
    if (NPBI + KSFTI) <= 0:
        for N in range(1, CNBI + 1):
            IGPN[N] = NSBRD - (NPBI + KSFTI) + N - 1
            KGPN[N] = NSIRT + N - 1
    else:
        for N in range(1, CNBI + 1):
            IGPN[N] = NSBRD + N - 1
            KGPN[N] = NSIRT + (NPBI + KSFTI) + N - 1

    for N in range(1, CNBI + 1):
        GP[N] = DATA_MESH.X[IGPN[N]] - DATA_MESH.X[KGPN[N]]

    CNIW = DATA_MESH.CNIW
    NSIRD = DATA_MESH.NSIRD
    NSWRT = DATA_MESH.NSWRT
    if (NPIW - KSFTI + KSFTW) <= 0:
        for N in range(1, CNIW + 1):
            IGPN[CNBI + N] = NSIRD - (NPIW - KSFTI + KSFTW) + N - 1
            KGPN[CNBI + N] = NSWRT + N - 1
    else:
        for N in range(1, CNIW + 1):
            IGPN[CNBI + N] = NSIRD + N - 1
            KGPN[CNBI + N] = NSWRT + (NPIW - KSFTI + KSFTW) + N - 1

    for N in range(1, CNIW + 1):
        GP[CNBI + N] = DATA_MESH.X[IGPN[CNBI + N]] - DATA_MESH.X[KGPN[CNBI + N]]
        GGP[N] = GP[CNBI + N]

    VGP = XTM(GP, CNBI, -1)

    for N in range(1, INI + 1):
        DATA_MESH.X[NSIRT - 1 + N] = DATA_MESH.X[NSIRT - 1 + N] + VGP

    VGP = XTM(GGP, CNIW, -1)

    for N in range(1, INW + 1):
        DATA_MESH.X[NSWRT - 1 + N] = DATA_MESH.X[NSWRT - 1 + N] + VGP

    NG = CNIW + CNBI
    for I in range(1, NG + 1):
        GP[I] = DATA_MESH.X[IGPN[I]] - DATA_MESH.X[KGPN[I]]

    INC = DATA_MESH.INC
    for I in range(1, NB + 1):
        GP[NG + I] = 0.0e0
        IGPN[NG + I] = INC[I]

    NP1 = NP + 1
    for I in range(1, NG + 1):
        IHY[I] = NP1
    IH = 1

    while True:
        for I in range(1, NP1 + 1):
            for J in range(1, 2 + 1):
                ICP[I, J] = 1

        for I in range(1, NB + 1):
            ICP[INC[I], 1] = 0

        ICP[INC[NB + 1], 2] = 0
        ICP[INC[NB + 2], 2] = 0
        ICP[INC[NB + 3], 2] = 0
        for N in range(1, NG + 1):
            ICP[IGPN[N], 1] = 0

        for I in range(1, NG + 1):
            for J in range(1, 2 + 1):
                ICP[IHY[I], J] = 1

        NEQ = 0
        for I in range(1, NP + 1):
            for J in range(1, 2 + 1):
                if ICP[I, J] >= 0.5:
                    NEQ = NEQ + 1
                    ICP[I, J] = NEQ

        for I in range(1, NG + 1):
            for J in range(1, 2 + 1):
                if ICP[IGPN[I], J] < 1: ICP[IGPN[I], J] = -ICP[KGPN[I], J]

        for I in range(1, NEQ + 1):
            IDGL[I] = I + 1
        NE = DATA_MESH.NE
        MS = DATA_MESH.MS
        for N in range(1, NE + 1):
            IA = MS[N, 1]
            JA = MS[N, 2]
            MA = MS[N, 3]
            ND[1] = abs(ICP[IA, 1])
            ND[2] = abs(ICP[IA, 2])
            ND[3] = abs(ICP[JA, 1])
            ND[4] = abs(ICP[JA, 2])
            ND[5] = abs(ICP[MA, 1])
            ND[6] = abs(ICP[MA, 2])
            KS = NEQ
            for KK in range(1, 6 + 1):
                if (ND[KK] > 0) and (ND[KK] < KS): KS = ND[KK]
            for KK in range(1, 6 + 1):
                ICPR = ND[KK]
                if ICPR == 0: continue
                if IDGL[ICPR] > KS: IDGL[ICPR] = KS

        LMAX = 0
        IDGL[1] = 1
        for I in range(2, NEQ + 1):
            LBD = I - IDGL[I] + 1
            IDGL[I] = IDGL[I - 1] + LBD
            if LBD > LMAX: LMAX = LBD
        NKK = IDGL[NEQ]

        for I in range(1, NEQ + 1):
            F[I] = 0.0e0

        NSK = int((DATA_MESH.NL + 1) / 2)
        NM = int((DATA_MESH.NL - 1) / 2)

        PS = DATA_FORC.PS
        QS = DATA_FORC.QS
        kforce = 1.000
        FF[NSK] = PS * QS * SP * kforce

        QM1 = 3 * NM * 1.0e0
        QM2 = (NM + 1) * 1.0e0
        QM3 = (2 * NM + 1) * 1.0e0
        QM = QM1 / QM2 / QM3

        FDLT = PS * QS * SP * (kforce - 1.0e0) * 3.0e0 * (NM * 1.0e0) / (NSK * 1.0e0)

        SSQ = NM * NM * 1.0e0
        for K in range(1, NM + 1):
            FF[NSK - K] = FF[NSK] - FDLT * K * K * 1.0e0 / SSQ
            FF[NSK + K] = FF[NSK - K]

        KOFF = DATA_MESH.KOFF
        for K in range(1, DATA_MESH.NL + 1):
            F[ICP[NPM + KSFTW - NSK - KOFF + K, 1]] = FF[K]

        BFI = DATA_FORC.BFI
        BFW = DATA_FORC.BFW
        F[ICP[IFJI[1], 1]] = BFI
        F[ICP[IFJI[2], 1]] = BFI
        F[ICP[IFJW[1], 1]] = BFW
        F[ICP[IFJW[2], 1]] = BFW

        for I in range(1, NKK + 1):
            QK[I] = 0.0e0

        NGB = NG + NB
        S0 = 0
        IDX = 0
        for N in range(1, NE + 1):
            QKS(N, NGB)
        if IDX < 0: return

        EQS(NEQ, LMAX)
        for I in range(1, NP + 1):
            for J in range(1, 2 + 1):
                DATA_MESH.DP[I, J] = 0.0e0

        for K in range(1, NP + 1):
            ICPX = ICP[K, 1]
            ICPY = ICP[K, 2]
            if ICPX > 0: DATA_MESH.DP[K, 1] = F[ICPX]
            if ICPY > 0: DATA_MESH.DP[K, 2] = F[ICPY]

        for K in range(1, NG + 1):
            if ICP[IGPN[K], 1] < 0: DATA_MESH.DP[IGPN[K], 1] = DATA_MESH.DP[KGPN[K], 1] - GP[K]
            if ICP[IGPN[K], 2] < 0: DATA_MESH.DP[IGPN[K], 2] = DATA_MESH.DP[KGPN[K], 2]

        for I in range(1, NP + 1):
            for J in range(1, 2 + 1):
                DATA_MESH.RDS[I, J] = 0.0e0

        for N in range(1, NE + 1):
            RFS(N)

        IHX = 10
        IY = 0
        DV1 = -0.1e0
        for K in range(1, NG + 1):
            if IHY[K] < NP1: continue
            if DATA_MESH.RDS[IGPN[K], 1] > DV1: continue
            IY = 2
            IHY[K] = IGPN[K]

        IZ = 0
        DV2 = 0.001e0
        for K in range(1, NG + 1):
            if IHY[K] > NP: continue
            if DATA_MESH.DP[KGPN[K], 1] < DATA_MESH.DP[IHY[K], 1] + GP[K] + DV2: continue
            IZ = 2
            IHY[K] = NP1

        if IY < 1 and IZ < 1: return
        IH = IH + 1
        if IH > IHX: return
