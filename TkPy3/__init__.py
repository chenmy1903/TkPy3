# -*- coding: UTF-8 -*-
"""TkPy3 PythonIDE"""
import os
import random
import sys
import traceback
import datetime
import warnings

from pyqtgraph.examples.__main__ import ExampleLoader

from PyQt5.Qt import PYQT_VERSION_STR
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QCloseEvent
from PyQt5.QtWidgets import (
    QMainWindow,
    QStatusBar,
    QMenuBar,
    QMessageBox,
    QFileDialog,
    QApplication,
    QAction,
    QMenu,
    QMdiSubWindow)

from TkPy3.default_configs import add_config, add_diff, get_configs, reset_configs
from TkPy3.tkpy3_tools.base_mainwindow import BaseTkPy3, TkPyDockWidget
from TkPy3.tkpy3_tools.help import TkPyHelpWidget, HelpServer
from TkPy3.tkpy3_tools.start import setup as tkpy3_setup, set_icon_to_tkpy3
from TkPy3.tkpy3_tools.config_window import ConfigDialog
from TkPy3.tkpy3_tools.editor import BaseEditor, EditSubWindow
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

__author__ = 'chenmy1903'

pixmaps = {
    'run': os.path.join(images_icon_dir, 'editor_icons', 'run.png'),
    'shell': os.path.join(images_icon_dir, 'shell_icons', 'pyshell.ico'),
    'new_file': os.path.join(images_icon_dir, 'editor_icons', 'filenew.png'),
    'open_file': os.path.join(images_icon_dir, 'editor_icons', 'fileopen.png'),
    'save_file': os.path.join(images_icon_dir, 'editor_icons', "filesave.png"),
    'saveas_file': os.path.join(images_icon_dir, 'editor_icons', "filesaveas.png"),
    'exit': os.path.join(images_icon_dir, 'editor_icons', 'fileclose.png'),
    'restart': os.path.join(images_icon_dir, 'editor_icons', 'restart_window.jpg'),
    'close_all': os.path.join(images_icon_dir, 'editor_icons', "filecloseall.png"),
    'config': os.path.join(images_icon_dir, 'config_icons', 'advanced.png'),
    'python_file': os.path.join(images_icon_dir, 'file_icons', 'py.ico'),
}


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        add_diff()
        self.assert_activate()
        self.untitled_number = 0
        self.help_dock_open: bool = False
        self.not_save_list = []
        self.setWindowTitle(get_configs()['init_title'])
        self.tip = QStatusBar()
        self.setStatusBar(self.tip)
        self.base_tkpy = BaseTkPy3()
        self.help_dock = TkPyDockWidget()
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
        # ----------------------------------------
        self.FileToolsBar = self.addToolBar('文件')
        self.RunToolsBar = self.addToolBar('运行')
        self.HelpToolsBar = self.addToolBar('帮助')
        self.get_start()

    def get_start(self):
        self.add_editor_window()
        self.add_tools_bar_items()
        self.init_help_dock_widget()
        self.add_menus()
        self.setWindowState(Qt.WindowMaximized)
        self.help_dock.open_window.connect(lambda: self.setHelpWidgetOpen(True))
        self.help_dock.close_window.connect(lambda: self.setHelpWidgetOpen(False))

    def setHelpWidgetOpen(self, b: bool):
        self.help_dock_open = b
        print(b)

    def open_python_shell(self):
        pyshell_window = QMdiSubWindow()
        shell = TkPyShell()
        pyshell_window.setWindowIcon(QIcon(pixmaps['shell']))
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
                    ) + datetime.timedelta(days=random.randint(5, 40)))
                else:
                    add_config('end_activate_day', True)

        elif isinstance(get_configs()['end_activate_day'], bool):
            add_config('is_activate', True)

        elif get_configs()['end_activate_day'] <= datetime.date.today():
            add_config('is_activate', False)
            self.assert_activate()
        random_activation_codes()

    def open_activate_window(self):
        dialog = ActivateDialog()
        dialog.exec_()
        return dialog.permanent_activation

    def add_tools_bar_items(self):
        self.FileToolsBar.actionTriggered[QAction].connect(self.MenuEvents)
        self.FileToolsBar.addAction(QIcon(pixmaps["open_file"]), '打开')
        self.FileToolsBar.addAction(QIcon(pixmaps["new_file"]), '新建')
        self.FileToolsBar.addSeparator()
        self.FileToolsBar.addAction(QIcon(pixmaps['save_file']), '保存')
        self.FileToolsBar.addAction(QIcon(pixmaps['saveas_file']), '另存为')
        # --------------------------------------------------------------------
        self.RunToolsBar.actionTriggered[QAction].connect(self.MenuEvents)
        self.RunToolsBar.addAction(QIcon(pixmaps["run"]), '运行')
        # --------------------------------------------------------------------
        self.HelpToolsBar.actionTriggered[QAction].connect(self.MenuEvents)
        self.HelpToolsBar.addAction('帮助')

    def add_menus(self):
        self.Menu.triggered[QAction].connect(self.MenuEvents)
        new = self.FileMenu.addAction(QIcon(pixmaps["new_file"]), '新建')
        new.setShortcut('Ctrl+N')
        new.setStatusTip('新建文件')
        open = self.FileMenu.addAction(QIcon(pixmaps["open_file"]), '打开')
        open.setShortcut('Ctrl+O')
        open.setStatusTip('打开文件')
        self.FileMenu.addSeparator()
        save = self.FileMenu.addAction(QIcon(pixmaps['save_file']), '保存')
        save.setShortcut('Ctrl+S')
        save.setStatusTip('保存文件')
        saveas = self.FileMenu.addAction(QIcon(pixmaps['saveas_file']),
                                         '另存为')
        saveas.setStatusTip('另存为文件')
        saveas.setShortcut('Ctrl+Shift+S')
        save_all = self.FileMenu.addAction(QIcon(pixmaps['save_file']),
                                           "保存所有文件")
        save_all.setStatusTip('保存所有文件')
        self.FileMenu.addSeparator()
        close_window = self.FileMenu.addAction(QIcon(pixmaps["exit"]), '退出TkPy3')
        close_window.setShortcut('Ctrl+Q')
        close_window.setStatusTip('退出TkPy3主窗口')
        close_window = self.FileMenu.addAction(
            QIcon(pixmaps["restart"]), '重启TkPy3')
        close_window.setShortcut('Ctrl+Shift+R')
        close_window.setStatusTip('重启TkPy3')
        # --------------------------------------------------------------
        sort_windows = self.ViewMenu.addAction('排列子窗口')
        self.ViewMenu.addSeparator()
        sort_windows.setStatusTip('排列所有打开的内部主窗口')
        close_all_files = self.ViewMenu.addAction(
            QIcon(pixmaps["close_all"]),
            '关闭所有子窗口')
        close_all_files.setStatusTip('关闭所有子窗口')
        # --------------------------------------------------------------
        run = self.RunMenu.addAction(QIcon(pixmaps["run"]), '运行')
        run.setShortcut('F5')
        run.setStatusTip('运行代码')
        # --------------------------------------------------------------
        self.TerminalMenu.addAction(QIcon(pixmaps["shell"]), '打开Python Shell').setStatusTip('打开Python Shell')
        self.TerminalMenu.addAction(QIcon(pixmaps["shell"]), '打开终端').setStatusTip(
            '打开系统终端')
        self.TerminalMenu.addSeparator()
        config_tkpy3 = self.TerminalMenu.addAction(QIcon(pixmaps['config']), '设置')
        config_tkpy3.setStatusTip('设置TkPy3')
        self.TerminalMenu.addAction('重置TkPy3的设置').setStatusTip('重置TkPy3的设置')
        self.TerminalMenu.addSeparator()
        ToolsMenu: QMenu = self.TerminalMenu.addMenu('工具')
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
        self.HelpMenu.addAction('PyQt5示例').setStatusTip('打开PyQt5示例窗口')
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
TkPy3官网: https://github.com/chenmy1903/TkPy3

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
        elif event.text() == '重置TkPy3的设置':
            res = QMessageBox.question(self, '问题', '是否重置所有设置')
            if res == QMessageBox.Yes:
                reset_configs()
                QMessageBox.information(self, '提示', '重置完成。')
        elif event.text() == '打开终端':
            os.system(sys.executable + ' -u "' + os.path.join(
                BASE_DIR, 'SystemTemplates/run_terminal_script.py') + '"')
        elif event.text() == '保存所有文件':
            self.save_files()
        elif event.text() == '帮助':
            print(self.help_dock_open)
            if not self.help_dock_open:
                self.addDockWidget(Qt.RightDockWidgetArea, self.help_dock)
                print('opened')
            else:
                self.removeDockWidget(self.help_dock)
                print('closed')
        elif event.text() == 'PyQt5示例':
            loader = ExampleLoader()
            loader.setWindowTitle('TkPy3 PyQt5示例')

    def open_file(self):
        file_name, ok = QFileDialog.getOpenFileName(
            self, '打开文件', '', 'Python 源文件 (*.py *.pyw)')
        if ok:
            self.add_editor_window(TkPyEventType(file_name))

    def init_help_dock_widget(self):
        self.help_dock.setWindowTitle('TkPy3帮助')
        self.help_dock.setWidget(TkPyHelpWidget())
        self.help_dock.setAllowedAreas(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea)

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
            self.untitled_number += 1
        else:
            file_name = event.text()

        def not_save():
            sub.setWindowTitle(
                '*' + (edit.file_name or get_configs()['new_file_title'] + ' ' + str(sub.number)) + '*')
            if sub.widget().file_name not in self.not_save_list:
                self.not_save_list.append(sub.widget().file_name)
            sub.setSave(False)

        def save():
            sub.setWindowTitle(
                edit.file_name or get_configs()['new_file_title'] + ' ' + str(sub.number))
            if sub.widget().file_name in self.not_save_list:
                self.not_save_list.remove(sub.widget().file_name)
            sub.setSave(True)

        sub = EditSubWindow()
        sub.setNumber(self.untitled_number)
        sub.resize(700, 500)
        sub.setWindowTitle(get_configs()[
                               'new_file_title'] + ' ' + str(sub.number) if not file_name else os.path.abspath(
            file_name))
        sub.setWindowIcon(QIcon(pixmaps["python_file"]))
        edit = BaseEditor(sub)
        if file_name:
            edit.open(file_name)
        sub.setWidget(edit)
        edit.not_save.connect(not_save)
        edit.save.connect(save)
        self.windows_mdi.addSubWindow(sub)
        sub.show()

    def closeEvent(self, event: QCloseEvent) -> None:
        if self.not_save_list:
            res = QMessageBox.question(self, 'TkPy3 - 问题', '还有文件未保存,是否保存所有文件之后退出TkPy3？',
                                       QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                                       QMessageBox.Cancel)

            if res == QMessageBox.Yes:
                if self.save_files(on_exit=True):
                    event.accept()
                else:
                    event.ignore()
            elif res == QMessageBox.No:
                event.accept()
            elif res == QMessageBox.Cancel:
                event.ignore()

    def save_files(self, *, on_exit=False):
        for window in self.windows_mdi.subWindowList():
            widget = window.widget()
            if widget.file_name:
                widget.save_file(widget.file_name)
            elif not window.save or not on_exit:
                file_name, ok = QFileDialog.getSaveFileName(
                    self, f'保存文件 {window.windowTitle().replace("*", "")}', '',
                    'Python 文件 (*.py *.pyw)')
                if ok:
                    widget.save_file(file_name)
                else:
                    return False
        return True

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

    def show_warning(self, message: str):
        QMessageBox.warning(self, '警告', message)
        warnings.warn(message)

    def restart_window(self):
        res = QMessageBox.question(self, '问题', '是否重启TkPy3')
        if res == QMessageBox.Yes:
            self.close()
            self.show()


def main():
    server = HelpServer()
    server.start()
    app = QApplication(sys.argv)
    tkpy3_setup(app)
    widget = MainWindow()
    widget.show()
    return_code = app.exec_()
    server.terminate()
    if return_code:
        raise TkPyQtError('TkPy3在运行中出现错误。') from None
    return return_code


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as error:
        MainWindow().show_error_and_exit()
        raise TkPyIdeError(str(error)) from error
