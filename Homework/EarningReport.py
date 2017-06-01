""" Quarterly Earning Report Docstring
    This module implements the functions: get_quarter_begin, get_quarter_end,
        get_current_quarter_dates, print_last_day_quarter,
        get_default_report_dates, get_yahoo, and get_earnings_data.
    The get_quarter_begin function calculates the first day of the current quarter.
    The get_quarter_end function calculates the last day of the current quarter.
    The get_current_quarter_dates returns the formatted begin and end dates.
    The get_earnings_data first calls get_yahoo and if no earnings date, then
        calls get_default_report_dates for the estimated earnings report dates.
    The get_yahoofunction will download stock price data from Yahoo finance,
        saves the daily quote information and returns the earnings report date(s).
"""

import bisect
from collections import OrderedDict
import datetime
import json
import logging

from time import sleep
import requests
from lxml import html


def get_quarter_begin():
    """ Returns the first day of the current quarter
        Uses the bisect and datetime libraries.
    Returns:
        datetime.date: The return value is the first day of fiscal quarter: yyyy-mm-dd.
    """
    today = datetime.date.today()
    qbegins = [datetime.date(today.year, month, 1) for month in (1, 4, 7, 10)]
    idx = bisect.bisect(qbegins, today)
    return qbegins[idx-1]


def get_quarter_end(par_date=None):
    """ Returns the last day of the current fiscal quarter.
        Uses the datetime library.
    Args:
         par_date (datetime.date): Optional argument, the default date is today.
    Returns:
        datetime.date: The return value is the last day of fiscal quarter: yyyy-mm-dd.
    """
    if par_date is None:
        date = datetime.date.today()
    else:
        date = par_date
    quarter = int((date.month - 1) / 3 + 1)
    month = 3 * quarter
    remaining = int(month / 12)
    return(datetime.date(date.year + remaining, month % 12 + 1, 1) +
           datetime.timedelta(days=-1))


def get_current_quarter_dates():
    """ Returns start and end dates of current quarter formatted to use in function call.
        Uses the strftime method from the datetime library.
    Returns:
        begin_quarter: (str) format mm-dd-yyyy
        end_date: (str) format mm-dd-yyyy
    """
    begin_quarter = get_quarter_begin().strftime('%m-%d-%Y')
    end_date = get_quarter_end().strftime('%m-%d-%Y')
    print("Current Quarter Date: %s to %s " % (begin_quarter, end_date))


def print_last_day_quarter():
    """ Helper function for printing results of get_last_day_quarter()
        Uses the strftime method to format the date from the datetime library.
    """
    quater_end_date = get_quarter_end()
    quater_end_date = quater_end_date.strftime('%B %d, %Y')
    print("The current fiscal quarter ends on %s.\n" % quater_end_date)


def get_default_report_dates(par_end_date=None):
    """Uses datetime library to return the default report date range.
    Args:
        par_end_date (datetime.date): Optional arg, default date is last day of current quarter.
    Returns:
        first_date (datetime.date): The first return value.
        last_date (datetime.date): The second return value.
    """
    if par_end_date is None:
        date = get_quarter_end()
    else:
        date = get_quarter_end(par_end_date)
    start_day_num = (date + datetime.timedelta(days=30)).weekday()
    day_num_target = 4
    diff = day_num_target - start_day_num
    last_date = (date + datetime.timedelta(days=30)) + datetime.timedelta(days=diff)
    first_date = last_date - datetime.timedelta(days=4)
    return first_date, last_date


