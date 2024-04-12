## Market Data Crawler

---

This is a Python module that our team has implemented to crawl the financial market data using various strategies.

The code is implemented under the design principle of configuration-driven application and the use of [strategy design
pattern](https://en.wikipedia.org/wiki/Strategy_pattern).

---

### Set-up Steps

Programming language: Python 3.12.0+

It is recommended to set up the development/testing environment with python virtual environment (venv). 

```sh
# To initiate the virtual environment setup for the very first time, go to src/python folder and execute
python -m venv venv

# Kick off the virtual environment, go to src/python folder and execute
cd ./venv/Scripts
./activate.bat     # For WINDOWS CMD
./Activate.ps1     # For WINDOWS PowerShell
source ./activate  # For MAC & LINUX

# To install the required python libraries/dependencies, go to src/python folder and execute
pip install -r requirements.txt
```

For the web crawling strategies which require the use of [Selenium](https://www.selenium.dev/) library, the 
implementation uses Chrome Driver by default. Unless there is any strong reason, please follow to use the Chrome Driver
for consistency reason.

---

### Data Model

Given different data sources may give different structure/naming of the data, it is important to standardize the format 
of the crawler's output. To organize the data model efficiently, we use python's built-in 
[dataclasses](https://docs.python.org/3/library/dataclasses.html)  library to declare the schema of several important 
data object.

For this crawler module, it is the main producer of the dataclasses object as defined in 
[market_data.py](https://github.com/jackylaucf/HKU-MScCS-Capstone/blob/main/src/python/model/market_data.py), which 
defines the schema of the market data (Daily Price & Intraday Price of the stocks / indices)

---

### Data Scraping Strategies

For the different regions (e.g., Hong Kong, India, Japan, etc.) and the different type of market data (e.g., index 
constituents, constituents prices, index prices, etc.), we may need to rely on different market data sources (i.e., the
**strategies**), to fetch the data appropriately.

Strategy design pattern allows us to define the [abstract class of data scraping strategy](https://github.com/jackylaucf/HKU-MScCS-Capstone/blob/main/src/python/crawler/strategy/SourceStrategy.py) 
and let different sources to have its own generic implementation while complying with a unified interface. All 
strategies can be found in the 
[strategy](https://github.com/jackylaucf/HKU-MScCS-Capstone/tree/main/src/python/crawler/strategy) folder. 

| abstract method                  | purpose                                                                                  |
|----------------------------------|------------------------------------------------------------------------------------------|
| get_source_name()                | Define the source name as an identifier                                                  |
| get_constituents()               | Implement the crawling mechanism of getting the constituents of an index                 |
| get_daily_prices(ticker: str)    | Implement the crawling mechanism of getting the daily price of a stock or stock index    |
| get_intraday_prices(ticker: str) | Implement the crawling mechanism of getting the intraday price of a stock or stock index |

The following table shows the concrete strategy classes that have been implemented

| strategy                          | data source                                                                                                                                                                                                                                                                                           | constituents    | daily price     |
|-----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|-----------------|
| [BusinessInsiderSourceStrategy](https://github.com/jackylaucf/HKU-MScCS-Capstone/blob/main/src/python/crawler/strategy/BusinessInsiderSourceStrategy.py) | https://markets.businessinsider.com                                                                                                                                                                                                                                                                   | Not Implemented | Implemented     |
| [ImportCsvSourceStrategy](https://github.com/jackylaucf/HKU-MScCS-Capstone/blob/main/src/python/crawler/strategy/ImportCsvSourceStrategy.py) | Raw CSV files as provided in [dataset/market_data/input/csv](https://github.com/jackylaucf/HKU-MScCS-Capstone/tree/main/dataset/market_data/input/csv). The schema of the csv should align with the one defined in the data model as described in the previous section (column order does not matter) | Implemented     | Implemented     |
| [NSEIndiaSourceStrategy](https://github.com/jackylaucf/HKU-MScCS-Capstone/blob/main/src/python/crawler/strategy/NSEIndiaSourceStrategy.py) | https://www.niftyindices.com                                                                                                                                                                                                                                                                          | Implemented     | Not Implemented |
| [NikkeiJPSourceStrategy](https://github.com/jackylaucf/HKU-MScCS-Capstone/blob/main/src/python/crawler/strategy/NikkeiJPSourceStrategy.py) | https://indexes.nikkei.co.jp                                                                                                                                                                                                                                                                          | Implemented     | Not Implemented |
| [SinaSourceStrategy](https://github.com/jackylaucf/HKU-MScCS-Capstone/tree/main/src/python/crawler/strategy) | http://vip.stock.finance.sina.com.cn                                                                                                                                                                                                                                                                  | Implemented     | Not Implemented |
| [TradingViewSourceStrategy](https://github.com/jackylaucf/HKU-MScCS-Capstone/blob/main/src/python/crawler/strategy/TradingViewSourceStrategy.py) | https://www.tradingview.com                                                                                                                                                                                                                                                                           | Implemented     | Not Implemented |
| [YahooSourceStrategy](https://github.com/jackylaucf/HKU-MScCS-Capstone/blob/main/src/python/crawler/strategy/YahooSourceStrategy.py) | https://finance.yahoo.com                                                                                                                                                                                                                                                                             | Not Implemented | Implemented     |

---

### Crawler Implementation

As the implementation of various data scraping strategies are defined,  what is left to do is to define a general data 
scraping flow and configure different indices with their appropriate crawling strategies.

The general data scraping flow is defined in the 
[MarketFetcher](https://github.com/jackylaucf/HKU-MScCS-Capstone/blob/main/src/python/crawler/market_fetcher.py) class. 
For different indices, developer need to provide the FetcherStrategies object to create the corresponding MarketFetcher 
object.

Such design made the crawler to be configuration-based and each indices are decoupled from the data scraping strategies.

To find the configuration, please visit 
[data_crawler_main.py](https://github.com/jackylaucf/HKU-MScCS-Capstone/blob/main/src/python/crawler/data_crawler_main.py).
This file also serves as the entry point to test each of the market data crawler.

---

### Experience Sharing

1. There is no free lunch - it is ideal if we can get all the required data from one platform only but it is not that 
easy if we want to do it **for free**. For example, Yahoo Finance provides the historical daily prices
only but list of index constituents cannot be found there. Therefore, we need to exploit different resources 
(i.e., crawling strategies)
2. Some platforms are crawler-unfriendly. Since there is no free lunch, platforms like https://www.investing.com/ use 
techniques like the `access-control-allow-origin` header to prevent crawlers from exploiting their internal API and 
fetching their data with ease. Apart from using the access control header, investing.com  even have done a cleanup on
their rendered HTML, which makes Selenium web crawling approach (HTML parsing) almost impossible to be implemented. 
3. To tackle the above issue, we have to resort to manual effort. That is why we have the [ImportCsvSourceStrategy](https://github.com/jackylaucf/HKU-MScCS-Capstone/blob/main/src/python/crawler/strategy/ImportCsvSourceStrategy.py).
For some of the dataset, we have to manually copy the data from the website and place them in a CSV file as it is hard /
not economical to implement a generic crawler strategy.
4. While we are using the online resources for free, we also need to do the data scraping responsibly. This does not 
only protect the data provider from getting overwhelming requests from your crawler, it also prevents your IP from 
getting blacklisted on their website. In the [MarketFetcher](https://github.com/jackylaucf/HKU-MScCS-Capstone/blob/main/src/python/crawler/market_fetcher.py) 
class, you can see we always let the thread sleep for 1 to 20 seconds (randomly) before we fire another requests.
5. HTTP header spoofing is one of the useful techniques for data scraping. Some websites (like the NSE official page)
check the `User-Agent` header and reject the requests from python crawler. Spoofing can be done to resolve such issue.
See [http_utils.py](https://github.com/jackylaucf/HKU-MScCS-Capstone/blob/main/src/python/crawler/http_utils.py)
