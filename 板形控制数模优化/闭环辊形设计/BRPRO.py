from DATA_ROLL import DataRoll
from DATA_MESH import DataMesh
import numpy as np


def BRPRO():
    data_mesh = DataMesh()
    data_roll = DataRoll()
    data_mesh.SP = data_roll.LB / (data_mesh.INB - 1)
    GQGBFILE = ".\\IN\\BR.TXT"
    fcontent = np.loadtxt(GQGBFILE, delimiter='\t')
    XH = fcontent[:, 0]
    BRPR0 = fcontent[:, 1]
    for i in range(1, data_mesh.INB+1):
        data_mesh.PROBR[i] = data_mesh.PROBR[i] + BRPR0[i-1]

    OUTFILE = ".\\output\\BR.TXT"
    NO12 = open(OUTFILE, "w")
    NO12.write("  XH PROBR\n")
    for i in range(1, data_mesh.INB+1):
        wrstr = "%10.3f%10.3f\n" % (XH[i-1], data_mesh.PROBR[i])
        NO12.write(wrstr)
    NO12.close()
