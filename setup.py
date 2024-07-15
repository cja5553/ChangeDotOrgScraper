from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(here, "README.md")
with codecs.open(readme_path, encoding="utf-8") as fh:
    long_description = fh.read()
VERSION = '0.0.4'
DESCRIPTION = 'Scrapes online petition data from change.org'
LONG_DESCRIPTION = 'A package that scrapes online petition data from change.org, including the title, description, target audience, signature count, creator name, date created, location created, and victory status. Works by simply providing the url of the change.org petition search.'

# Setting up
setup(
    name="ChangeDotOrgScraper",
    version=VERSION,
    author="Charles Alba",
    author_email="alba@wustl.edu",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['requests','bs4', 'tqdm', 'pandas','ast'],
    license='MIT',
    keywords=['change.org','petitions','web scraping'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)