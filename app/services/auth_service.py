from datetime import timedelta
from typing import Any

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import ConflictException, UnauthorizedException
from app.core.security import create_access_token, get_password_hash, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.user import Token, UserCreate, UserLogin


class AuthService:
    def __init__(self, db: Session) -> None:
        self.user_repo = UserRepository(db)

    def register(self, payload: UserCreate) -> Token:
        if self.user_repo.get_by_email(payload.email) is not None:
            raise ConflictException("Email already registered")

        user = self.user_repo.create(
            email=str(payload.email),
            hashed_password=get_password_hash(payload.password),
        )
        access_token = create_access_token(user.id)
        return Token(access_token=access_token)

    def login(self, payload: UserLogin) -> Token:
        user = self.user_repo.get_by_email(str(payload.email))
        if user is None or not verify_password(payload.password, user.hashed_password):
            raise UnauthorizedException("Invalid email or password")
        if not user.is_active:
            raise UnauthorizedException("User account is inactive")

        access_token = create_access_token(user.id)
        return Token(access_token=access_token)
