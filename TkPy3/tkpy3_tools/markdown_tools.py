import markdown
import sys
from PyQt5.QtWidgets import QDialog, QGridLayout, QWidget, QHBoxLayout, QSplitter, QPushButton, QLabel, QTextBrowser, \
    QFileDialog, QMessageBox, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from pygments.formatters.html import HtmlFormatter
from qtconsole.pygments_highlighter import PygmentsHighlighter

from TkPy3.default_configs import get_configs
from pygments.lexers.html import HtmlLexer

from TkPy3.tkpy3_tools.start import tkpy3_setup

image_url = \
    'https://' \
    'imgsa.baidu.com/forum/w%3D580/sign=8eafdc1f9e82d158bb8259b9b00b19d5/07489682b9014a90a9a51c4cab773912b21bee03.jpg'


def to_html(text):
    css = HtmlFormatter().get_style_defs('.codehilite')
    extensions = [
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        'markdown.extensions.tables'
    ]
    style_code = f'''
<style>
{css}
</style>
'''
    return style_code + markdown.markdown(text, extensions=extensions)


class PyQt5MarkdownDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.resize(1200, 400)
        self.setWindowTitle('TkPy3 Markdown转换器')
        self.layout = QGridLayout(self)
        self.file_name = ''
        self.view_frame = QWidget()
        self.view_layout = QHBoxLayout()
        self.view_splitter = QSplitter(Qt.Horizontal)
        self.view_frame.setLayout(self.view_layout)
        self.loadMarkdown_file_button = QPushButton()
        self.show_file_name = QLabel()
        self.text_view = QTextBrowser()
        self.html_view = QWebEngineView()
        self.save_button = QPushButton()
        PygmentsHighlighter(self.text_view, HtmlLexer())
        self.init_ui()

    def init_ui(self):
        self.loadMarkdown_file_button.setText('选择Markdown文件')
        self.html_view.setHtml(
            f'<h1>欢迎使用TkPy3 Markdown转换器</h1>\
            <img src={image_url}>')
        self.show_file_name.setText('请选择文件')
        self.save_button.setText('保存Html文件')
        self.save_button.setDisabled(True)
        self.loadMarkdown_file_button.setWhatsThis('点击浏览MarkDown文件')
        self.loadMarkdown_file_button.clicked.connect(self.choice_file)
        self.save_button.clicked.connect(self.save_file)
        self.layout.addWidget(self.loadMarkdown_file_button, 0, 0)
        self.layout.addWidget(self.show_file_name, 1, 0)
        self.view_layout.addWidget(self.view_splitter)
        self.view_splitter.addWidget(self.text_view)
        self.view_splitter.addWidget(self.html_view)
        self.layout.addWidget(self.view_frame, 2, 0)
        self.layout.addWidget(self.save_button, 3, 0)
        self.setLayout(self.layout)
        self.view_splitter.setSizes([300, 300])

    def save_file(self):
        text = self.text_view.toPlainText()
        file_name, ok = QFileDialog.getSaveFileName(self, '保存', '', 'Html文件 (*.html)')
        if ok:
            with open(file_name, 'w', encoding=get_configs()['default_file_encoding']) as f:
                f.write(text)

    def choice_file(self):
        file_name, ok = QFileDialog.getOpenFileName(
            self, '打开文件', '', 'Markdown文件 (*.md);; 所有文件 (*.*)')
        if ok:
            self.show_file_name.setText(file_name)
            self.file_name = file_name
            self.start_transformation()

    def start_transformation(self):
        if not self.file_name:
            QMessageBox.information(self, '提示', '还未选择文件。')
        with open(self.file_name, encoding=get_configs()['default_file_encoding']) as f:
            text = f.read()
        html = to_html(text)
        self.text_view.setPlainText(html)
        self.html_view.setHtml(html)
        self.save_button.setDisabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tkpy3_setup(app)
    dialog = PyQt5MarkdownDialog()
    sys.exit(dialog.exec_())
