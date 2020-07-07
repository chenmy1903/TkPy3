from PyQt5.QtCore import QUrl
from multiprocessing import Process
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout

from TkPy3.tkpy_doc.serever_configs import port
from TkPy3.tkpy_doc import run_server


class HelpServer(Process):
    def run(self) -> None:
        run_server(port=port)


class TkPyHelpWidget(QDialog):
    url = f'http://localhost:{port}/'
    title: str = 'TkPy3 帮助'

    def __init__(self, parent=None):
        super(TkPyHelpWidget, self).__init__(parent)
        self.vboxlayout = QVBoxLayout()
        self.resize(1000, 500)
        self.setWindowTitle(self.title)
        self.view = QWebEngineView()
        self.reset_to_home = QPushButton('回到主页')
        self.setLayout(self.vboxlayout)
        self.go_home()
        self.vboxlayout.addWidget(self.reset_to_home, 0)
        self.vboxlayout.addWidget(self.view, 1)
        self.reset_to_home.setWhatsThis('回到主页')
        self.reset_to_home.setToolTip(self.url)

    def go_home(self):
        self.view.load(QUrl(self.url))
        self.view.reload()


class PythonPackageHelpDialog(TkPyHelpWidget):
    url = f'http://localhost:{port}/python/package/help'
    title = 'Python Package Help'
