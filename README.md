# Assignment 3 - Alan, Vibilan, Jerri, Nahian

## TODO next
- [ ] change argparse to include `strategy1_type` and `strategy2_type`.
- [ ] fit a multiple linear regression model to get two coefficients: labels (returns) fromt he current month while features come from the previous month backwards.
- [ ] re-compute featuresusing the current month.
- [ ] get a single score for each stock.
- [ ] select stocks with the '--top_pct' score and go long on them.
- [ ] Repeat for the next month.
- [ ] In the repoort, include the coefficients of the linear regression and respectice t-values.

## Questions
1. How to first build the linear regression?
2. How many days back to we go?

## Setting up virtual environment (recommended)

1. Run `python3 -m venv .venv`.
2. Run `source .venv/bin/activate` to activate the virtual environment. This command needs to be run **before every session**.

## Direction of use

1. To install packages, run `pip install -r requirements.txt`.

## Updating environment

1. If you install new packages, run `pip freeze > requirements.txt` afterwards to update the environment requirements.

## Usage

### Backtesting Strategy

To backtest the momentum strategy with an initial AUM of 10000, with 100 days to calculate returns and on the top 10% of the stock universe (AAPL, TSLA, LMT, BA, GOOG, AMZN, NVDA, META, WMT, MCD) from January 1, 2022 to March 18, 2023, run the following: 

* `python backtest_two_signal_strategy.py --tickers AAPL,TSLA,LMT,BA,GOOG,AMZN,NVDA,META,WMT,MCD --b 20220101 --e 20230318 --initial_aum 10000 --strategy1_type M --days1 100 --top_pct 10 --strategy2_type M --days2 100`

To backtest the reversal strategy with an initial AUM of 10000, with 20 days to calculate returns and on the top 20% of the stock universe (AAPL, TSLA, GOOG, META, NFLX) from June 1, 2022 to today, run the following: 

* `python backtest_strategy.py --tickers AAPL,TSLA,GOOG,META,NFLX --b 20220601 --initial_aum 10000 --strategy_type R --days 20 --top_pct 20`

### Note

The plot filenames can be specified but default to `daily_aum.png` and `cumulative_ic.png`.

### Unit Tests

Run the unit tests using the following command:

* `pytest -vv`

To see the code coverage report, run the following command:

1. `coverage run -m pytest`
2. `coverage report`

### Project Accomplishments

1. Produces the correct analytics and plot
2. Code coverage of the project is 98%
3. Functions have been tested for multiple scenarios
4. Functions have been correctly typed

Screenshot of pytest results of the project:

![screenshot-2023-03-19-23:41:04](https://user-images.githubusercontent.com/61618719/226187908-5d4cf8ce-a03e-4e5f-9016-61e4567ea493.png)

Screenshot of code coverage report of the project:

![screenshot-2023-03-19-23:41:27](https://user-images.githubusercontent.com/61618719/226187895-1c058e7f-38e4-4844-a583-741fe47d822a.png)

