import logging

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QMainWindow, QFileDialog

from calibrator.DbWrapper import DbWrapper
from calibrator.Record import Record
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
        self.vsup_ideal_num.display('5.000')
        self.clear_cal_results()
        self.load_settings()
        [self.can_if_combo_box.addItem(i['channel'], i) for i in BoardComm.get_interfaces()]
        self.connect_tutton.clicked.connect(self.on_connect_clicked)

    def closeEvent(self, event):
        self.calibrator = None
        self.save_settings()

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
    def clear_cal_results(self):
        self.id_line_edit.setText('')
        self.cal_l_m_num.display(0)
        self.cal_h_m_num.display(0)
        self.cal_l_t_num.display(0)
        self.cal_h_t_num.display(0)
        self.vsup_pb.setValue(0)
        self.cal_pb.setValue(0)
        self.update_pf_status(False)

    def on_board_calibrated(self, record, cal_data):
        self.id_line_edit.setText(record.board_id)
        self.cal_l_m_num.display(record.vlm)
        self.cal_h_m_num.display(record.vhm)
        self.cal_l_t_num.display(record.vld)
        self.cal_h_t_num.display(record.vhd)
        self.vsup_pb.setValue(cal_data['tol_vsup'])
        self.cal_pb.setValue(cal_data['tol_bd'])
        self.update_pf_status(cal_data['pf'])
        self.status_indicator('CalComplete')
        self.db.add_record(record)

    def on_board_disconnected(self):
        self.status_indicator('WaitForBoard')
        self.clear_cal_results()


    def update_pf_status(self, value: bool):
        # if(value):
            # self.pass_fail_label.
        pass
