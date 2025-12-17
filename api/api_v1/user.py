from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession

from crud.user import get_user, add_user, put_user, delete_user
from db import db_session

from schemas import GetUserData, AddUserData, PutUserData, DeleteUserData

router = APIRouter(tags=["User"])