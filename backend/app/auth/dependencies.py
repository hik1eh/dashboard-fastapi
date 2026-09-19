from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User
from app.auth.repositories import UserRepository
from app.db.session import get_db
from app.core.security import decode_access_token

DbSession = Annotated[AsyncSession, Depends(get_db)]


bearer_scheme = HTTPBearer(auto_error=False)


async def current_user(
    db: DbSession,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Требуется авторизация",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not credentials or credentials.scheme.lower() != "bearer":
        raise credentials_error
    user_id = decode_access_token(credentials.credentials)
    if not user_id:
        raise credentials_error
    repository = UserRepository(db)
    user = await repository.by_id(user_id)
    if not user or not user.is_active:
        raise credentials_error
    return user


CurrentUser = Annotated[User, Depends(current_user)]
