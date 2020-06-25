# -*- coding: UTF-8 -*-
import sys
import os

import qdarkstyle
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from TkPy3.tkpy3_tools.start import tkpy3_setup
from TkPy3.version import version as tkpy_version
from TkPy3.tkpy3_tools.pip_tools import tkpy_pip
from TkPy3.locale_dirs import images_icon_dir, static_dir
from TkPy3.tkpy3_tools.qt_load import LoadWidget


class InstallThread(QThread):
    done = pyqtSignal()
    ok = pyqtSignal(str)
    package_name = pyqtSignal(str)
    falsed = pyqtSignal(str)

    def __init__(self, parent=None, *packages):
        QThread.__init__(self, parent)
        self.packages = packages

    def run(self):
        pip = tkpy_pip()
        for i in self.packages:
            self.package_name.emit(i)
            if pip.upgrade(i):
                self.falsed.emit(i)
            else:
                self.ok.emit(i)
        self.done.emit()


class RelyDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.resize(800, 400)
        self.setWindowTitle(f'TkPy{tkpy_version} 依赖')
        self.setWindowIcon(
            QIcon(os.path.join(images_icon_dir, 'help_icons', 'tools.png')))
        self.layout = QVBoxLayout(self)
        self.text_show_label = QLabel()
        self.view_list = QListWidget()
        self.setLayout(self.layout)
        self.get_start()

    def get_start(self):
        with open(os.path.join(static_dir, 'relys.txt'), encoding='UTF-8') as f:
            count = 0
            for package_name in f.read().split('\n'):
                if package_name:
                    self.view_list.insertItem(
                        count, QListWidgetItem(package_name))
                    count += 1
        self.layout.addWidget(self.text_show_label)
        self.layout.addWidget(self.view_list)
        self.text_show_label.setText('<h4>所有依赖: </h4>')


class InstallDialog(RelyDialog):
    def __init__(self):
        RelyDialog.__init__(self)
        self.setWindowTitle('安装TkPy3的依赖')
        self.buttons_frame = QWidget()
        self.buttons_layout = QHBoxLayout(self.buttons_frame)
        self.buttons_frame.setLayout(self.buttons_layout)
        self.installButton = QPushButton()
        self.cancelButton = QPushButton()
        self.yesnoinstall = False
        self.layout.addWidget(self.buttons_frame)
        install_packages = []
        for i in range(self.view_list.count()):
            install_packages.append(self.view_list.item(i).text())
        self.install_process = InstallThread(self, *install_packages)
        self.init_ui()

    def init_ui(self):
        self.buttons_layout.addWidget(self.installButton)
        self.buttons_layout.addWidget(self.cancelButton)
        self.installButton.setText('现在安装所有依赖')
        self.cancelButton.setText('取消安装')
        self.cancelButton.clicked.connect(self.close)
        self.installButton.clicked.connect(self.install_relys)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        if self.yesnoinstall:
            event.accept()
            return
        res = QMessageBox.question(self, '取消安装', '是否取消安装? \n\
如果你想再次运行安装程序，请在终端运行 \n\npython -m TkPy3.tkpy3_tools.relys')
        if res == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def install_relys(self):
        def install():
            def done():
                show_label.setText('<p>安装完成</p>')
                exit_button.setDisabled(False)
                message.append('安装完成。')
            dialog = QDialog()
            dialog.resize(600, 600)
            dialog.setWindowFlags(Qt.WindowStaysOnTopHint |
                                  Qt.FramelessWindowHint)
            dialog.setWindowTitle('TkPy3安装')
            layout = QVBoxLayout()
            title_label = QLabel()
            show_label = QLabel()
            message = QTextBrowser()
            exit_button = QPushButton()
            load_processbar = LoadWidget()
            title_label.setText('<h1>TkPy3安装</h1>')
            exit_button.setText('退出')
            exit_button.setDisabled(True)
            layout.addWidget(title_label, 0)
            layout.addWidget(show_label)
            layout.addWidget(message)
            layout.addWidget(exit_button)
            message.addAction(QAction(load_processbar))
            dialog.setLayout(layout)
            install_packages = []
            for i in range(self.view_list.count()):
                install_packages.append(self.view_list.item(i).text())

            self.close()
            self.install_process.start()
            message.append('开始安装。')
            exit_button.clicked.connect(dialog.close)
            self.install_process.falsed.connect(
                lambda p: message.append(f'Package {p} 安装失败。'))
            self.install_process.ok.connect(
                lambda p: message.append(f'Package {p} 安装成功。'))
            self.install_process.package_name.connect(lambda text: (show_label.setText(
                f'<h3>正在安装中... ...</h3><p>正在安装: {text}</p>'), message.append(f'安装 {text}')))
            self.install_process.done.connect(done)
            dialog.exec_()

        res = QMessageBox.question(self, '问题', '是否现在安装所有依赖?')
        if res == QMessageBox.No:
            return
        self.yesnoinstall = True
        install()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tkpy3_setup(app)
    dialog = InstallDialog()
    sys.exit(dialog.exec_())
