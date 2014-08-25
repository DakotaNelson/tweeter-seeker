from pymongo import MongoClient

class dbclient:
    """ handles all db methods for tweeter-seeker when using MongoDB"""

    def __init__(self, dbhost='localhost', dbport=27017):
        self.client = MongoClient(dbhost,dbport)
        self.db = self.client.tseeker

    def insert(self, collection, item,options={}):
        col = self.db[collection]
        return col.insert(item,options)

    def findOne(self, collection, query, projection={}):
        col = self.db[collection]
        return col.find_one(query)

    def find(self, collection, query, projection={}):
        col = self.db[collection]
        return col.find(query)

    def count(self, collection, query):
        col = self.db[collection]
        return col.find(query).count()
