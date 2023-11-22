import DATA_ROLL
import DATA_MESH
import DATA_FORC
import numpy as np
import math

IXB = np.array([0, 15, 65, 70, 100, 235, 300, 300, 235, 100, 70, 65, 15], dtype=np.float64)
IXI = np.array([0, 10, 15, 25, 40, 140, 170, 170, 140, 40, 25, 15, 10], dtype=np.float64)
IXW = np.array([0, 10, 15, 20, 40, 135, 160, 160, 135, 40, 20, 15, 10], dtype=np.float64)


def MES():
    IDP = np.zeros(48 + 1, dtype=np.int32)
    IDQ = np.zeros(48 + 1, dtype=np.int32)
    IVP = np.zeros(24 + 1, dtype=np.int32)
    IVQ = np.zeros(24 + 1, dtype=np.int32)
    IDE = np.zeros(48 + 1, dtype=np.int32)
    IDN = np.zeros(48 + 1, dtype=np.int32)
    IVE = np.zeros(24 + 1, dtype=np.int32)
    IVN = np.zeros(24 + 1, dtype=np.int32)
    I: int = 0
    JP: int = 0
    JQ: int = 0
    N: int = 0
    INB = DATA_MESH.INB
    IDP[1] = 1
    IDP[2] = 2 * INB + 1
    IDP[3] = 3 * INB + 10
    IDP[4] = 3 * INB + (INB - 1) / 4 + 21
    IDP[5] = 3 * INB + (INB - 1) / 2 + (INB - 1) / 4 / 2 + 37
    IDP[6] = 3 * INB + 3 * (INB - 1) / 4 + (INB - 1) / 4 / 2 + 48
    IDP[7] = 4 * INB + (INB - 1) / 2 + 68
    IDP[8] = 5 * INB + (INB - 1) / 2 + (INB - 1) / 4 + 73
    DATA_MESH.NPBR = 7 * INB + int((INB - 1) / 4) + 72
    NPBR = DATA_MESH.NPBR
    INI = DATA_MESH.INI
    IDP[9] = NPBR + 1
    IDP[10] = NPBR + 2 * INI + 1
    IDP[11] = NPBR + 3 * INI + 10
    IDP[12] = NPBR + 3 * INI + (INI - 1) / 4 + 21
    IDP[13] = NPBR + 3 * INI + (INI - 1) / 2 + (INI - 1) / 4 / 2 + 37
    IDP[14] = NPBR + 3 * INI + 3 * (INI - 1) / 4 + (INI - 1) / 4 / 2 + 48
    IDP[15] = NPBR + 4 * INI + (INI - 1) / 2 + 68
    IDP[16] = NPBR + 5 * INI + (INI - 1) / 2 + (INI - 1) / 4 + 73
    DATA_MESH.NPIR = 7 * INI + int((INI - 1) / 4) + 72
    NPIR = DATA_MESH.NPIR
    INW = DATA_MESH.INW
    IDP[17] = NPBR + NPIR + 1
    IDP[18] = NPBR + NPIR + 2 * INW + 1
    IDP[19] = NPBR + NPIR + 3 * INW + 10
    IDP[20] = NPBR + NPIR + 3 * INW + (INW - 1) / 4 + 21
    IDP[21] = NPBR + NPIR + 3 * INW + (INW - 1) / 2 + (INW - 1) / 4 / 2 + 37
    IDP[22] = NPBR + NPIR + 3 * INW + 3 * (INW - 1) / 4 + (INW - 1) / 4 / 2 + 48
    IDP[23] = NPBR + NPIR + 4 * INW + (INW - 1) / 2 + 68
    IDP[24] = NPBR + NPIR + 5 * INW + (INW - 1) / 2 + (INW - 1) / 4 + 73
    DATA_MESH.NPWR = 7 * INW + int((INW - 1) / 4) + 72
    NPWR = DATA_MESH.NPWR
    IDP[25] = 3 * INB + (INB - 1) / 2 + 32
    IDP[26] = 3 * INB + 3 * (INB - 1) / 4 + 43
    IDP[27] = 4 * INB + (INB - 1) / 4 + 68
    IDP[28] = 5 * INB + (INB - 1) / 4 + 73
    IDP[29] = (INB - 1) / 2 + 1
    IDP[30] = 2 * INB + (INB - 1) / 4 + 1
    IDP[31] = 3 * INB + (INB - 1) / 8 + 15
    IDP[32] = 3 * INB + (INB - 1) / 4 + (INB - 1) / 8 + 26
    IDP[33] = NPBR + 3 * INI + (INI - 1) / 2 + 32
    IDP[34] = NPBR + 3 * INI + 3 * (INI - 1) / 4 + 43
    IDP[35] = NPBR + 4 * INI + (INI - 1) / 4 + 68
    IDP[36] = NPBR + 5 * INI + (INI - 1) / 4 + 73
    IDP[37] = NPBR + (INI - 1) / 2 + 1
    IDP[38] = NPBR + 2 * INI + (INI - 1) / 4 + 1
    IDP[39] = NPBR + 3 * INI + (INI - 1) / 8 + 15
    IDP[40] = NPBR + 3 * INI + (INI - 1) / 4 + (INI - 1) / 8 + 26
    IDP[41] = NPBR + NPIR + 3 * INW + (INW - 1) / 2 + 32
    IDP[42] = NPBR + NPIR + 3 * INW + 3 * (INW - 1) / 4 + 43
    IDP[43] = NPBR + NPIR + 4 * INW + (INW - 1) / 4 + 68
    IDP[44] = NPBR + NPIR + 5 * INW + (INW - 1) / 4 + 73
    IDP[45] = NPBR + NPIR + (INW - 1) / 2 + 1
    IDP[46] = NPBR + NPIR + 2 * INW + (INW - 1) / 4 + 1
    IDP[47] = NPBR + NPIR + 3 * INW + (INW - 1) / 8 + 15
    IDP[48] = NPBR + NPIR + 3 * INW + (INW - 1) / 4 + (INW - 1) / 8 + 26

    IDQ[1] = IDP[1] + INB
    IDQ[2] = IDP[2] + (INB - 1) / 2 + 5
    IDQ[3] = IDP[3] + (INB - 1) / 4 + 11
    IDQ[4] = IDP[4] + (INB - 1) / 4 + 11
    IDQ[5] = IDP[5] + (INB - 1) / 4 + 11
    IDQ[6] = IDP[6] + (INB - 1) / 4 + 11
    IDQ[7] = IDP[7] + (INB - 1) / 2 + 5
    IDQ[8] = IDP[8] + INB
    IDQ[9] = IDP[9] + INI
    IDQ[10] = IDP[10] + (INI - 1) / 2 + 5
    IDQ[11] = IDP[11] + (INI - 1) / 4 + 11
    IDQ[12] = IDP[12] + (INI - 1) / 4 + 11
    IDQ[13] = IDP[13] + (INI - 1) / 4 + 11
    IDQ[14] = IDP[14] + (INI - 1) / 4 + 11
    IDQ[15] = IDP[15] + (INI - 1) / 2 + 5
    IDQ[16] = IDP[16] + INI
    IDQ[17] = IDP[17] + INW
    IDQ[18] = IDP[18] + (INW - 1) / 2 + 5
    IDQ[19] = IDP[19] + (INW - 1) / 4 + 11
    IDQ[20] = IDP[20] + (INW - 1) / 4 + 11
    IDQ[21] = IDP[21] + (INW - 1) / 4 + 11
    IDQ[22] = IDP[22] + (INW - 1) / 4 + 11
    IDQ[23] = IDP[23] + (INW - 1) / 2 + 5
    IDQ[24] = IDP[24] + INW
    IDQ[25] = IDP[25] + (INB - 1) / 4 + 11
    IDQ[26] = IDP[26] + (INB - 1) / 4 + 11
    IDQ[27] = IDP[27] + (INB - 1) / 2 + 5
    IDQ[28] = IDP[28] + INB
    IDQ[29] = IDP[29] + INB
    IDQ[30] = IDP[30] + (INB - 1) / 2 + 5
    IDQ[31] = IDP[31] + (INB - 1) / 4 + 11
    IDQ[32] = IDP[32] + (INB - 1) / 4 + 11
    IDQ[33] = IDP[33] + (INI - 1) / 4 + 11
    IDQ[34] = IDP[34] + (INI - 1) / 4 + 11
    IDQ[35] = IDP[35] + (INI - 1) / 2 + 5
    IDQ[36] = IDP[36] + INI
    IDQ[37] = IDP[37] + INI
    IDQ[38] = IDP[38] + (INI - 1) / 2 + 5
    IDQ[39] = IDP[39] + (INI - 1) / 4 + 11
    IDQ[40] = IDP[40] + (INI - 1) / 4 + 11
    IDQ[41] = IDP[41] + (INW - 1) / 4 + 11
    IDQ[42] = IDP[42] + (INW - 1) / 4 + 11
    IDQ[43] = IDP[43] + (INW - 1) / 2 + 5
    IDQ[44] = IDP[44] + INW
    IDQ[45] = IDP[45] + INW
    IDQ[46] = IDP[46] + (INW - 1) / 2 + 5
    IDQ[47] = IDP[47] + (INW - 1) / 4 + 11
    IDQ[48] = IDP[48] + (INW - 1) / 4 + 11

    IVP[1] = INB + 1
    IVP[2] = 2 * INB + (INB - 1) / 2 + 2
    IVP[3] = IVP[1] + (INB - 1) / 2
    IVP[4] = IVP[2] + (INB - 1) / 4 + 4
    IVP[5] = NPBR + INI + 1
    IVP[6] = NPBR + 2 * INI + (INI - 1) / 2 + 2
    IVP[7] = IVP[5] + (INI - 1) / 2
    IVP[8] = IVP[6] + (INI - 1) / 4 + 4
    IVP[9] = NPBR + NPIR + INW + 1
    IVP[10] = NPBR + NPIR + 2 * INW + (INW - 1) / 2 + 2
    IVP[11] = IVP[9] + (INW - 1) / 2
    IVP[12] = IVP[10] + (INW - 1) / 4 + 4
    IVP[13] = 4 * INB + 56
    IVP[14] = 4 * INB + 3 * (INB - 1) / 4 + 73
    IVP[15] = IVP[13] + (INB - 1) / 8 + 2
    IVP[16] = IVP[14] + (INB - 1) / 4
    IVP[17] = NPBR + 4 * INI + 56
    IVP[18] = NPBR + 4 * INI + 3 * (INI - 1) / 4 + 73
    IVP[19] = IVP[17] + (INI - 1) / 8 + 2
    IVP[20] = IVP[18] + (INI - 1) / 4
    IVP[21] = NPBR + NPIR + 4 * INW + 56
    IVP[22] = NPBR + NPIR + 4 * INW + 3 * (INW - 1) / 4 + 73
    IVP[23] = IVP[21] + (INW - 1) / 8 + 2
    IVP[24] = IVP[22] + (INW - 1) / 4

    IVQ[1] = IVP[1] + INB
    IVQ[2] = IVP[2] + (INB - 1) / 2 + 12
    IVQ[3] = IVP[3] + 3 * (INB - 1) / 4 + 1
    IVQ[4] = IVP[4] + (INB - 1) / 4 + (INB - 1) / 8 + 10
    IVQ[5] = IVP[5] + INI
    IVQ[6] = IVP[6] + (INI - 1) / 2 + 12
    IVQ[7] = IVP[7] + 3 * (INI - 1) / 4 + 1
    IVQ[8] = IVP[8] + (INI - 1) / 4 + (INI - 1) / 8 + 10
    IVQ[9] = IVP[9] + INW
    IVQ[10] = IVP[10] + (INW - 1) / 2 + 12
    IVQ[11] = IVP[11] + 3 * (INW - 1) / 4 + 1
    IVQ[12] = IVP[12] + (INW - 1) / 4 + (INW - 1) / 8 + 10
    IVQ[13] = IVP[13] + (INB - 1) / 4 + 8
    IVQ[14] = IVP[14] + (INB - 1) / 2 + 1
    IVQ[15] = IVP[15] + (INB - 1) / 4 + (INB - 1) / 8 + 10
    IVQ[16] = IVP[16] + 3 * (INB - 1) / 4 + 1
    IVQ[17] = IVP[17] + (INI - 1) / 4 + 8
    IVQ[18] = IVP[18] + (INI - 1) / 2 + 1
    IVQ[19] = IVP[19] + (INI - 1) / 4 + (INI - 1) / 8 + 10
    IVQ[20] = IVP[20] + 3 * (INI - 1) / 4 + 1
    IVQ[21] = IVP[21] + (INW - 1) / 4 + 8
    IVQ[22] = IVP[22] + (INW - 1) / 2 + 1
    IVQ[23] = IVP[23] + (INW - 1) / 4 + (INW - 1) / 8 + 10
    IVQ[24] = IVP[24] + 3 * (INW - 1) / 4 + 1

    IDE[1] = 1
    IDE[2] = INB + 3 * (INB - 1) / 4
    IDE[3] = INB + (INB - 1) / 2 + 3 * (INB - 1) / 4 + 3 * (INB - 1) / 8 + 6
    IDE[4] = INB + (INB - 1) / 2 + 3 * (INB - 1) / 4 + 5 * (INB - 1) / 8 + 16
    IDE[5] = 9 * INB + (INB - 1) / 4 + (INB - 1) / 8 + 70
    IDE[6] = 9 * INB + (INB - 1) / 2 + (INB - 1) / 8 + 80
    IDE[7] = 10 * INB + (INB - 1) / 4 + 95
    IDE[8] = 11 * INB + (INB - 1) / 2 + 94
    DATA_MESH.NEBR = 12 * INB + int((INB - 1) / 2) + 92
    NEBR = DATA_MESH.NEBR
    IDE[9] = NEBR + 1
    IDE[10] = NEBR + INI + 3 * (INI - 1) / 4
    IDE[11] = NEBR + INI + (INI - 1) / 2 + 3 * (INI - 1) / 4 + 3 * (INI - 1) / 8 + 6
    IDE[12] = NEBR + INI + (INI - 1) / 2 + 3 * (INI - 1) / 4 + 5 * (INI - 1) / 8 + 16
    IDE[13] = NEBR + 9 * INI + (INI - 1) / 4 + (INI - 1) / 8 + 70
    IDE[14] = NEBR + 9 * INI + (INI - 1) / 2 + (INI - 1) / 8 + 80
    IDE[15] = NEBR + 10 * INI + (INI - 1) / 4 + 95
    IDE[16] = NEBR + 11 * INI + (INI - 1) / 2 + 94
    DATA_MESH.NEIR = 12 * INI + int((INI - 1) / 2) + 92
    NEIR = DATA_MESH.NEIR
    IDE[17] = NEBR + NEIR + 1
    IDE[18] = NEBR + NEIR + INW + 3 * (INW - 1) / 4
    IDE[19] = NEBR + NEIR + INW + (INW - 1) / 2 + 3 * (INW - 1) / 4 + 3 * (INW - 1) / 8 + 6
    IDE[20] = NEBR + NEIR + INW + (INW - 1) / 2 + 3 * (INW - 1) / 4 + 5 * (INW - 1) / 8 + 16
    IDE[21] = NEBR + NEIR + 9 * INW + (INW - 1) / 4 + (INW - 1) / 8 + 70
    IDE[22] = NEBR + NEIR + 9 * INW + (INW - 1) / 2 + (INW - 1) / 8 + 80
    IDE[23] = NEBR + NEIR + 10 * INW + (INW - 1) / 4 + 95
    IDE[24] = NEBR + NEIR + 11 * INW + (INW - 1) / 2 + 94
    DATA_MESH.NEWR = 12 * INW + int((INW - 1) / 2) + 92
    NEWR = DATA_MESH.NEWR
    IDE[25] = 3 * INB + (INB - 1) / 8 + 24
    IDE[26] = 3 * INB + (INB - 1) / 4 + (INB - 1) / 8 + 34
    IDE[27] = 4 * INB + 49
    IDE[28] = 5 * INB + (INB - 1) / 4 + 48
    IDE[29] = 6 * INB + (INB - 1) / 4 + 47
    IDE[30] = 8 * INB + 45
    IDE[31] = 8 * INB + 7 * (INB - 1) / 8 + 51
    IDE[32] = 9 * INB + (INB - 1) / 8 + 60
    IDE[33] = NEBR + 3 * INI + (INI - 1) / 8 + 24
    IDE[34] = NEBR + 3 * INI + (INI - 1) / 4 + (INI - 1) / 8 + 34
    IDE[35] = NEBR + 4 * INI + 49
    IDE[36] = NEBR + 5 * INI + (INI - 1) / 4 + 48
    IDE[37] = NEBR + 6 * INI + (INI - 1) / 4 + 47
    IDE[38] = NEBR + 8 * INI + 45
    IDE[39] = NEBR + 8 * INI + 7 * (INI - 1) / 8 + 51
    IDE[40] = NEBR + 9 * INI + (INI - 1) / 8 + 60
    IDE[41] = NEBR + NEIR + 3 * INW + (INW - 1) / 8 + 24
    IDE[42] = NEBR + NEIR + 3 * INW + (INW - 1) / 4 + (INW - 1) / 8 + 34
    IDE[43] = NEBR + NEIR + 4 * INW + 49
    IDE[44] = NEBR + NEIR + 5 * INW + (INW - 1) / 4 + 48
    IDE[45] = NEBR + NEIR + 6 * INW + (INW - 1) / 4 + 47
    IDE[46] = NEBR + NEIR + 8 * INW + 45
    IDE[47] = NEBR + NEIR + 8 * INW + 7 * (INW - 1) / 8 + 51
    IDE[48] = NEBR + NEIR + 9 * INW + (INW - 1) / 8 + 60

    IDN[1] = IDE[1] + INB - 1 - 1
    IDN[2] = IDE[2] + (INB - 1) / 2 - 1
    IDN[3] = IDE[3] + (INB - 1) / 4 + 10 - 1
    IDN[4] = IDE[4] + (INB - 1) / 4 + 10 - 1
    IDN[5] = IDE[5] + (INB - 1) / 4 + 10 - 1
    IDN[6] = IDE[6] + (INB - 1) / 4 + 10 - 1
    IDN[7] = IDE[7] + (INB - 1) / 2 - 1
    IDN[8] = IDE[8] + INB - 1 - 1
    IDN[9] = IDE[9] + INI - 1 - 1
    IDN[10] = IDE[10] + (INI - 1) / 2 - 1
    IDN[11] = IDE[11] + (INI - 1) / 4 + 10 - 1
    IDN[12] = IDE[12] + (INI - 1) / 4 + 10 - 1
    IDN[13] = IDE[13] + (INI - 1) / 4 + 10 - 1
    IDN[14] = IDE[14] + (INI - 1) / 4 + 10 - 1
    IDN[15] = IDE[15] + (INI - 1) / 2 - 1
    IDN[16] = IDE[16] + INI - 1 - 1
    IDN[17] = IDE[17] + INW - 1 - 1
    IDN[18] = IDE[18] + (INW - 1) / 2 - 1
    IDN[19] = IDE[19] + (INW - 1) / 4 + 10 - 1
    IDN[20] = IDE[20] + (INW - 1) / 4 + 10 - 1
    IDN[21] = IDE[21] + (INW - 1) / 4 + 10 - 1
    IDN[22] = IDE[22] + (INW - 1) / 4 + 10 - 1
    IDN[23] = IDE[23] + (INW - 1) / 2 - 1
    IDN[24] = IDE[24] + INW - 1 - 1
    IDN[25] = IDE[25] + (INB - 1) / 4 + 10 - 1
    IDN[26] = IDE[26] + (INB - 1) / 4 + 10 - 1
    IDN[27] = IDE[27] + (INB - 1) / 2 - 1
    IDN[28] = IDE[28] + INB - 1 - 1
    IDN[29] = IDE[29] + INB - 1 - 1
    IDN[30] = IDE[30] + (INB - 1) / 2 - 1
    IDN[31] = IDE[31] + (INB - 1) / 4 + 10 - 1
    IDN[32] = IDE[32] + (INB - 1) / 4 + 10 - 1
    IDN[33] = IDE[33] + (INI - 1) / 4 + 10 - 1
    IDN[34] = IDE[34] + (INI - 1) / 4 + 10 - 1
    IDN[35] = IDE[35] + (INI - 1) / 2 - 1
    IDN[36] = IDE[36] + INI - 1 - 1
    IDN[37] = IDE[37] + INI - 1 - 1
    IDN[38] = IDE[38] + (INI - 1) / 2 - 1
    IDN[39] = IDE[39] + (INI - 1) / 4 + 10 - 1
    IDN[40] = IDE[40] + (INI - 1) / 4 + 10 - 1
    IDN[41] = IDE[41] + (INW - 1) / 4 + 10 - 1
    IDN[42] = IDE[42] + (INW - 1) / 4 + 10 - 1
    IDN[43] = IDE[43] + (INW - 1) / 2 - 1
    IDN[44] = IDE[44] + INW - 1 - 1
    IDN[45] = IDE[45] + INW - 1 - 1
    IDN[46] = IDE[46] + (INW - 1) / 2 - 1
    IDN[47] = IDE[47] + (INW - 1) / 4 + 10 - 1
    IDN[48] = IDE[48] + (INW - 1) / 4 + 10 - 1

    IVE[1] = INB - 1 + 1
    IVE[2] = 2 * (INB - 1) + (INB - 1) / 4 + 1
    IVE[3] = NEBR / 2 + INB - 1 + 1
    IVE[4] = NEBR / 2 + 2 * (INB - 1) + (INB - 1) / 4 + 1
    IVE[5] = NEBR + INI - 1 + 1
    IVE[6] = NEBR + 2 * (INI - 1) + (INI - 1) / 4 + 1
    IVE[7] = NEBR + NEIR / 2 + INI - 1 + 1
    IVE[8] = NEBR + NEIR / 2 + 2 * (INI - 1) + (INI - 1) / 4 + 1
    IVE[9] = NEBR + NEIR + INW - 1 + 1
    IVE[10] = NEBR + NEIR + 2 * (INW - 1) + (INW - 1) / 4 + 1
    IVE[11] = NEBR + NEIR + NEWR / 2 + INW - 1 + 1
    IVE[12] = NEBR + NEIR + NEWR / 2 + 2 * (INW - 1) + (INW - 1) / 4 + 1
    IVE[13] = NEBR / 2 - 2 * (INB - 1) - (INB - 1) / 4 - 3 * (INB - 1) / 8 - 6 + 1
    IVE[14] = NEBR / 2 - (INB - 1) - 3 * (INB - 1) / 4 + 1
    IVE[15] = NEBR - 2 * (INB - 1) - (INB - 1) / 4 - 3 * (INB - 1) / 8 - 6 + 1
    IVE[16] = NEBR - (INB - 1) - 3 * (INB - 1) / 4 + 1
    IVE[17] = NEBR + NEIR / 2 - 2 * (INI - 1) - (INI - 1) / 4 - 3 * (INI - 1) / 8 - 6 + 1
    IVE[18] = NEBR + NEIR / 2 - (INI - 1) - 3 * (INI - 1) / 4 + 1
    IVE[19] = NEBR + NEIR - 2 * (INI - 1) - (INI - 1) / 4 - 3 * (INI - 1) / 8 - 6 + 1
    IVE[20] = NEBR + NEIR - (INI - 1) - 3 * (INI - 1) / 4 + 1
    IVE[21] = NEBR + NEIR + NEWR / 2 - 2 * (INW - 1) - (INW - 1) / 4 - 3 * (INW - 1) / 8 - 6 + 1
    IVE[22] = NEBR + NEIR + NEWR / 2 - (INW - 1) - 3 * (INW - 1) / 4 + 1
    IVE[23] = NEBR + NEIR + NEWR - 2 * (INW - 1) - (INW - 1) / 4 - 3 * (INW - 1) / 8 - 6 + 1
    IVE[24] = NEBR + NEIR + NEWR - (INW - 1) - 3 * (INW - 1) / 4 + 1

    IVN[1] = IVE[1] + 3 * (INB - 1) / 4 - 1
    IVN[2] = IVE[2] + 3 * (INB - 1) / 8 + 6 - 1
    IVN[3] = IVE[3] + 3 * (INB - 1) / 4 - 1
    IVN[4] = IVE[4] + 3 * (INB - 1) / 8 + 6 - 1
    IVN[5] = IVE[5] + 3 * (INI - 1) / 4 - 1
    IVN[6] = IVE[6] + 3 * (INI - 1) / 8 + 6 - 1
    IVN[7] = IVE[7] + 3 * (INI - 1) / 4 - 1
    IVN[8] = IVE[8] + 3 * (INI - 1) / 8 + 6 - 1
    IVN[9] = IVE[9] + 3 * (INW - 1) / 4 - 1
    IVN[10] = IVE[10] + 3 * (INW - 1) / 8 + 6 - 1
    IVN[11] = IVE[11] + 3 * (INW - 1) / 4 - 1
    IVN[12] = IVE[12] + 3 * (INW - 1) / 8 + 6 - 1
    IVN[13] = IVE[13] + 3 * (INB - 1) / 8 + 6 - 1
    IVN[14] = IVE[14] + 3 * (INB - 1) / 4 - 1
    IVN[15] = IVE[15] + 3 * (INB - 1) / 8 + 6 - 1
    IVN[16] = IVE[16] + 3 * (INB - 1) / 4 - 1
    IVN[17] = IVE[17] + 3 * (INI - 1) / 8 + 6 - 1
    IVN[18] = IVE[18] + 3 * (INI - 1) / 4 - 1
    IVN[19] = IVE[19] + 3 * (INI - 1) / 8 + 6 - 1
    IVN[20] = IVE[20] + 3 * (INI - 1) / 4 - 1
    IVN[21] = IVE[21] + 3 * (INW - 1) / 8 + 6 - 1
    IVN[22] = IVE[22] + 3 * (INW - 1) / 4 - 1
    IVN[23] = IVE[23] + 3 * (INW - 1) / 8 + 6 - 1
    IVN[24] = IVE[24] + 3 * (INW - 1) / 4 - 1

    DATA_MESH.NP = NPBR + NPIR + NPWR
    DATA_MESH.NE = NEBR + NEIR + NEWR
    for I in range(1, DATA_MESH.NE + 1):
        for N in range(1, 3 + 1):
            DATA_MESH.MS[I, N] = 0

    for I in range(1, 48 + 1):
        JP = IDP[I]
        JQ = IDQ[I]
        for N in range(IDE[I], IDN[I] + 1, 2):
            if I >= 25:
                DATA_MESH.MS[N, 1] = JP
                DATA_MESH.MS[N, 2] = JP + 1
                DATA_MESH.MS[N, 3] = JQ
                DATA_MESH.MS[N + 1, 1] = JP + 1
                DATA_MESH.MS[N + 1, 2] = JQ + 1
                DATA_MESH.MS[N + 1, 3] = JQ
            else:
                DATA_MESH.MS[N, 1] = JP
                DATA_MESH.MS[N, 2] = JQ + 1
                DATA_MESH.MS[N, 3] = JQ
                DATA_MESH.MS[N + 1, 1] = JP
                DATA_MESH.MS[N + 1, 2] = JP + 1
                DATA_MESH.MS[N + 1, 3] = JQ + 1
            JP = JP + 1
            JQ = JQ + 1

    for I in range(1, 24 + 1):
        JP = IVP[I]
        JQ = IVQ[I]
        for N in range(IVE[I], IVN[I] + 1, 3):
            if I >= 13:
                DATA_MESH.MS[N, 1] = JP
                DATA_MESH.MS[N, 2] = JQ + 1
                DATA_MESH.MS[N, 3] = JQ
                DATA_MESH.MS[N + 1, 1] = JP
                DATA_MESH.MS[N + 1, 2] = JP + 1
                DATA_MESH.MS[N + 1, 3] = JQ + 1
                DATA_MESH.MS[N + 2, 1] = JP + 1
                DATA_MESH.MS[N + 2, 2] = JQ + 2
                DATA_MESH.MS[N + 2, 3] = JQ + 1
                JP = JP + 1
                JQ = JQ + 2
            else:
                DATA_MESH.MS[N, 1] = JP
                DATA_MESH.MS[N, 2] = JP + 1
                DATA_MESH.MS[N, 3] = JQ
                DATA_MESH.MS[N + 1, 1] = JP + 1
                DATA_MESH.MS[N + 1, 2] = JQ + 1
                DATA_MESH.MS[N + 1, 3] = JQ
                DATA_MESH.MS[N + 2, 1] = JP + 1
                DATA_MESH.MS[N + 2, 2] = JP + 2
                DATA_MESH.MS[N + 2, 3] = JQ + 1
                JP = JP + 2
                JQ = JQ + 1

    DATA_MESH.INC[1] = 3 * INB + (INB - 1) / 2 + 33
    DATA_MESH.INC[2] = 3 * INB + (INB - 1) / 2 + (INB - 1) / 4 + 41
    DATA_MESH.INC[3] = 3 * INB + (INB - 1) / 2 + (INB - 1) / 4 / 2 + 37
    DATA_MESH.INC[4] = NPBR + 3 * INI + (INI - 1) / 2 + (INI - 1) / 4 / 2 + 37
    DATA_MESH.INC[5] = NPBR + NPIR + 3 * INW + (INW - 1) / 2 + (INW - 1) / 4 / 2 + 37
    DATA_MESH.NSBRD = NPBR - (INB - 1)
    DATA_MESH.NSIRT = NPBR + 1
    DATA_MESH.NSIRD = NPBR + NPIR - (INI - 1)
    DATA_MESH.NSWRT = NPBR + NPIR + 1
    DATA_MESH.NSWRD = NPBR + NPIR + NPWR - (INW - 1)


