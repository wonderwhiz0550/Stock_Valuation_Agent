"""
Valuation Agent

Responsibilities:
1. DCF
2. Monte Carlo
3. Confidence Interval
4. Valuation Decision
5. Histogram Generation
"""

import numpy as np
import matplotlib.pyplot as plt


class ValuationAgent:

    def __init__(self, config):
        self.config = config

    def multi_stage_dcf(
        self,
        revenue,
        growth_rates,
        fcf_margin,
        discount_rate,
        terminal_growth_rate,
        shares_outstanding,
    ):

        high_growth_period = (
            self.config["high_growth_period"]
        )

        transition_period = (
            self.config["transition_period"]
        )

        high_growth_rate = growth_rates[0]

        transition_growth_rate = (
            growth_rates[1]
        )

        revenues = [
            revenue * (1 + high_growth_rate) ** t
            for t in range(
                1,
                high_growth_period + 1
            )
        ]

        revenues += [
            revenues[-1]
            * (1 + transition_growth_rate) ** t
            for t in range(
                1,
                transition_period + 1
            )
        ]

        if (
            self.config["terminal_method"]
            == "perpetual_growth"
        ):

            terminal_revenue = (
                revenues[-1]
                * (
                    1
                    + terminal_growth_rate
                )
            )

            terminal_fcf = (
                terminal_revenue
                * fcf_margin
            )

            terminal_value = (
                terminal_fcf
                / (
                    discount_rate
                    - terminal_growth_rate
                )
            )

        else:

            terminal_ebitda = (
                revenues[-1]
                * fcf_margin
            )

            terminal_value = (
                terminal_ebitda
                * self.config[
                    "exit_multiple"
                ]
            )

        fcfs = [
            rev * fcf_margin
            for rev in revenues
        ]

        npv = sum(
            fcf
            / (1 + discount_rate) ** t
            for t, fcf in enumerate(
                fcfs,
                start=1
            )
        )

        npv += (
            terminal_value
            / (
                1 + discount_rate
            )
            ** (
                high_growth_period
                + transition_period
            )
        )

        return npv / shares_outstanding

    def monte_carlo(
        self,
        company_data
    ):

        simulated_prices = []

        revenue = company_data["revenue"]

        stock_price = company_data[
            "stock_price"
        ]

        fcf_margin = (
            company_data["free_cash_flow"]
            / revenue
        )

        shares = company_data[
            "shares_outstanding"
        ]

        discount_rate = company_data[
            "discount_rate"
        ]

        for _ in range(
            self.config[
                "num_monte_carlo_sims"
            ]
        ):

            growth_rate = np.clip(
                np.random.normal(
                    0.05,
                    self.config[
                        "sensitivity_range"
                    ],
                ),
                -0.2,
                0.5,
            )

            discount_rate_sim = np.clip(
                np.random.normal(
                    discount_rate,
                    self.config[
                        "sensitivity_range"
                    ]
                    * discount_rate,
                ),
                0.01,
                0.20,
            )

            terminal_growth_rate_sim = (
                np.clip(
                    np.random.normal(
                        self.config[
                            "terminal_growth_rate"
                        ],
                        self.config[
                            "sensitivity_range"
                        ]
                        * self.config[
                            "terminal_growth_rate"
                        ],
                    ),
                    0.01,
                    0.06,
                )
            )

            try:

                price = self.multi_stage_dcf(
                    revenue,
                    [
                        growth_rate,
                        growth_rate * 0.5,
                    ],
                    fcf_margin,
                    discount_rate_sim,
                    terminal_growth_rate_sim,
                    shares,
                )

                if price > 0:
                    simulated_prices.append(
                        price
                    )

            except Exception:
                continue

        return simulated_prices

    @staticmethod
    def compare_prices(
        stock_price,
        fair_value,
    ):

        if stock_price < fair_value * 0.90:
            return "Undervalued"

        elif stock_price > fair_value * 1.10:
            return "Overvalued"

        return "Fairly Priced"

    def generate_plot(
        self,
        ticker,
        simulated_prices,
        stock_price,
        fair_value,
    ):

        plot_path = (
            "plots/valuation_plot.png"
        )

        plt.figure(figsize=(8, 5))

        plt.hist(
            simulated_prices,
            bins=50,
            alpha=0.75,
        )

        plt.axvline(
            stock_price,
            linestyle="dashed",
            label="Current Price",
        )

        plt.axvline(
            fair_value,
            linestyle="dashed",
            label="Fair Value",
        )

        plt.legend()

        plt.title(
            f"{ticker} Monte Carlo Valuation"
        )

        plt.tight_layout()

        plt.savefig(plot_path)

        plt.close()

        return plot_path

    def run(
        self,
        company_data
    ):

        simulated_prices = (
            self.monte_carlo(
                company_data
            )
        )

        if not simulated_prices:

            return {
                "status":
                "No valid simulations"
            }

        fair_value = np.mean(
            simulated_prices
        )

        lower_ci = np.percentile(
            simulated_prices,
            2.5
        )

        upper_ci = np.percentile(
            simulated_prices,
            97.5
        )

        valuation = (
            self.compare_prices(
                company_data[
                    "stock_price"
                ],
                fair_value,
            )
        )

        plot_path = (
            self.generate_plot(
                company_data["ticker"],
                simulated_prices,
                company_data[
                    "stock_price"
                ],
                fair_value,
            )
        )

        return {
            "status": "Success",
            "fair_value": fair_value,
            "valuation_status":
            valuation,
            "plot_path":
            plot_path,
            "confidence_interval":
            (
                lower_ci,
                upper_ci,
            ),
            "fcf_margin":
            company_data[
                "free_cash_flow"
            ]
            / company_data[
                "revenue"
            ],
            "revenue":
            company_data[
                "revenue"
            ],
            "free_cash_flow":
            company_data[
                "free_cash_flow"
            ],
            "stock_price":
            company_data[
                "stock_price"
            ],
        }