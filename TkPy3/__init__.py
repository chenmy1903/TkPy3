# -*- coding: UTF-8 -*-
"""TkPy3 PythonIDE"""
from __future__ import print_function, unicode_literals

import os
import random
import cgitb
import sys
import datetime
import warnings
import webbrowser

from PyQt5.Qt import PYQT_VERSION_STR
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QCloseEvent, QDropEvent, QDragEnterEvent
from PyQt5.QtWidgets import (
    QMainWindow,
    QStatusBar,
    QMenuBar,
    QMessageBox,
    QFileDialog,
    QApplication,
    QAction,
    QMenu,
    QMdiArea,
    QInputDialog,
    QWhatsThis,
)

from TkPy3.default_configs import add_config, add_diff, get_configs, reset_configs
from TkPy3.tkpy3_tools.gnu_gettext_extensions import _
from TkPy3.tkpy3_tools.base_mainwindow import BaseTkPy3, TkPyDockWidget, LineCountButton
from TkPy3.tkpy3_tools.core import windows_set_taskbar_icon
from TkPy3.tkpy3_tools.file_reopen import all_file_types
from TkPy3.tkpy3_tools.help import TkPyHelpWidget, HelpServer, PythonPackageHelpDialog
from TkPy3.tkpy3_tools.qt_file_view import QtUiFileView
from TkPy3.tkpy3_tools.star import StarDialog
from TkPy3.tkpy3_tools.start import setup as tkpy3_setup, set_icon_to_tkpy3, check_system
from TkPy3.tkpy3_tools.config_window import ConfigDialog
from TkPy3.tkpy3_tools.editor import BaseEditor, EditSubWindow
from TkPy3.tkpy3_tools.events import TkPyEventType, get_event
from TkPy3.locale_dirs import BASE_DIR, pixmaps
from TkPy3.tkpy3_tools.relys import RelyDialog, InstallDialog
from TkPy3.tkpy3_tools.markdown_tools import PyQt5MarkdownDialog
from TkPy3.tkpy3_tools.system import set_tray_items
from TkPy3.version import version as __version__
from TkPy3.tkpy3_tools.activate import ActivateDialog
from TkPy3.tkpy3_tools.activate_game import random_activation_codes
from TkPy3.tkpy3_tools.report import BugReportWindow, NewFunctionReportWindow
from TkPy3.tkpy3_tools.pyshell import TkPyShell

__author__ = 'chenmy1903'
tkpy3_github_url = "https://github.com/chenmy1903/TkPy3"

