from typing import Optional
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str
    rol: Optional[str] = None
    email: Optional[str] = None
    nombre: Optional[str] = None


class TokenData(BaseModel):
    id_usuario: Optional[int] = None
    email: Optional[EmailStr] = None
    rol: Optional[str] = None