"""
This module is responsible for getting, validating and organizing user input.
"""
from datetime import datetime
from typing import List, Tuple
import argparse

# Constants
DATETIME_FORMAT = "%Y%m%d"
DATE_TODAY = datetime.today().strftime(DATETIME_FORMAT)
MIN_TICKER_LENGTH = 1
MAX_TICKER_LENGTH = 5
MIN_DAYS = 1
MAX_DAYS = 250
MIN_PCT = 1
MAX_PCT = 100
DATE_LENGTH = 8

def get_args() -> argparse.Namespace:
  """
  argparse.Namespace: Returns the command line arguments entered 
    by the user
  """
  parser = argparse.ArgumentParser(
    description="""Fetches daily close prices from the internet for given
    tickers and time frame and then back tests some
    simple momentum and reversal monthly strategies.""")
  parser.add_argument("--tickers", type=str,
    help="The comma-separated stock tickers (e.g., MSFT,AMZN,WMT)",
    required=True)
  parser.add_argument("--b", type=int,
    help="The beginning date of the period in format YYYYMMDD",
    required=True)
  parser.add_argument("--e", type=int,
    help="The ending date of the period in format YYYYMMDD (optional)",
    required=False)
  parser.add_argument("--initial_aum", type=int,
    help="The initial asset under management (e.g., USD 10000)",
    required=True)
  parser.add_argument("--strategy_type", type=str,
    help="'M' (momentum) or 'R' (reversal)",
    required=True)
  parser.add_argument("--days", type=int,
    help="The number of trading days used to compute strategy-related returns",
    required=True)
  parser.add_argument("--top_pct", type=int,
    help="The percentage of stocks to pick to go long (1 to 100)",
    required=True)

  return parser

