from typing import Generic, TypeVar, List, Optional, Any
from pydantic import BaseModel

T = TypeVar("T")

class ResponseBase(BaseModel, Generic[T]):
    code: int = 0
    message: str = "ok"
    data: Optional[T] = None
    requestId: Optional[str] = None

class PageParams(BaseModel):
    page: int = 1
    pageSize: int = 20

class PageResponse(BaseModel, Generic[T]):
    total: int
    items: List[T]
