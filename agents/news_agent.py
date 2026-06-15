"""
News Agent

Responsibilities:
1. Fetch latest news
2. Perform lightweight sentiment tagging
3. Prepare data for GPT Thesis Agent

No OpenAI calls yet.
Those will happen in Thesis Agent.
"""

import yfinance as yf


class NewsAgent:

    POSITIVE_WORDS = [
        "beat",
        "growth",
        "surge",
        "record",
        "strong",
        "raise",
    ]

    NEGATIVE_WORDS = [
        "miss",
        "decline",
        "fall",
        "lawsuit",
        "cut",
        "weak",
    ]

    def classify_news(
        self,
        headline
    ):

        headline_lower = (
            headline.lower()
        )

        positive_score = sum(
            word in headline_lower
            for word in self.POSITIVE_WORDS
        )

        negative_score = sum(
            word in headline_lower
            for word in self.NEGATIVE_WORDS
        )

        if positive_score > negative_score:
            return "positive"

        if negative_score > positive_score:
            return "negative"

        return "neutral"

    def run(
        self,
        ticker
    ):

        stock = yf.Ticker(ticker)

        positive = []

        negative = []

        neutral = []

        try:

            news_items = stock.news[:10]

            for item in news_items:

                title = item.get(
                    "title",
                    ""
                )

                sentiment = (
                    self.classify_news(
                        title
                    )
                )

                news_data = {
                    "title": title,
                    "publisher":
                    item.get(
                        "publisher",
                        ""
                    ),
                }

                if sentiment == "positive":
                    positive.append(
                        news_data
                    )

                elif sentiment == "negative":
                    negative.append(
                        news_data
                    )

                else:
                    neutral.append(
                        news_data
                    )

        except Exception:

            pass

        return {
            "positive_news":
            positive,
            "negative_news":
            negative,
            "neutral_news":
            neutral,
        }