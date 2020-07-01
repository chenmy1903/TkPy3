from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QTreeView, QTextBrowser, QLineEdit, QSplitter, \
    QVBoxLayout, QGroupBox, QCheckBox, QPushButton

from TkPy3.tkpy3_tools.core import is_venv
from TkPy3.tkpy3_tools.pip_tools import tkpy_pip

import sys

pip = tkpy_pip()


class PythonPackageInstallToolsWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowTitle('Python Package Install Tools')
        self.search = QLineEdit()
        self.package_install_splitter = QSplitter(Qt.Horizontal)
        self.package_tree = QTreeView()
        self.package_info = QGroupBox()
        self.package_info_text = QTextBrowser()
        self.install_button = QPushButton('安装')
        self.user_install = QCheckBox()
        self.package_layout = QVBoxLayout()
        self.__init_ui()

    def __init_ui(self):
        self.prepare_package()
        self.user_install.setText('用户安装')
        if is_venv():
            self.user_install.setDisabled(True)
        self.search.setPlaceholderText('搜索')
        self.package_info.setTitle('信息')
        self.setLayout(self.package_layout)
        self.package_layout.addWidget(self.search, 0)
        self.package_layout.addWidget(self.package_install_splitter, 0)
        self.package_layout.addWidget(self.install_button, 0)
        self.package_install_splitter.addWidget(self.package_tree)
        self.package_install_splitter.addWidget(self.package_info)
        self.__make_package_info()

    def prepare_package(self):
        pass

    def __make_package_info(self):
        package_info = self.package_info
        layout = QVBoxLayout()
        layout.addWidget(self.package_info_text, 0)
        layout.addWidget(self.user_install, 0)
        package_info.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = PythonPackageInstallToolsWidget()
    widget.show()
    sys.exit(app.exec_())
