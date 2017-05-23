import datetime
import unittest

from quarterly_earning_report import *

class TestQuarterlyEarningReport(unittest.TestCase):

    def test_get_last_day_quarter(self):
        END_OF_SPRING_2017 = datetime.date(2017, 6, 30)
        test_spring_date = datetime.date(2017, 5, 2) # YYYY, M, D
        test_date_value = get_last_day_quarter(test_spring_date)
        self.assertEqual(test_date_value, END_OF_SPRING_2017)

    def test_get_default_report_dates(self):
        test_fall_date = datetime.date(2017, 10, 1)
        test_fall_date = get_default_report_dates(test_fall_date)
        test_spring_date = datetime.date(2017, 5, 2)
        test_spring_date = get_default_report_dates(test_spring_date)
        self.assertIn(datetime.datetime(2017, 7, 24, 0, 0), test_spring_date)
        self.assertNotIn(datetime.datetime(2017, 7, 30, 0, 0), test_fall_date)

    def test_get_current_data(self):
        test_amazon_dates = "07-25-2017"
        returned_amazon_dates = get_earnings_data("Amazon", "AMZN")
        self.assertIn(test_amazon_dates, returned_amazon_dates)

if __name__ == '__main__':
    unittest.main()