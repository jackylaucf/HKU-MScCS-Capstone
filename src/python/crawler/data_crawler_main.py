from crawler.market_fetcher import FetcherStrategies, MarketFetcher, MarketDataType
from crawler.strategy.TradingViewSourceStrategy import TradingViewSourceStrategy
from crawler.strategy.YahooSourceStrategy import YahooSourceStrategy


def hsi():
    strategies = FetcherStrategies(index_price=YahooSourceStrategy('^HSI'),
                                   constituents=TradingViewSourceStrategy('HSI-HSI'),
                                   constituents_price=YahooSourceStrategy('^HSI',
                                                                          YahooSourceStrategy.get_ticker_formatter(
                                                                              suffix='.HK', zfill=4)))
    return MarketFetcher('hsi', strategies)


def nifty_50():
    strategies = FetcherStrategies(index_price=YahooSourceStrategy('^NSEI'),
                                   constituents=TradingViewSourceStrategy('NSE-NIFTY'),
                                   constituents_price=YahooSourceStrategy('^NSEI',
                                                                          YahooSourceStrategy.get_ticker_formatter(
                                                                              suffix='.NS')))
    return MarketFetcher('nifty_50', strategies)


def kosdaq():
    strategies = FetcherStrategies(index_price=YahooSourceStrategy('^KQ11'),
                                   constituents=TradingViewSourceStrategy('KRX-KOSDAQ'),
                                   constituents_price=YahooSourceStrategy('^KQ11',
                                                                          YahooSourceStrategy.get_ticker_formatter(
                                                                              suffix='.KQ', zfill=6)))
    return MarketFetcher('kosdaq', strategies)


if __name__ == '__main__':
    kosdaq().fetch(MarketDataType.CONSTITUENTS_DAILY)
