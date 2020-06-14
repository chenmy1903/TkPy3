# -*- coding: UTF-8 -*-
import sys
import time
import random
import pyperclip
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread
from TkPy3.default_configs import add_config, get_configs
from TkPy3.tkpy3_tools.activate_game import run_activate_game


def get_one_activate_code():
    code = ''
    chars = list('QWERTYUIOPASDFGHJKLZCVBNM')
    for i in range(4):
        for i in range(4):
            code += random.choice(chars)
        code += '-'
    return code[0:-1]


def random_activation_codes():
    codes = []
    for i in range(5):
        codes.append(get_one_activate_code())
    add_config('activate_codes', codes)


class ActivateDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle('激活TkPy3')
        self.layout = QGridLayout()
        self.view = QStackedWidget()
        self.activate = QWidget()
        self.evaluate = QWidget()
        self.get_activate_code = QPushButton('没有激活码?获取它！')
        self.activate_button = QPushButton()
        self.init_ui()

    def init_ui(self):
        self.create_activate_qwidget()
        self.activate_button.setText('激活')
        self.get_activate_code.clicked.connect(self.start_activate_code_game)
        self.activate_button.setDisabled(True)
        self.layout.addWidget(self.activate, 0, 0)
        self.layout.addWidget(self.get_activate_code, 1, 0)
        self.layout.addWidget(self.activate_button, 1, 1)
        self.setLayout(self.layout)

    def create_activate_qwidget(self):
        layout = QFormLayout()
        activate_text = QLineEdit()
        activate_text.setInputMask('XXXX-XXXX-XXXX-XXXX;X')
        layout.addRow('请输入TkPy3的激活码: ', activate_text)
        self.activate.setLayout(layout)
    
    def activate_tkpy(self):
        code = get_configs()['input_activate_code']

    def start_activate_code_game(self):
        QMessageBox.information(
            self, '如何获取激活码', '获取激活码规则：\n 玩飞船大战游戏，分数达到指定分数时即可获取激活码。')
        self.get_activate_code.setDisabled(True)
        score = run_activate_game()
        self.get_activate_code.setDisabled(False)    
        if score > 3:
            code = random.choice(get_configs()['activate_codes'])
            print(code)
            QMessageBox.information(self, '提示', f'激活码获取成功，激活码是{code}，将自动为您将激活码复制到剪贴板。')
            clipboard = QApplication.clipboard()
            clipboard.clear()
            clipboard.setText(code)

    def create_evaluate_qwidget(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = ActivateDialog()
    sys.exit(dialog.exec_())
