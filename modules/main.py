import sys
from os import getenv, environ
from modules.dao import Dao
from modules.scraper import find_pec
from modules.gui import RootWindow


def main():
    for var in {'CAP_KEY', 'DB_USER', 'DB_PWD', 'DATA_SITEKEY', 'URL', 'TAX_EXAMPLE'}:
        if getenv(var) == '':
            environ[var] = input('Insert ' + var + ': ')
    RootWindow(submit_tax)


def memoize(func):
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
    return find_pec(tax_code)


main()

sys.exit()
