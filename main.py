import logging
import sys

from PyQt5.QtWidgets import QApplication

from calibrator.UiWrapper import UiWrapper

if __name__ == '__main__':
    logging.getLogger(__name__)
    app = QApplication(sys.argv)
    window = UiWrapper()
    window.show()
    app.exec()
