import logging

from PyQt5.QtWidgets import QPlainTextEdit


class QTextHandler(logging.Handler):
    def __init__(self, qtextedit: QPlainTextEdit ):
        super(QTextHandler, self).__init__()

        self.widget = qtextedit
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)+"\n"
        self.widget.insertPlainText(msg)

    def write(self, m):
        pass
