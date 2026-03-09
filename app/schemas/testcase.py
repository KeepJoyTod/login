from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field

# --- Dependency ---

class Dependency(BaseModel):
    dependsOnTestcaseIds: List[str]
    strategy: str = "stopOnFail" # stopOnFail, continue

# --- Extractor ---

class Extractor(BaseModel):
    type: str # jsonPath, header, regex
    name: str # variable name
    path: Optional[str] = None # for jsonPath
    key: Optional[str] = None # for header
    regex: Optional[str] = None # for regex

# --- Assertion ---

class Assertion(BaseModel):
    type: str # statusCode, jsonPath, header, bodyContains
    op: Optional[str] = "eq" # eq, ne, gt, lt, exists, notExists, contains
    expected: Optional[Any] = None
    path: Optional[str] = None # for jsonPath
    key: Optional[str] = None # for header

# --- TestCase Definition ---

class StepRequest(BaseModel):
    method: str
    path: str
    headers: Optional[Dict[str, str]] = {}
    query: Optional[Dict[str, Any]] = {}
    body: Optional[Any] = None

class TestCaseStep(BaseModel):
    type: str = "http"
    name: str
    request: StepRequest
    assertions: List[Assertion] = []
    extractors: List[Extractor] = []

class TestCaseDefinition(BaseModel):
    steps: List[TestCaseStep] = []
    variables: Optional[Dict[str, Any]] = {}

# --- TestCase ---

class TestCaseBase(BaseModel):
    interfaceId: str
    moduleId: Optional[str] = None
    name: str
    type: str # positive, negative, boundary
    priority: str = "medium" # high, medium, low
    definition: Optional[TestCaseDefinition] = None
    tags: Optional[List[str]] = []

class TestCaseCreate(TestCaseBase):
    pass

class TestCaseUpdate(TestCaseBase):
    pass

class TestCase(TestCaseBase):
    id: str
    projectId: str
    createdAt: Optional[Any] = None
    updatedAt: Optional[Any] = None

    class Config:
        from_attributes = True
