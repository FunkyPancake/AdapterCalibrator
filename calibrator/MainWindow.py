import logging

from PySide6.QtCore import QTimer, QUrl, Slot, QSettings, Qt
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QLabel, QMainWindow
from PySide6.QtSerialBus import QCanBus, QCanBusDevice, QCanBusFrame

from calibrator.ApplicationError import ApplicationError
from calibrator.DbWrapper import DbWrapper
from calibrator.QTextHandler import QTextHandler
from calibrator.BoardCalibrator import BoardCalibrator, CalData
from calibrator.ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, logger: logging.Logger):
        super().__init__()
        self.m_ui = Ui_MainWindow()

        self.logger = logger
        self.is_connected__ = False
        self.calibrator__ = None
        self.db__ = None

        self.m_ui.setupUi(self)
        self.m_ui.pass_fail_label.setAttribute(Qt.WA_StyledBackground, True)

        self.logger.addHandler(QTextHandler(self.m_ui.log_text))
        self.load_settings()
        self.clear_cal_results()
        self.update_can_if_list()
        self.m_ui.connect_tutton.clicked.connect(self.on_connect_clicked)

    @Slot()
    def closeEvent(self, event):
        self.calibrator__ = None
        self.db__ = None
        self.save_settings()

    @Slot()
    def on_connect_clicked(self):
        if self.is_connected__:
            self.db__ = None
            self.calibrator__ = None
            self.is_connected__ = False
            self.update_status('disconnected')
        else:
            if self.m_ui.can_if_combo_box.currentText() != '' and self.m_ui.db_path_line_edit.text() != '':
                item = self.m_ui.can_if_combo_box.currentData()
                try:
                    tolerance = self.m_ui.tol_sb.value()
                    self.calibrator__ = BoardCalibrator(self.logger, interface=item, bitrate='500000',
                                                        max_tolerance=tolerance)
                    self.db__ = DbWrapper(self.logger, self.m_ui.db_path_line_edit.text())

                    self.calibrator__.add_cal_started_callback(self.on_cal_started)
                    self.calibrator__.add_cal_finished_callback(self.on_board_calibrated)
                    self.calibrator__.add_cal_broken_callback(self.on_board_disconnected)
                    self.is_connected__ = True
                    self.update_status('connected')
                    self.m_ui.cal_pb.setMinimum(-tolerance)
                    self.m_ui.cal_pb.setMaximum(tolerance)
                    self.m_ui.vsup_pb.setMinimum(-tolerance)
                    self.m_ui.vsup_pb.setMaximum(tolerance)
                    self.calibrator__.start_calibration()
                except ApplicationError as e:
                    pass
            else:
                self.update_can_if_list()

    def load_settings(self):
        settings = QSettings('./calibrator.ini', QSettings.IniFormat)
        self.m_ui.tol_sb.setValue(float(settings.value('Tolerance', 1.0)))
        self.m_ui.db_path_line_edit.setText(settings.value('Db_Path', ''))
        self.logger.setLevel(settings.value('LogLevel', 'ERROR'))

    def save_settings(self):
        settings = QSettings('./calibrator.ini', QSettings.IniFormat)
        settings.setValue('Tolerance', self.m_ui.tol_sb.value())
        settings.setValue('Db_Path', self.m_ui.db_path_line_edit.text())

    def clear_cal_results(self):
        self.m_ui.id_line_edit.setText('')
        self.m_ui.vsup_ideal_num.display(0)
        self.m_ui.vsup_meas_num.display(0)
        self.m_ui.cal_l_m_num.display(0)
        self.m_ui.cal_h_m_num.display(0)
        self.m_ui.cal_l_t_num.display(0)
        self.m_ui.cal_h_t_num.display(0)
        self.m_ui.vsup_pb.setValue(0)
        self.m_ui.cal_pb.setValue(0)
        self.update_pf_status(False)
        self.update_cal_status('IDLE')

    def update_status(self, text):
        self.m_ui.status_indicator.setText(text)

    def update_pf_status(self, value: bool):
        if value:
            self.m_ui.pass_fail_label.setText('PASS')
            self.m_ui.pass_fail_label.setStyleSheet('background-color: green;')
        else:
            self.m_ui.pass_fail_label.setText('FAIL')
            self.m_ui.pass_fail_label.setStyleSheet('background-color: red;')

    def update_cal_status(self, status):
        self.m_ui.cal_status.setText(status)

    def update_can_if_list(self):
        [self.m_ui.can_if_combo_box.addItem(f"{i.plugin()}:{i.name()}", i) for i in BoardCalibrator.get_interfaces()]

    def on_cal_started(self):
        self.update_cal_status('IN PROGRESS')

    def on_board_disconnected(self):
        self.clear_cal_results()

    def on_board_calibrated(self, cal_data: CalData):
        self.m_ui.id_line_edit.setText(cal_data.record.board_id)
        self.m_ui.vsup_ideal_num.display(f"{self.calibrator__.vsup_trg:.3f}")
        self.m_ui.vsup_meas_num.display(f"{cal_data.record.vsup:.3f}")
        self.m_ui.cal_l_m_num.display(f"{cal_data.record.vlm:.3f}")
        self.m_ui.cal_h_m_num.display(f"{cal_data.record.vhm:.3f}")
        self.m_ui.cal_l_t_num.display(f"{cal_data.record.vld:.3f}")
        self.m_ui.cal_h_t_num.display(f"{cal_data.record.vhd:.3f}")
        self.m_ui.vsup_pb.setValue(cal_data.tol_vsup)
        self.m_ui.cal_pb.setValue(cal_data.tol_bd)
        self.update_pf_status(cal_data.pf)
        self.update_cal_status('COMPLETE')
        self.db__.add_record(cal_data.record)
