from PyQt5.QtWidgets import QDialog, QTextBrowser, QVBoxLayout

from qtconsole.pygments_highlighter import PygmentsHighlighter


class PythonFileViewDialog(QDialog):
    def __init__(self, text: str):
        super(PythonFileViewDialog, self).__init__()
        self.__text = QTextBrowser()
        self.__text.setText(text)
        PygmentsHighlighter(self.text)
        self.__layout = QVBoxLayout()
        self.setLayout(self.__layout)
        self.__layout.addWidget(self.__text)
