import logging
import sys

from PyQt5.QtWidgets import QApplication

from calibrator.UiWrapper import UiWrapper

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.FileHandler(filename='log,log', encoding='utf-8'))
    app = QApplication(sys.argv)
    window = UiWrapper(logger)
    window.show()
    app.exec()