def get_yahoo(ticker):
    """This function is a modified version of the code from the website:
    https://www.scrapehero.com/scrape-yahoo-finance-stock-market-data/
    The Scraping Logic starts by constructing the URL of the search
    results page from Yahoo Finance, e.g. the URL for Apple is:
    http://finance.yahoo.com/quote/AAPL?p=AAPL. The data from the search
    result page is downloaded using Python Requests and then parsed
    using LXML to navigate the HTML Tree Structure using XPaths with
    predefined XPaths for the details we need in the code. Saved values:
    "Previous Close"; "Open"; "Bid"; "Ask"; "Day's Range"; "52 Week Range";
        "Volume"; "Avg. Volume"; "Market Cap"; "Beta"; "PE Ratio (TTM)";
        "EPS (TTM)"; "Earnings Date"; "Dividend & Yield";
        "Ex-Dividend Date"; "1y Target Est"; "ticker"; "url"
    Args:
        ticker (str): company stock ticker symbol
    Returns:
        earnings_date (datetime date): formatted earnings date(s)
        date_list (list): list of dates with format mm/dd/yyyy
    """
    url = "http://finance.yahoo.com/quote/%s?p=%s" % (ticker, ticker)
    response = requests.get(url)
    logging.info("Parsing %s", str(url))
    sleep(4)
    parser = html.fromstring(response.text)
    summary_table = parser.xpath('//div[contains(@data-test,"summary-table")]//tr')
    summary_data = OrderedDict()
    other_details_json_link = \
        "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{0}?formatted=true&lang=" \
        "en-US&region=US&modules=summaryProfile%2CfinancialData%2CrecommendationTrend%2Cupgrade" \
        "DowngradeHistory%2Cearnings%2CdefaultKeyStatistics%2CcalendarEvents&corsDomain" \
        "=finance.yahoo.com".format(ticker)
    summary_json_response = requests.get(other_details_json_link)

    try:
        json_loaded = json.loads(summary_json_response.text)
        target = json_loaded["quoteSummary"]["result"][0]["financialData"]["targetMeanPrice"]['raw']
        earnings_list = json_loaded["quoteSummary"]["result"][0]["calendarEvents"]['earnings']
        eps = json_loaded["quoteSummary"]["result"][0]["defaultKeyStatistics"]["trailingEps"]['raw']
        date_list = []
        dateformatlist = []
        for i in earnings_list['earningsDate']:
            date_format = datetime.datetime.fromtimestamp(i["raw"]).strftime('%B %d, %Y')
            dateformatlist.append(date_format)
            date = datetime.datetime.fromtimestamp(i["raw"]).strftime('%m-%d-%Y')
            date_list.append(date)
        earnings_date = " - ".join(dateformatlist)
        for table_data in summary_table:
            raw_table_key = table_data.xpath('.//td[@class="C(black)"]//text()')
            raw_table_value = table_data.xpath('.//td[contains(@class,"Ta(end)")]//text()')
            table_key = ''.join(raw_table_key).strip()
            table_value = ''.join(raw_table_value).strip()
            summary_data.update({table_key: table_value})
        summary_data.update(
            {'1y Target Est': target, 'EPS (TTM)': eps,
             'Earnings Date': earnings_date, 'ticker': ticker, 'url': url})
        logging.info("Writing data to JSON output file")
        # store date in a JSON tree
        with open('%s_summary.json' % ticker, 'w') as file:
            json.dump(summary_data, file, indent=4)
        return earnings_date, date_list

    except ValueError:
        print("Failed to parse json response")
        return {"error": "Failed to parse json response"}


def get_earnings_data(company, ticker=None):
    """ Calls get_current_data() to get the next earnings report date and writes
        data to JSON file since we may want to show more than just the next earnings date.
    Args:
        company (str): First parameter, the company's name.
        ticker (str): Optional, the company stock ticker symbol.
    Returns:
        datelist (list): The return value. A list of 1 or 2 report dates mm/dd/yyyy.
    """
    company_dict = {"AMAZON": "AMZN", "APPLE": "AAPL", "GOOGLE": "GOOG",
                    "MICROSOFT": "MSFT", "NETFLIX": "NFLX"}
    if ticker is None:
        company = company.upper()
        stock = company_dict[company]
    else:
        ticker = ticker.upper()
        stock = ticker
    logging.info("Fetching data for %s", str(stock))
    earnings_date, date_list = get_yahoo(stock)
    if earnings_date == "":
        report_date1, report_date2 = get_default_report_dates()
        report_date1 = report_date1.strftime('%B %d, %Y')
        report_date2 = report_date2.strftime('%B %d, %Y')
        print("The next earnings report from %s is expected: %s - %s.\n" %
              (stock, str(report_date1), str(report_date2)))
    else:
        print("The next earnings report from %s is expected: %s.\n" %
              (stock, earnings_date))
    return date_list


if __name__ == "__main__":
    print(get_current_quarter_dates())
    print_last_day_quarter()
    get_earnings_data("Google")
