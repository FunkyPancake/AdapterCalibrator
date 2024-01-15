import logging

import pymongo

from calibrator.ApplicationError import ApplicationError
from calibrator.Record import Record


class DbWrapper:
    DB_NAME__ = 'AdapterCalibrator'
    COL_NAME__ = "Calibrations"

    def __init__(self, logger: logging.Logger, uri: str):
        self.logger = logger
        try:
            self.client__ = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5)
            self.db__ = self.client__[self.DB_NAME__]
            self.collection__ = self.db__[self.COL_NAME__]
            self.client__.server_info()
            logger.debug(f"Connected to {uri}")
        except pymongo.errors.ConnectionFailure as e:
            logger.fatal(f"Could not connect to the database, {e.message}")
            raise ApplicationError(e)
        except pymongo.errors.ServerSelectionTimeoutError as e:
            logger.fatal(f"Could not connect to the database, {e.message}")
            raise ApplicationError(e)

    def add_record(self, record: Record):
        (uid, inserted) = self.collection__.insert_one(record.as_dict())
        if inserted:
            self.logger.info(f"Record added to the database {uid}.")
        else:
            self.logger.error(r"Couldn't insert record to the db.")
