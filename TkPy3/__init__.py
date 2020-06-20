# -*- coding: UTF-8 -*-
import os
import platform
import sys
import traceback

from PyQt5 import QtGui
from PyQt5.Qt import PYQT_VERSION_STR
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from TkPy3.default_configs import add_config, add_diff, get_configs
from TkPy3.tkpy3_tools.base_mainwindow import BaseTkPy3
from TkPy3.tkpy3_tools.start import setup as tkpy3_setup
from TkPy3.tkpy3_tools.config_window import ConfigDialog
from TkPy3.tkpy3_tools.editor import BaseEditor
from TkPy3.tkpy3_tools.events import TkPyEventType
from TkPy3.locale_dirs import BASE_DIR, images_icon_dir
from TkPy3.tkpy3_tools.relys import RelyDialog, InstallDialog
from TkPy3.tkpy3_tools.markdown_tools import PyQt5MarkdownDialog
from TkPy3.version import version as __version__
from TkPy3.tkpy3_tools.errors import TkPyIdeError, TkPyQtError
from TkPy3.tkpy3_tools.activate import ActivateDialog
from TkPy3.tkpy3_tools.activate_game import random_activation_codes
from TkPy3.tkpy3_tools.report import BugReportWindow, NewFunctionReportWindow
from TkPy3.tkpy3_tools.pyshell import TkPyShell
import datetime

