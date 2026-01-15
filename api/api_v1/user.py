from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import UserDBError
from core.services.user import (
    add_user_service,
    delete_user_service,
    get_user_by_id_service,
    update_user_service,
)
from db import db_session
from schemas.user import AddUserData, DeleteUserData, GetUserData, UpdateUserData

router = APIRouter(tags=["User"])


@router.get("/{user_id}", response_model=GetUserData)
async def get_user_by_id(
    session: Annotated[AsyncSession, Depends(db_session.session_getter)],
    user_id: int,
):
    try:
        return await get_user_by_id_service(session, user_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")
    except UserDBError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add_user", response_model=GetUserData)
async def add_user(
    session: Annotated[AsyncSession, Depends(db_session.session_getter)],
    user_new: AddUserData = Body(...),
):
    try:
        return await add_user_service(session, user_new)
    except UserDBError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/update_user", response_model=GetUserData)
async def update_user(
    session: Annotated[AsyncSession, Depends(db_session.session_getter)],
    user_update: UpdateUserData = Body(...),
):
    try:
        return await update_user_service(session, user_update)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")
    except UserDBError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{user_id}", response_model=DeleteUserData)
async def delete_user(
    session: Annotated[AsyncSession, Depends(db_session.session_getter)],
    user_id: int,
):
    try:
        return await delete_user_service(session, user_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")
    except UserDBError as e:
        raise HTTPException(status_code=500, detail=str(e))
