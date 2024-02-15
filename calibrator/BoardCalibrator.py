import logging
from enum import Enum

from typing import List

from PySide6.QtCore import Slot, QByteArray
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

    def __init__(self, logger: logging.Logger, interface, bitrate, max_tolerance):
        pass
        self.max_tolerance = max_tolerance
        self.vsup_trg = 5.0
        self.vsup_meas = None
        self.cal_broken_callback = None
        self.cal_finished_callback = None
        self.cal_started_callback = None
        self.__logger = logger
        self.__cal_state = None
        self.__cal_active = True

        (device, error_string) = QCanBus.instance().createDevice(interface.plugin(), interface.name())
        if not device:
            self.__logger.fatal(f"Error creating device '{interface.plugin()}', reason: '{error_string}'")
            return
        self.__can_device = device
        self.__can_device.framesReceived.connect(self.process_received_frames)
        self.__logger.info(f"Connected to {interface.plugin()}:{interface.name()} @{bitrate} bps.")

    @staticmethod
    def get_interfaces() -> list:
        interfaces, error_string = QCanBus.instance().availableDevices('peakcan')

        return interfaces

    def __del__(self):
        self.stop_calibration()
        if self.__can_device:
            self.__can_device.shutdown()

    def send_tool_status(self, value: bool):
        self.__logger.info(f'Send status {value} to calibrator')
        frame = QCanBusFrame(identifier=self.CAN_CONTROL_ID, data=QByteArray([1 if value else 0], 1))
        send_frame(frame)

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
        self.send_tool_status(True)

    def stop_calibration(self):
        self.send_tool_status(False)

    @Slot()
    def process_received_frames(self):
        if not self.can_device__:
            return
        while self.can_device__.framesAvailable():
            frame = self.m_can_device.readFrame()
            if frame.frameId() == self.CAN_STATUS_ID:
                if frame.payload()[0] == self.State.Wait:
                    pass

                if frame.payload()[0] == self.State.InProgress:
                    pass

                if frame.payload()[0] == self.State.Done:
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


@Slot(QCanBusFrame)
def send_frame(self, frame):
    if self.m_can_device:
        self.m_can_device.writeFrame(frame)
