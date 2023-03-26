"""
This module is responsible for the backtest statistics.
"""
import pandas as pd
from math import sqrt
from typing import List

# Constants
DATETIME_STR_FORMAT = "%d/%m/%Y"
DATETIME = "datetime"
AUM = "aum"
IC = "ic"

# Yahoo Finance ticker properties
CLOSE_PRICE = "Close"
DIVIDENDS = "Dividends"

class BacktestStats:
  """
  Defines the BacktestStats class which calculates statistics based
  on the backtest portfolio performance and monthly information 
  coefficients. 
  """
  def __init__(self,
    portfolio_performance: pd.DataFrame,
    monthly_ic: pd.DataFrame):
    """
    This method initialises the BacktestStats class.

    Args:
      portfolio_performance (pd.Dataframe): The dataframe containing
        the portfolio performance information calculated during the 
        backtest simulation.
      monthly_ic (pd.Dataframe): The dataframe containing the monthly
        information coefficient information calculated during the 
        backtest simulation
    """
    self.portfolio_performance: pd.DataFrame = portfolio_performance
    self.monthly_ic: pd.DataFrame = monthly_ic

    """
    beginning_trading_date (pd.Timestamp): The timestamp of the 
      beginning trading day.
    ending_trading_date (pd.Timestamp): The timestamp of the 
      ending trading day.
    """
    self.beginning_trading_date: pd.Timestamp = \
      self.portfolio_performance[DATETIME][0]
    self.ending_trading_date: pd.Timestamp = \
      list(self.portfolio_performance[DATETIME])[-1]

  def get_beginning_trading_date_str(self) -> str:
    """
    str: Returns the beginning trading day as a formatted string.
    """
    return self.beginning_trading_date.strftime(DATETIME_STR_FORMAT)

  def get_ending_trading_date_str(self) -> str:
    """
    str: Returns the ending trading day as a formatted string.
    """
    return self.ending_trading_date.strftime(DATETIME_STR_FORMAT)

  def get_number_of_days(self) -> int:
    """
    int: Returns the number of calendar days from the beginning date
      to the ending date.
    """
    return (self.ending_trading_date - self.beginning_trading_date).days

  def get_initial_aum(self) -> float:
    """
    float: Returns the initial assets under management amount.
    """
    return self.portfolio_performance[AUM][0]

  def get_final_aum(self) -> float:
    """
    float: Returns the final assets under management amount.
    """
    return list(self.portfolio_performance[AUM])[-1]

  def get_profit_loss(self) -> float:
    """
    float: Returns the profit or loss of the backtest strategy 
      including dividends.
    """
    dividends = list(self.portfolio_performance["dividends"])[-1]
    return self.get_final_aum() - self.get_initial_aum() + dividends

  def get_total_stock_return(self) -> float:
    """
    float: Returns the total stock return of the backtest strategy
      (without dividends).
    """
    return (self.get_final_aum() - self.get_initial_aum()) \
      / self.get_initial_aum()

  def get_total_return(self) -> float:
    """
    float: Returns the total return of the backtest strategy
      (including dividends).
    """
    return self.get_profit_loss() / self.get_initial_aum()

  def get_annualized_rate_of_return(self) -> float:
    """
    float: Returns the annualized rate of return of the 
      backtest strategy calculated based on the formula 
      from the following source:
      https://www.investopedia.com/terms/a/annualized-rate.asp
    """
    return ((self.get_initial_aum() + self.get_profit_loss()) \
            / self.get_initial_aum()) ** (365 / self.get_number_of_days()) - 1

  def get_average_daily_aum(self) -> float:
    """
    float: Returns the average daily assets under management amount.
    """
    return sum(list(self.portfolio_performance[AUM])) \
      / len(self.portfolio_performance[AUM])

  def get_maximum_daily_aum(self) -> float:
    """
    float: Returns the maximum daily assets under management amount.
    """
    return max(list(self.portfolio_performance[AUM]))

  def get_daily_returns(self) -> List[float]:
    """
    List[float]: Returns a list of daily returns of the portfolio.
    """
    daily_returns = []
    daily_aum_list = list(self.portfolio_performance[AUM])
    for idx, daily_aum in enumerate(daily_aum_list[1:]):
      yesterday_aum = daily_aum_list[idx - 1]
      daily_return = (daily_aum - yesterday_aum) / yesterday_aum
      daily_returns.append(daily_return)
    return daily_returns

  def get_average_daily_return(self) -> float:
    """
    float: Returns the average daily return of the portfolio.
    """
    daily_returns = self.get_daily_returns()
    return sum(daily_returns) / len(daily_returns)

  def get_daily_standard_deviation(self) -> float:
    """
    float: Returns the standard deviation of the daily returns 
      of the portfolio.
    """
    daily_returns = self.get_daily_returns()
    average_daily_return = self.get_average_daily_return()
    daily_deviations = \
      [daily_return - average_daily_return for daily_return in daily_returns]
    squared_daily_deviations = \
      [daily_deviation ** 2 for daily_deviation in daily_deviations]
    average_squared_daily_deviations = \
      sum(squared_daily_deviations) / len(squared_daily_deviations)
    return sqrt(average_squared_daily_deviations)

  def get_daily_sharpe_ratio(self) -> float:
    """
    float: Returns the sharpe ratio of the portfolio (assuming 
      a daily risk-free rate of 0.01%) calculated based on the 
      formula from the following source:
      https://www.realvantage.co/insights/what-is-sharpe-ratio/
    """
    return (self.get_average_daily_return() - 0.0001) \
      / self.get_daily_standard_deviation()

  def print_summary(self) -> None:
    """
    None: Prints the formatted summary of the calculated portfolio
      statistics. 
    """
    out_str = f"""
    Begin Date: {self.get_beginning_trading_date_str()}
    End Date: {self.get_ending_trading_date_str()}
    Number of Days: {self.get_number_of_days()}
    Total Stock Return: {self.get_total_stock_return() * 100:.3f}%
    Total Return: {self.get_total_return() * 100:.3f}%
    Annualized Rate of Return: {self.get_annualized_rate_of_return() * 100:.3f}%
    Initial AUM: {self.get_initial_aum():.5f}
    Final AUM: {self.get_final_aum():.5f}
    Average Daily AUM: {self.get_average_daily_aum():.5f}
    Maximum Daily AUM: {self.get_maximum_daily_aum():.5f}
    Profit and Loss: {self.get_profit_loss():.5f}
    Average Daily Return: {self.get_average_daily_return() * 100:.5f}%
    Daily Standard Deviation: {self.get_daily_standard_deviation() * 100:.5f}%
    Daily Sharpe Ratio: {self.get_daily_sharpe_ratio():.5f}
    """
    print(out_str)

  def plot_daily_aum(self, path: str = "daily_aum") -> None:
    """
    Plots the daily asset under management amount throughout
    the backtesting period.

    Args:
      path (str): Specifies the path where the plot is saved.
      Defaults to "daily_aum".

    Returns:
      None: Generates a plot of the daily AUM and saves it to a file.
    """
    daily_aum = self.portfolio_performance.set_index(DATETIME)[AUM]
    fig = daily_aum.plot.line(
      title= "Daily AUM",
      grid=True,
      legend=False,
      xlabel="Close Date",
      ylabel="AUM ($)").get_figure()
    fig.savefig(path)
    fig.clf()

  def plot_monthly_cumulative_ic(self, path: str = "cumulative_ic") -> None:
    """
    Plots the monthly cumulative information coefficient throughout
    the backtesting period.

    Args:
      path (str): Specifies the path where the plot is saved.
      Defaults to "cumulative_ic".

    Returns:
      None: Generates a plot of the monthly IC and saves it to a file.
    """
    ic = self.monthly_ic.set_index(DATETIME)[IC]
    fig = ic.plot.line(
      title= "Monthly Cumulative IC",
      grid=True,
      legend=False,
      xlabel="Close Date",
      ylabel="Cumulative IC").get_figure()
    fig.savefig(path)
    fig.clf()


