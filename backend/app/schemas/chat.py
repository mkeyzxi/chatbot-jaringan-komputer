from typing import List, Optional, Literal

from pydantic import BaseModel, Field


class SourceMetadata(BaseModel):
    source: str
    page: int
    score: Optional[float] = None


class RetrievalInfo(BaseModel):
    k: int
    sources: List[SourceMetadata]


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000, description="Pertanyaan mahasiswa")
    mode: Literal["cepat", "berpikir"] = Field("berpikir", description="Mode jawaban: cepat atau berpikir")


class ChatResponse(BaseModel):
    answer: str
    retrieval: RetrievalInfo
    latency_ms: Optional[float] = None
