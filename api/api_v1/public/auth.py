from typing import Annotated
from fastapi import APIRouter, Body, Depends, Form

from schemas.auth import TokenResponse, LoginData
from core.services.auth import authenticate_user_service
from sqlalchemy.ext.asyncio import AsyncSession
from db import db_session


router = APIRouter(tags=["Auth"])


class LoginForm:
    """Конвертер form-data в Pydantic модель LoginData"""

    @classmethod
    def as_form(
        cls,
        username: str = Form(...),
        password: str = Form(...),
    ) -> LoginData:
        return LoginData(email=username, password=password)


@router.post("/login", response_model=TokenResponse)
async def login(
    session: Annotated[AsyncSession, Depends(db_session.session_getter)],
    login_data: LoginData = Depends(LoginForm.as_form),
):
    return await authenticate_user_service(session, login_data)
