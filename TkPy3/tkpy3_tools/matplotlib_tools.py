import matplotlib.pyplot as plt
import matplotlib as mpl
from PyQt5.QtWidgets import QWidget, QToolBar, QVBoxLayout, QStatusBar, QStackedWidget, QApplication, QMainWindow
from matplotlib._pylab_helpers import Gcf
from matplotlib.backends import backend_qt5

from PyQt5.QtCore import QObject, pyqtSignal

mpl.use('qt5Agg')


class ShowWindow(QStackedWidget):
    closing = pyqtSignal()

    def __init__(self, parent=None):
        QStackedWidget.__init__(self, parent)
        self.__statusBar = QStatusBar()

    def addToolBar(self, toolBar: QToolBar):
        if isinstance(toolBar, QToolBar):
            return toolBar
        elif isinstance(toolBar, str):
            toolBar = QToolBar(toolBar)
            return toolBar

    def statusBar(self):
        return self.__statusBar

    def centralWidget(self):
        return self.widget(self.currentIndex())

    def setCentralWidget(self, widget: QWidget):
        self.addWidget(widget)
        self.setCurrentIndex(0)

    def closeEvent(self, event):
        self.closing.emit()
        QWidget.closeEvent(self, event)


backend_qt5.MainWindow = ShowWindow


class Tools(QObject):
    images = pyqtSignal(list)

    def show(self):
        managers = Gcf.get_all_fig_managers()
        images = []
        for manager in managers:
            images.append(manager.canvas.manager)
        self.images.emit(images)


tools = Tools()

plt.show = tools.show
