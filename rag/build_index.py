"""
Build FAISS Index

Reads:
data/filings/

Creates:

data/faiss/index.faiss

data/faiss/metadata.pkl
"""

import os
import pickle
from pathlib import Path

import faiss
import numpy as np

from rag.chunking import (
    DocumentChunker
)

from rag.embeddings import (
    EmbeddingModel
)


class FAISSIndexBuilder:

    def __init__(self):

        self.chunker = (
            DocumentChunker()
        )

        self.embedder = (
            EmbeddingModel()
        )

        self.faiss_dir = Path(
            "data/faiss"
        )

        self.faiss_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def read_all_documents(self):

        documents = []

        filing_root = Path(
            "data/filings"
        )

        if not filing_root.exists():
            return documents

        for root, _, files in os.walk(
            filing_root
        ):

            for file in files:

                if (
                    file.endswith(".txt")
                    or file.endswith(".html")
                ):

                    path = (
                        Path(root)
                        / file
                    )

                    try:

                        with open(
                            path,
                            "r",
                            encoding="utf-8",
                            errors="ignore",
                        ) as f:

                            text = f.read()

                        ticker = (
                            path.parts[2]
                            if len(path.parts)
                            > 2
                            else "UNKNOWN"
                        )

                        documents.append(
                            {
                                "ticker":
                                ticker,
                                "path":
                                str(path),
                                "text":
                                text,
                            }
                        )

                    except Exception:
                        pass

        return documents

    def build(self):

        docs = (
            self.read_all_documents()
        )

        if len(docs) == 0:

            print(
                "No filings found."
            )

            return False

        metadata = []

        chunks = []

        for doc in docs:

            split_chunks = (
                self.chunker.chunk_text(
                    doc["text"]
                )
            )

            for chunk in split_chunks:

                chunks.append(chunk)

                metadata.append(
                    {
                        "ticker":
                        doc["ticker"],
                        "path":
                        doc["path"],
                        "text":
                        chunk,
                    }
                )

        embeddings = (
            self.embedder.encode(
                chunks
            )
        )

        dimension = (
            embeddings.shape[1]
        )

        index = faiss.IndexFlatL2(
            dimension
        )

        index.add(
            np.array(
                embeddings,
                dtype=np.float32,
            )
        )

        faiss.write_index(
            index,
            str(
                self.faiss_dir
                / "index.faiss"
            ),
        )

        with open(
            self.faiss_dir
            / "metadata.pkl",
            "wb",
        ) as f:

            pickle.dump(
                metadata,
                f,
            )

        print(
            f"Indexed {len(chunks)} chunks"
        )

        return True


if __name__ == "__main__":

    builder = FAISSIndexBuilder()

    builder.build()