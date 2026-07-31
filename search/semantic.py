"""Hybrid lexical and semantic search for indexed system objects."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Sequence

import numpy as np

from search.index import SearchIndex
from search.result import SearchResult
from search.tfidf import TFIDFSearchEngine


DEFAULT_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


class EmbeddingModel(Protocol):
    def encode(self, sentences: Sequence[str], **kwargs: object) -> np.ndarray:
        """Return one normalized embedding per input sentence."""


class SemanticSearchEngine:
    """Dense-vector search backed by a multilingual SentenceTransformer model."""

    def __init__(self, documents: Sequence[str], model: EmbeddingModel):
        self._model = model
        self._document_embeddings = self._encode(documents)

    @classmethod
    def from_pretrained(
        cls, documents: Sequence[str], model_name: str = DEFAULT_MODEL
    ) -> "SemanticSearchEngine":
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as error:  # pragma: no cover - depends on deployment
            raise RuntimeError(
                "Для семантического поиска установите sentence-transformers."
            ) from error

        # The first launch downloads a compact multilingual model and caches it
        # locally. Following launches use that cache.
        return cls(documents, SentenceTransformer(model_name))

    def scores(self, query: str) -> np.ndarray:
        if not query.strip() or self._document_embeddings.size == 0:
            return np.array([], dtype=float)
        return self._document_embeddings @ self._encode([query])[0]

    def _encode(self, sentences: Sequence[str]) -> np.ndarray:
        if not sentences:
            return np.empty((0, 0), dtype=float)
        embeddings = self._model.encode(
            list(sentences),
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        return np.asarray(embeddings, dtype=float)


@dataclass(frozen=True)
class SearchCapabilities:
    semantic_enabled: bool
    semantic_error: str | None = None


class HybridSearchEngine:
    """Ranks exact terms and meaning together, with a safe lexical fallback."""

    def __init__(
        self,
        index: SearchIndex,
        *,
        semantic_weight: float = 0.65,
        model_name: str = DEFAULT_MODEL,
        semantic_engine: SemanticSearchEngine | None = None,
    ):
        if not 0 <= semantic_weight <= 1:
            raise ValueError("semantic_weight must be between 0 and 1")

        self._index = index
        self._lexical = TFIDFSearchEngine(index)
        self._semantic_weight = semantic_weight
        self._semantic: SemanticSearchEngine | None = semantic_engine
        self._capabilities = SearchCapabilities(semantic_enabled=semantic_engine is not None)

        if semantic_engine is None and index.documents:
            try:
                self._semantic = SemanticSearchEngine.from_pretrained(
                    index.documents, model_name
                )
                self._capabilities = SearchCapabilities(semantic_enabled=True)
            except Exception as error:  # application still works offline
                self._capabilities = SearchCapabilities(
                    semantic_enabled=False, semantic_error=str(error)
                )

    @property
    def capabilities(self) -> SearchCapabilities:
        return self._capabilities

    def search(self, query: str, limit: int = 5) -> list[SearchResult]:
        if limit < 1 or not query or not query.strip() or not self._index.objects:
            return []

        lexical_scores = self._lexical_scores(query)
        if self._semantic is None:
            scores = lexical_scores
        else:
            semantic_scores = np.clip(self._semantic.scores(query), 0.0, 1.0)
            scores = (
                (1.0 - self._semantic_weight) * lexical_scores
                + self._semantic_weight * semantic_scores
            )

        ranked = np.argsort(scores)[::-1]
        return [
            SearchResult(object=self._index.objects[position], score=float(scores[position]))
            for position in ranked[:limit]
            if scores[position] > 0
        ]

    def search_one(self, query: str) -> SearchResult | None:
        results = self.search(query, limit=1)
        return results[0] if results else None

    def _lexical_scores(self, query: str) -> np.ndarray:
        vector = self._index.vectorizer.transform([query])
        # TF-IDF vectors are L2-normalized by default, so a dot product equals
        # cosine similarity and avoids allocating a pairwise similarity matrix.
        return (vector @ self._index.matrix.T).toarray().ravel()
