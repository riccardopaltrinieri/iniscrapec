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
 
### Installation

iniscrapec requires [python 3.7](https://https://www.python.org/) to run.       
How to get it from git
```sh
$ git clone https://github.com/riccardopaltrinieri/iniscrapec.git
```
How to install it with pip
```sh
$ pip install iniscrapec==0.0.2
```
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
