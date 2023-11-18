from qfluentwidgets import MessageBox


def showMessageBox(title, content, parent=None):
    w = MessageBox(title, content, parent=parent)
    w.yesButton.setText('ok')
    w.cancelButton.setText('close')
    w.exec()