from fastapi import HTTPException, status

class AuthError(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(
            status_code=status_code, 
            detail=detail
            )
        
class EmailAlreadyRegistred(AuthError):
    def __init__(self):
        super().__init__(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Пользователь с таким email уже существует"
        )

class InvalidCredentials(AuthError):
    def __init__(self):
        super().__init__(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Неверный email или password" 
        )