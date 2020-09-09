from os import getenv
from time import sleep
from urllib import request

import bs4 as bs
from dotenv import load_dotenv
from mechanize import Browser


def find_pec(tax_code):
    """ Function that takes a TAX code as parameter and look on the official
        gov website for the TAX corresponding PEC address"""
    browser = Browser()
    url = getenv('URL')
    browser.open(url)

    # Solving of the captcha code using a third part service by 2captcha.com
    data_sitekey = getenv('DATA_SITEKEY')
    captcha_token = solve_captcha()
    if captcha_token == 'MISSING_KEY':
        return captcha_token

    # Filling of the form
    browser.select_form('_1_WAR_searchpecsportlet_fmCompanies')
    browser.form['_1_WAR_searchpecsportlet_tax-code-vat'] = tax_code
    browser.form.find_control('_1_WAR_searchpecsportlet_g-recaptcha-response').readonly = False
    browser.form['_1_WAR_searchpecsportlet_g-recaptcha-response'] = captcha_token
    browser.submit()

    # Parsing of the result to find the pec
    soup = bs.BeautifulSoup(browser.response().read(), 'html5lib')
    label = soup.find("label", {'class': 'aui-field-label-inline-label'})
    if label is None:
        return 0

    return label.next_sibling.string


def solve_captcha():
    """request the captcha solving from the website 2captcha.com"""

    # Uses the API Key stored in the .env file (If you are not the developer you need to insert it)
    load_dotenv()
    data_sitekey = getenv('DATA_SITEKEY')
    cap_key = getenv('CAP_KEY')
    if cap_key == '' or data_sitekey == '':
        return 'MISSING_KEY'

    url = 'https://2captcha.com/in.php?' \
          'key=' + cap_key + \
          '&method=userrecaptcha' \
          '&pageurl=https://www.inipec.gov.it/cerca-pec/-/pecs/companies' \
          '&googlekey=' + data_sitekey

    # the site will return the id of the captcha element
    response = request.urlopen(url).read().decode("ascii")
    if response[0:5] == 'ERROR':
        return 'MISSING_KEY'
    captcha_id = response.split("|")[1]

    # Actual solving of the captcha
    url = 'https://2captcha.com/res.php?' \
          'key=' + cap_key + \
          '&action=get' \
          '&id=' + captcha_id
    token = request.urlopen(url).read().decode('ascii')

    # The computing will take a while so I request the result every 5 second
    while token == 'CAPCHA_NOT_READY':
        sleep(5)
        # print("still waiting") use this to be sure that it is still waiting for the answer
        token = request.urlopen(url).read().decode('ascii')

    print('Captcha token obtained: ' + token[0:20] + '...')
    return token.split("|")[1]


if __name__ == '__main__':
    print("This is a PEC scraper, please enter the TAX code of a company: ")
    pec = find_pec(input())
    if pec != 0:
        print(pec)
    else:
        print('PEC not found')
