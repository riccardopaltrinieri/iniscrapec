import sys
from os import getenv, environ

from modules import Dao, find_pec, RootWindow


def main():
    """ Main function of the package,
        It checks the env variables and starts the gui"""

    for var in {'CAP_KEY', 'DB_USER', 'DB_PWD', 'DATA_SITEKEY', 'URL', 'TAX_EXAMPLE'}:
        if getenv(var) == '':
            environ[var] = input(var + 'is missing, please insert it: ')
    RootWindow(submit_tax)


def memoize(func):
    """
    memoization: (definition https://en.wikipedia.org/wiki/Memoization)
    Check if the requester result is already stored in the cache or in
    the database to speed up the computation
    :param func: the function that took too much to compute
    :return: the result of the function (stored or not)
    """
    database = Dao()
    if database.client is None:
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


@memoize
def submit_tax(tax_code):
    """ Just call the corresponding method in the scraper module"""
    return find_pec(tax_code)


main()

sys.exit()
