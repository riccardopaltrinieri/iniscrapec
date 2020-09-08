from os import getenv

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import OperationFailure


class Dao:
    """ Class used to access to a database. It also contains a cache to speed up multiple queries"""

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
                self.client = 'WRONG_KEY'
        else:
            self.client = 'MISSING_KEY'

    def contains(self, key):
        """
        :param key: the tax code requested
        :return: true if the element is in the database
        """
        if key in self.cache:
            return True
        result = self.collection.find_one({'tax': key})
        return result is not None

    def get(self, key):
        """
        :param key: the tax code requested
        :return: the element in the database
        """
        if key in self.cache:
            return self.cache[key]
        value = self.collection.find_one({'tax': key})['pec']
        return value

    def add(self, key, value):
        """
        :param key: the tax code requested
        :param value: the pec code found
        :return: the element in the database
        """
        self.cache[key] = value
        self.collection.insert_one({'tax': key, 'pec': value})
