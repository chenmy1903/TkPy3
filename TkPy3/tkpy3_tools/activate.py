# -*- coding: UTF-8 -*-
import sys
import random
from PyQt5.QtWidgets import *
from TkPy3.default_configs import get_configs, add_config
from TkPy3.tkpy3_tools.activate_game import run_activate_game, random_activation_codes


class ActivateDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        if not get_configs()['activate_codes']:
            random_activation_codes()
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
        self.activate_button.clicked.connect(self.activate_tkpy3)
        self.setLayout(self.layout)

    def create_activate_qwidget(self):
        print(random.choice(get_configs()['activate_codes']))
        layout = QFormLayout()
        activate_text = QLineEdit()
        activate_text.textChanged.connect(self.assert_activate_code)
        activate_text.setInputMask('>AAAA-AAAA-AAAA-AAAA;#')
        layout.addRow('请输入TkPy3的激活码: ', activate_text)
        self.activate.setLayout(layout)

    def activate_tkpy3(self):
        add_config('is_activate', True)
        QMessageBox.information(self, '提示', '您已激活成功')
        self.close()

    def assert_activate_code(self, code):
        if code in get_configs()['activate_codes'] + get_configs()['permanent_activation_codes']:
            self.activate_button.setDisabled(False)
        else:
            self.activate_button.setDisabled(True)

    def start_activate_code_game(self):
        QMessageBox.information(
            self, '如何获取激活码', '获取激活码规则：\n 玩飞船大战游戏，分数达到指定分数时即可获取激活码。')
        self.get_activate_code.setDisabled(True)
        score = run_activate_game()
        self.get_activate_code.setDisabled(False)
        if score >= 40:
            code = random.choice(get_configs()['activate_codes'])
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
