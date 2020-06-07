# -*- coding: UTF-8 -*-
import os
import sys
import traceback

import qdarkstyle

from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from TkPy3.default_configs import add_diff, get_configs
from TkPy3.tkpy3_tools.config_window import ConfigDialog
from TkPy3.tkpy3_tools.editor import BaseEditor
from TkPy3.tkpy3_tools.events import TkPyEventType
from TkPy3.locale_dirs import BASE_DIR, images_icon_dir


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        add_diff()
        self.not_save_list = []
        self.setWindowTitle(get_configs()['init_title'])
        self.tools_bar = self.addToolBar('')
        self.tip = QStatusBar()
        self.setStatusBar(self.tip)
        self.windows_mdi = QMdiArea()
        self.setCentralWidget(self.windows_mdi)
        self.Menu: QMenuBar = self.menuBar()
        self.FileMenu = self.Menu.addMenu('文件')
        self.EditMenu = self.Menu.addMenu('编辑')
        self.SelectMenu = self.Menu.addMenu('选择')
        self.ViewMenu = self.Menu.addMenu('查看')
        self.GoToMenu = self.Menu.addMenu('转到')
        self.RunMenu = self.Menu.addMenu('运行')
        self.TermMenu = self.Menu.addMenu('终端')
        self.HelpMenu = self.Menu.addMenu('帮助')
        self.get_start()

    def get_start(self):
        self.add_editor_window()
        self.add_tools_bar_items()
        self.add_menus()
        self.tools_bar.setMovable(False)

    def add_tools_bar_items(self):
        self.tools_bar.actionTriggered[QAction].connect(self.MenuEvents)
        self.tools_bar.addAction(QIcon(os.path.join(images_icon_dir, 'editor_icons', 'filenew.png')),
                                 '新建').setStatusTip('新建文件')
        self.tools_bar.addAction(QIcon(os.path.join(images_icon_dir, 'editor_icons', 'fileopen.png')), '打开'). \
            setStatusTip(
            '打开文件')
        self.tools_bar.addSeparator()
        self.tools_bar.addAction(QIcon(os.path.join(images_icon_dir, 'editor_icons', 'filesave.png')), '保存'). \
            setStatusTip('保存文件')
        self.tools_bar.addAction(QIcon(os.path.join(images_icon_dir, 'editor_icons', 'filesaveas.png')), '另存为'). \
            setStatusTip('另存为文件')

    def add_menus(self):
        self.Menu.triggered[QAction].connect(self.MenuEvents)
        new = self.FileMenu.addAction(QIcon(os.path.join(images_icon_dir, 'editor_icons', 'filenew.png')), '新建')
        new.setShortcut('Ctrl+N')
        new.setStatusTip('新建文件')
        open = self.FileMenu.addAction(
            QIcon(os.path.join(images_icon_dir, 'editor_icons', 'fileopen.png')), '打开')
        open.setShortcut('Ctrl+O')
        open.setStatusTip('打开文件')
        self.FileMenu.addSeparator()
        save = self.FileMenu.addAction(QIcon(os.path.join(images_icon_dir, 'editor_icons', "filesave.png")),
                                       '保存')
        save.setShortcut('Ctrl+S')
        save.setStatusTip('保存文件')
        saveas = self.FileMenu.addAction(QIcon(os.path.join(images_icon_dir, 'editor_icons', "filesaveas.png")),
                                         '另存为')
        saveas.setStatusTip('另存为文件')
        saveas.setShortcut('Ctrl+Shift+S')
        self.FileMenu.addSeparator()
        close_window = self.FileMenu.addAction(QIcon(os.path.join(images_icon_dir, 'editor_icons', 'fileclose.png')),
                                               '退出TkPy3')
        close_window.setShortcut('Ctrl+Q')
        close_window.setStatusTip('退出TkPy3主窗口')
        # --------------------------------------------------------------
        sort_windows = self.ViewMenu.addAction('排列子窗口')
        self.ViewMenu.addSeparator()
        sort_windows.setStatusTip('排列所有打开的内部主窗口')
        close_all_files = self.ViewMenu.addAction(
            QIcon(os.path.join(images_icon_dir, 'editor_icons', "filecloseall.png")),
            '关闭所有子窗口')
        close_all_files.setStatusTip('关闭所有子窗口')
        # --------------------------------------------------------------
        config_tkpy3 = self.TermMenu.addAction(QIcon(os.path.join(images_icon_dir, 'config_icons', 'advanced.png')),
                                               '设置')
        config_tkpy3.setStatusTip('设置TkPy3')
        # --------------------------------------------------------------
        format_code = self.EditMenu.addAction('格式化代码')
        format_code.setShortcut('Ctrl+Alt+L')
        format_code.setStatusTip('使用AutoPEP8格式化代码')

    def MenuEvents(self, event):
        if event.text() == '新建':
            self.add_editor_window()
        elif event.text() == '打开':
            self.open_file()
        elif event.text() == '关闭所有窗口':
            self.windows_mdi.closeAllSubWindows()
        elif event.text() == '排列子窗口':
            self.windows_mdi.tileSubWindows()
        elif event.text() == '设置':
            self.open_config_dialog_window()
        elif event.text() == '退出TkPy3':
            res = QMessageBox.question(self, 'TkPy3 - 问题', '是否退出TkPy3?',
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if res == QMessageBox.Yes:
                self.close()
        elif event.text() == '格式化代码':
            self.windows_mdi.activeSubWindow().widget().autopep8_fix_code()
        elif event.text() in ['保存', '另存为']:
            window = self.windows_mdi.activeSubWindow()
            widget = window.widget()
            if widget.file_name and event.text() != '另存为':
                file_name, ok = widget.file_name, True
            else:
                file_name, ok = QFileDialog.getSaveFileName(self, event.text(), '', 'Python 源文件 (*.py *.pyw)')
            if ok:
                widget.save_file(file_name)

    def open_file(self):
        file_name, ok = QFileDialog.getOpenFileName(self, '打开文件', '', 'Python 源文件 (*.py *.pyw)')
        if ok:
            self.add_editor_window(TkPyEventType(file_name))

    def open_config_dialog_window(self):
        dialog = ConfigDialog()
        dialog.exec_()

    def add_editor_window(self, event=TkPyEventType()):
        if event.text() == 'TkPy3 Event type':
            file_name = ""
        else:
            file_name = event.text()
        sub = QMdiSubWindow()
        sub.resize(700, 500)
        sub.setWindowTitle(get_configs()['new_file_title'] if not file_name else os.path.abspath(file_name))
        sub.setWindowIcon(QIcon(os.path.join(images_icon_dir, 'file_icons', 'py.ico')))
        edit = BaseEditor()
        if file_name:
            edit.open(file_name)
        sub.setWidget(edit)
        self.windows_mdi.addSubWindow(sub)
        sub.show()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        if self.not_save_list:
            res = QMessageBox.question(self, 'TkPy3 - 问题', '还有文件未保存？是否退出保存之后TkPy3？',
                                       QMessageBox.Ok | QMessageBox.No | QMessageBox.Cancel,
                                       QMessageBox.Cancel)
            if res == QMessageBox.Yes:
                self.save_files()
                event.accept()
            elif res == QMessageBox.No:
                event.accept()
            elif res == QMessageBox.Cancel:
                event.ignore()

    def save_files(self):
        pass

    def show_error_and_exit(self):
        sys.last_type, sys.last_value, last_tb = ei = sys.exc_info()
        sys.last_traceback = last_tb
        try:
            lines = traceback.format_exception(ei[0], ei[1], last_tb.tb_next)
            if sys.excepthook is sys.__excepthook__:
                error_message = ''.join(lines)
            else:
                sys.excepthook(ei[0], ei[1], last_tb)
        finally:
            last_tb = ei = None
        QMessageBox.critical(self, '错误', f'TkPy3出现严重错误，需要退出。\n错误：\n\n{error_message}')
        self.close()


def main():
    app = QApplication(sys.argv)
    if get_configs()['open_dark_style']:
        style = qdarkstyle.load_stylesheet_pyqt5()
        app.setStyleSheet(style)
    app.setWindowIcon(QIcon(get_configs()['init_icon_path']))
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    try:
        main()
    except Exception:
        MainWindow().show_error_and_exit()
