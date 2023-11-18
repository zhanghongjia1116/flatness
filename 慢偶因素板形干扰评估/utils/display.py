from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class PandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None


class NumberedTableModel(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1] + 1  # 加上一列用于显示行号

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                if index.column() == 0:
                    return str(index.row() + 1)  # 显示行号
                else:
                    return str(self._data.iloc[index.row(), index.column() - 1])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if col == 0:
                return '序号'
            else:
                return self._data.columns[col - 1]
        return None


def display_dataframe_in_tableview(table_view, df, column_labels=None):
    # 创建一个QStandardItemModel来存储数据
    model = QStandardItemModel()

    if column_labels is None:
        column_labels = list(df.columns)

    model.setHorizontalHeaderLabels(column_labels)  # 设置表头

    for row in range(df.shape[0]):
        for col in range(df.shape[1]):
            item = QStandardItem(str(df.iat[row, col]))
            item.setTextAlignment(Qt.AlignCenter)
            model.setItem(row, col, item)

    table_view.setModel(model)
    table_view.resizeColumnsToContents()  # 调整列宽以适应数据`
