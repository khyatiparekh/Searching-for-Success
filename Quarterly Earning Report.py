""" Quarterly Earning Report Docstring
This module implement four functions: get_quarter_last_day, get_default_report_dates, 
current_data and get_data. get_qrater_last_day will calculate the last of the current quarter.
current_data function will download stock price data from Yahoo finance and extract 
earnings report date for selected company and get_data will read result from current_data. 
And if the data from Yahoo finance is not available, 
the output will be calculated from get_default_report_dates function.
""" 

# Import libraries
import numpy as np
import datetime
import json
import logging
import requests
import time

from lxml import html
from pandas.tseries.offsets import BDay 
from collections import OrderedDict
from time import sleep

def get_quarter_last_day(date):
    """
    Returns the last day of the current quarter.
    """
    quarter = int((date.month - 1) / 3 + 1)
    month = 3 * quarter
    remaining = int(month / 12)
    return(datetime.datetime(date.year + remaining, month % 12 + 1, 1) + 
           datetime.timedelta(days=-1))

def get_default_report_dates(date):
    """
    Uses datetime library to return the default report date range.
    """
    if (date + datetime.timedelta(days=32)).isoweekday() == 5:
        last_date = date + datetime.timedelta(days=32)
    elif (date + datetime.timedelta(days=33)).isoweekday() == 5:
        last_date = date + datetime.timedelta(days=33)
    elif (date + datetime.timedelta(days=34)).isoweekday() == 5:
        last_date = date + datetime.timedelta(days=34)
    elif (date + datetime.timedelta(days=35)).isoweekday() == 5:
        last_date = date + datetime.timedelta(days=35)
    elif (date + datetime.timedelta(days=36)).isoweekday() == 5:
        last_date = date + datetime.timedelta(days=36)
    elif (date + datetime.timedelta(days=37)).isoweekday() == 5:
        last_date = date + datetime.timedelta(days=37)
    else:
        last_date = date + datetime.timedelta(days=38)
    first_date = last_date - BDay(5)
    #print("5 business days from last_date:", (last_date - BDay(5)))    
    return first_date, last_date


def currentdata(ticker):
    """
    The currentdata function is a modified version of the code from the website:
    https://www.scrapehero.com/scrape-yahoo-finance-stock-market-data/
    The Scraping Logic for currentdata()
    Construct the URL of the search results page from Yahoo Finance. 
    For example, the URL for Apple-http://finance.yahoo.com/quote/AAPL?p=AAPL
    Download HTML of the search result page using Python Requests.
    Parse the page using LXML; LXML lets you navigate the 
    HTML Tree Structure using Xpaths. 
    We have predefined the XPaths for the details we need in the code.
    The data is then returned in a JSON format.
    """
    url = "http://finance.yahoo.com/quote/%s?p=%s" % (ticker, ticker)
    response = requests.get(url)
    logging.info("Parsing %s" % (url))
    sleep(4)
    parser = html.fromstring(response.text)
    summary_table = parser.xpath('//div[contains(@data-test,"summary-table")]//tr')
    summary_data = OrderedDict()
    other_details_json_link = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{0}?formatted=true&lang=en-US&region=US&modules=summaryProfile%2CfinancialData%2CrecommendationTrend%2CupgradeDowngradeHistory%2Cearnings%2CdefaultKeyStatistics%2CcalendarEvents&corsDomain=finance.yahoo.com".format(ticker)
    summary_json_response = requests.get(other_details_json_link)
    try:
        json_loaded_summary = json.loads(summary_json_response.text)
        y_Target_Est = json_loaded_summary["quoteSummary"]["result"][0]["financialData"]["targetMeanPrice"]['raw']
        earnings_list = json_loaded_summary["quoteSummary"]["result"][0]["calendarEvents"]['earnings']
        eps = json_loaded_summary["quoteSummary"]["result"][0]["defaultKeyStatistics"]["trailingEps"]['raw']
        datelist = []
        dateformatlist = []
        datefmt = "%m/%d/%Y"
        for i in earnings_list['earningsDate']:
            date_format = datetime.datetime.fromtimestamp(i["raw"]).strftime('%B %d, %Y')
            dateformatlist.append(date_format)
            date = datetime.datetime.fromtimestamp(i["raw"]).strftime('%m-%d-%Y')
            datelist.append(date)
        earnings_date = " - ".join(dateformatlist)
        for table_data in summary_table:
            raw_table_key = table_data.xpath('.//td[@class="C(black)"]//text()')
            raw_table_value = table_data.xpath('.//td[contains(@class,"Ta(end)")]//text()')
            table_key = ''.join(raw_table_key).strip()
            table_value = ''.join(raw_table_value).strip()
            summary_data.update({table_key: table_value})
        summary_data.update(
            {'1y Target Est': y_Target_Est, 'EPS (TTM)': eps, 
             'Earnings Date': earnings_date, 'ticker': ticker, 'url': url})
        return earnings_date, datelist, summary_data
    except ValueError:
        print("Failed to parse json response")
        return {"error": "Failed to parse json response"}

def getdata(ticker):
    """
    Currently only gets data from currentdata() and writes the data to a
    JSON file since we may want to show more than just the next earnings date.
    The next earings release date from to Yahoo is returned.
    """
    earnings_date, datelist, current_data = currentdata(ticker)
    logging.info("Writing data to output file")
    with open('%s_summary.json' % (ticker), 'w') as fp:
        json.dump(current_data, fp, indent=4)
    return earnings_date, datelist

# the code below this line would essentially go in main()
today = datetime.date.today()
quart_end = get_quarter_last_day(today)
rep_date1, rep_date2 = get_default_report_dates(quart_end)
# the reformatting must occur after the report date function is called
quart_end = quart_end.strftime('%B %d, %Y')
print("The current fiscal quarter ends on %s.\n" % quart_end)

stocks = ["AMZN"] #"AAPL", "GOOG", "MSFT", "NFLX"
for stock in stocks:
    logging.info("Fetching data for %s" % (stock))
    earnings_date, datelist = getdata(stock)
    if earnings_date == "":
        rep_date1 = rep_date1.strftime('%B %d, %Y')
        rep_date2 = rep_date2.strftime('%B %d, %Y')
        print("The next earnings report from %s is expected: %s - %s.\n" % 
              (stock, str(rep_date1), str(rep_date2)))
    else:
        print("The next earnings report from %s is expected: %s.\n" % 
              (stock, earnings_date))