from enum import Enum

import can


class BoardCommunication(object):
    class CalState(Enum):
        A = 1

    CAN_CONTROL_ID = 0x510
    CAN_DATA_ID = 0x500

    @property
    def pf_threshold(self) -> int:
        return self.__cal_state

    @pf_threshold.setter
    def pf_threshold(self, value: int):
        self.pf_threshold = value

    @property
    def cal_state(self) -> CalState:
        return self.__cal_state

    @cal_state.setter
    def cal_state(self, value: CalState):
        self.__cal_state = value

    @property
    def cal_active(self) -> bool:
        return self.__cal_active

    @cal_active.setter
    def cal_active(self, value: bool):
        self.__cal_active = value

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

    def __init__(self, interface, channel, bitrate):
        self.__cal_state = None
        self.__cal_active = True
        self.__bus = can.interface.Bus(interface=interface, channel=channel, bitrate=bitrate)

    def send_tool_status(self, status: bool):
        message = can.Message(arbitration_id=self.CAN_CONTROL_ID, dlc=1, data=[1 if status else 0])
        self.__bus.Send(message)

    def start_calibration(self):
        self.send_tool_status(True)
        can_reader = can.BufferedReader()
        while self.__cal_active:
            msg = can_reader.get_message(1)
            if msg is not None:
                msg_vsup = can_reader.get_message(5)
                msg_cal = can_reader.get_message(10)

    def stop_calibration(self):
        self.send_tool_status(False)
        pass
