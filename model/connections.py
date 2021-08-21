from pymongo import MongoClient, ASCENDING
from pymongo.collection import Collection

from settings import DB_URL


class Connections:
    """ Connection is special object, that is used to store ALL connections of this back-end """
    mongo_client: MongoClient
    tokens_db: Collection
    profiles_db: Collection

    def start_connections(self):
        """ This method is used for starting all connections """
        self.mongo_client = MongoClient(DB_URL)
        self.tokens_db = self.mongo_client.db.tokens_collection
        self.profiles_db = self.mongo_client.db.profiles_collection
        self.setup_indexes()

    def setup_indexes(self):
        """ Setting up indexes in MongoDB """
        self.tokens_db.create_index([('expiresAt', ASCENDING)], expireAfterSeconds=1)


# Singleton object
global connections
connections = Connections()