windows_set_taskbar_icon()
check_system()
cgitb.enable(format='text')


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        add_diff()
        self.tray = set_tray_items(self)
        self.tray.menu.triggered[QAction].connect(self.MenuEvents)
        # self.assert_activate()
        self.untitled_number = 0
        self.not_save_list = []
        self.setWindowTitle(get_configs()['init_title'])
        self.tip = QStatusBar()
        self.setStatusBar(self.tip)
        self.base_tkpy = BaseTkPy3()
        self.windows_mdi = self.base_tkpy.mdi
        self.line_count_button = LineCountButton(self.windows_mdi)
        self.setCentralWidget(self.base_tkpy)
        self.Menu: QMenuBar = self.menuBar()
        self.FileMenu = self.Menu.addMenu(_('文件'))
        self.EditMenu = self.Menu.addMenu(_('编辑'))
        self.SelectMenu = self.Menu.addMenu(_('选择'))
        self.ViewMenu = self.Menu.addMenu(_('查看'))
        self.GoToMenu = self.Menu.addMenu(_('转到'))
        self.RunMenu = self.Menu.addMenu(_('运行'))
        self.TerminalMenu = self.Menu.addMenu(_('终端'))
        self.HelpMenu = self.Menu.addMenu(_('帮助'))
        # ----------------------------------------
        self.FileToolsBar = self.addToolBar(_('文件'))
        self.RunToolsBar = self.addToolBar(_('运行'))
        self.HelpToolsBar = self.addToolBar(_('帮助'))
        self.tip.addPermanentWidget(self.line_count_button)
        self.get_start()

    def get_start(self):
        self.add_editor_window()
        self.add_tools_bar_items()
        self.add_menus()
        self.setWindowState(Qt.WindowMaximized)
        self.windows_mdi.setTabsClosable(True)
        self.windows_mdi.setViewMode(QMdiArea.TabbedView)
        self.windows_mdi.setTabsMovable(True)
        self.setAcceptDrops(True)
        self.line_count_button.clicked.connect(lambda: self.MenuEvents(TkPyEventType(_('转到行'))))
        self.line_count_button.setWhatsThis(_('转到行'))

    def open_python_shell(self):
        pyshell_window = EditSubWindow()
        shell = TkPyShell()
        shell.close_sub_window.connect(lambda: self.windows_mdi.removeSubWindow(pyshell_window))
        pyshell_window.setWindowIcon(QIcon(pixmaps['shell']))
        pyshell_window.resize(700, 500)
        pyshell_window.setWindowTitle(_('Python Shell'))
        pyshell_window.setWidget(shell)
        self.windows_mdi.addSubWindow(pyshell_window)
        pyshell_window.close_remove.connect(lambda: self.windows_mdi.removeSubWindow(pyshell_window))
        pyshell_window.show()

    def assert_activate(self, reactivate=False):
        if not get_configs()['is_activate'] or reactivate:
            permanent_activation = self.open_activate_window()
            if not get_configs()['is_activate']:
                QMessageBox.critical(self, _('错误'), _('TkPy3未激活，即将退出TkPy3。'))
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

        elif get_configs()['end_activate_day'] > datetime.date.today():
            add_config('is_activate', False)
            self.assert_activate()
        random_activation_codes()

    def open_activate_window(self):
        dialog = ActivateDialog()
        dialog.exec_()
        return dialog.permanent_activation

    def add_tools_bar_items(self):
        self.FileToolsBar.actionTriggered[QAction].connect(self.MenuEvents)
        open_file = self.FileToolsBar.addAction(QIcon(pixmaps["open_file"]), _('打开'))
        open_file.setStatusTip(_('打开文件'))
        open_file.setWhatsThis(_('打开文件'))
        new = self.FileToolsBar.addAction(QIcon(pixmaps["new_file"]), _('新建'))
        new.setWhatsThis(_('新建文件'))
        self.FileToolsBar.addSeparator()
        save = self.FileToolsBar.addAction(QIcon(pixmaps['save_file']), _('保存'))
        save.setWhatsThis(_('保存文件'))
        saveas = self.FileToolsBar.addAction(QIcon(pixmaps['saveas_file']), '另存为')
        saveas.setWhatsThis(_('另存为文件'))
        # --------------------------------------------------------------------
        self.RunToolsBar.actionTriggered[QAction].connect(self.MenuEvents)
        run_action = self.RunToolsBar.addAction(QIcon(pixmaps["run"]), _('运行'))
        run_action.setWhatsThis(_('运行代码'))
        # --------------------------------------------------------------------
        self.HelpToolsBar.actionTriggered[QAction].connect(self.MenuEvents)
        help_action = self.HelpToolsBar.addAction(_('帮助'))
        help_action.setWhatsThis(_('打开帮助'))

    def add_menus(self):
        self.Menu.triggered[QAction].connect(self.MenuEvents)
        new = self.FileMenu.addAction(QIcon(pixmaps["new_file"]), _('新建'))
        new.setShortcut(get_event('Ctrl+N'))
        new.setStatusTip(_('新建文件'))
        new.setWhatsThis(_('新建文件'))
        open = self.FileMenu.addAction(QIcon(pixmaps["open_file"]), _('打开'))
        open.setShortcut(get_event('Ctrl+O'))
        open.setStatusTip(_('打开文件'))
        open.setWhatsThis(_('打开文件'))
        self.FileMenu.addSeparator()
        save = self.FileMenu.addAction(QIcon(pixmaps['save_file']), _('保存'))
        save.setShortcut(get_event('Ctrl+S'))
        save.setStatusTip(_('保存文件'))
        save.setWhatsThis(_('保存文件'))
        saveas = self.FileMenu.addAction(QIcon(pixmaps['saveas_file']),
                                         _('另存为'))
        saveas.setStatusTip(_('另存为文件'))
        saveas.setWhatsThis(_('另存为文件'))
        saveas.setShortcut(get_event('Ctrl+Shift+S'))
        save_all = self.FileMenu.addAction(QIcon(pixmaps['save_all_file']),
                                           _("保存所有文件"))
        save_all.setStatusTip(_('保存所有文件'))
        save_all.setWhatsThis(_('保存所有文件'))
        self.FileMenu.addSeparator()
        close_window = self.FileMenu.addAction(QIcon(pixmaps["exit"]), _('退出TkPy3'))
        close_window.setShortcut(get_event('Ctrl+Q'))
        close_window.setStatusTip(_('退出TkPy3主窗口'))
        close_window.setWhatsThis(_('退出TkPy3'))
        reload_window = self.FileMenu.addAction(
            QIcon(pixmaps["restart"]), _('重启TkPy3'))
        reload_window.setShortcut('Ctrl+Shift+R')
        reload_window.setStatusTip(_('重启TkPy3'))
        reload_window.setWhatsThis(_('重启'))
        # --------------------------------------------------------------
        sort_windows = self.ViewMenu.addAction(_('排列子窗口'))
        self.ViewMenu.addSeparator()
        sort_windows.setStatusTip(_('排列所有打开的内部主窗口'))
        close_all_files = self.ViewMenu.addAction(
            QIcon(pixmaps["close_all"]),
            _('关闭所有子窗口'))
        close_all_files.setStatusTip(_('关闭所有子窗口'))
        # --------------------------------------------------------------
        run = self.RunMenu.addAction(QIcon(pixmaps["run"]), _('运行'))
        run.setShortcut(get_event('F5'))
        run.setStatusTip(_('运行代码'))
        # --------------------------------------------------------------
        open_python_shell = self.TerminalMenu.addAction(QIcon(pixmaps["shell"]), _('打开Python Shell'))
        open_python_shell.setStatusTip(_('打开Python Shell'))
        open_terminal = self.TerminalMenu.addAction(QIcon(pixmaps["terminal"]), _('打开终端'))
        open_terminal.setStatusTip(_('打开系统终端'))
        self.TerminalMenu.addSeparator()
        config_tkpy3 = self.TerminalMenu.addAction(QIcon(pixmaps['config']), _('设置'))
        config_tkpy3.setStatusTip(_('设置TkPy3'))
        reset_tkpy3 = self.TerminalMenu.addAction(_('重置TkPy3的设置'))
        reset_tkpy3.setStatusTip(_('重置TkPy3的设置'))
        self.TerminalMenu.addSeparator()
        ToolsMenu: QMenu = self.TerminalMenu.addMenu(_('工具'))
        markdown_to_html = ToolsMenu.addAction(_('Markdown转Html'))
        markdown_to_html.setStatusTip(
            _('TkPy3工具: Markdown转Html'))
        qt_file_view = ToolsMenu.addAction(QIcon(pixmaps["ui_previewer"]), _('Qt文件预览'))
        qt_file_view.setStatusTip(
            _('TkPy3工具: Qt文件预览'))
        # --------------------------------------------------------------
        select_all = self.SelectMenu.addAction(_('选择全部'))
        select_all.setStatusTip(_('选择全部文字'))
        select_all.setShortcut(get_event('Ctrl+A'))
        # --------------------------------------------------------------
        paste = self.EditMenu.addAction(QIcon(pixmaps['paste']), _('粘贴'))
        paste.setShortcut(get_event('Ctrl+V'))
        paste.setStatusTip(_('粘贴'))
        paste = self.EditMenu.addAction(QIcon(pixmaps['copy']), _('复制'))
        paste.setShortcut(get_event('Ctrl+C'))
        paste.setStatusTip('复制选中的文字')
        paste = self.EditMenu.addAction(QIcon(pixmaps['cut']), _('剪切'))
        paste.setShortcut(get_event('Ctrl+X'))
        paste.setStatusTip('剪切选中的文字')
        self.EditMenu.addSeparator()
        undo = self.EditMenu.addAction(QIcon(pixmaps['undo']), _('撤销'))
        undo.setShortcut(get_event('Ctrl+Z'))
        undo.setStatusTip('撤销上一个操作')
        redo = self.EditMenu.addAction(QIcon(pixmaps['redo']), _('撤回'))
        redo.setShortcut(get_event('Ctrl+Y'))
        redo.setStatusTip(_('撤回上一个操作'))
        self.EditMenu.addSeparator()
        format_code = self.EditMenu.addAction(_('格式化代码'))
        format_code.setShortcut(get_event('Ctrl+Alt+L'))
        format_code.setStatusTip(_('使用AutoPEP8格式化代码'))
        sort_imports = self.EditMenu.addAction(_('排列Import 语句'))
        sort_imports.setStatusTip(_('排列Import 语句'))
        # --------------------------------------------------------------
        whats_this = self.HelpMenu.addAction(QIcon(pixmaps['help_about']), _('这是什么'))
        whats_this.setShortcut('Shift+F2')
        whats_this.setStatusTip(_('这是什么?'))
        self.HelpMenu.addSeparator()
        about_tkpy3 = self.HelpMenu.addAction(_('关于TkPy3'))
        about_tkpy3.setStatusTip(_('关于TkPy3'))
        about_qt = self.HelpMenu.addAction(QIcon(pixmaps['about_qt']), _('关于PyQt5'))
        about_qt.setStatusTip(_('关于PyQt5'))
        open_python_package_help = self.HelpMenu.addAction(_('打开Python包帮助'))
        open_python_package_help.setStatusTip(_('打开Python包帮助'))
        self.HelpMenu.addSeparator()
        relyMenu = self.HelpMenu.addMenu(_('依赖管理'))
        view_relys = relyMenu.addAction(_('TkPy3的依赖'))
        view_relys.setStatusTip(_('查看TkPy3的依赖'))
        install_relys = relyMenu.addAction(_('安装TkPy3的所有依赖'))
        install_relys.setStatusTip(_('安装TkPy3的所有依赖'))
        self.HelpMenu.addSeparator()
        reactivate = self.HelpMenu.addAction(_('重新激活TkPy3'))
        reactivate.setStatusTip(_('打开TkPy3激活窗口以重新激活TkPy3'))
        self.HelpMenu.addSeparator()
        report_bug = self.HelpMenu.addAction(_('报告Bug'))
        report_bug.setStatusTip(_('在GitHub上报告TkPy3的Bug'))
        self.HelpMenu.addAction(_('报告TkPy3的功能改进')).setStatusTip(
            _('在Gitter上报告TkPy3的功能改进'))
        star_tkpy3 = self.HelpMenu.addAction(_('给TkPy3点个Star'))
        star_tkpy3.setStatusTip(_('给TkPy3点个Star'))
        open_tkpy3_github = self.HelpMenu.addAction(_('TkPy3的Github官网'))
        open_tkpy3_github.setStatusTip(_('打开TkPy3的Github官网'))
        # --------------------------------------------------------------
        goto_line_column: QAction = self.GoToMenu.addAction(_('转到行'))
        goto_line_column.setShortcut(get_event('Ctrl+L'))
        goto_line_column.setStatusTip(_('转到行'))
        # --------------------------------------------------------------

    def MenuEvents(self, event):
        if event.text() == _('新建'):
            self.add_editor_window()
        elif event.text() == _('打开'):
            self.open_file()
        elif event.text() == _('关闭所有窗口'):
            self.windows_mdi.closeAllSubWindows()
        elif event.text() == _('排列子窗口'):
            self.windows_mdi.tileSubWindows()
        elif event.text() == _('设置'):
            self.open_config_dialog_window()
        elif event.text() == _('退出TkPy3'):
            res = QMessageBox.question(self, _('TkPy3 - 问题'), _('是否退出TkPy3?'),
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if res == QMessageBox.Yes:
                self.close()
        elif event.text() == _('格式化代码'):
            if self.window_mdi_activate_is_pyshell():
                return
            self.windows_mdi.activeSubWindow().widget().autopep8_fix_code()
        elif event.text() in [_('保存'), _('另存为')]:
            if self.window_mdi_activate_is_pyshell():
                return
            window = self.windows_mdi.activeSubWindow()
            widget = window.widget()
            if widget.file_name and event.text() != _('另存为'):
                file_name, ok = widget.file_name, True
            else:
                file_name, ok = QFileDialog.getSaveFileName(
                    self, event.text(), '', all_file_types)
            if ok:
                widget.save_file(file_name)
        elif event.text() == _('关于TkPy3'):
            QMessageBox.information(self, _('关于TkPy3'), f"""TkPy3一个使用PyQt5制作的TkPy IDE
TkPy3: {__version__}
PyQt5: {PYQT_VERSION_STR}
TkPy3官网: https://github.com/chenmy1903/TkPy3

TkPy3激活:
激活到期时间: {get_configs()['end_activate_day'] if not isinstance(get_configs()['end_activate_day'], bool) else _("永久激活")}
-----------------------------------
{__author__} ©2020 All Rights Reserved.
                """)
        elif event.text() == _('TkPy3的依赖'):
            dialog = RelyDialog()
            dialog.exec_()
        elif event.text() == _('安装TkPy3的所有依赖'):
            dialog = InstallDialog()
            dialog.exec_()
        elif event.text() == _('运行'):
            if self.window_mdi_activate_is_pyshell():
                return
            window = self.windows_mdi.activeSubWindow()
            widget = window.widget()
            self.MenuEvents(TkPyEventType(_('保存')))
            if widget.file_name:
                widget.run()
        elif event.text() == _('粘贴'):
            window = self.windows_mdi.activeSubWindow()
            widget = window.widget()
            text = widget.text
            text.paste()
        elif event.text() == _('复制'):
            window = self.windows_mdi.activeSubWindow()
            widget = window.widget()
            text = widget.text
            text.copy()
        elif event.text() == _('剪切'):
            window = self.windows_mdi.activeSubWindow()
            widget = window.widget()
            text = widget.text
            text.cut()
        elif event.text() == _('撤销'):
            window = self.windows_mdi.activeSubWindow()
            widget = window.widget()
            text = widget.text
            text.undo()
        elif event.text() == _('撤回'):
            window = self.windows_mdi.activeSubWindow()
            widget = window.widget()
            text = widget.text
            text.redo()
        elif event.text() == _('选择全部'):
            window = self.windows_mdi.activeSubWindow()
            widget = window.widget()
            text = widget.text
            text.selectAll()
        elif event.text() == _('关于PyQt5'):
            QApplication.aboutQt()
        elif event.text() == _('Markdown转Html'):
            dialog = PyQt5MarkdownDialog()
            dialog.exec_()
        elif event.text() == _('重启TkPy3'):
            self.restart_window()
        elif event.text() == _('报告Bug'):
            bug_report_window = BugReportWindow()
            bug_report_window.exec_()
        elif event.text() == _('打开Python Shell'):
            self.open_python_shell()
        elif event.text() == _('报告TkPy3的功能改进'):
            NewFunctionReportWindow().exec_()
        elif event.text() == _('关闭所有子窗口'):
            self.windows_mdi.closeAllSubWindows()
            self.not_save_list = []
        elif event.text() == _('重新激活TkPy3'):
            self.assert_activate(True)
        elif event.text() == _('重置TkPy3的设置'):
            res = QMessageBox.question(self, _('问题'), _('是否重置所有设置'))
            if res == QMessageBox.Yes:
                reset_configs()
                QMessageBox.information(self, _('提示'), _('重置完成。'))
        elif event.text() == _('打开终端'):
            os.system('start cmd /C' + os.path.join(sys.exec_prefix, "python.exe") + ' -m IPython "' + os.path.join(
                BASE_DIR, 'SystemTemplates/run_terminal_script.py') + '"')
        elif event.text() == _('保存所有文件'):
            self.save_files()
        elif event.text() == _('帮助'):
            TkPyHelpWidget().exec_()

        elif event.text() == _('转到行'):
            if self.window_mdi_activate_is_pyshell():
                return
            text = self.windows_mdi.activeSubWindow().widget().text
            max_line = len(text.text().split('\n'))
            at_line = text.getCursorPosition()[0] + 1
            line, ok = QInputDialog.getInt(self, _('转到行'), _('请输入行号: '), at_line, 1, max_line)
            if ok:
                text.goto_line(line)
        elif event.text() == _('给TkPy3点个Star'):
            dialog = StarDialog()
            dialog.exec_()
        elif event.text() == _('TkPy3的Github官网'):
            webbrowser.open(tkpy3_github_url)
        elif event.text() == _('重新打开文件'):
            if self.window_mdi_activate_is_pyshell():
                return
            widget = self.windows_mdi.activeSubWindow().widget()
            if widget.file_name:
                if widget.file_name in self.not_save_list:
                    res = QMessageBox.question(self, _('问题'), _('文件未保存，是否保存后重新打开文件?'),
                                               QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
                    if res == QMessageBox.Yes:
                        widget.save_file(widget.file_name)
                    elif res == QMessageBox.Cancel:
                        return
                widget.save.emit()
                widget.open(widget.file_name)

        elif event.text() == _('打开Python包帮助'):
            PythonPackageHelpDialog().exec()
        elif event.text() == _('排列Import 语句'):
            if self.window_mdi_activate_is_pyshell():
                return
            widget = self.windows_mdi.activeSubWindow().widget()
            widget.sort_imports()
        elif event.text() == _('Qt文件预览'):
            dialog = QtUiFileView()
            dialog.exec_()
        elif event.text() == _('这是什么'):
            QWhatsThis.enterWhatsThisMode()

    def open_file(self):
        file_name, ok = QFileDialog.getOpenFileName(
            self, _('打开文件'), '', all_file_types)
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

    def open_config_dialog_window(self) -> None:
        dialog = ConfigDialog()
        dialog.exec_()

    def addSubMenu(self, menu: QMenu):
        menu.triggered[QAction].connect(self.MenuEvents)
        menu.addSeparator()
        menu.addAction(QIcon(pixmaps["open_file"]), _('重新打开文件'))

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

        def remove():
            save()
            self.windows_mdi.removeSubWindow(sub)

        sub = EditSubWindow()
        subMenu = sub.systemMenu()
        self.addSubMenu(subMenu)
        sub.setWindowState(Qt.WindowMaximized)
        sub.setNumber(self.untitled_number)
        sub.resize(700, 500)
        sub.setWindowTitle(get_configs()[
                               'new_file_title'] + ' ' + str(sub.number) if not file_name else os.path.abspath(
            file_name))
        sub.setWindowIcon(QIcon(pixmaps["python_file"]))
        edit = BaseEditor()
        if file_name:
            edit.open(file_name)
        sub.setWidget(edit)
        edit.not_save.connect(not_save)
        edit.save.connect(save)
        self.windows_mdi.addSubWindow(sub)
        sub.close_remove.connect(remove)
        sub.show()

    def closeEvent(self, event: QCloseEvent) -> None:
        QApplication.setQuitOnLastWindowClosed(True)
        if self.not_save_list:
            res = QMessageBox.question(self, _('TkPy3 - 问题'), _('还有文件未保存,是否保存所有文件之后退出TkPy3？'),
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
                    all_file_types)
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

    def show_warning(self, message: str):
        QMessageBox.warning(self, _('警告'), message)
        warnings.warn(message)

    def restart_window(self):
        res = QMessageBox.question(self, _('问题'), _('是否重启TkPy3'))
        if res == QMessageBox.Yes:
            self.close()
            os.system('start ' + sys.executable[-1: len('python.exe')] + 'pythonw ' + __file__)

    def dropEvent(self, event: QDropEvent) -> None:
        file_name = event.mimeData().text().split('file:///')[-1]
        if file_name.endswith('.py') or file_name.endswith('.pyw'):
            self.add_editor_window(TkPyEventType(file_name))
        else:
            QMessageBox.warning(self, _('警告'), _('只能打开py, pyw文件'))

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()


def main():
    server = HelpServer()
    server.start()
    app = QApplication(sys.argv)
    tkpy3_setup(app)
    widget = MainWindow()
    widget.show()
    app.setQuitOnLastWindowClosed(False)
    return_code = app.exec_()
    server.terminate()
    return return_code


if __name__ == '__main__':
    sys.exit(main())
