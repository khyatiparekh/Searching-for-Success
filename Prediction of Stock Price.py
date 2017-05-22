""""Prediction of Stock Price Docstring

This mocdule implement three functions: feature_selection,
prediction_model and prediction_stock_price. The first function,
featues_selection will use Lasso regression model to select
6 keywords that are significant to the company's stock performance.
And the second function predcition_model will predict the
likelihood of stock prices increase or decrease after upcomming
earning report released for given company. And the third function
prediction _stock_price will call the previous functions
based on the company name input.
"""

# Import libraries
import pandas as pd
import numpy as np


def feature_selection(X, y):
    """Given Google trends data on several keywords and the
       stock price performance on same company, this will select
       the most significant keywords that relate to the stock performance.

    Parameters
    ----------
    X: Dataframe.
       Data downloaded from Google Trends of standardized daily searched
       counts for selected keywords.Independent Variables.
    y: Array.
       Standardized daily stock prices for given company.

    Returns
    ------
    Output: Array
            The estimated coefficients of each keywords. The larger the
            absolute value the coefficient is, the more significant the
            keyword is to the stock performance.

    """

    # Import Libraries
    from sklearn.linear_model import LassoCV
    from sklearn.preprocessing import StandardScaler

    lasso = LassoCV(fit_intercept=False).fit(X, y)
    lambda_opt = lasso.alpha_*2
    beta_star = lasso.coef_
    return beta_star, lambda_opt


def prediction_model(X, y):
    """Given Google trends data on several keywords and the stock
       price performance on same company, this will select the most
       significant keywords that relate to the stock performance.

    Parameters
    ----------
    X: Dataframe.
    Data from Google Trends with keywords selected from feature_selection
    function only. Independent Variables.
    y: Array.
    Standardized daily stock prices for given company.

    Returns
    ------
    Output: float
    The likelihood of stock price increase. Value between 0 and 1.
    """

    # Import Libraries
    import datetime
    from sklearn import linear_model

    # Logistic Regression Model
    lr = linear_model.LogisticRegression(penalty='l2', fit_intercept=False, tol=10e-8, max_iter=1000)
    lr.fit(X, y)
    coef = lr.coef_
    return(np.mean(lr.predict(X[-90:])))


def prediction_stock_price(company):
    """Given Google trends data on several keywords and the stock
    price performance on same company, this will output the likelihood
    of the stock price increase for input company.

    Parameters
    ----------
    X: Dataframe.
    Data downloaded from Google Trends of standardized daily searched
    counts for selected keywords.Independent Variables. GoogleTrends.csv,
    MicrosoftTrends.csv and AmazonTrends.csv will be used based on
    the company selected.
    y: Array.
    Standardized daily stock prices for given company.

    Returns
    ------
    Output: Statement
    The likelihood of stock price increase for input company.
    Value between 0 and 1.

    """

    if company == 'Google':
        data = pd.read_csv('GoogleTrends.csv', sep=',')
    elif company == 'Microsoft':
        data = pd.read_csv('MicrosoftTrends.csv', sep=',')
    elif company == 'Amazon':
        data = pd.read_csv('AmazonTrends.csv', sep=',')
    else:
        print ('No Data Available')

    # Data Preparation
    X = data.drop('Price', axis=1)
    X = X.drop('date', axis=1)
    scaler = StandardScaler()
    y = data.Price
    y = scaler.fit_transform(y)

    beta_coeff, lamb = feature_selection(X, y)
    beta_coeff.argsort()[-6:][::-1]

    """Prepare Data for Logistic Regression. Transfrom Stock
    Price to Price Change. 1 for positive change 0 for not positive change."""
    data['Price Change'] = data['Price'].diff()
    data['Price Change'][data['Price Change'] > 0] = 1
    data['Price Change'][data['Price Change'] <= 0] = 0
    data = data.dropna(axis=0, how='any')
    X = data[beta_coeff.argsort()[-6:][::-1]]
    y = data['Price Change']

    prediction_model(X, y)
    print ("""Predicted probability the stock price will increase after
           releasing next quarter’s earnings report:  %.2f"""
           % prediction_model(X, y))

    # Result for Google, Microsoft and Amazon
    prediction_stock_price('Google')
    prediction_stock_price('Microsoft')
    prediction_stock_price('Amazon')
