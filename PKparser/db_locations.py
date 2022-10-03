import configparser
import pathlib

from pymongo import MongoClient


# read sensitive configs
config_path = pathlib.Path(__file__).parent.absolute() / "config.ini"
config = configparser.ConfigParser()
config.read(config_path)

ATLAS_URI = config['Mongo']['atlas_uri']
DB_NAME = config['Mongo']['db_name']


def initialize_db():
    mongo_client = MongoClient(ATLAS_URI)
    db = mongo_client[DB_NAME]
    return db
