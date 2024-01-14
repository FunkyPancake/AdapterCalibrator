import datetime
import shortuuid


class Record:
    def __init__(self, vsup, vlm, vhm):
        self.vsup = vsup
        self.vlm = vlm
        self.vhm = vhm
        self.board_id = shortuuid.ShortUUID().random(length=8)
        self.timestamp = datetime.datetime.utcnow().isoformat()

    def as_dict(self):
        return {
            'board_id': self.board_id,
            'timestamp': self.timestamp,
            'v_sup_meas': self.vsup,
            'v_low_meas': self.vlm,
            'v_high_meas': self.vhm
        }
