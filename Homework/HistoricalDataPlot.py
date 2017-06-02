
# coding: utf-8

# In[22]:

"""Historical Data Plot Docstring
This module implement oen function: historical_data_plot.
The function will read data for input company with selected keywords.
And then plot Google trends for selected keywords from previous
feature selection. Then plot daily adjusted close stock
price for given company.
"""


def historical_data_plot(company):
    """Given company selection, will read data for input company with
    selected keywords.And then plot Google trends for selected
    keywords from previous feature selection. Then plot daily
    adjusted close stock price for given company.

    Parameters
    ----------
    company: string
             Input company selection from user.

    Returns
    -------
    output: Interactive Plot of standardized Google daily searched counts of
            input keywords.
            And interactive Plot of daily closed stock price for selected
            company.
    """

    # Import Libraries
    import pandas as pd
    from pytrends.request import TrendReq
    from bokeh.charts import TimeSeries
    from bokeh.plotting import show, output_notebook
    output_notebook()

    google_username = "data515gtrend@gmail.com"
    google_password = "Data515gtrend123"

    if company == 'Google':
        data = pd.read_csv('Google.csv', sep=',', parse_dates=['Date'])
        selected_kw = ["Google Earth", "Google Maps", "Google Chrome",
                       "Google Cardboard", "Google Nexus"]
        stock = dict([
            ('GOOG', data['Price']),
            ('Date', data['Date'])]
        )
    elif company == 'Microsoft':
        data = pd.read_csv('Microsoft.csv', sep=',', parse_dates=['Date'])
        selected_kw = ["Microsoft Outlook", "Microsoft Powerpoint",
                       "Microsoft Office Product Key", "Microsoft Excel",
                       "Microsoft Skype"]
        stock = dict([
            ('MSFT', data['Price']),
            ('Date', data['Date'])]
        )
    elif company == 'Amazon':
        data = pd.read_csv('Amazon.csv', sep=',', parse_dates=['Date'])
        selected_kw = ["Amazon kindle", "Amazon order", "Amazon recall",
                       "Amazon register", "Amazon sucks"]
        stock = dict([
            ('AMZN', data['Price']),
            ('Date', data['Date'])]
        )
    else:
        print('No Data Available')
    pytrend = TrendReq(google_username, google_password,
                       custom_useragent='My Pytrends Script')
    pytrend.build_payload(kw_list=selected_kw,
                          timeframe='2006-10-01 2017-3-31')
    interest_over_time_df_amazon = pytrend.interest_over_time()
    trends_plot = TimeSeries(interest_over_time_df_amazon, xlabel='Date', dash=selected_kw, color=selected_kw)
    stock_plot = TimeSeries(stock, title="Daily Stock Adjusted Close Price",
                            ylabel='Stock Prices', x='Date')
    trends_plot.legend.location = "top_left"
    trends_plot.legend.click_policy='hide'
    trends_plot.title.text = 'Click on legend entries to hide the corresponding keywords lines'
    show(trends_plot)
    show(stock_plot)


# In[ ]:




# In[ ]:



