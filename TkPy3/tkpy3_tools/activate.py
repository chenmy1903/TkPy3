# -*- encoding: UTF-8 -*-
import sys
from PyQt5.QtWidgets import *

class ActivateDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle('激活TkPy3')
        self.layout = QGridLayout()
        self.view = QStackedWidget()
        self.activate = QWidget()
        self.evaluate = QWidget()
        self.activate_button = QPushButton(self)
        self.init_ui()
    
    def init_ui(self):
        self.create_activate_qwidget()
        self.activate_button.setText('激活')
        self.activate_button.setDisabled(True)
        self.layout.addWidget(self.activate, 0, 2)
        self.layout.addWidget(self.activate_button, 1, 2)
        self.setLayout(self.layout)

    def create_activate_qwidget(self):
        layout = QFormLayout()
        activate_text = QLineEdit()
        activate_text.setInputMask('XXXX-XXXX-XXXX-XXXXX;X')
        layout.addRow('请输入TkPy3的激活码: ', activate_text)
        self.activate.setLayout(layout)

    def create_evaluate_qwidget(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = ActivateDialog()
    sys.exit(dialog.exec_())

