from sklearn.metrics.pairwise import cosine_similarity
from search.index import SearchIndex
from search.result import SearchResult


class TFIDFSearchEngine:
    def __init__(self, index: SearchIndex):
        self._index = index

    def search(self,query: str,limit: int = 5,) -> list[SearchResult]:
        if not query or not query.strip() or not self._index.objects:
            return []

        vector = self._index.vectorizer.transform([query])
        similarities = cosine_similarity(vector,self._index.matrix,)[0]
        indices = similarities.argsort()[::-1]
        results = []

        for index in indices:
            score = float(similarities[index])
            if score <= 0:
                continue
            results.append(SearchResult(object=self._index.objects[index],score=score,))
            if len(results) == limit:
                break
        return results

    def search_one(self,query: str,) -> SearchResult | None:

        results = self.search(query, limit=1)
        if results:
            return results[0]
        return None