class InputData:
  """
  Defines the InputData class which validates and organises user input.
  """
  def __init__(self,
    tickers: str = -1,
    b: int = -1,
    e: int = -1,
    initial_aum: int = -1,
    strategy1_type: str = -1,
    strategy2_type: str = -1,
    days1: int = -1,
    days2: int = -1,
    top_pct: int = -1) -> None:
    """
    This method initialises the InputData class.

    Attributes:
      tickers (str): The user input of stocks in the universe.
      b (int): The user input of beginning date.
      e (int): The user input of ending date.
      intial_aum (int): The user input of initial AUM.
      strategy_type (str): The user input of strategy type.
      days (int): The user input of number of days to compute returns.
      top_pct (int): The user input of percentage of stocks to pick.
    """
    if tickers == -1:
      self.tickers = get_args().parse_args().tickers
    else:
      self.tickers = tickers

    if b == -1:
      self.b = get_args().parse_args().b
    else:
      self.b = b

    if e == -1:
      self.e = get_args().parse_args().e
    else:
      self.e = e

    if initial_aum == -1:
      self.initial_aum = get_args().parse_args().initial_aum
    else:
      self.initial_aum = initial_aum

    if strategy1_type == -1:
      self.strategy1_type = get_args().parse_args().strategy1_type
    else:
      self.strategy1_type = strategy1_type

    if strategy2_type == -1:
      self.strategy2_type = get_args().parse_args().strategy2_type
    else:
      self.strategy2_type = strategy2_type

    if days1 == -1:
      self.days1 = get_args().parse_args().days1
    else:
      self.days1 = days1

    if days2 == -1:
      self.days2 = get_args().parse_args().days2
    else:
      self.days2 = days2

    if top_pct == -1:
      self.top_pct = get_args().parse_args().top_pct
    else:
      self.top_pct = top_pct

  def get_tickers(self) -> List[str]:
    """
    Returns a validated list of tickers from user input.

    Raises:
      ValueError: If the ticker symbol is not a string, is not alphanumeric,
        is not between 1 to 5 characters long, or is not a valid ticker symbol.

    Returns:
      List[str]: Returns the list of tickers if each ticker has been validated.
    """
    if self.tickers is None:
      raise ValueError("Tickers must be specified.")
    tickers = [ticker.strip() for ticker in self.tickers.split(",")]
    for ticker in tickers:
      if not isinstance(ticker, str):
        raise ValueError("Ticker must be a string.")
      if not ticker.isalnum():
        raise ValueError(
          "Ticker must be a string of alphanumeric characters.")
      if len(ticker) > MAX_TICKER_LENGTH \
            or len(ticker) < MIN_TICKER_LENGTH:
        raise ValueError("Ticker must be between 1 to 5 characters long.")
    return tickers

  def get_beginning_date(self) -> str:
    """
    Returns a validated beginning date from the user input.

    Raises:
      ValueError: If the beginning date is not an integer, is not in format
        YYYYMMDD, is greater than the ending date, or is greater than the
        current date.

    Returns:
      str: Returns the beginning date if it has been validated.
    """
    if self.b is None:
      raise ValueError("Beginning date must be specified")
    if not isinstance(self.b, int):
      raise ValueError("Beginning date must be an integer.")
    if len(str(self.b)) != DATE_LENGTH:
      raise ValueError("Beginning date must be in format YYYYMMDD.")
    if self.b > int(DATE_TODAY):
      raise ValueError("""
      Beginning date must be less than or equal to the current date.""")
    return str(self.b)

  def get_ending_date(self) -> str:
    """
    Returns a validated ending date from the user input.

    Raises:
      ValueError: If the ending date is not an integer, is not in format
        YYYYMMDD, is less than the beginning date, or is greater than the
        current date.

    Returns:
      str: Returns the ending date if it has been validated.
    """
    if self.e is None:
      return str(DATE_TODAY)
    if len(str(self.e)) != DATE_LENGTH:
      raise ValueError("Ending date must be in format YYYYMMDD.")
    if self.e < self.b:
      raise ValueError("Ending date must be greater than or equal to the "
                        "beginning date.")
    if self.e > int(DATE_TODAY):
      raise ValueError("Ending date must be less than or equal to the current "
                        "date.")
    return str(self.e)

  def get_initial_aum(self) -> int:
    """
    Returns a validated initial asset under management from the user input.

    Raises:
      ValueError: If the initial asset under management is not an integer or
        is not a positive integer.

    Returns:
      int: Returns the initial asset under management if it has been validated.
    """
    if self.initial_aum is None:
      raise ValueError("Initial AUM must be specified.")
    if not isinstance(self.initial_aum, int):
      raise ValueError("Initial AUM must be an integer.")
    if self.initial_aum < 0:
      raise ValueError("Initial AUM must be a positive integer.")
    return self.initial_aum

  def get_top_pct(self) -> int:
    """
    Returns a validated top percentage from the user input.

    Raises:
      ValueError: If the top percentage is not an integer, is not between 
        1 to 100, or is not a valid top percentage.

    Returns:
      int: Returns the top percentage if it has been validated.
    """
    if self.top_pct is None:
      raise ValueError("Top percentage must be specified.")
    if not isinstance(self.top_pct, int):
      raise ValueError("Top percentage must be an integer.")
    if self.top_pct < MIN_PCT or self.top_pct > MAX_PCT:
      raise ValueError("Top percentage must be between 1 to 100.")
    return self.top_pct

  def get_strategy_and_days(self, n: int) -> Tuple[str, int]:
    """
    Returns a validated strategy type and number of trading days from
    the user input for a given strategy (n=1 or n=2).

    Args:
      n (int): The number of the strategy (1 or 2).

    Raises:
      ValueError: If the strategy type is not a string, is not 'M' or 'R',
        or is not a valid strategy type.
      ValueError: If the number of trading days is not an integer, is not
        between 1 to 250, or is not a valid number of trading days.

    Returns:
      Tuple[str, int]: Returns a tuple containing the strategy type and
        number of trading days if both have been validated.
    """
    if n != 1 and n != 2:
      raise ValueError("n must be either 1 or 2.")
    strategy_key = f"strategy{n}_type"
    days_key = f"days{n}"

    strategy = getattr(self, strategy_key)
    days = getattr(self, days_key)

    if strategy is None:
      raise ValueError(f"Strategy type for strategy {n} must be specified.")
    if not isinstance(strategy, str):
      raise ValueError(f"Strategy type for strategy {n} must be a string.")
    if strategy.upper() != "M" and strategy.upper() != "R":
      raise ValueError(
        f"""Strategy type for strategy {n} must be 'M' (momentum)
        or 'R' (reversal).""")

    if days is None:
      raise ValueError(f"""Number of trading days for strategy {n}
        must be specified.""")
    if not isinstance(days, int):
      raise ValueError(f"""Number of trading days for strategy {n} must
        be an integer.""")
    if days < MIN_DAYS or days > MAX_DAYS:
      raise ValueError(
          f"Number of trading days for strategy {n} must be between 1 to 250."
      )

    return strategy, days
