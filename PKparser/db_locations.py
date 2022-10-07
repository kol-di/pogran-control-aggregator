import configparser
import pathlib

from pymongo import MongoClient


# read sensitive configs
config_path = pathlib.Path(__file__).parent.absolute() / "config.ini"
config = configparser.ConfigParser()
config.read(config_path)

# ATLAS_URI = config['Mongo']['atlas_uri']
DB_NAME = config['Mongo']['db_name']


class MongodbService:
    _instance = None
    _clinet = None
    _db = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.__init__(cls._instance)
        return cls._instance

    @classmethod
    def close_connection(cls):
        if cls._clinet is None:
            return
        cls._clinet.close()

    def __init__(self):
        self._clinet = MongoClient('localhost', 27017)
        self._db = self._clinet[DB_NAME]

    def save_many(self, data):
        return self._db.locations.insert_many(data)

    def get_data(self):
        print(self._instance, self._clinet, self._db)
        return list(self._db.locations.find({}))

    def drop(self):
        self._db.locations.drop()
