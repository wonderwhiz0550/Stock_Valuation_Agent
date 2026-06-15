import streamlit as st

from config import DEFAULT_CONFIG
from agents.coordinator_agent import CoordinatorAgent

st.set_page_config(
    page_title="Stock Valuation Tool",
    layout="wide"
)

# --------------------------------------------------
# CSS
# --------------------------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(to right, #232526, #414345);
    color: #ffffff;
}

.card {
    background: rgba(255,255,255,0.07);
    border-radius: 1rem;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def format_large_number(number):

    if abs(number) >= 1_000_000_000:
        return f"${number / 1_000_000_000:.2f}B"

    elif abs(number) >= 1_000_000:
        return f"${number / 1_000_000:.2f}M"

    return f"${number:,.0f}"


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.markdown(
    "<h1 style='text-align:center;'>📊 Agentic Stock Valuation Platform</h1>",
    unsafe_allow_html=True
)

# --------------------------------------------------
# INPUT PANEL
# --------------------------------------------------

left, right = st.columns([2, 3])

config = DEFAULT_CONFIG.copy()

with left:

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    tabs = st.tabs([
        "🏢 Stock",
        "📈 Growth",
        "💸 Discount",
        "🎲 Simulation"
    ])

    with tabs[0]:

        ticker = st.text_input(
            "Stock Ticker",
            value="MSFT"
        )

    with tabs[1]:

        config[
            "default_analyst_growth_rate"
        ] = st.slider(
            "Analyst Growth Rate",
            0.01,
            0.20,
            0.07,
            0.001
        )

        config[
            "high_growth_period"
        ] = st.slider(
            "High Growth Period",
            1,
            15,
            8
        )

        config[
            "transition_period"
        ] = st.slider(
            "Transition Period",
            1,
            15,
            5
        )

        config[
            "terminal_growth_rate"
        ] = st.slider(
            "Terminal Growth Rate",
            0.0,
            0.10,
            0.035,
            0.001
        )

    with tabs[2]:

        config[
            "risk_free_rate"
        ] = st.slider(
            "Risk-Free Rate",
            0.0,
            0.10,
            0.035,
            0.001
        )

        config[
            "market_return"
        ] = st.slider(
            "Market Return",
            0.0,
            0.20,
            0.095,
            0.001
        )

        config[
            "default_discount_rate"
        ] = st.slider(
            "Default Discount Rate",
            0.0,
            0.20,
            0.011,
            0.001
        )

    with tabs[3]:

        config[
            "sensitivity_range"
        ] = st.slider(
            "Sensitivity Range",
            0.001,
            0.10,
            0.04,
            0.001
        )

        config[
            "num_monte_carlo_sims"
        ] = st.slider(
            "Monte Carlo Simulations",
            100,
            20000,
            10000,
            step=100
        )

        config[
            "exit_multiple"
        ] = st.slider(
            "Exit Multiple",
            5,
            40,
            20
        )

        config[
            "terminal_method"
        ] = st.radio(
            "Terminal Value Method",
            [
                "perpetual_growth",
                "exit_multiple"
            ]
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

# --------------------------------------------------
# OUTPUT PANEL
# --------------------------------------------------

with right:

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    if st.button("🚀 Run Valuation"):

        with st.spinner(
            "Running Agentic Analysis..."
        ):

            coordinator = (
                CoordinatorAgent(
                    config
                )
            )

            result = (
                coordinator.run_analysis(
                    ticker.upper()
                )
            )

            if result["status"] != "Success":

                st.error(
                    result["status"]
                )

            else:

                valuation = (
                    result["valuation"]
                )

                st.success(
                    "✅ Analysis Complete"
                )

                cols = st.columns(3)

                with cols[0]:

                    st.metric(
                        "📌 Current Price",
                        f"${valuation['stock_price']:.2f}"
                    )

                    st.metric(
                        "📈 Revenue",
                        format_large_number(
                            valuation["revenue"]
                        )
                    )

                with cols[1]:

                    st.metric(
                        "💰 Fair Value",
                        f"${valuation['fair_value']:.2f}"
                    )

                    st.metric(
                        "💸 Free Cash Flow",
                        format_large_number(
                            valuation[
                                "free_cash_flow"
                            ]
                        )
                    )

                with cols[2]:

                    st.metric(
                        "📊 Valuation",
                        valuation[
                            "valuation_status"
                        ]
                    )

                    st.metric(
                        "🧮 FCF Margin",
                        f"{valuation['fcf_margin']:.2%}"
                    )

                st.image(
                    valuation["plot_path"],
                    caption="📉 Monte Carlo Histogram",
                    use_container_width=True
                )

                # --------------------------
                # CONFIDENCE SCORE
                # --------------------------

                st.markdown("---")

                st.subheader(
                    "🎯 AI Confidence Score"
                )

                st.progress(
                    result[
                        "confidence_score"
                    ] / 100
                )

                st.write(
                    f"{result['confidence_score']}/100"
                )

                # --------------------------
                # AI MEMO
                # --------------------------

                st.markdown("---")

                st.subheader(
                    "🧠 AI Investment Memo"
                )

                st.markdown(
                    result["memo"]
                )

                # --------------------------
                # OPTIONAL DEBUG
                # --------------------------

                with st.expander(
                    "📂 Filing Insights"
                ):

                    st.markdown(
                        "### Growth Drivers"
                    )

                    st.write(
                        result["rag"][
                            "growth"
                        ]
                    )

                    st.markdown(
                        "### Management"
                    )

                    st.write(
                        result["rag"][
                            "management"
                        ]
                    )

                    st.markdown(
                        "### Risks"
                    )

                    st.write(
                        result["rag"][
                            "risks"
                        ]
                    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )