from typing import Annotated

from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.dependencies.guards import auth_guard
from core.services.user import (
    delete_user_service,
    get_user_by_id_service,
    update_user_service,
)
from db import db_session
from schemas.user import DeleteUserData, GetUserData, UpdateUserData

router = APIRouter(
    tags=["User"]
)


@router.get("/{user_id}", response_model=GetUserData)
async def get_user_by_id(
    session: Annotated[AsyncSession, Depends(db_session.session_getter)],
    user_id: int,
):
    return await get_user_by_id_service(session, user_id)


@router.put("/update_user", response_model=GetUserData)
async def update_user(
    session: Annotated[AsyncSession, Depends(db_session.session_getter)],
    user_update: UpdateUserData = Body(...),
):
    return await update_user_service(session, user_update)


@router.delete("/{user_id}", response_model=DeleteUserData)
async def delete_user(
    session: Annotated[AsyncSession, Depends(db_session.session_getter)],
    user_id: int,
):
    return await delete_user_service(session, user_id)
