import logging

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QMainWindow, QFileDialog

from calibrator.DbWrapper import DbWrapper
from calibrator.Ui_MainWindow import Ui_MainWindow
from calibrator.BoardComm import BoardComm


class UiWrapper(QMainWindow, Ui_MainWindow):
    def __init__(self, logger):
        super().__init__()
        self.logger = logger
        self.is_connected = False
        self.calibrator = None
        self.db = None
        self.setupUi(self)

        self.load_settings()
        [self.can_if_combo_box.addItem(i['channel'], i) for i in BoardComm.get_interfaces()]
        self.db_path_select_button.clicked.connect(self.on_db_path_button_clicked)
        self.connect_tutton.clicked.connect(self.on_connect_clicked)

    def closeEvent(self, event):
        self.calibrator = None
        self.save_settings()

    def on_db_path_button_clicked(self):
        try:
            (db_path, _) = QFileDialog.getOpenFileName(self)
            self.logger.debug(db_path)
            self.db_path_line_edit.setText(db_path)
        except KeyboardInterrupt as e:
            self.logger.debug(e)

    def on_connect_clicked(self):
        if self.is_connected:
            self.calibrator = None
            self.is_connected = False
            self.update_status('disconnected')
        else:
            if self.can_if_combo_box.currentData() != '' and self.db_path_line_edit.text() != '':
                item = self.can_if_combo_box.currentData()
                self.calibrator = BoardComm(self.logger, interface=item['interface'], channel=item[
                    'channel'], bitrate='500000')
                self.db = DbWrapper(self.logger, self.db_path_line_edit.text())
                self.init_ui_values(self.calibrator)
                self.is_connected = True
                self.update_status('connected')
            else:
                [self.can_if_combo_box.addItem(i['channel'], i) for i in BoardComm.get_interfaces()]

    def load_settings(self):
        settings = QSettings('./calibrator.ini', QSettings.IniFormat)
        self.tol_sb.setValue(float(settings.value('Tolerance', 1.0)))
        self.db_path_line_edit.setText(settings.value('Db_Path', ''))

    def save_settings(self):
        settings = QSettings('./calibrator.ini', QSettings.IniFormat)
        settings.setValue('Tolerance', self.tol_sb.value())
        settings.setValue('Db_Path', self.db_path_line_edit.text())

    def update_status(self, text):
        self.status_indicator.setText(text)

    def init_ui_values(self, calibrator):
        pass
