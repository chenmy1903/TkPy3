import os

from PyQt5 import uic
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QToolButton, QGridLayout, QLineEdit, QPushButton, \
    QMessageBox, QComboBox, QStyleFactory
from PyQt5.QtCore import pyqtSignal, Qt
import sys

from TkPy3 import get_configs
from TkPy3.tkpy3_tools.start import tkpy3_setup


class ViewWidget(QDialog):
    ok = pyqtSignal()

    def __init__(self, ui_file: str):
        QDialog.__init__(self)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMaximizeButtonHint)
        try:
            uic.loadUi(ui_file, self)
        except Exception:
            QMessageBox.critical(self, '错误', '有些Widget无法正常导入，可能会显示错误。')
        finally:
            self.ok.emit()

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.ok.emit()
        super(ViewWidget, self).closeEvent(a0)


class QtUiFileView(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle('TkPy Ui 文件预览器')
        self.__layout = QGridLayout()
        self.ShowFileEntry = QLineEdit()
        self.loadFileButton = QToolButton()
        self.view_button = QPushButton('显示')
        self.__style = QComboBox()
        self.__init_ui()

    def __init_ui(self):
        self.view_button.setDisabled(True)
        self.__style.addItems(QStyleFactory.keys())
        self.__style.currentIndexChanged.connect(
            lambda index: QApplication.setStyle(QStyleFactory.create(QStyleFactory.keys()[index])))
        self.ShowFileEntry.setPlaceholderText('Ui文件目录')
        self.ShowFileEntry.textChanged.connect(lambda: self.view_button.setEnabled(
            False) if not self.ShowFileEntry.text() else self.view_button.setEnabled(True))
        self.loadFileButton.setText('...')
        self.loadFileButton.clicked.connect(self.__load)
        self.view_button.clicked.connect(self.__view)
        self.setLayout(self.__layout)
        self.ShowFileEntry.setWhatsThis('文件')
        self.loadFileButton.setWhatsThis('选择文件')
        self.view_button.setWhatsThis('显示Ui文件')
        self.__layout.addWidget(self.ShowFileEntry, 0, 0)
        self.__layout.addWidget(self.loadFileButton, 0, 1)
        self.__layout.addWidget(self.__style, 1, 0)
        self.__layout.addWidget(self.view_button, 1, 1)

    def __load(self):
        file_name, ok = QFileDialog.getOpenFileName(self, '打开文件', '', 'Qt Ui文件 (*.ui)')
        if ok:
            self.ShowFileEntry.setText(file_name)

    def __view(self):
        file_name = self.ShowFileEntry.text()
        if not os.path.isfile(file_name):
            return QMessageBox.warning(self, '警告', '文件目录无效')
        self.view_button.setEnabled(False)
        view = ViewWidget(file_name)
        view.ok.connect(lambda: self.view_button.setEnabled(True))
        view.exec_()

    def closeEvent(self, a0: QCloseEvent) -> None:
        QApplication.setStyle(QStyleFactory.create(get_configs()['window_style']))
        QDialog.closeEvent(self, a0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tkpy3_setup(app)
    dialog = QtUiFileView()
    sys.exit(dialog.exec_())
