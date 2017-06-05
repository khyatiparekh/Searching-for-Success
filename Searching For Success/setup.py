# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='searching_for_success',
    version='1.0',
    description='Predicting stock price change on earnings release based on Google Trends data',
    author='DATA 515 Group',
    author_email='data515gtrend@gmail.com',
    url='https:/github.com/khyatiparekh/Data515_FinalProject/',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Students, Investors',
        'Topic :: Stock Market Prediction :: Google Trends',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU GENERAL PUBLIC LICENSE',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='google trends stock price prediction technology company',

    PACKAGES = find_packages(),
    #packages = ['EarningReport', 'HistoricalDataPlot', 'PredictionStockPrice'],

    # List run-time dependencies here.
    install_requires=["bokeh", "cycler", "icu", "jinja2", "jpeg", "libpng",
                      "lxml", "markupsafe", "matplotlib", "mkl", "numpy",
                      "openssl", "pandas", "pyparsing", "pyqt", "python-dateutil",
                      "pytz", "pyyaml", "qt", "requests", "sip", "six", "tk",
                      "tornado",  "zlib"],

    # $ pip install -e .[dev,test]
    extras_require={
        "pytrends": ["Unofficial API for Google Trends"],
        "BeautifulSoup4": ["Screen-scraping library"],
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.
    package_data={
        'amazon': ['Data/Amazon.csv'],
        'google': ['Data/Google.csv'],
        'microsoft': ['Data/Microsoft.csv'],
    }
)
