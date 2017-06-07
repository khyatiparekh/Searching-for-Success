"""
Unit tests for checking the availability of data
"""

import unittest
import pandas as pd

class TestPredictionStockPrice(unittest.TestCase):
    """
    Unit tests data availability
    """
    def setUp(self):
        self.goog_data = pd.read_csv('Google.csv', sep=',')
        self.amzn_data = pd.read_csv('Amazon.csv', sep=',')
        self.mic_data = pd.read_csv('Microsoft.csv', sep=',')


    def test_data_microsoft_success(self):
        """
        Checking if the selected keywords are in the Dataset
        """
        expected_columns = ('Outlook' and
                            'Powerpoint' and
                            'Office Product Key' and
                            'Excel' and
                            'Skype')

        test_columns = self.mic_data.columns
        self.assertTrue(expected_columns in test_columns)

    def test_data_microsoft_fail(self):
        """
        Checking if the selected keywords are in the Dataset
        """
        expected_columns = ('utlook' and
                            'owerpoint' and
                            'Offce Product Key' and
                            'Exel' and
                            'Sype')

        test_columns = self.mic_data.columns
        self.assertFalse(expected_columns in test_columns)

    def test_data_amazon_success(self):
        """
        Checking if the selected keywords are in the Dataset
        """
        expected_columns = ('Amazon kindle' and
                            'Amazon order' and
                            'Amazon recall' and
                            'Amazon register' and
                            'Amazon sucks')

        test_columns = self.amzn_data.columns
        self.assertTrue(expected_columns in test_columns)

    def test_data_amazon_fail(self):
        """
        Checking if the selected keywords are in the Dataset
        """
        expected_columns = ('kindle' and
                            'order' and
                            'recall' and
                            'register' and
                            'sucks')

        test_columns = self.amzn_data.columns
        self.assertFalse(expected_columns in test_columns)

    def test_data_google_success(self):
        """
        Checking if the selected keywords are in the Dataset
        """
        expected_columns = ('Earth' and
                            'Maps' and
                            'Chrome' and
                            'Cardboard' and
                            'Nexus')

        test_columns = self.goog_data.columns
        self.assertTrue(expected_columns in test_columns)

    def test_data_google_fail(self):
        """
        Checking if the selected keywords are in the Dataset
        """
        expected_columns = ('eath' and
                            'mps' and
                            'chome' and
                            'carboard' and
                            'neus')

        test_columns = self.goog_data.columns
        self.assertFalse(expected_columns in test_columns)


if __name__ == '__main__':
    unittest.main()
