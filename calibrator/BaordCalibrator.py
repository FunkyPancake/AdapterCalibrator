import logging

import can

from calibrator.ApplicationError import ApplicationError


class CalData:
    def __init__(self, record, tol_vsup, tol_bd, pf):
        self.record = record
        self.tol_vsup = tol_vsup
        self.tol_bd = tol_bd
        self.pf = pf


class BaordCalibrator(object):
    CAN_CONTROL_ID = 0x510
    CAN_DATA_ID = 0x500

    def __init__(self, logger: logging.Logger, interface, channel, bitrate, max_tolerance):
        self.cal_broken_callback = None
        self.cal_finished_callback = None
        self.cal_started_callback = None
        self.logger = logger
        self.__cal_state = None
        self.__cal_active = True
        try:
            self.__bus = can.interface.Bus(interface=interface, channel=channel, bitrate=bitrate)
            self.logger.info(f"Connected to {interface}:{channel} @{bitrate} bps.")
        except can.exceptions.CanInitializationError as e:
            self.logger.fatal(f"Could not connect to {interface}:{channel}, {e.message}.")
            raise ApplicationError(e)

    @staticmethod
    def get_interfaces():
        interfaces = []
        try:
            interfaces = can.detect_available_configs(['pcan'])
        except can.CanError as e:
            print(e)
        except FileNotFoundError as e:
            print(e)
        finally:
            return interfaces

    def __del__(self):
        self.stop_calibration()
        if self.__bus:
            self.__bus.shutdown()

    def send_tool_status(self, value: bool):
        self.logger.info(f'Send status {value} to calibrator')
        message = can.Message(arbitration_id=self.CAN_CONTROL_ID, dlc=1, data=[1 if value else 0])
        self.__bus.Send(message)

    def calc_calibration(self):

        return 1

    def start_calibration(self):
        self.send_tool_status(True)

    def stop_calibration(self):
        self.send_tool_status(False)

    def on_new_frame(self, frame):
        cal_result = self.calc_calibration()
        if self.cal_finished_callback:
            self.cal_finished_callback(cal_result)

    def add_cal_started_callback(self, callback):
        self.cal_started_callback = callback

    def add_cal_finished_callback(self, callback):
        self.cal_finished_callback = callback

    def add_cal_broken_callback(self, callback):
        self.cal_broken_callback = callback
