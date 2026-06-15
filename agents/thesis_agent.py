"""
Thesis Agent

Responsibilities:
1. Combine outputs from:
   - Valuation Agent
   - News Agent
   - RAG Agent

2. Generate:
   - Executive Summary
   - Growth Drivers
   - Risks
   - Bull Case
   - Bear Case
   - Final Assessment

3. Calculate Confidence Score

Uses:
GPT-4o
"""

import os
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()

class ThesisAgent:

    def __init__(self):

        self.client = OpenAI(
            api_key=os.getenv(
                "OPENAI_API_KEY"
            )
        )

    def calculate_confidence_score(
        self,
        valuation_data,
        news_data,
        rag_data
    ):
        """
        Simple heuristic.

        Can be improved later.
        """

        score = 50

        valuation_status = valuation_data.get(
            "valuation_status",
            ""
        )

        if valuation_status == "Undervalued":
            score += 10

        if len(news_data.get(
            "positive_news",
            []
        )) > len(
            news_data.get(
                "negative_news",
                []
            )
        ):
            score += 10

        if (
            rag_data.get("risks")
            and rag_data["risks"] !=
            "No filing context available."
        ):
            score += 15

        if (
            rag_data.get("growth")
            and rag_data["growth"] !=
            "No filing context available."
        ):
            score += 15

        return min(score, 100)

    def build_prompt(
        self,
        ticker,
        valuation_data,
        news_data,
        rag_data,
        confidence_score
    ):

        positive_news = "\n".join(
            [
                n["title"]
                for n in news_data.get(
                    "positive_news",
                    []
                )
            ]
        )

        negative_news = "\n".join(
            [
                n["title"]
                for n in news_data.get(
                    "negative_news",
                    []
                )
            ]
        )

        prompt = f"""
You are a senior equity research analyst.

Analyze the company below.

Ticker:
{ticker}

VALUATION DATA

Current Price:
{valuation_data['stock_price']:.2f}

Estimated Fair Value:
{valuation_data['fair_value']:.2f}

Valuation Status:
{valuation_data['valuation_status']}

FCF Margin:
{valuation_data['fcf_margin']:.2%}

Confidence Interval:
{valuation_data['confidence_interval']}

POSITIVE NEWS

{positive_news}

NEGATIVE NEWS

{negative_news}

SEC FILING INSIGHTS

Growth Drivers

{rag_data['growth']}

Management Commentary

{rag_data['management']}

Risks

{rag_data['risks']}

Generate a detailed investment memo.

Required Sections:

# Executive Summary

# Valuation Analysis

# Recent Developments

# Growth Drivers

# Key Risks

# Bull Case

# Bear Case

# Final Assessment

# Confidence Score

Confidence Score:
{confidence_score}/100

Be balanced and professional.
Use markdown formatting.
"""

        return prompt

    def generate_memo(
        self,
        prompt
    ):

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content":
                    """
You are a professional
equity research analyst.
                    """
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        return (
            response
            .choices[0]
            .message
            .content
        )

    def run(
        self,
        ticker,
        valuation_data,
        news_data,
        rag_data
    ):

        confidence_score = (
            self.calculate_confidence_score(
                valuation_data,
                news_data,
                rag_data
            )
        )

        prompt = self.build_prompt(
            ticker,
            valuation_data,
            news_data,
            rag_data,
            confidence_score
        )

        memo = self.generate_memo(
            prompt
        )

        return {
            "memo": memo,
            "confidence_score":
            confidence_score
        }