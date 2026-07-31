from dataclasses import dataclass
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from models.object import SystemObject

@dataclass(frozen=True)
class SearchIndex:
    vectorizer: TfidfVectorizer
    matrix: csr_matrix
    objects: list[SystemObject]
    documents: list[str]
