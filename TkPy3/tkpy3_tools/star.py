from PyQt5.QtGui import QCloseEvent
from helium import *
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QDialogButtonBox, QFormLayout, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal, Qt

from TkPy3.tkpy3_tools.start import tkpy3_setup


class StarProcess(QThread):
    user_name: str
    password: str
    ok = pyqtSignal()

    def run(self):
        star(self.user_name, self.password)
        self.ok.emit()


def star(user_name: str, password: str):
    start_chrome('https://github.com/login')
    write(user_name, 'Username')
    write(password, 'password')
    press(ENTER)
    go_to('https://github.com/chenmy1903/TkPy3')
    try:
        click('star')
    except LookupError:
        kill_browser()
        return False
    kill_browser()
    return True


class StarDialog(QDialog):
    def __init__(self):
        super(StarDialog, self).__init__()
        self.is_star = False
        self.setWindowTitle('点亮TkPy的Star - 登录Github')
        self.star_process = StarProcess()
        self.star_process.ok.connect(self.close)
        self.git_layout = QFormLayout()
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.username.setPlaceholderText('用户名')
        self.password.setPlaceholderText('密码')
        self.button_box = QDialogButtonBox()
        self.button_box.addButton('登录并点亮Star', QDialogButtonBox.AcceptRole)
        self.button_box.addButton('取消', QDialogButtonBox.RejectRole)
        self.button_box.accepted.connect(self.star)
        self.button_box.rejected.connect(self.close)
        self.init_ui()

    def init_ui(self):
        self.setLayout(self.git_layout)
        self.git_layout.addRow('用户名: ', self.username)
        self.git_layout.addRow('密码: ', self.password)
        self.git_layout.addWidget(self.button_box)
        self.password.setEchoMode(QLineEdit.Password)

    def star(self):
        res = QMessageBox.question(self, '问题', '确认账号和密码?')
        if res == QMessageBox.No:
            return
        if self.is_star:
            return
        self.is_star = True
        self.star_process.user_name = self.username.text()
        self.star_process.password = self.password.text()
        self.star_process.start()
        self.setEnabled(False)
        self.setWindowTitle('操作中... ...')

    def closeEvent(self, event: QCloseEvent) -> None:
        if self.is_star:
            event.accept()
        else:
            res = QMessageBox.question(self, '问题', '是否退出?', QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
            if res == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = StarDialog()
    tkpy3_setup(app)
    sys.exit(dialog.exec_())
