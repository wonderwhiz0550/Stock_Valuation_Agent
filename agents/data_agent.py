"""
Data Agent

Responsibilities:
1. Download financial data
2. Download company fundamentals
3. Calculate WACC / discount rate
4. Return standardized company data

No valuation logic here.
"""

import numpy as np
import requests
import yfinance as yf


class DataAgent:

    def __init__(self, config):
        self.config = config

    @staticmethod
    def validate_data(data, key, default=None):
        if data is not None and key in data and data[key] is not None:
            return data[key]

        return default if default is not None else np.nan

    def fetch_stock_data(self, ticker, max_retries=3):

        stock = yf.Ticker(ticker)

        retries = 0

        while retries < max_retries:

            try:

                stock_price_data = stock.history(period="1d")

                stock_price = (
                    stock_price_data["Close"].iloc[-1]
                    if not stock_price_data.empty
                    else np.nan
                )

                income_statement = stock.financials
                cashflow = stock.cashflow

                revenue = income_statement.loc["Total Revenue"].iloc[0]

                operating_cash_flow = (
                    cashflow.loc["Operating Cash Flow"].iloc[0]
                )

                capital_expenditure = (
                    cashflow.loc["Capital Expenditure"].iloc[0]
                    if "Capital Expenditure" in cashflow.index
                    else 0
                )

                free_cash_flow = (
                    operating_cash_flow - capital_expenditure
                )

                shares_outstanding = (
                    stock.info.get("sharesOutstanding", 1)
                )

                debt = self.validate_data(
                    stock.info,
                    "totalDebt",
                    0
                )

                market_cap = self.validate_data(
                    stock.info,
                    "marketCap",
                    np.nan
                )

                return {
                    "ticker": ticker,
                    "stock_price": stock_price,
                    "revenue": revenue,
                    "free_cash_flow": free_cash_flow,
                    "shares_outstanding": shares_outstanding,
                    "debt": debt,
                    "market_cap": market_cap,
                    "beta": stock.info.get("beta", 1),
                    "company_name": stock.info.get(
                        "longName",
                        ticker
                    ),
                }

            except Exception:
                retries += 1

        return None

    def fetch_analyst_growth_rate(self, ticker):

        try:

            url = (
                "https://www.alphavantage.co/query?"
                f"function=EARNINGS&symbol={ticker}&apikey=demo"
            )

            response = requests.get(url, timeout=20)

            data = response.json()

            annual_earnings = data.get(
                "annualEarnings",
                []
            )

            if len(annual_earnings) >= 2:

                latest_eps = float(
                    annual_earnings[0]["reportedEPS"]
                )

                previous_eps = float(
                    annual_earnings[1]["reportedEPS"]
                )

                growth_rate = (
                    latest_eps - previous_eps
                ) / previous_eps

                return growth_rate

        except Exception:
            pass

        return self.config[
            "default_analyst_growth_rate"
        ]

    def calculate_discount_rate(self, company_data):

        beta = company_data["beta"]

        debt = company_data["debt"]

        market_cap = company_data["market_cap"]

        cost_of_equity = (
            self.config["risk_free_rate"]
            + beta
            * (
                self.config["market_return"]
                - self.config["risk_free_rate"]
            )
        )

        cost_of_debt = self.config[
            "risk_free_rate"
        ]

        if (
            not np.isnan(debt)
            and not np.isnan(market_cap)
            and (debt + market_cap) > 0
        ):

            wacc = (
                cost_of_equity * market_cap
                + cost_of_debt * debt
            ) / (debt + market_cap)

            return wacc

        return cost_of_equity

    def run(self, ticker):

        company_data = self.fetch_stock_data(
            ticker
        )

        if company_data is None:
            return None

        company_data[
            "analyst_growth_rate"
        ] = self.fetch_analyst_growth_rate(
            ticker
        )

        company_data[
            "discount_rate"
        ] = self.calculate_discount_rate(
            company_data
        )

        return company_data