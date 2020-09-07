import sys

from PyQt5.QtWidgets import QLineEdit, QToolButton, QSplitter, QGridLayout, QWidget, QTabWidget, QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView

from TkPy3.tkpy3_tools.gnu_gettext_extensions import _
from TkPy3.tkpy3_tools.search import SearchWidget
from TkPy3.locale_dirs import pixmaps


class WebBroser(QWidget):
    title: str = _('浏览器')

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowIcon(QIcon(pixmaps['browser']))
        self.__layout = QGridLayout()
        self.__top_bar = QSplitter()
        self.__url_entry = QLineEdit()
        self.__search_entry = SearchWidget()
        self.__page_tab = QTabWidget()
        self.__page_tab.currentChanged.connect(self.setActionPage)
        self.__init_ui()

    def setActionPage(self, tab):
        print(tab)
        self.setWindowTitle(self.title)

    def addPage(self, url: str):
        web_widget = QWebEngineView()
        web_widget.load(QUrl(url))
        self.__page_tab.addTab(
            web_widget, web_widget.icon(), web_widget.title())

    def __init_ui(self):
        self.__top_bar.addWidget(self.__url_entry)
        self.__top_bar.addWidget(self.__search_entry)
        self.__layout.addWidget(self.__top_bar, 0, 0)
        self.__layout.addWidget(self.__page_tab, 1, 0)
        self.addPage('https://www.baidu.com')
        self.setLayout(self.__layout)


def _test():
    app = QApplication(sys.argv)
    widget = WebBroser()
    widget.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    _test()
