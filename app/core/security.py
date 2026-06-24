from datetime import datetime, timedelta, timezone
from typing import Optional, Union
import bcrypt
from jose import jwt
from app.core.config import settings

# Configuración JWT (mantené tus variables o tus imports de settings si los usabas)
SECRET_KEY = "TU_SECRET_KEY_SUPER_SECRETA"  # O de tus settings: settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña coincide usando el backend directo de bcrypt."""
    try:
        # bcrypt requiere que tanto el string como el hash estén en formato bytes
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """Genera el hash de la contraseña usando bcrypt de forma directa."""
    password_bytes = password.encode('utf-8')
    # Genera la sal e inyecta el hash
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode('utf-8')


def create_access_token(data: dict, expires_delta: timedelta = None):
    """Genera un token de acceso JWT estándar."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    print(f"🚀 SECURITY - Usando secreto para CODIFICAR: '{settings.JWT_SECRET}'")

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt