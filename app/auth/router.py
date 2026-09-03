from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.dependencies import CurrentUser, DbSession
from app.auth.exceptions import EmailAlreadyRegistred, InvalidCredentials
from app.auth.models import User
from app.auth.schemas import AuthResponse, LoginUserRequest, RegisterUserRequest, UserRead
from app.auth.services import AuthService

router = APIRouter(prefix='/auth', tags=['auth'])

def get_auth_service(db: DbSession) -> AuthService:
    return AuthService(db)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


@router.post('/register', response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(data: RegisterUserRequest, service: AuthServiceDep) -> AuthResponse:
    try:
        user = await service.register(data)
    except EmailAlreadyRegistred as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, 'Email is already registered') from exc
    return AuthResponse(user=user, message='Account created')

@router.post('/login', response_model=AuthResponse)
async def login(data: LoginUserRequest, service: AuthServiceDep) -> AuthResponse:
    try:
        user = await service.login(data)
    except InvalidCredentials as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Invalid email or password') from exc
    return AuthResponse(user=user, message='Sign in')

@router.post('/logout', status_code=status.HTTP_204_NO_CONTENT)
def logout() -> None:
    return None

@router.get('/me', response_model=UserRead)
async def me(user: CurrentUser) -> User:
    return user

