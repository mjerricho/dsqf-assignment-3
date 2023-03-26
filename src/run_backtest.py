"""
This module is responsible for running the backtest simulation.
"""
import pandas as pd
from math import ceil
from typing import Dict, List, Tuple

# Constants
MOMENTUM = "M"
REVERSAL = "R"
MOMENTUM_GAP = 20
DATE_FORMAT = "%Y%m%d"
AUM = "aum"
IC = "ic"
DATETIME = "datetime"
DIVIDENDS_DF = "dividends"

# Yahoo Finance Constants
CLOSE_PRICE = "Close"
DIVIDENDS = "Dividends"

class RunBacktest:
  """
  Defines the RunBacktest class which runs the backtest based on 
  the stock data obtained by the fetcher and the user defined
  inputs.
  """
  def __init__(self,
    stocks_data: Dict[str, pd.DataFrame],
    initial_aum: int,
    beginning_date: int,
    days: int,
    strategy: str,
    top_pct: int):
    """
    This method initialises the RunBacktest class.

    Args:
      stocks_data (Dict[str, pd.DataFrame]): The dictionary that matches 
        the stock ticker to the price information of the stock.
      initial_aum (int): The initial asset under management amount.
      beginning_date (str): The beginning date of the backtest period.
      days (int): The number of days to look back during calculation
        of stock returns.
      strategy (str): The backtesting strategy, either Momentum or Reversal.
      top_pct (int): The percentage of stocks to pick for the portfolio.
    """
    self.stocks_data: pd.DataFrame = stocks_data
    self.initial_aum: int = initial_aum
    self.beginning_date: str = beginning_date
    self.days: int = days
    self.strategy: str = strategy
    self.top_pct: int = top_pct

    """
    portfolio_performance (pd.DataFrame): The dataframe to store the 
      portfolio performance information such as AUM and dividends.
    portfolio (List[Tuple[str, float]]): The list containing the 
      current portfolio. Each element is a tuple of the stock ticker
      and the amount of the stock.
    portfolio_record (List[List[Tuple[str, float]]]): The list containing 
      a record of previous portfolios. Each element is a portfolio.
    monthly_ic (pd.DataFrame): The dataframe to store the monthly 
      cumulative information coefficient of the portfolio.
    """
    self.portfolio_performance: pd.DataFrame = pd.DataFrame()
    self.portfolio: List[Tuple[str, float]] = []
    self.portfolio_record: List[List[Tuple[str, float]]] = []
    self.monthly_ic: pd.DataFrame = pd.DataFrame()

  def get_month_end_indexes_from_b(self) -> List[int]:
    """
    List[int]: Returns the indexes of the month end dates starting
      from the beginning date.
    """
    datetime_indexes = list(self.stocks_data.values())[0].index.to_list()
    b_timestamp = pd.to_datetime(self.beginning_date, format=DATE_FORMAT)
    month_end_indexes = []

    for idx, datetime in enumerate(datetime_indexes[:-1]):
      if datetime.month != datetime_indexes[idx + 1].month \
        and datetime_indexes[idx].tz_localize(None) > b_timestamp:
        month_end_indexes.append(idx)

    return month_end_indexes

  def calc_stocks_to_buy(self, date_index: int) -> List[str]:
    """
    Calculates which stocks should be bought based on the backtest 
    strategy at a given date.

    Args:
      date_index (int): The index of the date at which the stocks are 
        bought.

    Returns:
      List[str]: Returns a list containing the stock tickers to
        be bought.
    """
    stocks = list(self.stocks_data.keys())
    stocks_returns = []
    is_momentum = self.strategy == MOMENTUM
    date_index -= MOMENTUM_GAP * is_momentum

    for stock in stocks:
      history = self.stocks_data[stock]
      end_close = history.iloc[date_index][CLOSE_PRICE]
      start_close = history.iloc[date_index - self.days][CLOSE_PRICE]
      pct_change = (end_close - start_close) / start_close * 100
      stocks_returns.append((stock, pct_change))

    stocks_returns.sort(key=lambda x: x[1], reverse=is_momentum)
    n_stocks = ceil(len(stocks) * (self.top_pct / 100))
    stocks_to_buy = [stock for stock, _ in stocks_returns[:n_stocks]]
    return stocks_to_buy

  def calc_portfolio(self,
    stocks_to_buy: List[str],
    aum: int,
    date_index: int) -> List[Tuple[str, float]]:
    """
    Calculates the portfolio based on which stocks need to be bought
    and the AUM amount.

    Args:
      stocks_to_buy (List[str]): The list of stocks to be bought.
      aum (int): The assets under management amount.
      date_index (int): The index of the date at which the stocks are 
        bought.

    Returns:
      List[Tuple[str, float]]: The list containing the portfolio. 
      Each element is a tuple of the stock ticker and the amount of 
      the stock.
    """
    aum_per_stock = aum / len(stocks_to_buy)
    stocks_amount = []
    for stock in stocks_to_buy:
      history = self.stocks_data[stock]
      price = history.iloc[date_index][CLOSE_PRICE]
      amount = aum_per_stock / price
      stocks_amount.append((stock, amount))
    return stocks_amount

  def init_portfolio_performance(self) -> None:
    """
    None: Initialises the portfolio performance dataframe with 
      the datetime indexes in the specified period, the initial 
      AUM and empty dividends.
    """
    datetime_indexes = list(self.stocks_data.values())[0].index.to_list() 
    self.portfolio_performance[DATETIME] = datetime_indexes
    self.portfolio_performance[AUM] = \
      [self.initial_aum for _ in range(len(datetime_indexes))]
    self.portfolio_performance[DIVIDENDS_DF] = \
      [0 for _ in range(len(datetime_indexes))]

  def calc_aum(self, date_index: int) -> float:
    """
    Calculates the assets under management amount for a given date.

    Args:
      date_index (int): The index of the date at which AUM must be 
        calculated

    Returns:
      float: Returns the AUM amount.
    """
    total_aum = 0
    for stock, amount in self.portfolio:
      end_close = self.stocks_data[stock].iloc[date_index][CLOSE_PRICE]
      total_aum += amount * end_close
    return total_aum

  def calc_dividends(self, date_index: int) -> float:
    """
    Calculates the dividends amount for a given date.

    Args:
      date_index (int): The index of the date at which dividends 
        must be calculated

    Returns:
      float: Returns the dividends amount.
    """
    total_dividends = 0
    for stock, amount in self.portfolio:
      dividends = self.stocks_data[stock].iloc[date_index][DIVIDENDS]
      total_dividends += amount * dividends
    return total_dividends

  def fill_up_portfolio_performance(self) -> None:
    """
    None: Simulates backtesting based on the user-defined information
      and strategy and fills up the dataframe of portfolio performance 
      with the calculated AUM and dividends for each day in the specified 
      period.
    """
    self.init_portfolio_performance()
    month_end_indexes = self.get_month_end_indexes_from_b()
    for day_idx in range(month_end_indexes[0], \
                         len(list(self.stocks_data.values())[0].index)):
      if day_idx in month_end_indexes:
        stocks_to_buy = self.calc_stocks_to_buy(day_idx)
        previous_aum = self.portfolio_performance.iloc[day_idx - 1][AUM]
        self.portfolio = self.calc_portfolio(stocks_to_buy,
                                             previous_aum,
                                             day_idx)
        self.portfolio_record.append(self.portfolio)

      self.portfolio_performance.at[day_idx, AUM] = self.calc_aum(day_idx)
      self.portfolio_performance.at[day_idx, DIVIDENDS_DF] = \
        self.portfolio_performance.at[day_idx - 1, DIVIDENDS_DF] \
          + self.calc_dividends(day_idx)

    datetime_indexes = self.portfolio_performance[DATETIME].to_list()
    b_idx = None
    for idx, datetime in enumerate(datetime_indexes):
      if datetime.tz_localize(None) >= \
        pd.to_datetime(self.beginning_date, format=DATE_FORMAT):
        b_idx = idx
        break
    self.portfolio_performance = \
      self.portfolio_performance[b_idx:].reset_index(drop=True)

  def calc_ic(self) -> None:
    """
    None: Simulates backtesting based on the user-defined information
      and strategy and fills up the dataframe of monthly cumulative 
      information coefficient for each month end day in the specified 
      period.
    """
    month_end_indexes = self.get_month_end_indexes_from_b()
    self.monthly_ic[DATETIME] = \
      list(self.stocks_data.values())[0].index[month_end_indexes[:-1]]
    self.monthly_ic[IC] = [0 for _ in range(len(month_end_indexes[:-1]))]

    number_stocks_bought = ceil(len(self.stocks_data) * (self.top_pct / 100))
    for i in range(len(month_end_indexes[:-1])):
      number_correct = 0

      for stock, _ in self.portfolio_record[i]:
        current_close = \
          list(self.stocks_data[stock][CLOSE_PRICE])[month_end_indexes[i]]
        next_close = \
          list(self.stocks_data[stock][CLOSE_PRICE])[month_end_indexes[i + 1]]
        if next_close > current_close:
          number_correct += 1

      prop_correct = number_correct / number_stocks_bought
      information_coeff = (2 * prop_correct) - 1
      if i == 0:
        self.monthly_ic.at[i, IC] = information_coeff
      else:
        self.monthly_ic.at[i, IC] = self.monthly_ic.at[i - 1, IC] \
          + information_coeff
