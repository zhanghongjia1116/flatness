# -*- coding: utf-8 -*-

"""
Module implementing Frame_4.
"""

from PyQt5.QtWidgets import QFrame
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from accidental_interference.roller.controller.myplot import MyFigure
from accidental_interference.roller.view.Ui_flatness import Ui_Frame_4


class Frame_4(QFrame, Ui_Frame_4):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (defaults to None)
        @type QWidget (optional)
        """
        super(Frame_4, self).__init__(parent)
        self.setupUi(self)
        try:
            self.textEdit_2.setVisible(False)
        except:
            pass

        # self.flat = IUStatistics()
        # self.flat.signalIUplot.connect(self.faltness_plot)

    def flatness_plot(self):
        try:
            self.horizontalLayout.itemAt(0).widget().deleteLater()
            self.horizontalLayout_2.itemAt(0).widget().deleteLater()
        except:
            pass
        self.data = self.textEdit_2.toPlainText().replace('[', '').replace(']', '').replace(' ', '').split(',')
        data = list(map(float, self.data))
        print(len(data))
        y = data
        F = MyFigure(width=8, height=10, dpi=100)
        axes = F.fig.add_subplot(111)
        # y = list
        axes.plot(y)
        axes.set_xlabel('采样点')
        axes.set_ylabel('IU值')
        self.horizontalLayout.addWidget(F)
        bar = NavigationToolbar(F, self)
        self.horizontalLayout_2.addWidget(bar)
        # self.lineEdit.setText(list)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    ui = Frame_4()
    ui.show()
    sys.exit(app.exec_())
