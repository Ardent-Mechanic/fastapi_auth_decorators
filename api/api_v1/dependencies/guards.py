from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from db import db_session
from core.security.jwt import decode_access_token
from core.services.user import get_user_by_id_service
from core.exceptions.custom_exceptions import UnauthorizedError
from model.user import User

from core.config import settings

path = f"{settings.api.prefix}{settings.api.v1.prefix}{settings.api.v1.auth}/login"

print(f"path == {path}")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=path)


async def get_current_user(
    session: Annotated[AsyncSession, Depends(db_session.session_getter)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    user_id = decode_access_token(token)
    user = await get_user_by_id_service(session, user_id)
    if not user:
        raise UnauthorizedError()
    return user


async def auth_guard(
    user: Annotated[User, Depends(get_current_user)],
) -> User:
    return user