def XYS():
    global IXB
    global IXI
    global IXW
    IXH = np.zeros((13 + 1, 3 + 1), dtype=np.float64)
    IYH = np.zeros((3 + 1, 3 + 1), dtype=np.float64)
    KNBR = np.zeros(13 + 1, dtype=np.int32)
    KNIR = np.zeros(13 + 1, dtype=np.int32)
    KNWR = np.zeros(13 + 1, dtype=np.int32)
    NBR = np.zeros(13 + 1, dtype=np.int32)
    NIR = np.zeros(13 + 1, dtype=np.int32)
    NWR = np.zeros(13 + 1, dtype=np.int32)

    IYB0 = np.zeros(DATA_MESH.INB + 1, dtype=np.float64)
    IYB1 = np.zeros(DATA_MESH.INB + 1, dtype=np.float64)
    IYB2 = np.zeros(DATA_MESH.INB + 1, dtype=np.float64)
    IYB3 = np.zeros(DATA_MESH.INB + 1, dtype=np.float64)
    IYI0 = np.zeros(DATA_MESH.INI + 1, dtype=np.float64)
    IYI1 = np.zeros(DATA_MESH.INI + 1, dtype=np.float64)
    IYI2 = np.zeros(DATA_MESH.INI + 1, dtype=np.float64)
    IYI3 = np.zeros(DATA_MESH.INI + 1, dtype=np.float64)
    IYW0 = np.zeros(DATA_MESH.INW + 1, dtype=np.float64)
    IYW1 = np.zeros(DATA_MESH.INW + 1, dtype=np.float64)
    IYW2 = np.zeros(DATA_MESH.INW + 1, dtype=np.float64)
    IYW3 = np.zeros(DATA_MESH.INW + 1, dtype=np.float64)

    INB = DATA_MESH.INB
    KNBR[1] = 1
    KNBR[2] = INB + 1
    KNBR[3] = 2 * INB + 1
    KNBR[4] = 2 * INB + (INB - 1) / 2 + 1 + 1
    KNBR[5] = 3 * INB + 10
    KNBR[6] = 3 * INB + (INB - 1) / 4 + 21
    KNBR[7] = 3 * INB + (INB - 1) / 2 + 32
    KNBR[8] = 3 * INB + 3 * (INB - 1) / 4 + 43
    KNBR[9] = 4 * INB + 53
    KNBR[10] = 4 * INB + (INB - 1) / 4 + 64
    KNBR[11] = 4 * INB + 3 * (INB - 1) / 4 + 73
    KNBR[12] = 5 * INB + (INB - 1) / 4 + 73
    KNBR[13] = 6 * INB + (INB - 1) / 4 + 73
    NPBR = DATA_MESH.NPBR
    INI = DATA_MESH.INI
    KNIR[1] = NPBR + 1
    KNIR[2] = NPBR + INI + 1
    KNIR[3] = NPBR + 2 * INI + 1
    KNIR[4] = NPBR + 2 * INI + (INI - 1) / 2 + 1 + 1
    KNIR[5] = NPBR + 3 * INI + 10
    KNIR[6] = NPBR + 3 * INI + (INI - 1) / 4 + 21
    KNIR[7] = NPBR + 3 * INI + (INI - 1) / 2 + 32
    KNIR[8] = NPBR + 3 * INI + 3 * (INI - 1) / 4 + 43
    KNIR[9] = NPBR + 4 * INI + 53
    KNIR[10] = NPBR + 4 * INI + (INI - 1) / 4 + 64
    KNIR[11] = NPBR + 4 * INI + 3 * (INI - 1) / 4 + 73
    KNIR[12] = NPBR + 5 * INI + (INI - 1) / 4 + 73
    KNIR[13] = NPBR + 6 * INI + (INI - 1) / 4 + 73
    NPIR = DATA_MESH.NPIR
    INW = DATA_MESH.INW
    KNWR[1] = NPBR + NPIR + 1
    KNWR[2] = NPBR + NPIR + INW + 1
    KNWR[3] = NPBR + NPIR + 2 * INW + 1
    KNWR[4] = NPBR + NPIR + 2 * INW + (INW - 1) / 2 + 1 + 1
    KNWR[5] = NPBR + NPIR + 3 * INW + 10
    KNWR[6] = NPBR + NPIR + 3 * INW + (INW - 1) / 4 + 21
    KNWR[7] = NPBR + NPIR + 3 * INW + (INW - 1) / 2 + 32
    KNWR[8] = NPBR + NPIR + 3 * INW + 3 * (INW - 1) / 4 + 43
    KNWR[9] = NPBR + NPIR + 4 * INW + 53
    KNWR[10] = NPBR + NPIR + 4 * INW + (INW - 1) / 4 + 64
    KNWR[11] = NPBR + NPIR + 4 * INW + 3 * (INW - 1) / 4 + 73
    KNWR[12] = NPBR + NPIR + 5 * INW + (INW - 1) / 4 + 73
    KNWR[13] = NPBR + NPIR + 6 * INW + (INW - 1) / 4 + 73

    NBR[1] = INB
    NBR[2] = INB
    NBR[3] = (INB - 1) / 2 + 1
    NBR[4] = (INB - 1) / 2 + 1 + 8
    NBR[5] = (INB - 1) / 4 + 1 + 10
    NBR[6] = (INB - 1) / 4 + 1 + 10
    NBR[7] = (INB - 1) / 4 + 1 + 10
    NBR[8] = (INB - 1) / 4 + 1 + 10
    NBR[9] = (INB - 1) / 4 + 1 + 10
    NBR[10] = (INB - 1) / 2 + 1 + 8
    NBR[11] = (INB - 1) / 2 + 1
    NBR[12] = INB
    NBR[13] = INB
    NIR[1] = INI
    NIR[2] = INI
    NIR[3] = (INI - 1) / 2 + 1
    NIR[4] = (INI - 1) / 2 + 1 + 8
    NIR[5] = (INI - 1) / 4 + 1 + 10
    NIR[6] = (INI - 1) / 4 + 1 + 10
    NIR[7] = (INI - 1) / 4 + 1 + 10
    NIR[8] = (INI - 1) / 4 + 1 + 10
    NIR[9] = (INI - 1) / 4 + 1 + 10
    NIR[10] = (INI - 1) / 2 + 1 + 8
    NIR[11] = (INI - 1) / 2 + 1
    NIR[12] = INI
    NIR[13] = INI
    NWR[1] = INW
    NWR[2] = INW
    NWR[3] = (INW - 1) / 2 + 1
    NWR[4] = (INW - 1) / 2 + 1 + 8
    NWR[5] = (INW - 1) / 4 + 1 + 10
    NWR[6] = (INW - 1) / 4 + 1 + 10
    NWR[7] = (INW - 1) / 4 + 1 + 10
    NWR[8] = (INW - 1) / 4 + 1 + 10
    NWR[9] = (INW - 1) / 4 + 1 + 10
    NWR[10] = (INW - 1) / 2 + 1 + 8
    NWR[11] = (INW - 1) / 2 + 1
    NWR[12] = INW
    NWR[13] = INW

    DB_NOM = 0.0
    DI_NOM = 0.0
    DW_NOM = 0.0
    for I in range(1, 12 + 1):
        DB_NOM = DB_NOM + IXB[I]
        DI_NOM = DI_NOM + IXI[I]
        DW_NOM = DW_NOM + IXW[I]

    DBN_NOM = 2 * (IXB[5] + IXB[6])
    DIN_NOM = 2 * (IXI[5] + IXI[6])
    DWN_NOM = 2 * (IXW[5] + IXW[6])
    for I in range(1, DATA_MESH.NP + 1):
        DATA_MESH.X[I] = 0.0
        DATA_MESH.Y[I] = 0.0

    for I in range(1, 3 + 1):
        IXB[I] = IXB[I] * DATA_ROLL.DB / DB_NOM
        IXI[I] = IXI[I] * DATA_ROLL.DI / DI_NOM
        IXW[I] = IXW[I] * DATA_ROLL.DW / DW_NOM

    for I in range(5, 8 + 1):
        IXB[I] = IXB[I] * DATA_ROLL.DBN / DBN_NOM
        IXI[I] = IXI[I] * DATA_ROLL.DIN / DIN_NOM
        IXW[I] = IXW[I] * DATA_ROLL.DWN / DWN_NOM

    IXB[4] = DATA_ROLL.DB / 2 - IXB[1] - IXB[2] - IXB[3] - IXB[5] - IXB[6]
    IXI[4] = DATA_ROLL.DI / 2 - IXI[1] - IXI[2] - IXI[3] - IXI[5] - IXI[6]
    IXW[4] = DATA_ROLL.DW / 2 - IXW[1] - IXW[2] - IXW[3] - IXW[5] - IXW[6]
    IXB[9] = IXB[4]
    IXI[9] = IXI[4]
    IXW[9] = IXW[4]
    for I in range(10, 12 + 1):
        IXB[I] = IXB[I] * DATA_ROLL.DB / DB_NOM
        IXI[I] = IXI[I] * DATA_ROLL.DI / DI_NOM
        IXW[I] = IXW[I] * DATA_ROLL.DW / DW_NOM

    for I in range(1, 3 + 1):
        IXH[13, I] = 0

    for LX in range(1, 12 + 1):
        IXH[13 - LX, 1] = IXH[14 - LX, 1] + IXB[LX]
        IXH[13 - LX, 2] = IXH[14 - LX, 2] + IXI[LX]
        IXH[13 - LX, 3] = IXH[14 - LX, 3] + IXW[LX]

    for J in range(1, 3 + 1):
        for LX in range(1, 13 + 1):
            NKS = KNBR[LX]
            if J == 2: NKS = KNIR[LX]
            if J == 3: NKS = KNWR[LX]
            INK = NBR[LX]
            if J == 2: INK = NIR[LX]
            if J == 3: INK = NWR[LX]
            for KK in range(1, INK + 1):
                DATA_MESH.X[NKS - 1 + KK] = IXH[LX, J] * 1e0

    for K in range(1, NPBR + 1):
        DATA_MESH.X[K] = DATA_MESH.X[K] + DATA_ROLL.DW * 1e0 + DATA_ROLL.DI * 1e0

    KK = NPBR + 1
    LX = NPBR + NPIR
    for K in range(KK, LX + 1):
        DATA_MESH.X[K] = DATA_MESH.X[K] + DATA_ROLL.DW * 1e0

    KK = INB - 1
    for I in range(1, KK + 1):
        IYB0[I] = DATA_MESH.SP

    KK = int((INB - 1) / 2)
    for I in range(1, KK + 1):
        IYB1[I] = 2 * DATA_MESH.SP

    for I in range(1, 4 + 1):
        IYB2[I] = DATA_ROLL.BRTR / 4

    KK = 4 + int((INB - 1) / 2)
    for I in range(5, KK + 1):
        IYB2[I] = 2 * DATA_MESH.SP

    KK = 4 + int((INB - 1) / 2) + 1
    LX = 8 + int((INB - 1) / 2)
    for I in range(KK, LX + 1):
        IYB2[I] = DATA_ROLL.BRTL / 4

    YSTP = 0
    KK = int((INB - 1) / 4) + 4
    for I in range(1, KK + 1):
        YSTP = YSTP + IYB2[I]

    IYB3[1] = 400.0 * DATA_ROLL.DB / DB_NOM
    IYB3[2] = (DATA_ROLL.LHR - YSTP) * 200.0 / (200.0 + 165.0)
    IYB3[3] = (DATA_ROLL.LHR - YSTP) * 165.0 / (200.0 + 165.0)
    IYB3[4] = DATA_ROLL.BRTR / 2
    IYB3[5] = DATA_ROLL.BRTR / 2
    KK = int((INB - 1) / 4) + 5
    for I in range(6, KK + 1):
        IYB3[I] = 4 * DATA_MESH.SP

    IYB3[KK + 1] = DATA_ROLL.BRTL / 2
    IYB3[KK + 2] = DATA_ROLL.BRTL / 2
    YSTP = 0
    KK = int((INB - 1) / 4) + 5
    LX = int((INB - 1) / 2) + 8
    for I in range(KK, LX + 1):
        YSTP = YSTP + IYB2[I]

    IYB3[KK + 3] = (DATA_ROLL.LHL - YSTP) * 165.0 / (200.0 + 165.0)
    IYB3[KK + 4] = (DATA_ROLL.LHL - YSTP) * 200.0 / (200.0 + 165.0)
    IYB3[KK + 5] = 400.0 * DATA_ROLL.DB / DB_NOM

    KK = INI - 1
    for I in range(1, KK + 1):
        IYI0[I] = DATA_MESH.SP

    KK = int((INI - 1) / 2)
    for I in range(1, KK + 1):
        IYI1[I] = 2 * DATA_MESH.SP

    for I in range(1, 4 + 1):
        IYI2[I] = DATA_ROLL.IRTR / 4

    KK = 4 + int((INI - 1) / 2)
    for I in range(5, KK + 1):
        IYI2[I] = 2 * DATA_MESH.SP

    KK = 4 + int((INI - 1) / 2) + 1
    LX = 8 + int((INI - 1) / 2)
    for I in range(KK, LX + 1):
        IYI2[I] = DATA_ROLL.IRTL / 4

    YSTP = 0
    KK = int((INI - 1) / 4) + 4
    for I in range(1, KK + 1):
        YSTP = YSTP + IYI2[I]

    IYI3[1] = 300.0 * DATA_ROLL.DI / DI_NOM
    IYI3[2] = (DATA_ROLL.LMR - YSTP) * 200.0 / (200.0 + 165.0)
    IYI3[3] = (DATA_ROLL.LMR - YSTP) * 165.0 / (200.0 + 165.0)
    IYI3[4] = DATA_ROLL.IRTR / 2
    IYI3[5] = DATA_ROLL.IRTR / 2
    KK = int((INI - 1) / 4) + 5
    for I in range(6, KK + 1):
        IYI3[I] = 4 * DATA_MESH.SP

    IYI3[KK + 1] = DATA_ROLL.IRTL / 2
    IYI3[KK + 2] = DATA_ROLL.IRTL / 2
    YSTP = 0
    KK = int((INI - 1) / 4) + 5
    LX = int((INI - 1) / 2) + 8
    for I in range(KK, LX + 1):
        YSTP = YSTP + IYI2[I]

    IYI3[KK + 3] = (DATA_ROLL.LML - YSTP) * 165.0 / (200.0 + 165.0)
    IYI3[KK + 4] = (DATA_ROLL.LML - YSTP) * 200.0 / (200.0 + 165.0)
    IYI3[KK + 5] = 300.0 * DATA_ROLL.DI / DI_NOM

    KK = INW - 1
    for I in range(1, KK + 1):
        IYW0[I] = DATA_MESH.SP

    KK = int((INW - 1) / 2)
    for I in range(1, KK + 1):
        IYW1[I] = 2 * DATA_MESH.SP

    for I in range(1, 4 + 1):
        IYW2[I] = DATA_ROLL.WRTR / 4

    KK = 4 + int((INW - 1) / 2)
    for I in range(5, KK + 1):
        IYW2[I] = 2 * DATA_MESH.SP

    KK = 4 + int((INW - 1) / 2) + 1
    LX = 8 + int((INW - 1) / 2)
    for I in range(KK, LX + 1):
        IYW2[I] = DATA_ROLL.WRTL / 4

    YSTP = 0
    KK = int((INW - 1) / 4) + 4
    for I in range(1, KK + 1):
        YSTP = YSTP + IYW2[I]

    IYW3[1] = 250.0 * DATA_ROLL.DW / DW_NOM
    IYW3[2] = (DATA_ROLL.LFR - YSTP) * 200.0 / (200.0 + 165.0)
    IYW3[3] = (DATA_ROLL.LFR - YSTP) * 165.0 / (200.0 + 165.0)
    IYW3[4] = DATA_ROLL.WRTR / 2
    IYW3[5] = DATA_ROLL.WRTR / 2
    KK = int((INW - 1) / 4) + 5
    for I in range(6, KK + 1):
        IYW3[I] = 4 * DATA_MESH.SP

    IYW3[KK + 1] = DATA_ROLL.WRTL / 2
    IYW3[KK + 2] = DATA_ROLL.WRTL / 2
    YSTP = 0
    KK = int((INW - 1) / 4) + 5
    LX = int((INW - 1) / 2) + 8
    for I in range(KK, LX + 1):
        YSTP = YSTP + IYW2[I]

    IYW3[KK + 3] = (DATA_ROLL.LFL - YSTP) * 165.0 / (200.0 + 165.0)
    IYW3[KK + 4] = (DATA_ROLL.LFL - YSTP) * 200.0 / (200.0 + 165.0)
    IYW3[KK + 5] = 250.0 * DATA_ROLL.DW / DW_NOM

    IYH[1, 1] = 0
    KK = int((INB - 1) / 2 / 2)
    for I in range(1, KK + 1):
        IYH[1, 1] = IYH[1, 1] + IYB1[I]

    IYH[2, 1] = 0
    KK = int((INB - 1) / 2 / 2) + 4
    for I in range(1, KK + 1):
        IYH[2, 1] = IYH[2, 1] + IYB2[I]

    IYH[3, 1] = 0
    KK = int((INB - 1) / 2 / 2 / 2) + 5
    for I in range(1, KK + 1):
        IYH[3, 1] = IYH[3, 1] + IYB3[I]

    IYH[1, 2] = 0
    KK = int((INI - 1) / 2 / 2)
    for I in range(1, KK + 1):
        IYH[1, 2] = IYH[1, 2] + IYI1[I]

    IYH[2, 2] = 0
    KK = int((INI - 1) / 2 / 2) + 4
    for I in range(1, KK + 1):
        IYH[2, 2] = IYH[2, 2] + IYI2[I]

    IYH[3, 2] = 0
    KK = int((INI - 1) / 2 / 2 / 2) + 5
    for I in range(1, KK + 1):
        IYH[3, 2] = IYH[3, 2] + IYI3[I]

    IYH[1, 3] = 0
    KK = int((INW - 1) / 2 / 2)
    for I in range(1, KK + 1):
        IYH[1, 3] = IYH[1, 3] + IYW1[I]

    IYH[2, 3] = 0
    KK = int((INW - 1) / 2 / 2) + 4
    for I in range(1, KK + 1):
        IYH[2, 3] = IYH[2, 3] + IYW2[I]

    IYH[3, 3] = 0
    KK = int((INW - 1) / 2 / 2 / 2) + 5
    for I in range(1, KK + 1):
        IYH[3, 3] = IYH[3, 3] + IYW3[I]

    for J in range(1, 3 + 1):
        for LX in range(1, 13 + 1):
            NKS = KNBR[LX]
            if J == 2: NKS = KNIR[LX]
            if J == 3: NKS = KNWR[LX]
            INK = NBR[LX] - 1
            if J == 2: INK = NIR[LX] - 1
            if J == 3: INK = NWR[LX] - 1
            if LX == 4 or LX == 10:
                DATA_MESH.Y[NKS] = -IYH[2, J] * 1e0
                for K in range(1, INK + 1):
                    if J == 1: YSTP = IYB2[K] * 1e0
                    if J == 2: YSTP = IYI2[K] * 1e0
                    if J == 3: YSTP = IYW2[K] * 1e0
                    DATA_MESH.Y[NKS + K] = DATA_MESH.Y[NKS + K - 1] + YSTP
            elif LX == 3 or LX == 11:
                DATA_MESH.Y[NKS] = -IYH[1, J] * 1e0
                for K in range(1, INK + 1):
                    if J == 1: YSTP = IYB1[K] * 1e0
                    if J == 2: YSTP = IYI1[K] * 1e0
                    if J == 3: YSTP = IYW1[K] * 1e0
                    DATA_MESH.Y[NKS + K] = DATA_MESH.Y[NKS + K - 1] + YSTP
            elif LX > 4 and LX < 10:
                DATA_MESH.Y[NKS] = -IYH[3, J] * 1e0
                for K in range(1, INK + 1):
                    if J == 1: YSTP = IYB3[K] * 1e0
                    if J == 2: YSTP = IYI3[K] * 1e0
                    if J == 3: YSTP = IYW3[K] * 1e0
                    DATA_MESH.Y[NKS + K] = DATA_MESH.Y[NKS + K - 1] + YSTP
            else:
                DATA_MESH.Y[NKS] = -IYH[1, J] * 1e0
                for K in range(1, INK + 1):
                    if J == 1: YSTP = IYB0[K] * 1e0
                    if J == 2: YSTP = IYI0[K] * 1e0
                    if J == 3: YSTP = IYW0[K] * 1e0
                    DATA_MESH.Y[NKS + K] = DATA_MESH.Y[NKS + K - 1] + YSTP


