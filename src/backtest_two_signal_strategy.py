import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from scipy.stats import t
from datetime import datetime
from typing import Dict, Tuple
import math
import calendar

class TwoSignalStrategyBacktest:
    def __init__(self, args, stocks_data: Dict[str, pd.DataFrame]):
        self.args = args
        self.stocks_data = stocks_data
        self.daily_aum = []
        self.monthly_cumulative_ic = []

    def _compute_strategy_features(self, stock_data: pd.DataFrame, days: int, strategy_type: str) -> pd.Series:
        if strategy_type == 'M':
            return stock_data['Close'].pct_change(days).shift(20)
        elif strategy_type == 'R':
            return -stock_data['Close'].pct_change(days)
        else:
            raise ValueError("Invalid strategy type")

    def _compute_coefficients(self, month: int, stocks_data: Dict[str, pd.DataFrame]) -> Tuple[float, float]:
        X = []
        y = []

        for ticker, stock_data in stocks_data.items():
            strategy1 = self._compute_strategy_features(stock_data, self.args.days1, self.args.strategy1_type)
            strategy2 = self._compute_strategy_features(stock_data, self.args.days2, self.args.strategy2_type)
            features = pd.concat([strategy1.shift(), strategy2.shift()], axis=1).dropna()
            # is it confirmed dropna()?
            returns = stock_data['Close'].pct_change().shift(-1)

            valid_data = features.join(returns).dropna()
            valid_data = valid_data[valid_data.index.month == (month - 1) % 12]

            X.append(valid_data.iloc[:, :2].values)
            y.append(valid_data.iloc[:, 2].values)

        X = np.vstack(X)
        y = np.hstack(y)

        model = LinearRegression()
        model.fit(X, y)

        t_values = self._compute_t_values(X, y, model.coef_, model.intercept_)

        return model.coef_, t_values

    def _compute_t_values(self, X: np.ndarray, y: np.ndarray, coef: np.ndarray, intercept: float) -> np.ndarray:
        n = len(y)
        k = X.shape[1]
        y_pred = X.dot(coef) + intercept
        resid = y - y_pred
        SSE = np.sum(resid ** 2)
        SE_squared = SSE / (n - k - 1)
        XTX_inv = np.linalg.inv(X.T.dot(X))
        SE_coef = np.sqrt(np.diagonal(XTX_inv) * SE_squared)
        t_values = coef / SE_coef
        return t_values

    def _compute_scores(self, stocks_data: Dict[str, pd.DataFrame], coefficients: Tuple[float, float]) -> Dict[str, float]:
        scores = {}
        for ticker, stock_data in stocks_data.items():
            strategy1 = self._compute_strategy_features(stock_data, self.args.days1, self.args.strategy1_type)
            strategy2 = self._compute_strategy_features(stock_data, self.args.days2, self.args.strategy2_type)
            features = pd.concat([strategy1, strategy2], axis=1).dropna()
            scores[ticker] = (coefficients[0] * features.iloc[-1, 0] + coefficients[1] * features.iloc[-1, 1])

        return scores

    def _get_last_trading_day_of_month(self, year: int, month: int, stock_data: pd.DataFrame) -> pd.Timestamp:
        last_day_of_month = calendar.monthrange(year, month)[1]
        dt = pd.Timestamp(year, month, last_day_of_month)
        while dt not in stock_data.index:
                dt -= pd.Timedelta(days=1)
        return dt

    def _run_backtest(self):
        initial_aum = self.args.initial_aum
        aum = initial_aum
        daily_returns = []

        current_date = pd.Timestamp(self.args.b)
        end_date = pd.Timestamp(self.args.e) if self.args.e else self.stocks_data[next(iter(self.stocks_data))].index[-1]

        while current_date <= end_date:
            year = current_date.year
            month = current_date.month
            last_trading_day_of_month = self._get_last_trading_day_of_month(year, month, self.stocks_data[next(iter(self.stocks_data))])

            if current_date == last_trading_day_of_month:
                coefficients, t_values = self._compute_coefficients(month, self.stocks_data)
                print(f"Month: {month}, Coefficient t-values: {t_values}")
                scores = self._compute_scores(self.stocks_data, coefficients)
                sorted_stocks = sorted(scores.items(), key=lambda x: x[1], reverse=True)
                top_stocks = sorted_stocks[:math.ceil(len(sorted_stocks) * self.args.top_pct / 100)]

                stock_returns = []

                for ticker, _ in top_stocks:
                    stock_data = self.stocks_data[ticker]
                    stock_return = stock_data.loc[last_trading_day_of_month, 'Close'] / stock_data.loc[current_date, 'Close'] - 1
                    stock_returns.append(stock_return)

                daily_return = np.mean(stock_returns)
                daily_returns.append(daily_return)
                aum *= (1 + daily_return)
                self.daily_aum.append(aum)

                month += 1
                if month == 13:
                    year += 1
                    month = 1
                current_date = pd.Timestamp(year, month, 1)

        self.monthly_cumulative_ic = np.cumsum(daily_returns)
        self._compute_and_print_statistics()

    def _compute_and_print_statistics(self):
        days = len(self.daily_aum)
        begin_date = pd.Timestamp(self.args.b)
        end_date = pd.Timestamp(self.args.e) if self.args.e else self.stocks_data[next(iter(self.stocks_data))].index[-1]
        total_return = self.daily_aum[-1] / self.args.initial_aum - 1
        annualized_rate_of_return = (1 + total_return) ** (365 / days) - 1
        initial_aum = self.args.initial_aum
        final_aum = self.daily_aum[-1]
        average_daily_aum = np.mean(self.daily_aum)
        max_daily_aum = np.max(self.daily_aum)
        pnl = final_aum - initial_aum
        average_daily_return = np.mean(self.monthly_cumulative_ic)
        daily_standard_deviation = np.std(self.monthly_cumulative_ic)
        daily_sharpe_ratio = (average_daily_return - 0.0001) / daily_standard_deviation

        print("Begin date:", begin_date.strftime('%Y-%m-%d'))
        print("End date:", end_date.strftime('%Y-%m-%d'))
        print("Number of days:", days)
        print("Total stock return (adjusted for dividends):", total_return)
        print("Total return (of the AUM invested):", total_return)
        print("Annualized rate of return (of the AUM invested):", annualized_rate_of_return)
        print("Initial AUM:", initial_aum)
        print("Final AUM:", final_aum)
        print("Average daily AUM:", average_daily_aum)
        print("Maximum daily AUM:", max_daily_aum)
        print("PnL (of the AUM invested):", pnl)
        print("Average daily return of the portfolio (i.e., of the AUM invested):", average_daily_return)
        print("Daily Standard deviation of the return of the portfolio:", daily_standard_deviation)
        print("Daily Sharpe Ratio of the portfolio (assume a daily risk-free rate of 0.01%):", daily_sharpe_ratio)

    def run(self):
        self._run_backtest()

