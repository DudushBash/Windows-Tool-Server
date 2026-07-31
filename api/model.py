from pydantic import BaseModel, Field


class ToolRequest(BaseModel):
    tool: str
    arguments: dict = Field(default_factory=dict)

class ToolResponse(BaseModel):
    success: bool
    message: str


class SearchHit(BaseModel):
    id: str
    name: str
    path: str
    type: str
    description: str
    score: float


class SearchResponse(BaseModel):
    semantic_enabled: bool
    results: list[SearchHit]


class IndexRefreshResponse(BaseModel):
    indexed_objects: int
