import datetime
import shortuuid


class Record:
    def __init__(self, vsup, vlm, vhm, vld, vhd, vls, vhs):
        self.vhs = vhs
        self.vls = vls
        self.vhd = vhd
        self.vld = vld
        self.vsup = vsup
        self.vlm = vlm
        self.vhm = vhm
        self.board_id = shortuuid.ShortUUID().random(length=8)
        self.timestamp = datetime.datetime.utcnow().isoformat()

    def as_dict(self):
        return {
            'board_id': self.board_id,
            'timestamp': self.timestamp,
            'v_sup': self.vsup,
            'v_low': self.vls,
            'v_high': self.vhs
        }
