from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel
from .base import PageResponse

# --- Job Step ---

class JobStep(BaseModel):
    name: str
    status: str # pending, running, success, fail, skipped
    duration: Optional[float] = None
    errorMessage: Optional[str] = None

# --- Runtime Log ---

class RuntimeLog(BaseModel):
    seq: int
    level: str # info, warn, error
    message: str
    ts: float

class RuntimeLogList(BaseModel):
    nextSeq: int
    items: List[RuntimeLog]

# --- Job Result ---

class JobResultGenerate(BaseModel):
    generatedTestcases: List[Dict[str, Any]] = []

class JobResultRun(BaseModel):
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    failures: List[Dict[str, Any]] = []

# --- Job ---

class JobBase(BaseModel):
    projectId: str
    type: str # generate, run
    status: str # pending, running, success, fail, cancelled
    progress: int = 0
    steps: List[JobStep] = []

class JobCreate(JobBase):
    pass

class JobUpdate(JobBase):
    pass

class Job(JobBase):
    id: str
    createdAt: Optional[Any] = None
    updatedAt: Optional[Any] = None
    result: Optional[Union[JobResultGenerate, JobResultRun]] = None

    class Config:
        from_attributes = True

# --- API Requests ---

class GenerateRequest(BaseModel):
    projectId: str
    interfaceId: str
    envId: str
    types: List[str] # positive, negative, boundary
    maxCases: int = 6
    dependencyTestcaseIds: Optional[List[str]] = []
    mode: str = "append"

class RunRequest(BaseModel):
    projectId: str
    envId: str
    testcaseIds: List[str]
    suiteId: Optional[str] = None

class JobIdResponse(BaseModel):
    jobId: str
