"""
Embedding Generator

Uses:
all-MiniLM-L6-v2

Fast
Free
Good quality
"""

from sentence_transformers import (
    SentenceTransformer
)


class EmbeddingModel:

    def __init__(self):

        self.model = (
            SentenceTransformer(
                "all-MiniLM-L6-v2"
            )
        )

    def encode(
        self,
        texts,
    ):

        return self.model.encode(
            texts,
            show_progress_bar=False,
            convert_to_numpy=True,
        )