"""
FAISS Retrieval

Loads:

index.faiss
metadata.pkl

Returns:
Top K relevant chunks
"""

import pickle

import faiss
import numpy as np

from rag.embeddings import (
    EmbeddingModel
)


class FAISSRetriever:

    def __init__(self):

        self.index = (
            faiss.read_index(
                "data/faiss/index.faiss"
            )
        )

        with open(
            "data/faiss/metadata.pkl",
            "rb",
        ) as f:

            self.metadata = (
                pickle.load(f)
            )

        self.embedder = (
            EmbeddingModel()
        )

    def search(
        self,
        query,
        ticker=None,
        k=5,
    ):

        query_vector = (
            self.embedder.encode(
                [query]
            )
        )

        distances, indices = (
            self.index.search(
                np.array(
                    query_vector,
                    dtype=np.float32,
                ),
                k * 4,
            )
        )

        results = []

        for idx in indices[0]:

            if idx < 0:
                continue

            chunk = (
                self.metadata[idx]
            )

            if (
                ticker
                and chunk["ticker"]
                != ticker
            ):
                continue

            results.append(chunk)

            if len(results) >= k:
                break

        return results