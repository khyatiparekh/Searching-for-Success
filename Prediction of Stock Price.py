"""Prediction of Stock Price Docstring

This mocdule implement two functions: feature_selection
and prediction_model. The first function, featues_selection will
use Lasso regression model to select keywords that are significant
to the company's stock performance. And the second function predcition_model
will predict the likelihood of stock prices increase or decrease
after upcomming earning report released for given company.
"""

#Import Libraries
import pandas as pd

from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler

# Data Preparation
amazon = pd.read_csv('amazonTrends.csv', sep=',')
amazon.dropna(axis=0, how='any')
X = amazon.drop('Price', axis=1)
X = X.drop('date', axis=1)
scaler = StandardScaler()
y = amazon.Price
y = scaler.fit_transform(y)

def feature_selection(X, y):
    """Given Google trends data on several keywords and the stock price performance on 
       same company, this will select the most significant keywords that relate to
       the stock performance.
       
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
            The estimated coefficients of each keywords. The larger the absolute value 
            the coefficient is, the more significant the keyword is to the stock performance.

    """
    lasso = LassoCV(fit_intercept=False).fit(X, y)
    lambda_opt = lasso.alpha_*2  # Note scikit-learn's objective function is different from ours
    beta_star = lasso.coef_
    return beta_star, lambda_opt
beta_coeff, lamb = feature_selection(X,y)
beta_coeff.argsort()[-3:][::-1]
print('The number of column of keywords that are important to stock prices are  %s' % (beta_coeff.argsort()[-3:][::-1]))

#Prepare Data for Logistic Regression. Transfrom Stock Price to Price Change. 1 for positive change 0 for not positive change.
amazon['Price Change'] = amazon['Price'].diff()
amazon['Price Change'][amazon['Price Change']>0]=1
amazon['Price Change'][amazon['Price Change']<=0]=0
amazon = amazon.dropna(axis=0, how='any')
X = np.column_stack((amazon['Amazon Error'],amazon['Amazon Kindle']))
X = np.column_stack((X,amazon['Amazon Order']))
y = amazon['Price Change']

def prediction_model(X, y):
    """Given Google trends data on several keywords and the stock price performance on 
       same company, this will select the most significant keywords that relate to
       the stock performance.

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
        The estimated coefficients of each keywords. The larger the absolute value 
        the coefficient is, the more significant the keyword is to the stock performance.

    """

    # Import Libraries
    import datetime
    from sklearn import linear_model

    #Logistic Regression Model
    lr = linear_model.LogisticRegression(penalty='l2', fit_intercept=False, tol=10e-8, max_iter=1000)
    lr.fit(X, y)
    coef = lr.coef_ #coefficient for 'Amazon Error', 'Amazon Kindle' and 'Amazon Order'
    return(np.mean(lr.predict(X[-90:]))) # predict upcomming quarter
print ('Predicted probability the stock price will increase after releasing next quarter’s earnings report:  %.2f' % prediction_model(X, y))