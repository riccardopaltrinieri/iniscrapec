import sys
from os import getenv, environ
from dotenv import load_dotenv

from modules import Dao, find_pec, RootWindow


def memoize(func):
    """
    memoization: (definition https://en.wikipedia.org/wiki/Memoization)
    Check if the requester result is already stored in the cache or in
    the database to speed up the computation
    :param func: the function that took too much to compute
    :return: the result of the function (stored or not)
    """
    database = Dao()
    if database.client in ('MISSING_KEY', 'WRONG_KEY'):
        if database.client == 'WRONG_KEY':
            print("The username or password for database in the .env file is wrong")
        else:
            print("The username or password for database in the .env file is missing")
        return 'MISSING_KEY'

    def helper(code):
        if database.contains(code):
            result = database.get(code)
        else:
            result = func(code)
            if result not in (0, 'MISSING_KEY'):
                database.add(code, result)
        return result

    return helper


if __name__ == '__main__':

    load_dotenv()
    for var in {'CAP_KEY', 'DB_USER', 'DB_PWD', 'DATA_SITEKEY', 'URL', 'TAX_EXAMPLE'}:
        key = getenv(var)
        if key is None or key == '':
            print(var + ' in the .env file is missing.')
            environ[var] = input('Write it in the file to save it or enter it just for this time: ')

    mem_findpec = memoize(find_pec)
    RootWindow(mem_findpec)


sys.exit()
