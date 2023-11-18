from enum import Enum

from qfluentwidgets import FluentIconBase, Theme, getIconColor


class MyIcon(FluentIconBase, Enum):
    # 异常板形监测溯源
    实际板形 = '实际板形'
    工艺参数 = '工艺参数'
    相关性分析 = '相关性分析'
    贡献度分析 = '贡献度分析'

    # 板形质量评价
    板形描述 = '板形描述'
    一卷全长 = '一卷全长'
    一卷头中尾 = '一卷头中尾'
    全年质量 = '全年质量'
    综合评价 = '综合评价'

    # 慢偶因素板形干扰评估
    CLASS = 'class'
    LIQUID = 'liquid'
    REDUCTION = '压平'
    MATERIAL = '材料'
    ROLLING = 'rolling'
    STOP = '急停'

    # 板形调控功效挖掘
    压下倾斜 = '压下倾斜'
    工作辊 = '工作辊'
    中间辊弯辊 = '中间辊弯辊'
    CVC窜辊 = 'CVC窜辊'

    # 板形生成数据建模
    有无 = '有'
    多分类 = '分类'
    回归 = '回归'

    # 板形控制能力评价
    预设定值 = '预设定值'
    动态控制 = '控制'
    CVC = 'CVC'
    支撑辊 = '支撑辊'

    # 板形控制数模优化
    预设定表格 = '预设定表格'
    预设定机理 = '预设定机理'
    反馈控制 = '反馈控制'
    设计 = '闭环辊形设计'

    def path(self, theme=Theme.AUTO):
        return f":/icons/icons/{self.value}_{getIconColor(theme)}.svg"
