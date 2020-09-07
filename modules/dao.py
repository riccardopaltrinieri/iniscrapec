from os import getenv
from pymongo import MongoClient
from dotenv import load_dotenv
from pymongo.errors import OperationFailure


class Dao:

    def __init__(self):
        self.cache = {}
        load_dotenv()
        db_user = getenv('DB_USER')
        db_password = getenv('DB_PWD')
        if db_user != '' and db_password != '':
            self.client = MongoClient("mongodb+srv://" + db_user + ":" + db_password +
                                      "@cluster0.utmqp.mongodb.net/"
                                      "inipec?retryWrites=true&w=majority")
            self.collection = self.client.inipec.tax_to_pec
            try:
                self.collection.find_one({})
            except OperationFailure:
                self.client = None

    def contains(self, key):
        if key in self.cache:
            return True
        result = self.collection.find_one({'tax': key})
        return result is not None

    def get(self, key):
        if key in self.cache:
            return self.cache[key]
        value = self.collection.find_one({'tax': key})['pec']
        self.cache[key] = value
        return value

    def add(self, key, value):
        self.cache[key] = value
        self.collection.insert_one({'tax': key, 'pec': value})
