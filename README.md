# iniscrapec

iniscrapec is a simple scraper project that take a TAX Code of a company and return the PEC address 
of it

### Tech

iniscrapec uses a number of open source projects to work properly:

* [pip]==20.2.2
* [beautifulsoup4]~=4.9.1
* [mechanize]~=0.4.5
* [pymongo]~=3.11.0
* [dnspython]~=2.0.0
* [python_dotenv]~=0.14.0
* [setuptools]~=50.3.0

And iniscrapec itself is open source with a [public repository](https://github.com/riccardopaltrinieri/iniscrapec)
on GitHub.

Also it uses a third part service to solve the reCaptcha "I am not a robot"

* [[2captcha]](https://2captcha.com/)
 
### Installation

iniscrapec requires [python 3.7](https://https://www.python.org/) to run.       

How to get it from git
```sh
$ git clone https://github.com/riccardopaltrinieri/iniscrapec.git
```
<sub> 
You can also install it from pip with
*pip install iniscrapec* but something doesn't work well
</sub>

#### After installation
You need to fill the environment variables in the .env file:    
```
CAP_KEY = "" # The API key given from the site 2capthca.com
DB_USER = "" # The user of the Mongo DB 
DB_PWD = "" # The password of the Mongo DB
DATA_SITEKEY = "" # The captcha code as written in the step 2 of the link below
URL = "https://www.inipec.gov.it/cerca-pec/-/pecs/companies" #the gov website where to search the pec
TAX_EXAMPLE = "" # Variable used for testing and debugging
```
[link on how to use 2captcha](https://2captcha.com/2captcha-api#solving_recaptchav2_new)        

How to run it with a simple [tkinter] gui
```sh
$ cd .\path\of\repo\iniscrapec
$ python3 iniscrapec.py
```
You can also use only the scraper code with
```sh
$ cd .\iniscrapec\modules
$ python3 scraper.py
```

License
----

MIT
