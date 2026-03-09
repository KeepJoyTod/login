from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import testcase as schemas
from ..schemas.base import PageResponse

# Router for /testcases/{id}
testcases_router = APIRouter(
    prefix="/testcases",
    tags=["testcases"],
)

@testcases_router.get("/{testcase_id}", response_model=schemas.TestCase)
def get_testcase(testcase_id: str, db: Session = Depends(get_db)):
    return schemas.TestCase(
        id=testcase_id,
        projectId="p_1",
        interfaceId="api_1",
        name="Create Project - Positive",
        type="positive"
    )

# Router for /projects/{id}/testcases
project_testcases_router = APIRouter(
    prefix="/projects/{project_id}/testcases",
    tags=["testcases"],
)

@project_testcases_router.post("/", response_model=schemas.TestCase)
def create_testcase(
    project_id: str,
    testcase: schemas.TestCaseCreate,
    db: Session = Depends(get_db)
):
    return schemas.TestCase(
        id="tc_1",
        projectId=project_id,
        interfaceId=testcase.interfaceId,
        name=testcase.name,
        type=testcase.type
    )

@project_testcases_router.get("/", response_model=PageResponse[schemas.TestCase])
def list_project_testcases(
    project_id: str,
    interfaceId: Optional[str] = None,
    page: int = 1,
    pageSize: int = 20,
    db: Session = Depends(get_db)
):
    return PageResponse(total=1, items=[
        schemas.TestCase(
            id="tc_1",
            projectId=project_id,
            interfaceId=interfaceId or "api_1",
            name="Create Project - Positive",
            type="positive"
        )
    ])