__author__ = 'chenmy1903'


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        add_diff()
        self.assert_activate()
        self.not_save_list = []
        self.setWindowTitle(get_configs()['init_title'])
        self.tools_bar = self.addToolBar('')
        self.tip = QStatusBar()
        self.setStatusBar(self.tip)
        self.base_tkpy = BaseTkPy3()
        self.windows_mdi = self.base_tkpy.mdi
        self.setCentralWidget(self.base_tkpy)
        self.Menu: QMenuBar = self.menuBar()
        self.FileMenu = self.Menu.addMenu('文件')
        self.EditMenu = self.Menu.addMenu('编辑')
        self.SelectMenu = self.Menu.addMenu('选择')
        self.ViewMenu = self.Menu.addMenu('查看')
        self.GoToMenu = self.Menu.addMenu('转到')
        self.RunMenu = self.Menu.addMenu('运行')
        self.TerminalMenu = self.Menu.addMenu('终端')
        self.HelpMenu = self.Menu.addMenu('帮助')
        self.get_start()

    def get_start(self):
        self.add_editor_window()
        self.add_tools_bar_items()
        self.add_menus()
        self.tools_bar.setMovable(False)
        self.setWindowState(Qt.WindowMaximized)

    def open_python_shell(self):
        pyshell_window = QMdiSubWindow()
        shell = TkPyShell()
        pyshell_window.setWindowIcon(
            QIcon(os.path.join(images_icon_dir, 'shell_icons', 'pyshell.ico')))
        pyshell_window.resize(700, 500)
        pyshell_window.setWindowTitle('Python Shell')
        pyshell_window.setWidget(shell)
        self.windows_mdi.addSubWindow(pyshell_window)
        pyshell_window.show()

    def assert_activate(self, reactivate=False):
        if not get_configs()['is_activate'] or reactivate:
            permanent_activation = self.open_activate_window()
            if not get_configs()['is_activate']:
                QMessageBox.critical(self, '错误', 'TkPy3未激活，即将退出TkPy3。')
                sys.exit()
            else:
                add_config('is_activate', True)
                if not permanent_activation:
                    add_config('end_activate_day', datetime.date.today(
                    ) + datetime.timedelta(days=30))
                else:
                    add_config('end_activate_day', True)

        elif isinstance(get_configs()['end_activate_day'], bool):
            add_config('is_activate', True)
            random_activation_codes()

        elif get_configs()['end_activate_day'] <= datetime.date.today():
            add_config('is_activate', False)
            self.assert_activate()
            random_activation_codes()

    def open_activate_window(self):
        dialog = ActivateDialog()
        dialog.exec_()
        return dialog.permanent_activation

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
        new = self.FileMenu.addAction(
            QIcon(os.path.join(images_icon_dir, 'editor_icons', 'filenew.png')), '新建')
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
        close_window = self.FileMenu.addAction(
            QIcon(os.path.join(images_icon_dir, 'editor_icons', 'restart_window.jpg')),
            '重启TkPy3')
        close_window.setShortcut('Ctrl+Shift+R')
        close_window.setStatusTip('重启TkPy3')
        # --------------------------------------------------------------
        sort_windows = self.ViewMenu.addAction('排列子窗口')
        self.ViewMenu.addSeparator()
        sort_windows.setStatusTip('排列所有打开的内部主窗口')
        close_all_files = self.ViewMenu.addAction(
            QIcon(os.path.join(images_icon_dir, 'editor_icons', "filecloseall.png")),
            '关闭所有子窗口')
        close_all_files.setStatusTip('关闭所有子窗口')
        # --------------------------------------------------------------
        run = self.RunMenu.addAction(QIcon(os.path.join(images_icon_dir, 'editor_icons', 'run.png')),
                                     '运行')
        run.setShortcut('F5')
        run.setStatusTip('运行代码')
        # --------------------------------------------------------------
        self.TerminalMenu.addAction(QIcon(
            os.path.join(images_icon_dir, 'shell_icons', 'pyshell.ico')), '打开Python Shell').setStatusTip(
            '打开Python Shell')
        self.TerminalMenu.addSeparator()
        config_tkpy3 = self.TerminalMenu.addAction(QIcon(os.path.join(images_icon_dir, 'config_icons', 'advanced.png')),
                                                   '设置')
        config_tkpy3.setStatusTip('设置TkPy3')
        self.TerminalMenu.addSeparator()
        ToolsMenu = self.TerminalMenu.addMenu('工具')
        ToolsMenu.addAction('Markdown转Html').setStatusTip(
            'TkPy3工具: Markdown转Html')
        # --------------------------------------------------------------
        select_all = self.SelectMenu.addAction('选择全部')
        select_all.setStatusTip('选择全部文字')
        select_all.setShortcut('Ctrl+A')
        # --------------------------------------------------------------
        paste = self.EditMenu.addAction('粘贴')
        paste.setShortcut('Ctrl+V')
        paste.setStatusTip('粘贴')
        paste = self.EditMenu.addAction('复制')
        paste.setShortcut('Ctrl+C')
        paste.setStatusTip('复制选中的文字')
        paste = self.EditMenu.addAction('剪切')
        paste.setShortcut('Ctrl+X')
        paste.setStatusTip('剪切选中的文字')
        self.EditMenu.addSeparator()
        undo = self.EditMenu.addAction('撤销')
        undo.setShortcut('Ctrl+Z')
        undo.setStatusTip('撤销上一个操作')
        redo = self.EditMenu.addAction('撤销')
        redo.setShortcut('Ctrl+Y')
        redo.setStatusTip('撤回上一个操作')
        self.EditMenu.addSeparator()
        format_code = self.EditMenu.addAction('格式化代码')
        format_code.setShortcut('Ctrl+Alt+L')
        format_code.setStatusTip('使用AutoPEP8格式化代码')
        # --------------------------------------------------------------
        self.HelpMenu.addAction('关于TkPy3').setStatusTip('关于TkPy3')
        self.HelpMenu.addAction('关于PyQt5').setStatusTip('关于PyQt5')
        self.HelpMenu.addSeparator()
        relyMenu = self.HelpMenu.addMenu('依赖管理')
        relyMenu.addAction('TkPy3的依赖').setStatusTip('查看TkPy3的依赖')
        relyMenu.addAction('安装TkPy3的所有依赖').setStatusTip('安装TkPy3的所有依赖')
        self.HelpMenu.addSeparator()
        self.HelpMenu.addAction('重新激活TkPy3').setStatusTip('打开TkPy3激活窗口以重新激活TkPy3')
        self.HelpMenu.addSeparator()
        self.HelpMenu.addAction('报告Bug').setStatusTip('在GitHub上报告TkPy3的Bug')
        self.HelpMenu.addAction('报告TkPy3的功能改进').setStatusTip(
            '在Gitter上报告TkPy3的功能改进')
        # --------------------------------------------------------------

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
            if self.window_mdi_activate_is_pyshell():
                return
            self.windows_mdi.activeSubWindow().widget().autopep8_fix_code()
        elif event.text() in ['保存', '另存为']:
            if self.window_mdi_activate_is_pyshell():
                return
            window = self.windows_mdi.activeSubWindow()
            widget = window.widget()
            if widget.file_name and event.text() != '另存为':
                file_name, ok = widget.file_name, True
            else:
                file_name, ok = QFileDialog.getSaveFileName(
                    self, event.text(), '', 'Python 源文件 (*.py *.pyw)')
            if ok:
                widget.save_file(file_name)
        elif event.text() == '关于TkPy3':
            QMessageBox.information(self, '关于TkPy3', f"""TkPy3一个使用PyQt5制作的TkPy IDE
TkPy3: {__version__}
PyQt5: {PYQT_VERSION_STR}

TkPy3激活:
激活到期时间: {get_configs()['end_activate_day'] 
            if not isinstance(get_configs()['end_activate_day'], bool) else "永久激活"}
-----------------------------------
{__author__} ©2020 All Rights Reserved.
                """)
        elif event.text() == 'TkPy3的依赖':
            dialog = RelyDialog()
            dialog.exec_()
        elif event.text() == '安装TkPy3的所有依赖':
            dialog = InstallDialog()
            dialog.exec_()
        elif event.text() == '运行':
            if self.window_mdi_activate_is_pyshell():
                return
            window = self.windows_mdi.activeSubWindow()
            widget = window.widget()
            self.MenuEvents(TkPyEventType('保存'))
            if widget.file_name:
                widget.run()
        elif event.text() == '粘贴':
            window = self.windows_mdi.activeSubWindow()
            widget = window.widget()
            text = widget.text
            text.paste()
        elif event.text() == '复制':
            window = self.windows_mdi.activeSubWindow()
            widget = window.widget()
            text = widget.text
            text.copy()
        elif event.text() == '剪切':
            window = self.windows_mdi.activeSubWindow()
            widget = window.widget()
            text = widget.text
            text.cut()
        elif event.text() == '撤销':
            window = self.windows_mdi.activeSubWindow()
            widget = window.widget()
            text = widget.text
            text.undo()
        elif event.text() == '撤回':
            window = self.windows_mdi.activeSubWindow()
            widget = window.widget()
            text = widget.text
            text.redo()
        elif event.text() == '选择全部':
            window = self.windows_mdi.activeSubWindow()
            widget = window.widget()
            text = widget.text
            text.selectAll()
        elif event.text() == '关于PyQt5':
            QMessageBox.aboutQt(self, '关于PyQt5')
        elif event.text() == 'Markdown转Html':
            dialog = PyQt5MarkdownDialog()
            dialog.exec_()
        elif event.text() == '重启TkPy3':
            self.restart_window()
        elif event.text() == '报告Bug':
            bug_report_window = BugReportWindow()
            bug_report_window.exec_()
        elif event.text() == '打开Python Shell':
            self.open_python_shell()
        elif event.text() == '报告TkPy3的功能改进':
            NewFunctionReportWindow().exec_()
        elif event.text() == '关闭所有子窗口':
            self.windows_mdi.closeAllSubWindows()
        elif event.text() == '重新激活TkPy3':
            self.assert_activate(True)

    def open_file(self):
        file_name, ok = QFileDialog.getOpenFileName(
            self, '打开文件', '', 'Python 源文件 (*.py *.pyw)')
        if ok:
            self.add_editor_window(TkPyEventType(file_name))

    def window_mdi_activate_is_pyshell(self):
        if not self.window_mdi_activate_is_not_none():
            return True
        return isinstance(self.windows_mdi.activeSubWindow().widget(), TkPyShell)

    def window_mdi_activate_is_not_none(self):
        try:
            getattr(self.windows_mdi.activeSubWindow(), 'widget')
        except Exception:
            return False
        return True

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
        sub.setWindowTitle(get_configs()[
                               'new_file_title'] if not file_name else os.path.abspath(file_name))
        sub.setWindowIcon(
            QIcon(os.path.join(images_icon_dir, 'file_icons', 'py.ico')))
        edit = BaseEditor(sub)
        if file_name:
            edit.open(file_name)
        sub.setWidget(edit)
        edit.not_save.connect(lambda: sub.setWindowTitle(
            '*' + (edit.file_name or get_configs()['new_file_title']) + '*'))
        edit.save.connect(lambda: sub.setWindowTitle(
            edit.file_name or get_configs()['new_file_title']))
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
        for window in self.windows_mdi.subWindowList():
            widget = window.widget()
            widget.save_file()

    def save_open_windows(self):
        file_names = []
        for window in self.windows_mdi.subWindowList():
            widget = window.widget()
            if widget.file_name:
                file_names.append(widget.file_name)
        print(file_names)

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
        QMessageBox.critical(
            self, '错误', f'TkPy3出现严重错误，需要退出。\n错误：\n\n{error_message}')
        sys.exit(1)

    def restart_window(self):
        res = QMessageBox.question(self, '问题', '是否重启TkPy3')
        if res == QMessageBox.Yes:
            self.close()
            self.show()


def main():
    app = QApplication(sys.argv)
    tkpy3_setup(app)
    widget = MainWindow()
    widget.show()
    return_code = app.exec_()
    if return_code:
        raise TkPyQtError('TkPy3在运行中出现错误。') from None

    return return_code


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as error:
        MainWindow().show_error_and_exit()
        raise TkPyIdeError(str(error)) from error
