from typing import Annotated

from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.services.user import (
    add_user_service,
)
from db import db_session
from schemas.user import AddUserData, GetUserData

router = APIRouter(tags=["User"])


@router.post("/add_user", response_model=GetUserData)
async def add_user(
    session: Annotated[AsyncSession, Depends(db_session.session_getter)],
    user_new: AddUserData = Body(...),
):
    return await add_user_service(session, user_new)

