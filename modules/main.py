from modules.dao import Dao
from modules.gui import RootWindow
from modules.scraper import find_pec


def main():
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
