import logging

from PyQt5 import Qt
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QMainWindow

from calibrator.ApplicationError import ApplicationError
from calibrator.DbWrapper import DbWrapper
from calibrator.QTextHandler import QTextHandler
from calibrator.Ui_MainWindow import Ui_MainWindow
from calibrator.BaordCalibrator import BaordCalibrator, CalData


class UiWrapper(QMainWindow, Ui_MainWindow):
    def __init__(self, logger: logging.Logger):
        super().__init__()
        self.logger = logger
        self.is_connected__ = False
        self.calibrator__ = None
        self.db__ = None

        self.setupUi(self)
        self.pass_fail_label.setAttribute(Qt.Qt.WA_StyledBackground, True)

        self.logger.addHandler(QTextHandler(self.log_text))
        self.load_settings()
        self.clear_cal_results()
        self.update_can_if_list()
        self.connect_tutton.clicked.connect(self.on_connect_clicked)

    def closeEvent(self, event):
        self.calibrator__ = None
        self.db__ = None
        self.save_settings()

    def on_connect_clicked(self):
        if self.is_connected__:
            self.db__ = None
            self.calibrator__ = None
            self.is_connected__ = False
            self.update_status('disconnected')
        else:
            if self.can_if_combo_box.currentData() != '' and self.db_path_line_edit.text() != '':
                item = self.can_if_combo_box.currentData()
                try:
                    tolerance = self.tol_sb.value()
                    self.calibrator__ = BaordCalibrator(self.logger, interface=item['interface'], channel=item[
                        'channel'], bitrate='500000', max_tolerance=tolerance)
                    self.calibrator__.add_cal_started_callback(self.on_cal_started)
                    self.calibrator__.add_cal_finished_callback(self.on_board_calibrated)
                    self.calibrator__.add_cal_broken_callback(self.on_board_disconnected)
                    self.db__ = DbWrapper(self.logger, self.db_path_line_edit.text())
                    self.is_connected__ = True
                    self.update_status('connected')
                    self.cal_pb.setMinimum(-tolerance)
                    self.cal_pb.setMaximum(tolerance)
                    self.vsup_pb.setMinimum(-tolerance)
                    self.vsup_pb.setMaximum(tolerance)
                    self.calibrator__.start_calibration()
                except ApplicationError as e:
                    pass
            else:
                self.update_can_if_list()

    def load_settings(self):
        settings = QSettings('./calibrator.ini', QSettings.IniFormat)
        self.tol_sb.setValue(float(settings.value('Tolerance', 1.0)))
        self.db_path_line_edit.setText(settings.value('Db_Path', ''))
        self.logger.setLevel(settings.value('LogLevel', 'ERROR'))

    def save_settings(self):
        settings = QSettings('./calibrator.ini', QSettings.IniFormat)
        settings.setValue('Tolerance', self.tol_sb.value())
        settings.setValue('Db_Path', self.db_path_line_edit.text())

    def clear_cal_results(self):
        self.id_line_edit.setText('')
        self.vsup_ideal_num(0)
        self.vsup_meas_num.display(0)
        self.cal_l_m_num.display(0)
        self.cal_h_m_num.display(0)
        self.cal_l_t_num.display(0)
        self.cal_h_t_num.display(0)
        self.vsup_pb.setValue(0)
        self.cal_pb.setValue(0)
        self.update_pf_status(False)
        self.update_cal_status('IDLE')

    def update_status(self, text):
        self.status_indicator.setText(text)

    def update_pf_status(self, value: bool):
        if value:
            self.pass_fail_label.setText('PASS')
            self.pass_fail_label.setStyleSheet('background-color: green;')
        else:
            self.pass_fail_label.setText('FAIL')
            self.pass_fail_label.setStyleSheet('background-color: red;')

    def update_cal_status(self, status):
        self.cal_status.setText(status)

    def update_can_if_list(self):
        [self.can_if_combo_box.addItem(i['channel'], i) for i in BaordCalibrator.get_interfaces()]

    def on_cal_started(self):
        self.update_cal_status('IN PROGRESS')

    def on_board_disconnected(self):
        self.clear_cal_results()

    def on_board_calibrated(self, cal_data: CalData):
        self.id_line_edit.setText(cal_data.record.board_id)
        self.vsup_ideal_num.display(self.calibrator__.vsup_trg)
        self.vsup_meas_num.display(cal_data.record.vsup)
        self.cal_l_m_num.display(cal_data.record.vlm)
        self.cal_h_m_num.display(cal_data.record.vhm)
        self.cal_l_t_num.display(cal_data.record.vld)
        self.cal_h_t_num.display(cal_data.record.vhd)
        self.vsup_pb.setValue(cal_data.tol_vsup)
        self.cal_pb.setValue(cal_data.tol_bd)
        self.update_pf_status(cal_data.pf)
        self.update_cal_status('COMPLETE')
        self.db__.add_record(cal_data.record)
