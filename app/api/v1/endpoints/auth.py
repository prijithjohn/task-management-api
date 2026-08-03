from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database.session import get_db
from app.schemas.user import Token, UserCreate, UserLogin, UserResponse
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=Token, status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)) -> Token:
    service = AuthService(db)
    return service.register(payload)


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)) -> Token:
    service = AuthService(db)
    return service.login(payload)


@router.get("/me", response_model=UserResponse)
def get_me(current_user=Depends(get_current_user)) -> UserResponse:
    return UserResponse.model_validate(current_user)
