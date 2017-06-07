"""
Unit Tests for the methods in Prediction Stock Price
"""

import unittest
import pandas as pd
import numpy as np
from PredictionStockPrice import *
from sklearn import linear_model
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LassoCV

class TestPredictionStockPrice(unittest.TestCase):
    """
    Unit tests for each case
    """
    def setUp(self):
        self.data = pd.read_csv('Microsoft.csv')
        self.kw_no_price = self.data.drop('Price', axis=1)
        self.keyword = self.kw_no_price.drop('Date', axis=1)
        self.price = self.data.Price

    def test_feature_selection_success(self):
        """
        Testing for Feature Selection Success Case
        """
        lasso = LassoCV(fit_intercept=False).fit(self.keyword, self.price)
        expected_beta = lasso.coef_
        test_beta = feature_selection(self.keyword, self.price)
        self.assertEqual(np.around(test_beta, decimals=1).all(),
                         np.around(expected_beta, decimals=1).all())

    def test_feature_selection_fail(self):
        """
        Testing for Feature Selection Failure case
        """
        lasso = LassoCV(fit_intercept=False).fit(self.keyword, self.price)
        expected_beta = (lasso.coef_)*2
        test_beta = feature_selection(self.keyword, self.price)
        self.assertNotEqual(np.around(test_beta, decimals=1)[0],
                            np.around(expected_beta, decimals=1)[0])

    def test_prediction_model_success(self):
        """
        Testing for Prediction Model Success Case
        """
        data = self.data
        keywords = data.drop('Price', axis=1)
        keywords = keywords.drop('Date', axis=1)
        price = data.Price.values.reshape(-1, 1)
        scaler = StandardScaler()
        price = scaler.fit_transform(price).ravel()

        beta_coeff = feature_selection(keywords, price)

        data['Price Change'] = data['Price'].diff()
        data.loc[data['Price Change'] > 0] = 1
        data.loc[data['Price Change'] <= 0] = 0
        data = data.dropna(axis=0, how='any')
        keywords = data[beta_coeff.argsort()[-5:][::-1]]
        price = data['Price Change'].ravel()
        model = linear_model.LogisticRegression(penalty='l2', fit_intercept=False, tol=10e-8,
                                                max_iter=1200)
        model.fit(keywords, price.ravel())
        prob = round(np.mean(model.predict(keywords[-90:])), 3)

        expected_prediction = prob

        test_prediction = prediction_model(keywords, price)
        self.assertEqual(np.around(test_prediction, decimals=2),
                         np.around(expected_prediction, decimals=2))

    def test_prediction_model_fail(self):
        """
        Testing for Prediction Model Failure case
        """
        data = self.data
        keywords = data.drop('Price', axis=1)
        keywords = keywords.drop('Date', axis=1)
        price = data.Price.values.reshape(-1, 1)
        scaler = StandardScaler()
        price = scaler.fit_transform(price).ravel()

        beta_coeff = feature_selection(keywords, price)
        data['Price Change'] = data['Price'].diff()
        data.loc[data['Price Change'] > 0] = 1
        data.loc[data['Price Change'] <= 0] = 0
        data = data.dropna(axis=0, how='any')
        keywords = data[beta_coeff.argsort()[-5:][::-1]]
        price = data['Price Change'].ravel()
        model = linear_model.LogisticRegression(penalty='l2', fit_intercept=False, tol=10e-8,
                                                max_iter=1200)
        model.fit(keywords, price.ravel())

        expected_prediction = 1

        test_prediction = prediction_model(keywords, price)
        self.assertNotEqual(np.around(test_prediction, decimals=2),
                            np.around(expected_prediction, decimals=2))

    def test_prediction_stock_price_microsoft_success(self):
        """
         Testing for Prediction on Microsoft
        """
        test_output = prediction_stock_price('Microsoft')
        expected_output = 0.489
        self.assertEqual(test_output, expected_output)

    def test_prediction_stock_price_google_success(self):
        """
        Testing for Prediction on Google
        """
        test_output = prediction_stock_price('Google')
        expected_output = 0.644
        self.assertEqual(test_output, expected_output)

    def test_prediction_stock_price_amazon_success(self):
        """
        Testing for Prediction on Amazon
        """
        test_output = prediction_stock_price('Amazon')
        expected_output = 0.589
        self.assertEqual(test_output, expected_output)

    def test_prediction_stock_price_invalidquote_success(self):
        """
        Testing for Prediction on Invalid Quote
        """
        test_output = prediction_stock_price('InValidQuote')
        expected_output = 'No Data Available'
        self.assertEqual(test_output, expected_output)

    def test_prediction_stock_price_0_success(self):
        """
        Testin Prediction on Invalid Data
        """
        test_output = prediction_stock_price(0)
        expected_output = 'No Data Available'
        self.assertEqual(test_output, expected_output)

if __name__ == '__main__':
    unittest.main()
