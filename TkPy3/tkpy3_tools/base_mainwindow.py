# -*- coding: UTF-8 -*-
import typing

from PyQt5.QtGui import QCloseEvent, QMouseEvent, QIcon, QBrush, QColor
from PyQt5.QtWidgets import QDockWidget, QSplitter, QWidget, QHBoxLayout, QApplication, QMdiArea, QTabBar, \
    QStackedWidget, QVBoxLayout, QToolButton
from PyQt5.QtCore import pyqtSignal, Qt

import sys
import tkinter as tk

from TkPy3.tkpy3_tools.pyshell import TkPyShell
from TkPy3.tkpy3_tools.editor import EditSubWindow
from TkPy3.tkpy3_tools.text import TkPyTextEdit
from TkPy3.tkpy3_tools.start import tkpy3_setup


class TkPyDockWidget(QDockWidget):
    close_window = pyqtSignal()
    open_window = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(TkPyDockWidget, self).__init__(*args, **kwargs)
        self.open_window.emit()

    def closeEvent(self, event: QCloseEvent):
        self.close_window.emit()
        return super(TkPyDockWidget, self).closeEvent(event)


class TabBar(QTabBar):
    clicked = pyqtSignal()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        index = self.tabAt(event.pos())
        if index == self.currentIndex():
            self.clicked.emit()
        else:
            QTabBar.mousePressEvent(self, event)


class SideBar(QWidget):
    def __init__(self, parent=None, *, side=tk.TOP):
        QWidget.__init__(self, parent)
        self.side = side
        self.tabBar = TabBar()
        self.tabBar.clicked.connect(self.__tabBar_auto_hide)
        self.widget_view = QStackedWidget()
        self.__hide = False
        if side in [tk.TOP, tk.BOTTOM]:
            self.__layout = QVBoxLayout()
        elif side in [tk.LEFT, tk.RIGHT]:
            self.__layout = QHBoxLayout()
        self.__init_ui()

    def __tabBar_auto_hide(self):
        if self.__hide:
            self.widget_view.widget(self.tabBar.currentIndex()).show()
            self.__hide = False
        else:
            self.widget_view.widget(self.tabBar.currentIndex()).hide()
            self.__hide = True

    def __init_ui(self):
        self.setLayout(self.__layout)
        self.tabBar.currentChanged.connect(self.widget_view.setCurrentIndex)
        if self.side not in [tk.RIGHT, tk.BOTTOM]:
            self.__layout.addWidget(self.tabBar)
            self.__layout.addWidget(self.widget_view)
        else:
            self.__layout.addWidget(self.widget_view)
            self.__layout.addWidget(self.tabBar)

    def addTab(self, widget: QWidget, title: str, icon: QIcon = None):
        if not icon:
            self.tabBar.addTab(title)
        else:
            self.tabBar.addTab(icon, title)
        self.widget_view.addWidget(widget)


class TkPyMdiArea(QMdiArea):
    sub_add = pyqtSignal()

    def __init__(self, parent=None):
        super(TkPyMdiArea, self).__init__(parent)

    def addSubWindow(self, *args):
        self.sub_add.emit()
        super(TkPyMdiArea, self).addSubWindow(*args)


class LineCountButton(QToolButton):
    def __init__(self, main_mdi: TkPyMdiArea, parent=None):
        QToolButton.__init__(self, parent)
        self.setAutoRaise(True)
        self.__mdi = main_mdi
        self.__mdi.subWindowActivated.connect(self.__update)
        self.__mdi.sub_add.connect(self.__update)

    def __update(self):
        pos = lambda: text.getCursorPosition()
        update = lambda: self.setText(':'.join([str(pos()[0] + 1), str(pos()[1])]))
        if self.__mdi.activeSubWindow():
            if not isinstance(self.__mdi.activeSubWindow().widget(), TkPyShell):
                text: TkPyTextEdit = self.__mdi.activeSubWindow().widget().text
                text.cursorPositionChanged.connect(update)
                update()


class BaseTkPy3(QWidget):
    open_file_event = pyqtSignal(str)

    def __init__(self, parent=None):
        super(BaseTkPy3, self).__init__(parent)
        self.layout = QHBoxLayout()
        self.splitter = QSplitter()
        self.mdi = TkPyMdiArea()
        self.mdi_background_style = QBrush(QColor(160, 160, 160, 255))
        self.mdi_background_style.setStyle(Qt.Dense4Pattern)
        self.mdi.setBackground(self.mdi_background_style)
        self.mdi.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdi.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdi.setObjectName('WindowMdi')
        self.init_ui()

    def init_ui(self):
        self.setLayout(self.layout)
        self.splitter.addWidget(self.mdi)
        self.layout.addWidget(self.splitter, 0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tkpy3_setup(app)
    tkpy3 = BaseTkPy3()
    window = EditSubWindow()
    window.resize(600, 600)
    window.setWindowTitle('TkPy3 Sub Window')
    tkpy3.mdi.addSubWindow(window)
    tkpy3.show()
    tkpy3.setWindowTitle('TkPy3 Test')
    sys.exit(app.exec_())
