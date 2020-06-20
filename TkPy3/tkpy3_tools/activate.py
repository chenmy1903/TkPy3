# -*- coding: UTF-8 -*-
import sys
import random
import time

from PyQt5.QtWidgets import *
from TkPy3.default_configs import get_configs, add_config
from TkPy3.tkpy3_tools.activate_game import run_activate_game, random_activation_codes
from TkPy3.tkpy3_tools.start import tkpy3_setup


class ActivateDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        if not get_configs()['activate_codes']:
            random_activation_codes()
        self.setWindowTitle('激活TkPy3')
        self.permanent_activation = False
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
        self.layout.addWidget(QLabel('<h1>TkPy3激活</h1>'), 0, 0)
        self.view.addWidget(self.activate)
        self.view.setCurrentIndex(0)
        self.layout.addWidget(self.view, 1, 0)
        self.layout.addWidget(self.get_activate_code, 2, 0)
        self.layout.addWidget(self.activate_button, 2, 1)
        self.activate_button.clicked.connect(self.activate_tkpy3)
        self.assert_activate_code()
        self.get_activate_code.setWhatsThis('没有激活码?通过玩游戏获取激活码。')
        self.setLayout(self.layout)

    def create_activate_qwidget(self):
        layout = QFormLayout()
        activate_text = QLineEdit()
        activate_text.textChanged.connect(self.assert_activate_code)
        activate_text.setInputMask('>AAAA-AAAA-AAAA-AAAA;_')
        activate_text.setWhatsThis('在此处输入激活码')
        layout.addRow('请输入TkPy3的激活码: ', activate_text)
        self.activate.setLayout(layout)

    def activate_tkpy3(self):
        add_config('is_activate', True)
        QMessageBox.information(self, '提示', '您已激活成功')
        self.close()

    def assert_activate_code(self, code: str = ""):
        if code in get_configs()['activate_codes'] + get_configs()['permanent_activation_codes']:
            self.activate_button.setWhatsThis('点击<b>此处</b>激活TkPy3')
            self.activate_button.setDisabled(False)
            if code in get_configs()['permanent_activation_codes']:
                self.permanent_activation = True
        elif not code.replace('-', ''):
            self.activate_button.setWhatsThis('请输入激活码')
            self.activate_button.setDisabled(True)
        elif len(code) != len('AAAA-AAAA-AAAA-AAAA'):
            self.activate_button.setWhatsThis('激活码输入位数不对')
            self.activate_button.setDisabled(True)
        else:
            self.activate_button.setWhatsThis('无法激活TkPy3 (激活码错误)')
            self.activate_button.setDisabled(True)

    def start_activate_code_game(self):
        max_score = random.randint(20, 40)
        res = QMessageBox.question(
            self, '如何获取激活码', f'获取激活码规则：\n 玩飞船大战游戏，分数达到{max_score}分时即可获取激活码。')
        if res == QMessageBox.No:
            return
        self.setDisabled(True)
        score = run_activate_game()
        self.setDisabled(False)
        if score >= max_score:
            code = random.choice(get_configs()['activate_codes'])
            time.sleep(1)
            QMessageBox.information(self, '提示', f'激活码获取成功，激活码是{code}，将自动为您将激活码复制到剪贴板。')
            clipboard = QApplication.clipboard()
            clipboard.clear()
            clipboard.setText(code)

    def create_evaluate_qwidget(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tkpy3_setup(app)
    dialog = ActivateDialog()
    sys.exit(dialog.exec_())
