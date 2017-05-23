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


def feature_selection(keywords, price):
    """Given Google trends data on several keywords and the
       stock price performance on same company, this will select
       the most significant keywords that relate to the stock performance.

    Parameters
    ----------
    keywords: Dataframe.
       Data downloaded from Google Trends of standardized daily searched
       counts for selected keywords.Independent Variables.
    price: Array.
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

    lasso = LassoCV(fit_intercept=False).fit(keywords, price)
    beta_star = lasso.coef_
    return beta_star


def prediction_model(keywords, price):
    """Given Google trends data on several keywords and the stock
       price performance on same company, this will select the most
       significant keywords that relate to the stock performance.

    Parameters
    ----------
    keywords: Dataframe.
    Data from Google Trends with keywords selected from feature_selection
    function only. Independent Variables.
    price: Array.
    Standardized daily stock prices for given company.

    Returns
    ------
    Output: float
    The likelihood of stock price increase. Value between 0 and 1.
    """

    # Import Libraries
    from sklearn import linear_model

    # Logistic Regression Model
    model = linear_model.LogisticRegression(penalty='l2', fit_intercept=False, tol=10e-8,
                                            max_iter=1000)
    model.fit(keywords, price)
    return np.mean(model.predict(keywords[-90:]))


def prediction_stock_price(company):
    """Given Google trends data on several keywords and the stock
    price performance on same company, this will output the likelihood
    of the stock price increase for input company.

    Parameters
    ----------
    keywords: Dataframe.
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
    # Import Libraries
    from sklearn.preprocessing import StandardScaler

    if company == 'Google':
        data = pd.read_csv('Google.csv', sep=',')
    elif company == 'Microsoft':
        data = pd.read_csv('Microsoft.csv', sep=',')
    elif company == 'Amazon':
        data = pd.read_csv('Amazon.csv', sep=',')
    else:
        print('No Data Available')

    # Data Preparation
    keywords = data.drop('Price', axis=1)
    keywords = keywords.drop('Date', axis=1)
    price = data.Price
    scaler = StandardScaler()
    price = scaler.fit_transform(price)

    beta_coeff = feature_selection(keywords, price)

    #Transfrom Stock Price to Price Change. 1 for positive change 0 for not positive change.
    data['Price Change'] = data['Price'].diff()
    data['Price Change'][data['Price Change'] > 0] = 1
    data['Price Change'][data['Price Change'] <= 0] = 0
    data = data.dropna(axis=0, how='any')
    keywords = data[beta_coeff.argsort()[-5:][::-1]]
    price = data['Price Change']

    prediction_model(keywords, price)
    print("""Predicted probability the stock price will increase after
           releasing next quarter’s earnings report:  %.2f"""
          % prediction_model(keywords, price))


