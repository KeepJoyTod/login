from fastapi import HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.user import RegisterResponse, UserLoginRequest, UserRegisterRequest


def register_user(db: Session, payload: UserRegisterRequest) -> RegisterResponse:
    conflict_stmt = select(User).where(
        or_(
            User.username == payload.username,
            User.email == payload.email,
            User.phone == payload.phone if payload.phone else False,
        )
    )
    existing_user = db.execute(conflict_stmt).scalar_one_or_none()
    if existing_user:
        if existing_user.username == payload.username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Username already exists"
            )
        if existing_user.email == payload.email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email already exists"
            )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Phone already exists"
        )

    user = User(
        username=payload.username,
        email=payload.email,
        phone=payload.phone,
        password_hash=hash_password(payload.password),
    )
    db.add(user)

    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user",
        )

    token = create_access_token(user_id=user.id, username=user.username)
    return RegisterResponse(access_token=token, user_id=user.id)


def login_user(db: Session, payload: UserLoginRequest) -> RegisterResponse:
    stmt = select(User).where(User.username == payload.username)
    user = db.execute(stmt).scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )

    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )

    token = create_access_token(user_id=user.id, username=user.username)
    return RegisterResponse(access_token=token, user_id=user.id)


def get_user_by_id(db: Session, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    return db.execute(stmt).scalar_one_or_none()
