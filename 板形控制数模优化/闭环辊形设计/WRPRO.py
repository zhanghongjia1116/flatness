from DATA_ROLL import DataRoll
from DATA_MESH import DataMesh
import numpy as np


def WRPRO():
    data_roll = DataRoll()
    data_mesh = DataMesh()
    data_mesh.SP = data_roll.LB / (data_mesh.INB - 1)
    GQGWFILE = ".\\IN\\WR.TXT"
    fcontent = np.loadtxt(GQGWFILE, delimiter='\t')
    WRPR0 = fcontent[:, 1]
    for i in range(1, data_mesh.INW+1):
        data_mesh.PROWR[i] = data_mesh.PROWR[i] + WRPR0[i-1]

    OUTFILE = ".\\output\\WR.TXT"
    NO16 = open(OUTFILE, "w")
    NO16.write("  XH PROWR\n")
    for i in range(1, data_mesh.INW+1):
        wrstr = "%10.3f%10.3f\n" % ((i-1)*data_mesh.SP, data_mesh.PROWR[i])
        NO16.write(wrstr)
    NO16.close()