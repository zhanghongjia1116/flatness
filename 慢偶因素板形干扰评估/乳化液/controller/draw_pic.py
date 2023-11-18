import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.lines import Line2D


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=10, height=8, dpi=100):
        # 配置中文显示
        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        plt.rcParams["toolbar"] = "toolbar2"

        self.fig = Figure(figsize=(width, height), dpi=dpi)  # 新建一个figure

        # self.axes = self.fig.add_subplot(111)  # 建立一个子图，如果要建立复合图，可以在这里修改
        self.canvas = FigureCanvas(self.fig)
        # self.axes.hold(False)  # 每次绘图的时候不保留上一次绘图的结果
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        self.resize(width, height)
        '''定义FigureCanvas的尺寸策略，这部分的意思是设置FigureCanvas，使之尽可能的向外填充空间。'''
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        # Adjust layout to fill the entire canvas
        self.fig.tight_layout()

    def avgIUAndLiquid(self, count, avg_list, length_list):
        self.ax = self.fig.add_subplot(111)
        int_length_list = [int(length) for length in length_list]
        scatter = self.ax.scatter(x=count, y=avg_list, c=int_length_list, cmap='plasma')
        # 添加图例
        self.ax.legend(*scatter.legend_elements(), title='钢卷号')

        # 对数据进行排序
        sorted_indices = sorted(range(len(count)), key=lambda k: count[k])
        count_sorted = [count[i] for i in sorted_indices]
        avg_list_sorted = [avg_list[i] for i in sorted_indices]

        # 连接散点的线段
        self.ax.plot(count_sorted, avg_list_sorted, color='lightblue', linewidth=1)
        # self.ax.plot(count, avg_list, color='lightblue', linewidth=1)
        # 在每个散点上添加标签
        for x, y, length in zip(count, avg_list, int_length_list):
            self.ax.text(x, y - 0.1, str(length), ha='center', va='top', rotation=45)  # 这里调整为向上偏移

        self.ax.grid()
        self.ax.set_xlabel('浓度')
        self.ax.set_ylabel('IU均值')
        self.ax.set_title('浓度与IU均值关系')
        # plt.savefig(r'./特定时间/浓度与IU均值关系.jpg', dpi=500)

    def 板坯牌号IU钢卷数变化散点(
            self,
            policy_count, avg_list_sub, volumes_list_sub, avg_list_all_time,
            volumes_list_all_time, x_range
    ):
        self.ax = self.fig.add_subplot(111)
        scatter_1 = self.ax.scatter(x=policy_count, y=avg_list_sub, c=volumes_list_sub, cmap='plasma',
                                    label='选择时间段',
                                    marker='^')

        # 添加颜色条
        cbar_1 = plt.colorbar(scatter_1, ax=self.ax)  # 使用 ax 参数指定颜色条的位置
        # 设置颜色条标签
        cbar_1.set_label('选择时间段钢卷数量')

        scatter_2 = self.ax.scatter(x=x_range, y=avg_list_all_time, c=volumes_list_all_time, cmap='plasma',
                                    # marker='^',
                                    label='所有时间段钢卷数量')
        # 添加颜色条
        cbar_2 = plt.colorbar(scatter_2, ax=self.ax)  # 使用 ax 参数指定颜色条的位置
        # 设置颜色条标签
        cbar_2.set_label('所有时间段钢卷数量')

        # 创建一个用于图例的虚拟散点图，只显示普通的三角形标记，无颜色
        # 添加图例元素
        legend_elements = [
            Line2D([0], [0], marker='^', color='gray', label='选择时间段', markersize=8, linestyle='None'),
            Line2D([0], [0], marker='o', color='gray', label='所有时间段', markersize=8, linestyle='None')
        ]

        self.ax.grid()
        # 添加图例，使用虚拟散点图来显示标签
        self.ax.legend(handles=legend_elements)
        self.ax.set_xlabel('板坯牌号')
        # self.ax.set_xticks(policy_count, rotation='vertical')
        # plt.xticks(x_range, sorted_policy_count.astype(int))
        # 设置 x 轴刻度
        self.ax.set_xticks(policy_count)
        self.ax.set_xticklabels(policy_count, rotation='vertical')
        self.ax.set_ylabel('IU均值')
        self.ax.set_title('板坯牌号与IU均值关系')

    def liquidBoxDiagram(self, 浓度, PH值, 电导率, 月份):
        self.fig.subplots_adjust(left=0.060, right=0.945, top=0.940, bottom=0.080, hspace=0.335)
        self.fig.suptitle('年度乳化液数据箱线图')
        self.axes1 = self.fig.add_subplot(311)
        self.axes1.boxplot(浓度)
        self.axes1.set_ylabel('乳化液浓度')
        self.axes1.set_xlabel('月份')
        # 设置横轴标签
        self.axes1.set_xticklabels(月份)
        self.axes1.grid(True)

        self.axes2 = self.fig.add_subplot(312)
        self.axes2.boxplot(PH值)
        # 设置y轴范围(0, 14)
        self.axes2.set_ylim(5, 6)
        self.axes2.set_ylabel('乳化液PH值')
        self.axes2.set_xlabel('月份')
        self.axes2.grid(True)
        # 设置横轴标签
        self.axes2.set_xticklabels(月份)

        self.axes3 = self.fig.add_subplot(313)
        self.axes3.boxplot(电导率)
        self.axes3.set_ylabel('乳化液电导率')
        self.axes3.set_xlabel('月份')
        self.axes3.grid(True)
        # 设置横轴标签
        self.axes3.set_xticklabels(月份)

    # def qualityAndIULine(self, volumes_list_all_time, ):
