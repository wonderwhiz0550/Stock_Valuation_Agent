"""
RAG Agent

Responsibilities:

1. Download SEC filings
2. Build FAISS index
3. Query filings
4. Extract investment context

Output:

{
   risks: ...,
   growth: ...,
   management: ...
}
"""

from rag.sec_downloader import (
    SECFilingDownloader
)

from rag.build_index import (
    FAISSIndexBuilder
)

from rag.retrieve import (
    FAISSRetriever
)


class RAGAgent:

    def __init__(self):

        self.downloader = (
            SECFilingDownloader()
        )

    def ensure_company_data(
        self,
        ticker,
    ):

        try:

            self.downloader.download_latest_filings(
                ticker
            )

            builder = (
                FAISSIndexBuilder()
            )

            builder.build()

        except Exception as e:

            print(
                f"RAG setup error: {e}"
            )

    def retrieve_context(
        self,
        ticker,
    ):

        try:

            retriever = (
                FAISSRetriever()
            )

            risks = (
                retriever.search(
                    "major business risks",
                    ticker=ticker,
                    k=3,
                )
            )

            growth = (
                retriever.search(
                    "growth opportunities",
                    ticker=ticker,
                    k=3,
                )
            )

            management = (
                retriever.search(
                    "management strategy capital allocation",
                    ticker=ticker,
                    k=3,
                )
            )

            return {
                "risks":
                "\n".join(
                    [
                        x["text"][:1200]
                        for x in risks
                    ]
                ),
                "growth":
                "\n".join(
                    [
                        x["text"][:1200]
                        for x in growth
                    ]
                ),
                "management":
                "\n".join(
                    [
                        x["text"][:1200]
                        for x in management
                    ]
                ),
            }

        except Exception:

            return {
                "risks":
                "No filing context available.",
                "growth":
                "No filing context available.",
                "management":
                "No filing context available.",
            }

    def run(
        self,
        ticker,
    ):

        self.ensure_company_data(
            ticker
        )

        return self.retrieve_context(
            ticker
        )