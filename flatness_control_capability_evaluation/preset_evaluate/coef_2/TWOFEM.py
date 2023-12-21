from flatness_control_capability_evaluation.preset_evaluate.coef_2 import DATA_FORC
from flatness_control_capability_evaluation.preset_evaluate.coef_2 import DATA_MESH
from flatness_control_capability_evaluation.preset_evaluate.coef_2 import DATA_ROLL
from flatness_control_capability_evaluation.preset_evaluate.coef_2 import DATA_SHAP
from flatness_control_capability_evaluation.preset_evaluate.coef_2.POSTPROC import POSTPROC
from flatness_control_capability_evaluation.preset_evaluate.coef_2.ROLLFEM import ROLLFEM
from flatness_control_capability_evaluation.preset_evaluate.coef_2.ROLLMESH import ROLLMESH


def TWOFEM(DB0, DI0, DW0, BW0, QS0, SFTI0, BFI0, BFW0, PROBR0, PROIR0, PROWR0):
    DATA_MESH.PROBR = PROBR0  # 81个节点
    DATA_MESH.PROIR = PROIR0  # 97个节点
    DATA_MESH.PROWR = PROWR0  # 81个节点
    DATA_MESH.SP = DATA_ROLL.LB / (DATA_MESH.INB - 1)

    DATA_ROLL.DB = DB0
    DATA_ROLL.DI = DI0
    DATA_ROLL.DW = DW0

    DATA_FORC.BW = BW0
    DATA_FORC.QS = QS0
    DATA_FORC.SFTI = SFTI0
    DATA_FORC.BFI = BFI0
    DATA_FORC.BFW = BFW0

    ROLLMESH()
    ROLLFEM()
    POSTPROC()

    return DATA_SHAP.CW, DATA_SHAP.PHCW, DATA_SHAP.PHCQ, DATA_SHAP.QBI, DATA_SHAP.QIW
