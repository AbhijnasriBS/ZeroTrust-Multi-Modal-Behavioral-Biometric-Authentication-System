import pymongo


class Database:
    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['Bank']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        # print(collection,query)
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def find_collection(collection):
        return Database.DATABASE[collection].find()

    @staticmethod
    def update(collection, query, values):
        Database.DATABASE[collection].update_one(query, values)
        return Database.DATABASE[collection]

    @staticmethod
    def delete_one_record(collection, query):
        # print(collection,query)
        return Database.DATABASE[collection].delete_one(query)

    @staticmethod
    def delete_many_record(collection, query):
        # print(collection,query)
        return Database.DATABASE[collection].delete_many(query)
