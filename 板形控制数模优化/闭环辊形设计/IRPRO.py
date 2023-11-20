import DATA_ROLL
import DATA_MESH
import numpy as np


def IRPRO():
    FLGCVC = 2
    DATA_MESH.SP = DATA_ROLL.LB / (DATA_MESH.INB - 1)
    GQGIFILE = ".\\IN\\IR.TXT"
    fcontent = np.loadtxt(GQGIFILE, dtype=np.float, delimiter='\t')
    XH = fcontent[:, 0]
    IRPR0 = fcontent[:, 1]
    for i in range(1, DATA_MESH.INI+1):
        DATA_MESH.PROIR[i] = DATA_MESH.PROIR[i] + IRPR0[i-1]

    OUTFILE = ".\\OUT\\IR.TXT"
    NO14 = open(OUTFILE, "w")
    NO14.write("  XH PROIR\n")
    for i in range(1, DATA_MESH.INI+1):
        wrstr = "%10.3f%10.3f\n" % (XH[i-1], DATA_MESH.PROIR[i])
        NO14.write(wrstr)
    NO14.close()
