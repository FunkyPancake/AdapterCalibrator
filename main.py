import logging
import sys

from PySide6.QtWidgets import QApplication

from calibrator.MainWindow import MainWindow

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    # logging.basicConfig(format='%(asctime)s,[%(levelname)s] - %(message)')
    logger.addHandler(logging.FileHandler(filename='log.log', encoding='utf-8'))
    app = QApplication(sys.argv)
    window = MainWindow(logger)
    window.show()
    app.exec()
