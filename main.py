import sys
from BoardCommunication.BoardCommunication import BoardCommunication as Bc
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout()
    button_config = QPushButton('Config')
    box = QLineEdit()
    button_config.clicked.connect(lambda: box.setText('clicked'))
    layout.addWidget(box)
    layout.addWidget(button_config)
    layout.addWidget(QPushButton('Top'))
    layout.addWidget(QPushButton('Bottom'))
    layout.addWidget(QLineEdit(" ".join([x["channel"] for x in Bc.get_interfaces()])))
    window.setLayout(layout)
    window.show()
    app.exec()
