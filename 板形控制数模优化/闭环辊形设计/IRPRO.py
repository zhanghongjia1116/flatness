from DATA_ROLL import DataRoll
from DATA_MESH import DataMesh
import numpy as np


def IRPRO():
    data_roll = DataRoll()
    data_mesh = DataMesh()
    data_mesh.SP = data_roll.LB / (data_mesh.INB - 1)
    GQGIFILE = ".\\IN\\IR.TXT"
    fcontent = np.loadtxt(GQGIFILE, delimiter='\t')
    XH = fcontent[:, 0]
    IRPR0 = fcontent[:, 1]
    for i in range(1, data_mesh.INI + 1):
        data_mesh.PROIR[i] = data_mesh.PROIR[i] + IRPR0[i - 1]

    OUTFILE = ".\\output\\IR.TXT"
    NO14 = open(OUTFILE, "w")
    NO14.write("  XH PROIR\n")
    for i in range(1, data_mesh.INI + 1):
        wrstr = "%10.3f%10.3f\n" % (XH[i - 1], data_mesh.PROIR[i])
        NO14.write(wrstr)
    NO14.close()
