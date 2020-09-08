from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_descript = fh.read()

setup(
    name='inipec-scraper',
    version='0.0.2',
    packages=find_packages(),
    url='https://github.com/riccardopaltrinieri/inipec-scraper',
    license='MIT',
    author='Riccardo Paltrinieri',
    author_email='paltrinieri.rg@gmail.com',
    description='Web scraper that take a TAX Code and return the PEC address of the company',
    long_description=long_descript,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
