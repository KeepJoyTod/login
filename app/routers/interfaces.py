from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import interface as schemas
from ..schemas.base import PageResponse

router = APIRouter(
    prefix="/interfaces",
    tags=["interfaces"],
    responses={404: {"description": "Not found"}},
)

# Project-level interface listing
# Usually this would be under /projects/{id}/interfaces, but can be here too with query param
# PRD says: GET /projects/{projectId}/interfaces
# I will implement a separate router for project sub-resources or just use query param here?
# PRD explicitly lists /projects/{projectId}/interfaces.
# I will add a router in projects.py or here.
# Let's put it here for cleaner separation by resource type, but the path might need to be adjusted or I handle it via query param.
# But for strict adherence to PRD path:
# I will use APIRouter for /projects/{projectId}/interfaces in a separate block or file?
# Actually, I can just include a router for that specific path here.

@router.post("/", response_model=schemas.Interface)
def create_interface(interface: schemas.InterfaceCreate, db: Session = Depends(get_db)):
    return schemas.Interface(
        id="api_1", 
        projectId="p_1",
        method=interface.method,
        path=interface.path,
        title=interface.title
    )

@router.get("/{interface_id}", response_model=schemas.Interface)
def get_interface(interface_id: str, db: Session = Depends(get_db)):
    return schemas.Interface(
        id=interface_id, 
        projectId="p_1", 
        method="POST", 
        path="/api/v1/projects", 
        title="Create Project"
    )

# Sub-router for project interfaces
project_interfaces_router = APIRouter(
    prefix="/projects/{project_id}/interfaces",
    tags=["interfaces"],
)

@project_interfaces_router.get("/", response_model=PageResponse[schemas.Interface])
def list_project_interfaces(
    project_id: str, 
    page: int = 1, 
    pageSize: int = 20, 
    keyword: Optional[str] = None,
    moduleId: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return PageResponse(total=1, items=[
        schemas.Interface(
            id="api_1", 
            projectId=project_id, 
            method="POST", 
            path="/api/v1/projects", 
            title="Create Project"
        )
    ])
