from pymongo import MongoClient

class dbclient:
    """ handles all db methods for tweeter-seeker when using MongoDB"""

    def __init__(self, dbhost='localhost', dbport=27017):
        self.client = MongoClient(dbhost,dbport)
        self.db = self.client.tseeker

    def insert(self, collection, item,options={}):
        col = self.db[collection]
        return col.insert(item,options)

    def update(self, collection, item, changes):
        col = self.db[collection]
        return col.update(item, changes)

    def upsert(self, collection, item):
        col = self.db[collection]
        return col.update(query, update, {'upsert':True})

    def findOne(self, collection, query, projection={}):
        col = self.db[collection]
        return col.find_one(query,projection)

    def results(self, collection, query):
        col = self.db[collection]
        return col.find(query).count()

    def find(self, collection, query, projection={}):
        col = self.db[collection]
        return col.find(query,projection)

    def count(self, collection, query):
        col = self.db[collection]
        return col.find(query).count()

    def findGreatest(self, collection, field, sortdir=1, n=1):
        col = self.db[collection]
        return col.find().sort( [(field,sortdir)] ).limit(n)
