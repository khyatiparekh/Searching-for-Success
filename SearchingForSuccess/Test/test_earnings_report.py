"""Quarterly Earning Report Unit test Docstring

Unit tests for EarningReport.py. THis uses a hardcoded
date that this test was written on to pass into other functions.
"""

import datetime
import unittest

from EarningReport import get_quarter_begin, get_default_report_dates, get_quarter_end, get_current_quarter_dates, get_yahoo, get_earnings_data

DATE = datetime.date(2017, 6, 5)


class TestEarningsReport(unittest.TestCase):

    """ This class runs all the unit tests for EarningReports
        It uses the date defined above as a hardcoded date instead
        using current datetime.
    """
    def test_get_quarter_begin(self):
        """
        Unit test for the function get_quarter_begin
        """
        test = get_quarter_begin()
        self.assertEqual((str(test)), '2017-04-01')

    def test_quarter_end(self):
        """
        Unit test for the function get_quarter_end
        """
        get_quarter_end(DATE)
        self.assertEqual('2017-06-30', str(get_quarter_end(DATE))

                         )

    def test_default_report_dates(self):
        """
        Unit test for the function get_quarter_end
        """
        self.assertEqual((datetime.date(2017, 7, 24), datetime.date(2017, 7, 28)),
                         get_default_report_dates(DATE))

    def test_get_earning_data(self):
        """
        Unit test for the function get_quarter_end
        """
        self.assertEqual(['07-25-2017', '07-30-2017'], get_earnings_data('amazon'))


if __name__ == '__main__':
    unittest.main()
