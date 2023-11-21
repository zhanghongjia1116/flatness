import numpy as np

from DATA_ROLL import DataRoll
from DATA_MESH import DataMesh
from DATA_FORC import DataForc
from DATA_SHAP import DataShap
from BRPRO import BRPRO
from IRPRO import IRPRO
from WRPRO import WRPRO
from ROLLMESH import ROLLMESH
from ROLLFEM import ROLLFEM
from POSTPROC import POSTPROC


FILE1 = ".\\OUT\\CW.TXT"
FILE2 = ".\\OUT\\QBI.TXT"
FILE3 = ".\\OUT\\QIW.TXT"
FILE4 = ".\\OUT\\GAP.TXT"
FILE5 = ".\\OUT\\FORCE.TXT"
NO1 = open(FILE1, "w")
NO2 = open(FILE2, "w")
NO3 = open(FILE3, "w")
NO4 = open(FILE4, "w")
NO5 = open(FILE5, "w")

BRPRO()
IRPRO()
WRPRO()

NO1.write(" NUM DB DI DW BW QS SFTI BFI BFW CW WDG PHCW PHCQ EDG QBI QIW NYBI NYIW\n")
NUM = 0
I = np.arange(1, DATA_MESH.INB + 1)
Res2 = DATA_MESH.SP * (I - (DATA_MESH.INB + 1) / 2)
NO2.write(("{:>4d}" + "{:>10.4f}" * DATA_MESH.INB + "\n").format(*([NUM] + Res2.tolist())))

I = np.arange(1, DATA_MESH.INI + 1)
Res3 = DATA_MESH.SP * (I - (DATA_MESH.INI + 1) / 2)
NO3.write(("{:>4d}" + "{:>12.4f}" * DATA_MESH.INI + "\n").format(*([NUM] + Res3.tolist())))

I = np.arange(1, DATA_MESH.INW + 1)
Res4 = DATA_MESH.SP * (I - (DATA_MESH.INW + 1) / 2)
NO4.write(("{:>4d}" + "{:>12.4f}" * DATA_MESH.INW + "\n").format(*([NUM] + Res4.tolist())))

NO5.write(" RSX1 RSX2 RSX3 RSX4 RSX5 RSX6 RSX7 FX FY\n")

NUM = 1

for I in range(1, 1 + 1):
    DATA_ROLL.DB = 1150.0  # 支持辊直径
    DATA_ROLL.DI = 560.0   # 中间辊直径
    DATA_ROLL.DW = 470.0   # 工作辊直径

    for N in range(1, 6 + 1):
        if N == 1: DATA_FORC.BW = 820.0  # 带钢宽度mm
        if N == 2: DATA_FORC.BW = 1020.0
        if N == 3: DATA_FORC.BW = 1220.0
        if N == 4: DATA_FORC.BW = 1420.0
        if N == 5: DATA_FORC.BW = 1620.0
        if N == 6: DATA_FORC.BW = 1820.0
        for V in range(1, 5 + 1):
            DATA_FORC.QS = 0.4  # 单位板宽轧制力 t/mm
            if V == 2: DATA_FORC.QS = 0.8
            if V == 3: DATA_FORC.QS = 1.2
            if V == 4: DATA_FORC.QS = 1.6
            if V == 5: DATA_FORC.QS = 2.0
            # for J in range(2, 2 + 1):
            for J in range(1, 3 + 1):
                DATA_FORC.SFTI = 100.0  # 中间辊窜辊  负值等实际的正窜辊
                if J == 2: DATA_FORC.SFTI = 0.0
                if J == 3: DATA_FORC.SFTI = -100.0
                # for K in range(1, 1 + 1):
                for K in range(1, 3 + 1):
                    DATA_FORC.BFI = 0.0   # 中间辊弯辊
                    if K == 2: DATA_FORC.BFI = 65.0
                    if K == 3: DATA_FORC.BFI = 130.0
                    # for M in range(2, 2 + 1):
                    for M in range(1, 3 + 1):
                        DATA_FORC.BFW = -35.0   # 工作辊弯辊
                        if M == 2: DATA_FORC.BFW = 0.0
                        if M == 3: DATA_FORC.BFW = 50.0
                        ROLLMESH()  # 生成网格
                        ROLLFEM()   # 有限元
                        POSTPROC()  # 导出结果
                        # CW 辊缝凸度   PHCW二次凸度    PHCQ 四次凸度    EDG 边降    QBI 支持辊与中间辊接触应力分布不均匀度
                        NO1.write(("{:>4d}" + "{:>8.1f}" * 15 + "{:>4d}" + "{:>4d}" + "\n").format(*([NUM] + [
                            DATA_ROLL.DB] + [DATA_ROLL.DI] + [DATA_ROLL.DW] + [DATA_FORC.BW] + [DATA_FORC.QS] +
                            [DATA_FORC.SFTI] + [DATA_FORC.BFI] + [DATA_FORC.BFW] + [DATA_SHAP.CW] + [DATA_SHAP.WDG] +
                            [DATA_SHAP.PHCW] + [DATA_SHAP.PHCQ] + [DATA_SHAP.EDG] + [DATA_SHAP.QBI] + [DATA_SHAP.QIW] +
                            [DATA_MESH.NYBI] + [DATA_MESH.NYIW])))

                        print(("{:>4d}" + "{:>8.1f}" * 11 + "\n").format(*([NUM] + [DATA_FORC.BW] + [DATA_FORC.QS] +
                            [DATA_FORC.SFTI] + [DATA_FORC.BFI] +[DATA_FORC.BFW] + [DATA_SHAP.CW] +[DATA_SHAP.PHCW] +
                            [DATA_SHAP.PHCQ] +[DATA_SHAP.EDG] + [DATA_SHAP.QBI] + [DATA_SHAP.QIW])))

                        NO4.write(("{:>4d}" + "{:>10.4f}" * DATA_MESH.INW + "\n").format(
                            *([NUM] + DATA_MESH.PRFL[1:DATA_MESH.INW+1, 6].tolist())))

                        NO2.write(("{:>4d}" + "{:>12.4f}" * DATA_MESH.INB + "\n").format(
                            *([NUM] + DATA_MESH.RDT[1:DATA_MESH.INB + 1, 8].tolist())))

                        NO3.write(("{:>4d}" + "{:>12.4f}" * DATA_MESH.INI + "\n").format(
                            *([NUM] + DATA_MESH.RDT[1:DATA_MESH.INI + 1, 9].tolist())))

                        NO5.write(("{:>4d}" + "{:>10.2f}" * 9 + "\n").format(
                            *([NUM] + DATA_MESH.RSX[1:(9+1)].tolist())))

                        NUM = NUM + 1

NO1.close()
NO2.close()
NO3.close()
NO4.close()
NO5.close()
