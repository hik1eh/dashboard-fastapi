from sqlalchemy.ext.asyncio import AsyncSession
from starlette.concurrency import run_in_threadpool

from app.auth.exceptions import EmailAlreadyRegistred, InvalidCredentials
from app.auth.models import User
from app.auth.repositories import UserRepository
from app.auth.schemas import RegisterUserRequest, LoginUserRequest
from app.core.security import hash_password, verify_password


class AuthService:
    
    def __init__(self, session: AsyncSession) -> None: 
        self.session = session
        self.users = UserRepository(session)
    
    async def register(self, data: RegisterUserRequest) -> User:
        email = data.email.lower()
        if await self.users.by_email(email):
            raise EmailAlreadyRegistred

        encoded_password = await run_in_threadpool(hash_password, data.password)
        user = User(
            email=email,
            name=data.name.strip(),
            password_hash = encoded_password
        )
        self.users.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def login(self, data: LoginUserRequest) -> User:
        user = await self.users.by_email(data.email.lower())
        password_is_valid = bool(
            user and await run_in_threadpool(verify_password, data.password, user.password_hash)
        )
        if not user or not password_is_valid:
            raise InvalidCredentials
        return user