def THY(R1, X1, X2):
    KK = 0
    H1 = X1 / R1
    H2 = X2 / R1
    if H1 > 1.0000000000001e0:
        H1 = 1.0e0
        KK = 1
    if H2 > 1.0000000000001e0:
        H2 = 1.0e0
        KK = 1

    if KK < 1:
        S1 = math.asin(H1 - 0.00000000000001e0)
        S2 = math.asin(H2 - 0.00000000000001e0)
        DH = H1 * H1 * H1 - H2 * H2 * H2
        THK = 0.75e0 * R1 * (S1 - S2 - 0.25e0 * (math.sin(4 * S1) - math.sin(4 * S2))) / DH
    else:
        THK = 100000.0e0
    return THK


def THS():
    X = DATA_MESH.X
    TEQB = DATA_MESH.TEQB
    TEQI = DATA_MESH.TEQI
    TEQW = DATA_MESH.TEQW
    NE = DATA_MESH.NE
    MS = DATA_MESH.MS
    NEBR = DATA_MESH.NEBR
    NEIR = DATA_MESH.NEIR
    NEWR = DATA_MESH.NEWR
    INB = DATA_MESH.INB
    INI = DATA_MESH.INI
    INW = DATA_MESH.INW
    DB = DATA_ROLL.DB
    DI = DATA_ROLL.DI
    DW = DATA_ROLL.DW

    TKK = np.zeros(33+1)
    IES = np.zeros(132+1, dtype=np.int32)
    IEN = np.zeros(132+1, dtype=np.int32)
    IR = np.zeros(33+1)
    ICX = np.zeros(33+1)

    IES[1] = 1
    IES[2] = NEBR / 2 - (INB - 1) + 1
    IES[3] = NEBR / 2 + 1
    IES[4] = NEBR - (INB - 1) + 1
    IES[5] = IES[1] + (INB - 1)
    IES[6] = IES[2] - 3 * (INB - 1) / 4
    IES[7] = IES[3] + (INB - 1)
    IES[8] = IES[4] - 3 * (INB - 1) / 4
    IES[9] = IES[5] + 3 * (INB - 1) / 4
    IES[10] = IES[6] - (INB - 1) / 2
    IES[11] = IES[7] + 3 * (INB - 1) / 4
    IES[12] = IES[8] - (INB - 1) / 2
    IES[13] = IES[9] + (INB - 1) / 2 + 6
    IES[14] = IES[10] - 3 * (INB - 1) / 8
    IES[15] = IES[11] + (INB - 1) / 2
    IES[16] = IES[12] - 3 * (INB - 1) / 8 - 6
    IES[17] = IES[13] + 3 * (INB - 1) / 8 + 10
    IES[18] = IES[14] - (INB - 1) / 4 - 6
    IES[19] = IES[15] + 3 * (INB - 1) / 8 + 6
    IES[20] = IES[16] - (INB - 1) / 4 - 10
    IES[21] = IES[17] + 2 * (INB - 1) / 8 + 10
    IES[22] = IES[18] - (INB - 1) / 4 - 10
    IES[23] = IES[19] + 2 * (INB - 1) / 8 + 10
    IES[24] = IES[20] - (INB - 1) / 4 - 10
    IES[25] = IES[13] - 6
    IES[26] = IES[14] - 6
    IES[27] = IES[15] + 3 * (INB - 1) / 8
    IES[28] = IES[16] + 3 * (INB - 1) / 8
    IES[29] = IES[25] + 3 * (INB - 1) / 8 + 6 + 6
    IES[30] = IES[26] - 2 * (INB - 1) / 8 - 4
    IES[31] = IES[27] + 2 * (INB - 1) / 8 + 6
    IES[32] = IES[28] - 3 * (INB - 1) / 8 - 10
    IES[33] = IES[29] + 2 * (INB - 1) / 8 + 10
    IES[34] = IES[30] - 2 * (INB - 1) / 8 - 10
    IES[35] = IES[31] + 2 * (INB - 1) / 8 + 10
    IES[36] = IES[32] - 2 * (INB - 1) / 8 - 10
    IES[37] = IES[29] - 6
    IES[38] = IES[30] - 6
    IES[39] = IES[31] + 4
    IES[40] = IES[32] + 4
    IES[41] = IES[33] - 6
    IES[42] = IES[34] - 6
    IES[43] = IES[35] + 4
    IES[44] = IES[36] + 4
    IES[45] = NEBR + 1
    IES[46] = NEBR + NEIR / 2 - (INI - 1) + 1
    IES[47] = NEBR + NEIR / 2 + 1
    IES[48] = NEBR + NEIR - (INI - 1) + 1
    IES[49] = IES[45] + (INI - 1)
    IES[50] = IES[46] - 3 * (INI - 1) / 4
    IES[51] = IES[47] + (INI - 1)
    IES[52] = IES[48] - 3 * (INI - 1) / 4
    IES[53] = IES[49] + 3 * (INI - 1) / 4
    IES[54] = IES[50] - (INI - 1) / 2
    IES[55] = IES[51] + 3 * (INI - 1) / 4
    IES[56] = IES[52] - (INI - 1) / 2
    IES[57] = IES[53] + (INI - 1) / 2 + 6
    IES[58] = IES[54] - 3 * (INI - 1) / 8
    IES[59] = IES[55] + (INI - 1) / 2
    IES[60] = IES[56] - 3 * (INI - 1) / 8 - 6
    IES[61] = IES[57] + 3 * (INI - 1) / 8 + 10
    IES[62] = IES[58] - (INI - 1) / 4 - 6
    IES[63] = IES[59] + 3 * (INI - 1) / 8 + 6
    IES[64] = IES[60] - (INI - 1) / 4 - 10
    IES[65] = IES[61] + 2 * (INI - 1) / 8 + 10
    IES[66] = IES[62] - (INI - 1) / 4 - 10
    IES[67] = IES[63] + 2 * (INI - 1) / 8 + 10
    IES[68] = IES[64] - (INI - 1) / 4 - 10
    IES[69] = IES[57] - 6
    IES[70] = IES[58] - 6
    IES[71] = IES[59] + 3 * (INI - 1) / 8
    IES[72] = IES[60] + 3 * (INI - 1) / 8
    IES[73] = IES[69] + 3 * (INI - 1) / 8 + 6 + 6
    IES[74] = IES[70] - 2 * (INI - 1) / 8 - 4
    IES[75] = IES[71] + 2 * (INI - 1) / 8 + 6
    IES[76] = IES[72] - 3 * (INI - 1) / 8 - 10
    IES[77] = IES[73] + 2 * (INI - 1) / 8 + 10
    IES[78] = IES[74] - 2 * (INI - 1) / 8 - 10
    IES[79] = IES[75] + 2 * (INI - 1) / 8 + 10
    IES[80] = IES[76] - 2 * (INI - 1) / 8 - 10
    IES[81] = IES[73] - 6
    IES[82] = IES[74] - 6
    IES[83] = IES[75] + 4
    IES[84] = IES[76] + 4
    IES[85] = IES[77] - 6
    IES[86] = IES[78] - 6
    IES[87] = IES[79] + 4
    IES[88] = IES[80] + 4
    IES[89] = NEBR + NEIR + 1
    IES[90] = NEBR + NEIR + NEWR / 2 - (INW - 1) + 1
    IES[91] = NEBR + NEIR + NEWR / 2 + 1
    IES[92] = NEBR + NEIR + NEWR - (INW - 1) + 1
    IES[93] = IES[89] + (INW - 1)
    IES[94] = IES[90] - 3 * (INW - 1) / 4
    IES[95] = IES[91] + (INW - 1)
    IES[96] = IES[92] - 3 * (INW - 1) / 4
    IES[97] = IES[93] + 3 * (INW - 1) / 4
    IES[98] = IES[94] - (INW - 1) / 2
    IES[99] = IES[95] + 3 * (INW - 1) / 4
    IES[100]= IES[96] - (INW - 1) / 2
    IES[101] = IES[97] + (INW - 1) / 2 + 6
    IES[102] = IES[98] - 3 * (INW - 1) / 8
    IES[103] = IES[99] + (INW - 1) / 2
    IES[104] = IES[100] - 3 * (INW - 1) / 8 - 6
    IES[105] = IES[101] + 3 * (INW - 1) / 8 + 10
    IES[106] = IES[102] - (INW - 1) / 4 - 6
    IES[107] = IES[103] + 3 * (INW - 1) / 8 + 6
    IES[108] = IES[104] - (INW - 1) / 4 - 10
    IES[109] = IES[105] + 2 * (INW - 1) / 8 + 10
    IES[110] = IES[106] - (INW - 1) / 4 - 10
    IES[111] = IES[107] + 2 * (INW - 1) / 8 + 10
    IES[112] = IES[108] - (INW - 1) / 4 - 10
    IES[113] = IES[101] - 6
    IES[114] = IES[102] - 6
    IES[115] = IES[103] + 3 * (INW - 1) / 8
    IES[116] = IES[104] + 3 * (INW - 1) / 8
    IES[117] = IES[113] + 3 * (INW - 1) / 8 + 6 + 6
    IES[118] = IES[114] - 2 * (INW - 1) / 8 - 4
    IES[119] = IES[115] + 2 * (INW - 1) / 8 + 6
    IES[120] = IES[116] - 3 * (INW - 1) / 8 - 10
    IES[121] = IES[117] + 2 * (INW - 1) / 8 + 10
    IES[122] = IES[118] - 2 * (INW - 1) / 8 - 10
    IES[123] = IES[119] + 2 * (INW - 1) / 8 + 10
    IES[124] = IES[120] - 2 * (INW - 1) / 8 - 10
    IES[125] = IES[117] - 6
    IES[126] = IES[118] - 6
    IES[127] = IES[119] + 4
    IES[128] = IES[120] + 4
    IES[129] = IES[121] - 6
    IES[130] = IES[122] - 6
    IES[131] = IES[123] + 4
    IES[132] = IES[124] + 4

    IEN[1] = IES[1] + (INB - 1) - 1
    IEN[2] = IES[2] + (INB - 1) - 1
    IEN[3] = IES[3] + (INB - 1) - 1
    IEN[4] = IES[4] + (INB - 1) - 1
    IEN[5] = IES[5] + 3 * (INB - 1) / 4 - 1
    IEN[6] = IES[6] + 3 * (INB - 1) / 4 - 1
    IEN[7] = IES[7] + 3 * (INB - 1) / 4 - 1
    IEN[8] = IES[8] + 3 * (INB - 1) / 4 - 1
    IEN[9] = IES[9] + (INB - 1) / 2 - 1
    IEN[10] = IES[10] + (INB - 1) / 2 - 1
    IEN[11] = IES[11] + (INB - 1) / 2 - 1
    IEN[12] = IES[12] + (INB - 1) / 2 - 1
    IEN[13] = IES[13] + 3 * (INB - 1) / 8 - 1
    IEN[14] = IES[14] + 3 * (INB - 1) / 8 - 1
    IEN[15] = IES[15] + 3 * (INB - 1) / 8 - 1
    IEN[16] = IES[16] + 3 * (INB - 1) / 8 - 1
    IEN[17] = IES[17] + 2 * (INB - 1) / 8 - 1
    IEN[18] = IES[18] + 2 * (INB - 1) / 8 - 1
    IEN[19] = IES[19] + 2 * (INB - 1) / 8 - 1
    IEN[20] = IES[20] + 2 * (INB - 1) / 8 - 1
    IEN[21] = IES[21] + 2 * (INB - 1) / 8 - 1
    IEN[22] = IES[22] + 2 * (INB - 1) / 8 - 1
    IEN[23] = IES[23] + 2 * (INB - 1) / 8 - 1
    IEN[24] = IES[24] + 2 * (INB - 1) / 8 - 1
    IEN[25] = IES[25] + 6 - 1
    IEN[26] = IES[26] + 6 - 1
    IEN[27] = IES[27] + 6 - 1
    IEN[28] = IES[28] + 6 - 1
    IEN[29] = IES[29] + 4 - 1
    IEN[30] = IES[30] + 4 - 1
    IEN[31] = IES[31] + 4 - 1
    IEN[32] = IES[32] + 4 - 1
    IEN[33] = IES[33] + 4 - 1
    IEN[34] = IES[34] + 4 - 1
    IEN[35] = IES[35] + 4 - 1
    IEN[36] = IES[36] + 4 - 1
    IEN[37] = IES[37] + 6 - 1
    IEN[38] = IES[38] + 6 - 1
    IEN[39] = IES[39] + 6 - 1
    IEN[40] = IES[40] + 6 - 1
    IEN[41] = IES[41] + 6 - 1
    IEN[42] = IES[42] + 6 - 1
    IEN[43] = IES[43] + 6 - 1
    IEN[44] = IES[44] + 6 - 1
    IEN[45] = IES[45] + (INI - 1) - 1
    IEN[46] = IES[46] + (INI - 1) - 1
    IEN[47] = IES[47] + (INI - 1) - 1
    IEN[48] = IES[48] + (INI - 1) - 1
    IEN[49] = IES[49] + 3 * (INI - 1) / 4 - 1
    IEN[50] = IES[50] + 3 * (INI - 1) / 4 - 1
    IEN[51] = IES[51] + 3 * (INI - 1) / 4 - 1
    IEN[52] = IES[52] + 3 * (INI - 1) / 4 - 1
    IEN[53] = IES[53] + (INI - 1) / 2 - 1
    IEN[54] = IES[54] + (INI - 1) / 2 - 1
    IEN[55] = IES[55] + (INI - 1) / 2 - 1
    IEN[56] = IES[56] + (INI - 1) / 2 - 1
    IEN[57] = IES[57] + 3 * (INI - 1) / 8 - 1
    IEN[58] = IES[58] + 3 * (INI - 1) / 8 - 1
    IEN[59] = IES[59] + 3 * (INI - 1) / 8 - 1
    IEN[60] = IES[60] + 3 * (INI - 1) / 8 - 1
    IEN[61] = IES[61] + 2 * (INI - 1) / 8 - 1
    IEN[62] = IES[62] + 2 * (INI - 1) / 8 - 1
    IEN[63] = IES[63] + 2 * (INI - 1) / 8 - 1
    IEN[64] = IES[64] + 2 * (INI - 1) / 8 - 1
    IEN[65] = IES[65] + 2 * (INI - 1) / 8 - 1
    IEN[66] = IES[66] + 2 * (INI - 1) / 8 - 1
    IEN[67] = IES[67] + 2 * (INI - 1) / 8 - 1
    IEN[68] = IES[68] + 2 * (INI - 1) / 8 - 1
    IEN[69] = IES[69] + 6 - 1
    IEN[70] = IES[70] + 6 - 1
    IEN[71] = IES[71] + 6 - 1
    IEN[72] = IES[72] + 6 - 1
    IEN[73] = IES[73] + 4 - 1
    IEN[74] = IES[74] + 4 - 1
    IEN[75] = IES[75] + 4 - 1
    IEN[76] = IES[76] + 4 - 1
    IEN[77] = IES[77] + 4 - 1
    IEN[78] = IES[78] + 4 - 1
    IEN[79] = IES[79] + 4 - 1
    IEN[80] = IES[80] + 4 - 1
    IEN[81] = IES[81] + 6 - 1
    IEN[82] = IES[82] + 6 - 1
    IEN[83] = IES[83] + 6 - 1
    IEN[84] = IES[84] + 6 - 1
    IEN[85] = IES[85] + 6 - 1
    IEN[86] = IES[86] + 6 - 1
    IEN[87] = IES[87] + 6 - 1
    IEN[88] = IES[88] + 6 - 1
    IEN[89] = IES[89] + (INW - 1) - 1
    IEN[90] = IES[90] + (INW - 1) - 1
    IEN[91] = IES[91] + (INW - 1) - 1
    IEN[92] = IES[92] + (INW - 1) - 1
    IEN[93] = IES[93] + 3 * (INW - 1) / 4 - 1
    IEN[94] = IES[94] + 3 * (INW - 1) / 4 - 1
    IEN[95] = IES[95] + 3 * (INW - 1) / 4 - 1
    IEN[96] = IES[96] + 3 * (INW - 1) / 4 - 1
    IEN[97] = IES[97] + (INW - 1) / 2 - 1
    IEN[98] = IES[98] + (INW - 1) / 2 - 1
    IEN[99] = IES[99] + (INW - 1) / 2 - 1
    IEN[100] = IES[100] + (INW - 1) / 2 - 1
    IEN[101] = IES[101] + 3 * (INW - 1) / 8 - 1
    IEN[102] = IES[102] + 3 * (INW - 1) / 8 - 1
    IEN[103] = IES[103] + 3 * (INW - 1) / 8 - 1
    IEN[104] = IES[104] + 3 * (INW - 1) / 8 - 1
    IEN[105] = IES[105] + 2 * (INW - 1) / 8 - 1
    IEN[106] = IES[106] + 2 * (INW - 1) / 8 - 1
    IEN[107] = IES[107] + 2 * (INW - 1) / 8 - 1
    IEN[108] = IES[108] + 2 * (INW - 1) / 8 - 1
    IEN[109] = IES[109] + 2 * (INW - 1) / 8 - 1
    IEN[110] = IES[110] + 2 * (INW - 1) / 8 - 1
    IEN[111] = IES[111] + 2 * (INW - 1) / 8 - 1
    IEN[112] = IES[112] + 2 * (INW - 1) / 8 - 1
    IEN[113] = IES[113] + 6 - 1
    IEN[114] = IES[114] + 6 - 1
    IEN[115] = IES[115] + 6 - 1
    IEN[116] = IES[116] + 6 - 1
    IEN[117] = IES[117] + 4 - 1
    IEN[118] = IES[118] + 4 - 1
    IEN[119] = IES[119] + 4 - 1
    IEN[120] = IES[120] + 4 - 1
    IEN[121] = IES[121] + 4 - 1
    IEN[122] = IES[122] + 4 - 1
    IEN[123] = IES[123] + 4 - 1
    IEN[124] = IES[124] + 4 - 1
    IEN[125] = IES[125] + 6 - 1
    IEN[126] = IES[126] + 6 - 1
    IEN[127] = IES[127] + 6 - 1
    IEN[128] = IES[128] + 6 - 1
    IEN[129] = IES[129] + 6 - 1
    IEN[130] = IES[130] + 6 - 1
    IEN[131] = IES[131] + 6 - 1
    IEN[132] = IES[132] + 6 - 1
    for I in range(1, NE+1):
        DATA_MESH.TH[I] = 0.0

    for I in range(1, 33+1):
        DATA_MESH.NO_S[I] = IES[4 * (I - 1) + 1]
        DATA_MESH.NO_S[I + 33] = IES[4 * (I - 1) + 2]

    for I in range(1, 33+1):
        if I >= 1 and I <= 6:  IR[I] = DB / 2
        if I >= 7 and I <= 9:  IR[I] = IXB[4] + IXB[5] + IXB[6]
        if I >= 10 and I <= 11: IR[I] = IXB[5] + IXB[6]
        if I >= 12 and I <= 17: IR[I] = DI / 2
        if I >= 18 and I <= 20: IR[I] = IXI[4] + IXI[5] + IXI[6]
        if I >= 21 and I <= 22: IR[I] = IXI[5] + IXI[6]
        if I >= 23 and I <= 28: IR[I] = DW / 2
        if I >= 29 and I <= 31: IR[I] = IXW[4] + IXW[5] + IXW[6]
        if I >= 32 and I <= 33: IR[I] = IXW[5] + IXW[6]

    for I in range(1, 33+1):
        if I >= 1 and I <= 11:  ICX[I] = DB / 2 + DW + DI
        if I >= 12 and I <= 22:  ICX[I] = DI / 2 + DW
        if I >= 23 and I <= 33:  ICX[I] = DW / 2

    for K in range(1, 33+1):
        N = IES[(K - 1) * 4 + 1]
        R1 = IR[K] * 1e0
        CX = ICX[K] * 1e0
        X1 = abs(DATA_MESH.X[MS[N, 1]] - CX)
        X2 = abs(DATA_MESH.X[MS[N, 3]] - CX)
        if X1 < X2:
            XX1 = X2
            XX2 = X1
        else:
            XX1 = X1
            XX2 = X2
        TKK[K] = THY(R1, XX1, XX2)

    EQB = ((DB / 2) ** 3 - (DB / 2 - IXB[1]) ** 3) / (
                (DB / 2 - IXB[1]) ** 3 - (DB / 2 - IXB[1] - IXB[2]) ** 3)
    EQI = ((DI / 2) ** 3 - (DI / 2 - IXI[1]) ** 3) / (
                (DI / 2 - IXI[1]) ** 3 - (DI / 2 - IXI[1] - IXI[2]) ** 3)
    EQW = ((DW / 2) ** 3 - (DW / 2 - IXW[1]) ** 3) / (
                (DW / 2 - IXW[1]) ** 3 - (DW / 2 - IXW[1] - IXW[2]) ** 3)
    TRB = (TKK[1] - TEQB) * EQB
    TRI = (TKK[12] - TEQI) * EQI
    TRW = (TKK[23] - TEQW) * EQW

    TKK[1] = TEQB
    TKK[12] = TEQI
    TKK[23] = TEQW

    TKK[2] = TKK[2] + TRB
    TKK[13] = TKK[13] + TRI
    TKK[24] = TKK[24] + TRW

    for K in range(1, 33+1):
        for M in range(1, 4+1):
            M1 = IES[(K - 1) * 4 + M]
            M2 = IEN[(K - 1) * 4 + M]
            for I in range(M1, M2+1):
                DATA_MESH.TH[I] = TKK[K]


