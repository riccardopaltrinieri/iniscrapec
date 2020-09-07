import bs4 as bs
import urllib.request
import mechanize
from dotenv import load_dotenv
from os import getenv
from time import sleep


def find_pec(tax_code):
    br = mechanize.Browser()
    url = getenv('URL')
    br.open(url)

    data_sitekey = getenv('DATA_SITEKEY')
    captcha_token = solve_captcha(data_sitekey)
    if captcha_token == 'MISSING_KEY':
        return captcha_token

    # Filling of the form
    br.select_form('_1_WAR_searchpecsportlet_fmCompanies')
    br.form['_1_WAR_searchpecsportlet_tax-code-vat'] = tax_code
    br.form.find_control('_1_WAR_searchpecsportlet_g-recaptcha-response').readonly = False
    br.form['_1_WAR_searchpecsportlet_g-recaptcha-response'] = captcha_token
    br.submit()

    # Parsing of the result to find the pec
    soup = bs.BeautifulSoup(br.response().read(), 'html5lib')
    label = soup.find("label", {'class': 'aui-field-label-inline-label'})

    if label is not None:
        return label.next_sibling.string
    else:
        return 0


def solve_captcha(data_sitekey):
    # request the captcha solving from the website 2captcha.com
    load_dotenv()
    cap_key = getenv('CAP_KEY')
    if cap_key == '':
        return 'MISSING_KEY'
    url = 'https://2captcha.com/in.php?' \
          'key=' + cap_key + \
          '&method=userrecaptcha' \
          '&pageurl=https://www.inipec.gov.it/cerca-pec/-/pecs/companies' \
          '&googlekey=' + data_sitekey
    # the site will return the id of the captcha element
    response = urllib.request.urlopen(url).read()
    captcha_id = response.decode("ascii").split("|")[1]

    # Actual solving of the captcha
    url = 'https://2captcha.com/res.php?' \
          'key=' + cap_key + \
          '&action=get' \
          '&id=' + captcha_id
    token = urllib.request.urlopen(url).read().decode('ascii')
    while token == 'CAPCHA_NOT_READY':
        sleep(5)
        print("still waiting")
        token = urllib.request.urlopen(url).read().decode('ascii')

    print('Captcha token obtained: ' + token[0:20] + '...')
    return token.split("|")[1]
