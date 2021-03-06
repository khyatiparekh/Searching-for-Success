<img src="https://github.com/khyatiparekh/Data515_FinalProject/blob/master/logo.png" width="80">

# Searching For Success 
## Using google searches to predict the stock market

Searching For Success is a template project that can help an amateur investor to visualize search trends 
on Google for selected company and get probability that the stock price will increase when 
the quarterly reports will be released for that company.

To use it as a template for your own project, you will need to clone this
repository into your computer and follow the instructions in the `setup.py` in SearchingForSuccess.

First, let me explain all the different moving parts that make up the
python project, and all the elements which allow us to effectively
share it with others, test it, document it, and track its evolution.

We recommend using conda to install matplotlib and other such libraries to ensure smooth running of the module.

## Organization of the  project

The project has the following structure:  
   * Searching For Success  
     * |- README.md  
     * |- LICENSE  
     * |- SearchingForSuccess  
        * |- __init__.py  
        * |- Submodule
           * |- __init__.py  
           * |- EarningReport.py  
           * |- PredictionStockPrice.py  
           * |- HistoricalDataPlot.py  
        * |- tests 
           * |- __init__.py  
           * |- test_earnings_report.py  
           * |- test_prediction_stock_price.py  
           * |- test_historical_data_plot.py  
        * |- setup.py   
      * |- Doc 
        * |- Design Specification and Project Plan
        * |- Functional Specification
        * |- Presentation
      * |- Examples  
           * |- Example with Amazon
      * .gitignore  
     
In the following sections we will examine these elements one by one. First,
let's consider the core of the project. This is the code inside of
`EarningReport.py, PredictionStockPrice.py and HistoricalPlot.py` in SearchingForSuccess/Submodule folder 

## Module Code
We place the module code in three files called `EarningReport.py, PredictionStockPrice.py and HistoricalPlot.py`
in the Submodule folder in SearchingForSuccess.  For the functions to work, we need to run the interface.ipynb 
which contains code that imports everything in that file into the namespace of the project:  
`import EarningReport  
 import PredictionStockPrice   
 import HistoricalPlot`  
 
### EarningReport.py

This module implements the functions: 

1) get_quarter_begin, 
2) get_quarter_end,
3) get_current_quarter_dates, 
4) print_last_day_quarter, 
5) get_default_report_dates, 
6) get_yahoo, and 
7) get_earnings_data.

The get_quarter_begin function calculates the first day of the current quarter.

The get_quarter_end function calculates the last day of the current quarter.

The get_current_quarter_dates returns the formatted begin and end dates.

The get_earnings_data first calls get_yahoo and if no earnings date, then calls get_default_report_dates for the estimated earnings report dates.

The get_yahoofunction will download stock price data from Yahoo finance, saves the daily quote information and returns the earnings report date(s).

### PredictionStockPrice.py

This module implements three functions: 
1) feature_selection,
2) prediction_model and, 
3) prediction_stock_price. 

The first function,
features_selection will use Lasso regression model to select
5 keywords that are significant to the company's stock performance.
And the second function predcition_model will predict the
likelihood of stock prices increase or decrease after upcoming
earning report released for given company. And the third function
prediction _stock_price will call the previous functions
based on the company name input.

### HistoricalDataPlot.py

This module implements one function: historical_data_plot.

The function will read the data for the input company with selected keywords and then plot Google trends for selected keywords from previous feature selection. 
Then plot daily adjusted close stock price for given company.

### How to use module

Once you have run setup.py, choose the company for which you would like to see the prediction.

In the textbox you will enter:
1 for Amazon
2 for Google
3 for Microsoft

The module will then output:
1) The current quarter dates, 
2) When the current fiscal quarter ends, 
3) When the next earnings report is expected from that company
4) Plots to show the google trends for select keywords of that company
5) The predicted probability that the stock price will increase after the next quarter's earnings have been released.

## Project Data
In this case, the project data is rather small, and recorded in csv files saved in `SearchingForSuccess/Data`.  
For Amazon, Google and Microsoft:  
Daily Stock Price Data from 2007 - 2017  
Daily Google Keywords Search Index Data 2007 - 2017  

## Example

We have a demo notebook for Amazon. It will import all modules and generate output for Amazon by running the notebook.  

## Testing  

It consists of unit tests for `EarningReport.py, PredictionStockPrice.py and HistoricalPlot.py`.

## Documentation

This folder contains all the documentation related to the project, namely:
1) Design specification and project plan,
2) Final presentation,
3) Functional specification




