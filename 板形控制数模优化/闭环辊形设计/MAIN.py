import numpy as np
from TWOFEM import TWOFEM
import DATA_SHAP

BSHA = np.zeros(101) #支持辊辊形占据前81个节点
ISHA = np.zeros(101) #中间辊辊形占据前97个节点
WSHA = np.zeros(101) #工作辊辊形占据前81个节点

DB0 = 1150.0         #支持辊辊径
DI0 = 560.0          #中间辊辊径
DW0 = 470.0          #工作辊辊径

BW0 = 820.0          #带钢宽度
QS0 = 0.4            #单位板宽轧制力
SFTI0 = 100.0        #中间辊窜辊
BFI0 = 0.0           #中间辊弯辊
BFW0 = -35.0         #工作辊弯辊

TWOFEM(DB0,DI0,DW0,BW0,QS0,SFTI0,BFI0,BFW0,BSHA,ISHA,WSHA)

print(DATA_SHAP.CW)     #辊缝凸度
print(DATA_SHAP.PHCW)   #二次凸度
print(DATA_SHAP.PHCQ)   #四次凸度
print(DATA_SHAP.QBI)    #支持辊中间辊辊间接触压力不均匀度
print(DATA_SHAP.QIW)    #中间辊工作辊辊间接触压力不均匀度