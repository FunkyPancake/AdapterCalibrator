import sys
from BoardCommunication.BoardCommunication import BoardCommunication as Bc
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QMainWindow
import logging
from MainWindow.MainWindow import Ui_MainWindow

if __name__ == '__main__':
    logging.getLogger(__name__)
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    window.show()
    app.exec()
