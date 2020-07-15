from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

import sys


class BugReportWindow(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle('提交Bug')
        self.resize(1500, 700)
        self.layout = QVBoxLayout()
        self.title_label = QLabel('<h2>报告TkPy3的Bug (使用中文)</h2>')
        self.github_post = QWebEngineView()
        self.github_post.setUrl(
            QUrl('https://github.com/chenmy1903/TkPy3/issues/new'))
        self.init_ui()

    def init_ui(self):
        self.layout.addWidget(self.title_label, 0)
        self.layout.addWidget(self.github_post, 1)
        self.setLayout(self.layout)


class NewFunctionReportWindow(BugReportWindow):
    def __init__(self):
        BugReportWindow.__init__(self)
        self.setWindowTitle('提交新功能')
        self.title_label.setText('<h2>报告TkPy3的功能改进或新功能</h2>')
        self.github_post.setUrl(QUrl('https://gitter.im/TkPy3/rtnew_repo'))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    bug_report_window = BugReportWindow()
    sys.exit(bug_report_window.exec_())
