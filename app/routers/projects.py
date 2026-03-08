from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import project as schemas

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    # Logic to create project
    return schemas.Project(id="p_1", name=project.name, status="active", description=project.description)

@router.get("/", response_model=schemas.ProjectList)
def list_projects(
    page: int = 1, 
    pageSize: int = 20, 
    keyword: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    # Logic to list projects
    return schemas.ProjectList(total=1, items=[
        schemas.Project(id="p_1", name="demo", status="active", description="Demo Project")
    ])

@router.get("/{project_id}", response_model=schemas.Project)
def get_project(project_id: str, db: Session = Depends(get_db)):
    return schemas.Project(id=project_id, name="demo", status="active")

# --- Environments ---

@router.post("/{project_id}/environments", response_model=schemas.Environment)
def create_environment(
    project_id: str, 
    env: schemas.EnvironmentCreate, 
    db: Session = Depends(get_db)
):
    return schemas.Environment(
        id="env_1", 
        projectId=project_id, 
        name=env.name, 
        baseUrl=env.baseUrl,
        auth=env.auth,
        variables=env.variables
    )

@router.get("/{project_id}/environments", response_model=List[schemas.Environment])
def list_environments(project_id: str, db: Session = Depends(get_db)):
    return []
