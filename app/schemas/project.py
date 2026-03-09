from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from .base import PageResponse

# --- Project ---

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    pass

class Project(ProjectBase):
    id: str
    status: str
    createdAt: Optional[Any] = None
    updatedAt: Optional[Any] = None

    class Config:
        from_attributes = True

class ProjectList(PageResponse[Project]):
    pass

# --- Module ---

class ModuleBase(BaseModel):
    name: str
    description: Optional[str] = None
    parentId: Optional[str] = None

class ModuleCreate(ModuleBase):
    pass

class Module(ModuleBase):
    id: str
    projectId: str
    
    class Config:
        from_attributes = True

# --- Environment ---

class EnvironmentAuth(BaseModel):
    authType: str  # e.g., 'bearer', 'basic', 'apiKey'
    tokenVar: Optional[str] = None
    loginTestcaseId: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None

class EnvironmentBase(BaseModel):
    name: str
    baseUrl: str
    headers: Optional[Dict[str, str]] = {}
    auth: Optional[EnvironmentAuth] = None
    variables: Optional[Dict[str, Any]] = {}

class EnvironmentCreate(EnvironmentBase):
    secretVariables: Optional[Dict[str, str]] = {} # Write-only

class EnvironmentUpdate(EnvironmentBase):
    secretVariables: Optional[Dict[str, str]] = None

class Environment(EnvironmentBase):
    id: str
    projectId: str
    # secretVariables are NOT returned in read model for security (PRD 9.4)

    class Config:
        from_attributes = True
