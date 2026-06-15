"""
Global configuration used by all agents.

The Streamlit frontend will update values dynamically
before passing them to the Coordinator Agent.
"""

DEFAULT_CONFIG = {
    "risk_free_rate": 0.035,
    "market_return": 0.095,
    "terminal_growth_rate": 0.035,
    "default_discount_rate": 0.011,
    "default_analyst_growth_rate": 0.07,
    "high_growth_period": 8,
    "transition_period": 5,
    "sensitivity_range": 0.04,
    "num_monte_carlo_sims": 10000,
    "terminal_method": "exit_multiple",
    "exit_multiple": 20,
    "confidence_level": 0.95,
}