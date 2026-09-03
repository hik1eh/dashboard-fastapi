from typing import Annotated
from uuid import UUID

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User
from app.auth.repositories import UserRepository
from app.db.session import get_db

DbSession = Annotated[AsyncSession, Depends(get_db)]


async def current_user(
    db: DbSession,
    x_user_id: str | None = Header(default=None),
) -> User:
    """Temporary development user dependency.

    This is not authentication. During the learning phase the frontend sends an
    optional X-User-Id header. If it is absent, the API uses the first user or
    creates a demo user so planner endpoints can be studied before JWT exists.
    """

    repository = UserRepository(db)
    if x_user_id:
        try:
            user = await repository.by_id(UUID(x_user_id))
        except ValueError as exc:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid X-User-Id") from exc
        if not user or not user.is_active:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
        return user

    user = await repository.first()
    if user and user.is_active:
        return user

    user = User(
        email="demo@example.com",
        name="Demo",
        password_hash="not-used-in-dev-mode",
    )
    repository.add(user)
    await db.commit()
    await db.refresh(user)
    return user


CurrentUser = Annotated[User, Depends(current_user)]
