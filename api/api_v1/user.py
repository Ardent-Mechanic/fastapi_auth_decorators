from typing import Annotated

from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
)
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import UserDBError
from crud.user import (
    add_user_db,
    delete_user_db,
    get_user_by_id_db,
    update_user_db,
)
from db import db_session

from schemas import GetUserData, AddUserData, UpdateUserData
from schemas.user import DeleteUserData, UpdateUserData

router = APIRouter(tags=["User"])


@router.get("/{user_id}", response_model=GetUserData, summary="")
async def get_user_by_id(
    session: Annotated[
        AsyncSession,
        Depends(db_session.session_getter),
    ],
    user_id: int,
):
    try:
        user = await get_user_by_id_db(session=session, user_id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except UserDBError as e:
        raise HTTPException(status_code=500, detail="Database error")


@router.post("/add_user", response_model=GetUserData, summary="")
async def add_user(
    session: Annotated[
        AsyncSession,
        Depends(db_session.session_getter),
    ],
    user_new: AddUserData = Body(...),
):
    try:
        return await add_user_db(session=session, user_new=user_new)
    except UserDBError as e:
        raise HTTPException(status_code=500, detail="Database error")


@router.put("/update_user", response_model=UpdateUserData, summary="")
async def update_user(
    session: Annotated[
        AsyncSession,
        Depends(db_session.session_getter),
    ],
    user_update: UpdateUserData = Body(...),
):
    try:
        user = await update_user_db(session, user_update)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except UserDBError as e:
        raise HTTPException(status_code=500, detail="Database error")
    
@router.delete("/{user_id}", response_model=DeleteUserData, summary="")
async def delete_user(
    session: Annotated[
        AsyncSession,
        Depends(db_session.session_getter),
    ],
    user_delete: DeleteUserData,
):
    try:
        user = await delete_user_db(session=session, user_id=user_delete.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        else:
            return user
    except UserDBError as e:
        raise HTTPException(status_code=500, detail="Database error")