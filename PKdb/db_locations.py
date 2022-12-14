from pymongo import MongoClient

import os

DEBUG = os.getenv("DEBUG") == 'True'

MONGODB_HOST = 'localhost' if DEBUG else 'mongodb_service'    # matches service name in docker-compose
DB_NAME = 'pk_db'   # matches db name in docker-compose


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
        self._clinet = MongoClient(MONGODB_HOST, 27017)
        self._db = self._clinet[DB_NAME]

    def save_many(self, data):
        return self._db.locations.insert_many(data)

    def get_data(self):
        return list(self._db.locations.find({}))

    def drop(self):
        self._db.locations.drop()

    def filter(self, locations=None, transport=None, date_from=None, date_to=None):
        query_locs = {"locations": {"$in": locations}} if locations else {}
        query_transport = {"transport": {"$in": transport}} if transport else {}
        query_date_from = {"date": {"$gte": date_from}} if date_from else {}
        query_date_to = {"date": {"$lte": date_to}} if date_to else {}
        return list(self._db.locations.find({"$and": [query_locs, query_transport, query_date_from, query_date_to]}))


