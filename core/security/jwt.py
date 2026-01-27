from datetime import datetime, timedelta
from typing import Any

from jose import JWTError, jwt
from core.config import settings
from core.exceptions.custom_exceptions import UnauthorizedError


def create_access_token(subject: int, expires_delta: timedelta | None = None) -> str:
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.jwt.access_token_expire_minutes))
    payload: dict[str, Any] = {"sub": str(subject), "exp": expire}
    return jwt.encode(payload, settings.jwt.secret_key, algorithm=settings.jwt.algorithm)

def decode_access_token(token: str) -> int:
    try:
        payload = jwt.decode(token, settings.jwt.secret_key, algorithms=[settings.jwt.algorithm])
        user_id = payload.get("sub")
        if user_id is None:
            raise UnauthorizedError(headers={"WWW-Authenticate": "Bearer"}, detail="Invalid token")
        return int(user_id)
    except JWTError:
        raise UnauthorizedError(headers={"WWW-Authenticate": "Bearer"}, detail="Invalid token")
    