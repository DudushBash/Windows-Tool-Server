from sklearn.feature_extraction.text import TfidfVectorizer
from database.repository import SystemObjectRepository
from search.index import SearchIndex
from models.object import SystemObject

class SearchIndexBuilder:
    def __init__(self, repository: SystemObjectRepository):
        self._repository = repository

    def build(self) -> SearchIndex:
        objects = self._repository.get_all()
        documents = [self._build_document(obj) for obj in objects]

        if not documents:
            # TfidfVectorizer cannot be fitted on an empty corpus.  Keeping an
            # empty, fitted index makes a fresh installation usable as well.
            documents = ["placeholder"]
            vectorizer = TfidfVectorizer(lowercase=True, ngram_range=(1, 2))
            matrix = vectorizer.fit_transform(documents)[:0]
            return SearchIndex(
                vectorizer=vectorizer,
                matrix=matrix,
                objects=[],
                documents=[],
            )

        vectorizer = TfidfVectorizer(lowercase=True,ngram_range=(1, 2),)
        matrix = vectorizer.fit_transform(documents)
        return SearchIndex(
            vectorizer=vectorizer,
            matrix=matrix,
            objects=objects,
            documents=documents,
        )

    @staticmethod
    def _build_document(obj: SystemObject) -> str:
        # Repeat the display name once: it is important for application search,
        # but no longer overwhelms descriptions and keywords.
        parts = [obj.name, obj.name, obj.description, *obj.keywords]
        return " ".join(part.lower() for part in parts if part)
