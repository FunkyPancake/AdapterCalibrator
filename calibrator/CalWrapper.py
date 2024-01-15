from enum import Enum


class CalWrapper:
    class CalState(Enum):
        A = 1

    def __init__(self, logger):
        self.__logger = logger
        self.__cal_active = False
        self.__cal_state = self.CalState.A
        self.__pf_threshold = 0

    @property
    def __pf_threshold(self) -> int:
        return self.__pf_threshold

    @__pf_threshold.setter
    def __pf_threshold(self, value: int):
        self.__pf_threshold = value

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

    def connect(self):
        pass

    def disconnect(self):
        pass

    def on_cal_complete(self):
        pass
