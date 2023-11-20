import DATA_ROLL
import DATA_MESH
import numpy as np


def WRPRO():
    DATA_MESH.SP = DATA_ROLL.LB / (DATA_MESH.INB - 1)
    GQGWFILE = ".\\IN\\WR.TXT"
    fcontent = np.loadtxt(GQGWFILE, dtype=np.float, delimiter='\t')
    WRPR0 = fcontent[:, 1]
    for i in range(1, DATA_MESH.INW+1):
        DATA_MESH.PROWR[i] = DATA_MESH.PROWR[i] + WRPR0[i-1]

    OUTFILE = ".\\OUT\\WR.TXT"
    NO16 = open(OUTFILE, "w")
    NO16.write("  XH PROWR\n")
    for i in range(1, DATA_MESH.INW+1):
        wrstr = "%10.3f%10.3f\n" % ((i-1)*DATA_MESH.SP, DATA_MESH.PROWR[i])
        NO16.write(wrstr)
    NO16.close()