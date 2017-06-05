import unittest
import pandas as pd
from sklearn.linear_model import LassoCV
import numpy as np
from Submodule.PredictionStockPrice import *
from sklearn import linear_model

mic_data = pd.read_csv('Microsoft.csv')
kw = mic_data.drop('Price', axis=1)
kw = kw.drop('Date', axis=1)
pr = mic_data.Price

class TestPredictionStockPrice(unittest.TestCase):


    def test_feature_selection_Success(self):
        expected_beta = [ 0,0,0.15377572,0.01381917,0.02242265,0.00396967, 0.1834983,0.01472143,0.02718057,-0.23020966,0,0.00387069,0.18631227,0,0.17873151]
        test_beta = feature_selection(kw, pr)

        self.assertEqual(np.around(test_beta, decimals=1).all(), np.around(expected_beta, decimals=1).all())

    def test_feature_selection_Fail(self):
        expected_beta = [ 1,0,0.15377572,0.01381917,0.02242265,0.00396967, 0.1834983,0.01472143,0.02718057,-0.23020966,0,0.00387069,0.18631227,0,0.17873151]
        test_beta = feature_selection(kw, pr)

        self.assertNotEqual(np.around(test_beta, decimals=1)[0], np.around(expected_beta, decimals=1)[0])

    def test_prediction_model_Success(self):
        mic_data = pd.read_csv('Microsoft.csv')
        keywords = mic_data.drop('Price', axis=1)
        keywords = keywords.drop('Date', axis=1)
        price = mic_data.Price

        beta_coeff = feature_selection(keywords, price)
        # Transfrom Stock Price to Price Change. 1 for positive change 0 for not positive change.
        mic_data['Price Change'] = mic_data['Price'].diff()
        mic_data['Price Change'][mic_data['Price Change'] > 0] = 1
        mic_data['Price Change'][mic_data['Price Change'] <= 0] = 0
        mic_data = mic_data.dropna(axis=0, how='any')
        keywords = mic_data[beta_coeff.argsort()[-5:][::-1]]
        price = mic_data['Price Change']

        # Logistic Regression Model
        model = linear_model.LogisticRegression(penalty='l2', fit_intercept=False, tol=10e-8, max_iter=1000)
        model.fit(keywords, price)
        prob = np.mean(model.predict(keywords[-90:]))
        expected_prediction = prob

        test_prediction = prediction_model(keywords, price)
        self.assertEqual(np.around(test_prediction, decimals=2), np.around(expected_prediction, decimals=2))

    def test_prediction_model_Fail(self):
        mic_data = pd.read_csv('Microsoft.csv')
        keywords = mic_data.drop('Price', axis=1)
        keywords = keywords.drop('Date', axis=1)
        price = mic_data.Price

        beta_coeff = feature_selection(keywords, price)
        # Transfrom Stock Price to Price Change. 1 for positive change 0 for not positive change.
        mic_data['Price Change'] = mic_data['Price'].diff()
        mic_data['Price Change'][mic_data['Price Change'] > 0] = 1
        mic_data['Price Change'][mic_data['Price Change'] <= 0] = 0
        mic_data = mic_data.dropna(axis=0, how='any')
        keywords = mic_data[beta_coeff.argsort()[-5:][::-1]]
        price = mic_data['Price Change']
        expected_prediction = 1

        test_prediction = prediction_model(keywords, price)
        self.assertNotEqual(np.around(test_prediction, decimals=2), np.around(expected_prediction, decimals=2))

    def test_prediction_stock_price_Microsoft_Success(self):
        test_Output = prediction_stock_price('Microsoft')
        expected_Output = """Predicted probability the stock price will increase after releasing next quarter’s earnings report: 0.20"""
        self.assertEqual(test_Output, expected_Output)

    def test_prediction_stock_price_Google_Success(self):
        test_Output = prediction_stock_price('Google')
        expected_Output = """Predicted probability the stock price will increase after releasing next quarter’s earnings report: 1.00"""
        self.assertEqual(test_Output, expected_Output)

    def test_prediction_stock_price_Amazon_Success(self):
        test_Output = prediction_stock_price('Amazon')
        expected_Output = """Predicted probability the stock price will increase after releasing next quarter’s earnings report: 0.92"""
        self.assertEqual(test_Output, expected_Output)

    def test_prediction_stock_price_InValidQuote_Success(self):
        test_Output = prediction_stock_price('InValidQuote')
        expected_Output = 'No Data Available'
        self.assertEqual(test_Output, expected_Output)

    def test_prediction_stock_price_0_Success(self):
        test_Output = prediction_stock_price(0)
        expected_Output = 'No Data Available'
        self.assertEqual(test_Output, expected_Output)

if __name__ == '__main__':
    unittest.main()
