from os import getenv, environ
from modules import Dao
from modules import RootWindow
from modules import find_pec


def main():
    for var in {'CAP_KEY', 'DB_USER', 'DB_PWD', 'DATA_SITEKEY', 'URL', 'TAX_EXAMPLE'}:
        if getenv(var) == '':
            environ[var] = input('Insert ' + var + ': ')
    gui = RootWindow(submit_tax)


def memoize(f):
    database = Dao()
    if database.client is None:
        return 'MISSING_KEY'

    def helper(code):
        if database.contains(code):
            result = database.get(code)
        else:
            result = f(code)
            if result != 0 and result != 'MISSING_KEY':
                database.add(code, result)
        return result

    return helper


@memoize
def submit_tax(tax_code):
    return find_pec(tax_code)


main()

exit()
