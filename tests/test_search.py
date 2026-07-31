import numpy as np

from models.object import ObjectType, SystemObject
from search.index import SearchIndex
from search.semantic import HybridSearchEngine, SemanticSearchEngine


class FakeEmbeddingModel:
    def encode(self, sentences, **kwargs):
        vectors = {
            "web browser internet": [1.0, 0.0],
            "spreadsheet budget tables": [0.0, 1.0],
            "open a web page": [0.9, 0.1],
        }
        return np.array([vectors[item] for item in sentences])


def test_hybrid_search_ranks_a_semantic_match():
    from sklearn.feature_extraction.text import TfidfVectorizer

    objects = [
        SystemObject("1", "Browser", "browser.exe", ObjectType.APPLICATION, "", (), {}),
        SystemObject("2", "Sheets", "sheets.exe", ObjectType.APPLICATION, "", (), {}),
    ]
    documents = ["web browser internet", "spreadsheet budget tables"]
    vectorizer = TfidfVectorizer().fit(documents)
    index = SearchIndex(vectorizer, vectorizer.transform(documents), objects, documents)
    semantic = SemanticSearchEngine(documents, FakeEmbeddingModel())
    engine = HybridSearchEngine(index, semantic_engine=semantic)

    results = engine.search("open a web page")

    assert results[0].object.name == "Browser"
    assert results[0].score > results[1].score
