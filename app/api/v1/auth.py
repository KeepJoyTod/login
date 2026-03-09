from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.rate_limit import limiter
from app.schemas.user import RegisterResponse, UserLoginRequest, UserRegisterRequest
from app.services.auth_service import login_user, register_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(payload: UserRegisterRequest, db: Session = Depends(get_db)) -> RegisterResponse:
    return register_user(db=db, payload=payload)


@router.post(
    "/login",
    response_model=RegisterResponse,
    status_code=status.HTTP_200_OK,
)
@limiter.limit("5/5minutes")
def login(
    request: Request, payload: UserLoginRequest, db: Session = Depends(get_db)
) -> RegisterResponse:
    return login_user(db=db, payload=payload)
