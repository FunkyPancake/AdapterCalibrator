import logging
from enum import Enum

from typing import List

from PySide6.QtCore import Slot
from PySide6.QtSerialBus import QCanBus, QCanBusDevice, QCanBusFrame

from calibrator.ApplicationError import ApplicationError
from calibrator.Record import Record


class CalData:
    def __init__(self, record, tol_vsup, tol_bd, pf):
        self.record = record
        self.tol_vsup = tol_vsup
        self.tol_bd = tol_bd
        self.pf = pf


class BoardCalibrator(object):
    class State(Enum):
        Wait = 0
        InProgress = 1
        Done = 2

    CAN_CONTROL_ID = 0x510
    CAN_STATUS_ID = 0x500
    CAN_DATA_ID = 0x501
    CAN_VSUP_ID = 0x502

    def __init__(self, logger: logging.Logger, interface, channel, bitrate, max_tolerance):
        self.notifier__ = None
        self.max_tolerance = max_tolerance
        self.vsup_trg = 5.0
        self.vsup_meas = None
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
        self.__bus.send(message)

    def calc_calibration(self):
        pf = True
        tol_vsup = (self.vsup_meas - self.vsup_trg) / self.vsup_trg
        tol_bd = 0

        pf &= tol_vsup <= self.max_tolerance
        pf &= tol_bd <= self.max_tolerance
        # todo finish calculation
        record = Record(0, 0, 0, 0, 0, 0)
        return CalData(record=record, tol_vsup=tol_vsup, tol_bd=tol_bd, pf=pf)

    def start_calibration(self):
        listener: List[MessageRecipient] = [self.on_new_can_message]
        self.notifier__ = can.Notifier(self.__bus, listener)
        self.send_tool_status(True)

    def stop_calibration(self):
        self.notifier__.stop()
        self.send_tool_status(False)


@Slot
def on_new_can_message(self, frame: can.message) -> None:
    if frame.arbitration_id == self.CAN_STATUS_ID:
        if frame.data[0] == self.State.Wait:
            pass

        if frame.data[0] == self.State.InProgress:
            pass

        if frame.data[0] == self.State.Done:
            cal_result = self.calc_calibration()
            if self.cal_finished_callback:
                self.cal_finished_callback(cal_result)

    if frame.arbitration_id == self.CAN_DATA_ID:
        pass

    if frame.arbitration_id == self.CAN_VSUP_ID:
        self.vsup_meas = float(frame.data[1] << 8 + frame.data[0])


def add_cal_started_callback(self, callback):
    self.cal_started_callback = callback


def add_cal_finished_callback(self, callback):
    self.cal_finished_callback = callback


def add_cal_broken_callback(self, callback):
    self.cal_broken_callback = callback
