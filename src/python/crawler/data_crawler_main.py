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


if __name__ == '__main__':
    hsi().fetch(MarketDataType.CONSTITUENTS_DAILY)
