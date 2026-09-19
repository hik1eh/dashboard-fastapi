from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, StringConstraints

UserName = Annotated[str, StringConstraints(
    strip_whitespace=True, 
    min_length=2, 
    max_length=40
)]

class RegisterUserRequest(BaseModel):
    email : EmailStr
    name : UserName
    password: str = Field(min_length=8, max_length=128)
    
class LoginUserRequest(BaseModel):
    email: EmailStr
    password : str
    
class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id : UUID
    email : EmailStr
    name : str

class AuthResponse(BaseModel):
    user : UserRead
    message : str