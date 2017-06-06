import unittest
import pandas as pd
import numpy as np
from PredictionStockPrice import *
from sklearn import linear_model
from sklearn.preprocessing import StandardScaler

data = pd.read_csv('Microsoft.csv')
kw = data.drop('Price', axis=1)
kw = kw.drop('Date', axis=1)
pr = data.Price


class TestPredictionStockPrice(unittest.TestCase):
    def test_feature_selection_success(self):
        expected_beta = [0, 0, 0.15377572, 0.01381917, 0.02242265, 0.00396967, 0.1834983,
                         0.01472143, 0.02718057, -0.23020966, 0, 0.00387069, 0.18631227,
                         0, 0.17873151]
        test_beta = feature_selection(kw, pr)
        self.assertEqual(np.around(test_beta, decimals=1).all(),
                         np.around(expected_beta, decimals=1).all())

    def test_feature_selection_fail(self):
        expected_beta = [1, 0, 0.15377572, 0.01381917, 0.02242265, 0.00396967, 0.1834983,
                         0.01472143, 0.02718057, -0.23020966, 0, 0.00387069, 0.18631227,
                         0, 0.17873151]
        test_beta = feature_selection(kw, pr)
        self.assertNotEqual(np.around(test_beta, decimals=1)[0],
                            np.around(expected_beta, decimals=1)[0])

    def test_prediction_model_success(self):
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
        test_output = prediction_stock_price('Microsoft')
        expected_output = 0.489
        self.assertEqual(test_output, expected_output)

    def test_prediction_stock_price_google_success(self):
        test_output = prediction_stock_price('Google')
        expected_output = 0.644
        self.assertEqual(test_output, expected_output)

    def test_prediction_stock_price_amazon_success(self):
        test_output = prediction_stock_price('Amazon')
        expected_output = 0.589
        self.assertEqual(test_output, expected_output)

    def test_prediction_stock_price_invalidquote_success(self):
        test_output = prediction_stock_price('InValidQuote')
        expected_output = 'No Data Available'
        self.assertEqual(test_output, expected_output)

    def test_prediction_stock_price_0_success(self):
        test_output = prediction_stock_price(0)
        expected_output = 'No Data Available'
        self.assertEqual(test_output, expected_output)

if __name__ == '__main__':
    unittest.main()