def XYP():
    INB = DATA_MESH.INB
    INI = DATA_MESH.INI
    INW = DATA_MESH.INW
    NSBRD = DATA_MESH.NSBRD
    NSIRT = DATA_MESH.NSIRT
    NSIRD = DATA_MESH.NSIRD
    NSWRT = DATA_MESH.NSWRT
    NSWRD = DATA_MESH.NSWRD
    X = DATA_MESH.X
    Y = DATA_MESH.Y
    NP = DATA_MESH.NP
    SP = DATA_MESH.SP
    PROBR = DATA_MESH.PROBR
    PROIR = DATA_MESH.PROIR
    PROWR = DATA_MESH.PROWR
    NPBR = DATA_MESH.NPBR
    NPIR = DATA_MESH.NPIR

    SFTI = DATA_FORC.SFTI
    SFTW = DATA_FORC.SFTW

    DI = DATA_ROLL.DI
    DW = DATA_ROLL.DW

    TPBR = 0.0e0
    if SFTI < 0 and abs(SFTI - int(SFTI / SP) * SP) > SP / 2:
        DATA_MESH.KSFTI = int(SFTI / SP) - 1
    elif SFTI > 0 and abs(SFTI - int(SFTI / SP) * SP) > SP / 2:
        DATA_MESH.KSFTI = int(SFTI / SP) + 1
    else:
        DATA_MESH.KSFTI = int(SFTI / SP)

    if SFTW < 0 and abs(SFTW - int(SFTW / SP) * SP) > SP / 2:
        DATA_MESH.KSFTW = int(SFTW / SP) - 1
    elif SFTW > 0 and abs(SFTW - int(SFTW / SP) * SP) > SP / 2:
        DATA_MESH.KSFTW = int(SFTW / SP) + 1
    else:
        DATA_MESH.KSFTW = int(SFTW / SP)

    DATA_MESH.KSFTW = 0

    DATA_FORC.SFTI = DATA_MESH.KSFTI * SP
    DATA_FORC.SFTW = DATA_MESH.KSFTW * SP
    SFTI = DATA_FORC.SFTI
    SFTW = DATA_FORC.SFTW
    KK = NPBR + NPIR
    for I in range(NSIRT, KK+1):
        DATA_MESH.Y[I] = DATA_MESH.Y[I] - SFTI

    for I in range(NSWRT, NP+1):
        DATA_MESH.Y[I] = DATA_MESH.Y[I] - SFTW

    for I in range(1, INB+1):
        DATA_MESH.X[NSBRD - 1 + I] = DATA_MESH.X[NSBRD - 1 + I] + PROBR[I] * 0.001e0
        if DATA_MESH.X[NSBRD - 1 + I] < (DW + DI): DATA_MESH.X[NSBRD - 1 + I] = DW + DI

    for I in range(1, INI+1):
        DATA_MESH.X[NSIRT - 1 + I] = DATA_MESH.X[NSIRT - 1 + I] - PROIR[I] * 0.001e0
        DATA_MESH.X[NSIRD - 1 + I] = DATA_MESH.X[NSIRD - 1 + I] + PROIR[I] * 0.001e0

    for I in range(1, INI+1):
        if DATA_MESH.X[NSIRT - 1 + I] > (DW + DI): DATA_MESH.X[NSIRT - 1 + I] = DW + DI
        if DATA_MESH.X[NSIRD - 1 + I] < DW: DATA_MESH.X[NSIRD - 1 + I] = DW

    for I in range(1, INW+1):
        DATA_MESH.X[NSWRT - 1 + I] = DATA_MESH.X[NSWRT - 1 + I] - PROWR[I] * 0.001e0
        DATA_MESH.X[NSWRD - 1 + I] = DATA_MESH.X[NSWRD - 1 + I] + PROWR[I] * 0.001e0

    for I in range(1, INW+1):
        if DATA_MESH.X[NSWRT - 1 + I] > DW: DATA_MESH.X[NSWRT - 1 + I] = DW
        if DATA_MESH.X[NSWRD - 1 + I] < 0.0e0: DATA_MESH.X[NSWRD - 1 + I] = 0.0e0


def ROLLMESH():
    MES()
    XYS()
    THS()
    XYP()
