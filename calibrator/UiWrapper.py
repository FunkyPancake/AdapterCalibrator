import logging

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QMainWindow, QFileDialog

from calibrator.Ui_MainWindow import Ui_MainWindow
from calibrator.BoardComm import BoardComm


class UiWrapper(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.is_connected = False
        self.calibrator = None
        self.setupUi(self)
        [self.can_if_combo_box.addItem(i['channel'], i) for i in BoardComm.get_interfaces()]
        self.db_path_select_button.clicked.connect(self.on_db_path_button_clicked)
        self.load_settings()
        self.connect_tutton.clicked.connect(self.on_connect_clicked)

    def closeEvent(self, event):
        self.calibrator = None
        self.save_settings()

    def on_db_path_button_clicked(self):
        (db_path, _) = QFileDialog.getOpenFileName(self)
        self.logger.debug(db_path)
        self.db_path_line_edit.setText(db_path)

    def on_connect_clicked(self):
        if self.is_connected:
            self.calibrator = None
            self.is_connected = False
            self.update_status('disconnected')
        else:
            self.init_ui_values()
            item = self.can_if_combo_box.currentData()
            self.calibrator = BoardComm(interface=item['interface'], channel=item['channel'], bitrate='500000')
            self.is_connected = True
            self.update_status('connected')

    def load_settings(self):
        settings = QSettings('./calibrator.ini', QSettings.IniFormat)
        self.tol_sb.setValue(settings.value('Tolerance', 1.0))
        self.db_path_line_edit.setText(settings.value('Db_Path', ''))

    def save_settings(self):
        settings = QSettings('./calibrator.ini', QSettings.IniFormat)
        settings.setValue('Tolerance', self.tol_sb.value())
        settings.setValue('Db_Path', self.db_path_line_edit.text())

    def update_status(self, text):
        self.status_indicator.setText(text)

    def init_ui_values(self):
        pass
