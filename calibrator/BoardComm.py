import logging
from enum import Enum

import can


class BoardComm(object):
    CAN_CONTROL_ID = 0x510
    CAN_DATA_ID = 0x500

    def __init__(self, logger, interface, channel, bitrate):
        self.logger = logger
        self.__cal_state = None
        self.__cal_active = True
        self.__bus = can.interface.Bus(interface=interface, channel=channel, bitrate=bitrate)

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
        if self.__bus:
            self.__bus.shutdown()

    def send_tool_status(self, value: bool):
        message = can.Message(arbitration_id=self.CAN_CONTROL_ID, dlc=1, data=[1 if value else 0])
        self.__bus.Send(message)
        self.logger.info(f'State {value} sent to calibrator')

    def calc_calibration(self, vsup, cal_points):

        return 1

    def start_calibration(self):
        self.send_tool_status(True)
        can_reader = can.BufferedReader()
        while self.__cal_active:
            msg = can_reader.get_message(1)
            if msg is not None:
                msg_vsup = can_reader.get_message(5)
                msg_cal = can_reader.get_message(10)
                cal_result = self.calc_calibration(msg_vsup.data, msg_cal.data)
                self.save_cal_results(cal_result)

    def save_cal_results(self, cal_result):
        pass
