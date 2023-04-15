from src.stocks_fetcher import StocksFetcher
import pandas as pd
import os

# config
path = "./test/data/"


# fetching the data
# ticker_symbols = ["WMT", "AMZN", "NFLX", "SPY"]
# beginning_date = "20220801"
# ending_date = "20230410"
# sf = StocksFetcher()
# data = sf.fetch_stocks_data(
#     ticker_symbols,
#     beginning_date,
#     ending_date
# )

# downloading data
# for ticker_symbol in ticker_symbols:
#     data[ticker_symbol].to_csv(path + ticker_symbol + ".csv")

# importing data
# stocks_data = dict()
# filenames = os.listdir(path)
# for filename in filenames:
#     stocks_data[filename.replace(".csv", "")] = pd.read_csv(path + filename)