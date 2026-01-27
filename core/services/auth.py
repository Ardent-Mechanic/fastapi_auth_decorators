from crud.user import get_user_by_email_db
from sqlalchemy.ext.asyncio import AsyncSession
from core.exceptions.custom_exceptions import NotFoundError, UnauthorizedError
from schemas.auth import LoginData, TokenResponse
from core.security.jwt import create_access_token
from core.security.password_hasher import verify_password

async def authenticate_user_service(
    session: AsyncSession,
    login_data: LoginData,
) -> TokenResponse:
    
    user = await get_user_by_email_db(session, login_data.email)
    if not user:
        raise NotFoundError(detail="User not found")
    if not verify_password(login_data.password, user.hashed_password):
        raise UnauthorizedError(detail="Invalid credentials")
    token = create_access_token(subject=user.user_id, expires_delta=None)
    return TokenResponse(access_token=token)