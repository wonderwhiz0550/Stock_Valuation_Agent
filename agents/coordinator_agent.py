"""
Coordinator Agent

This is the master orchestrator.

Workflow:

Ticker
  ↓
Data Agent
  ↓
Valuation Agent
  ↓
News Agent
  ↓
RAG Agent
  ↓
Thesis Agent
  ↓
Final Output

Streamlit only talks to this agent.
"""

from agents.data_agent import (
    DataAgent
)

from agents.valuation_agent import (
    ValuationAgent
)

from agents.news_agent import (
    NewsAgent
)

from agents.rag_agent import (
    RAGAgent
)

from agents.thesis_agent import (
    ThesisAgent
)


class CoordinatorAgent:

    def __init__(
        self,
        config
    ):

        self.config = config

        self.data_agent = (
            DataAgent(config)
        )

        self.valuation_agent = (
            ValuationAgent(config)
        )

        self.news_agent = (
            NewsAgent()
        )

        self.rag_agent = (
            RAGAgent()
        )

        self.thesis_agent = (
            ThesisAgent()
        )

    def run_analysis(
        self,
        ticker
    ):
        """
        Main orchestration function.
        """

        company_data = (
            self.data_agent.run(
                ticker
            )
        )

        if company_data is None:

            return {
                "status":
                "Failed to fetch stock data"
            }

        valuation_result = (
            self.valuation_agent.run(
                company_data
            )
        )

        if (
            valuation_result.get(
                "status"
            )
            != "Success"
        ):
            return valuation_result

        news_result = (
            self.news_agent.run(
                ticker
            )
        )

        try:

            rag_result = (
                self.rag_agent.run(
                    ticker
                )
            )

        except Exception:

            rag_result = {
                "risks":
                "No filing context available.",
                "growth":
                "No filing context available.",
                "management":
                "No filing context available."
            }

        thesis_result = (
            self.thesis_agent.run(
                ticker=ticker,
                valuation_data=
                valuation_result,
                news_data=
                news_result,
                rag_data=
                rag_result
            )
        )

        return {

            "status": "Success",

            "ticker":
            ticker,

            "valuation":
            valuation_result,

            "news":
            news_result,

            "rag":
            rag_result,

            "memo":
            thesis_result["memo"],

            "confidence_score":
            thesis_result[
                "confidence_score"
            ]
        }