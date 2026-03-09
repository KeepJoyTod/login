from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field

# --- Schema Definition ---

class FieldSchema(BaseModel):
    name: str
    type: str  # string, number, boolean, object, array
    required: bool = False
    minLength: Optional[int] = None
    maxLength: Optional[int] = None
    example: Optional[Any] = None
    description: Optional[str] = None
    items: Optional['FieldSchema'] = None # For arrays
    properties: Optional[List['FieldSchema']] = None # For objects

class RequestSchema(BaseModel):
    contentType: str = "application/json"
    fields: List[FieldSchema] = []

class ResponseSchema(BaseModel):
    successExample: Optional[Dict[str, Any]] = None
    fields: List[FieldSchema] = []

class InterfaceSchema(BaseModel):
    request: RequestSchema = Field(default_factory=RequestSchema)
    response: ResponseSchema = Field(default_factory=ResponseSchema)

# --- Interface ---

class InterfaceBase(BaseModel):
    title: str
    method: str
    path: str
    description: Optional[str] = None
    moduleId: Optional[str] = None
    schema: Optional[InterfaceSchema] = None
    tags: Optional[List[str]] = []

class InterfaceCreate(InterfaceBase):
    pass

class InterfaceUpdate(InterfaceBase):
    pass

class Interface(InterfaceBase):
    id: str
    projectId: str
    createdAt: Optional[Any] = None
    updatedAt: Optional[Any] = None

    class Config:
        from_attributes = True
