import DATA_ROLL
import DATA_MESH
import numpy as np


def BRPRO():
    DATA_MESH.SP = DATA_ROLL.LB / (DATA_MESH.INB - 1)
    GQGBFILE = ".\\IN\\BR.TXT"
    fcontent = np.loadtxt(GQGBFILE, dtype=np.float, delimiter='\t')
    XH = fcontent[:, 0]
    BRPR0 = fcontent[:, 1]
    for i in range(1, DATA_MESH.INB+1):
        DATA_MESH.PROBR[i] = DATA_MESH.PROBR[i] + BRPR0[i-1]

    OUTFILE = ".\\OUT\\BR.TXT"
    NO12 = open(OUTFILE, "w")
    NO12.write("  XH PROBR\n")
    for i in range(1, DATA_MESH.INB+1):
        wrstr = "%10.3f%10.3f\n" % (XH[i-1], DATA_MESH.PROBR[i])
        NO12.write(wrstr)
    NO12.close()
