from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QWidget, QMessageBox

from TkPy3 import pixmaps


class TrayIcon(QSystemTrayIcon):
    def __init__(self, parent: QWidget = None):
        QSystemTrayIcon.__init__(self, parent)
        self.menu = QMenu()
        self.__init_ui()
        self.__set_menu()
        self.activated.connect(self.clicked)

    def __init_ui(self):
        self.setIcon(QIcon(pixmaps["tkpy3"]))

    def __set_menu(self):
        menu = self.menu
        menu.addAction('帮助')
        menu.addAction(QIcon(pixmaps['shell']), '打开终端')
        menu.addSeparator()
        menu.addAction(QIcon(pixmaps["exit"]), '退出TkPy3')
        self.setContextMenu(menu)

    def clicked(self, button: int):
        parent: QWidget = self.parent()
        if button == 2:
            pass
        elif button == 3:
            if parent.isVisible():
                parent.hide()
            else:
                parent.show()


def set_tray_items(widget: QWidget):
    icon = TrayIcon(widget)
    icon.show()
    return icon
