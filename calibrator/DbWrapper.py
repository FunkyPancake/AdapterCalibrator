
import pymongo
from calibrator.Record import Record


class DbWrapper:
    DB_NAME__ = 'AdapterCalibrator'
    COL_NAME__ = "Calibrations"

    def __init__(self, logger, db_url):
        self.logger = logger
        self.client__ = pymongo.MongoClient(db_url)
        self.db__ = self.client__[self.DB_NAME__]
        self.collection__ = self.db__[self.COL_NAME__]

    def add_record(self, record: Record):
        return self.collection__.insert_one(record.as_dict())
