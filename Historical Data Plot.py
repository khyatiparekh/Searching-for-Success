"""Historical Data Plot Docstring
This module implement two functions: google_search_trends_plot and stock_plot.
The first function, google_search_rends_plot, plot Google trends for selected
keywords form feature selection. The second function, plot daily adjusted close stock
price for given company.
"""

def google_search_trends_plot(selected_kw):
    """Given keywords list, this plot the standardized Google daily searched counts.
    
    Parameters
    ----------
    selected_kw: Array
                 Selected keywords array identified from feature selection function 
                 on given company.
    
    Returns
    -------
    output: Interactive Plot of standardized Google daily searched counts of input keywords.
    """
    
    # Import Libraries
    import bokeh
    import pandas as pd

    from pytrends.request import TrendReq
    from bokeh.charts import TimeSeries, show, output_file, Line
    from bokeh.layouts import column
    %matplotlib inline
    from bokeh.plotting import figure, output_file, show, output_notebook 
    output_notebook()

    google_username = "data515gtrend@gmail.com"
    google_password = "Data515gtrend123"
    path = ""

    # Login to Google. Only need to run this once, the rest of requests will use the same session.
    pytrend = TrendReq(google_username, google_password, custom_useragent='My Pytrends Script')
    pytrend.build_payload(kw_list=selected_kw, timeframe='2006-10-01 2017-3-31')

    # Interest Over Time
    interest_over_time_df = pytrend.interest_over_time()
    p = TimeSeries(interest_over_time_df, xlabel='Date')
    show(p)

selected_kw = ["Amazon Kindle","Amazon Error","Amazon Order"] #Identified from feature selection
google_search_trends_plot(selected_kw)

def stock_plot():
    """Given company selection, this plot daily stock adjusted close price of selected company(AMZN).
    
    Parameters
    ----------
    company: String
             Default AMZN.
    
    Returns
    -------
    output: Interactive Plot of daily stock adjusted close price of AMZN.
    """
    #Import Libraries
    import bokeh
    import pandas as pd
    
    from bokeh.charts import TimeSeries, show, output_file
    
    AMZN = pd.read_csv("AMZN.csv",parse_dates=['Date'])
    AMZN.set_index('Date', inplace=True)
    p = TimeSeries(AMZN['Adj Close'],title="AMZN Daily Adjusted Close Price", ylabel='Stock Prices', xlabel='Date')

    show(p)
stock_plot()