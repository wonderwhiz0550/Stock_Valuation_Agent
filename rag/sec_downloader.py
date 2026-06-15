"""
SEC Filing Downloader

Downloads latest:
- 10-K
- 10-Q

Stores raw filing text locally.

Folder Structure:

data/
 └── filings/
      └── MSFT/
           ├── 10K_latest.txt
           └── 10Q_latest.txt

Requires:
pip install sec-edgar-downloader
"""

from pathlib import Path
from sec_edgar_downloader import Downloader


class SECFilingDownloader:

    def __init__(
        self,
        company_name="Stock Valuation AI",
        email="wonderwhiz0550@gmail.com",
    ):

        self.base_path = Path(
            "data/filings"
        )

        self.base_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.downloader = Downloader(
            str(self.base_path),
            company_name,
            email,
        )

    def download_latest_filings(
        self,
        ticker,
    ):

        try:

            self.downloader.get(
                "10-K",
                ticker,
                limit=1,
            )

            self.downloader.get(
                "10-Q",
                ticker,
                limit=1,
            )

            return True

        except Exception as e:

            print(
                f"SEC download failed: {e}"
            )

            return False