import logging

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import UserDBError
from model.user import User

logger_db = logging.getLogger("db")


async def get_user_by_id_db(
    session: AsyncSession,
    user_id: int,
) -> User | None:
    try:
        stmt = select(User).where(User.user_id == user_id)
        result = await session.scalars(stmt)
        return result.one_or_none()
    except SQLAlchemyError as e:
        logger_db.error(f"DB ERROR WHILE FETCHING USER {user_id}: {e}")
        raise UserDBError(str(e))


async def add_user_db(
    session: AsyncSession,
    user: User,
) -> User:
    try:
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    except SQLAlchemyError as e:
        await session.rollback()
        logger_db.error(f"DB ERROR WHILE ADD USER: {e}")
        raise UserDBError(str(e))


async def update_user_db(
    session: AsyncSession,
    user: User,
) -> User:
    try:
        await session.commit()
        await session.refresh(user)
        return user
    except SQLAlchemyError as e:
        await session.rollback()
        logger_db.error(f"DB ERROR WHILE UPDATE USER {user.user_id}: {e}")
        raise UserDBError(str(e))


async def delete_user_db(
    session: AsyncSession,
    user: User,
) -> User:
    try:
        await session.delete(user)
        await session.commit()
        return user
    except SQLAlchemyError as e:
        await session.rollback()
        logger_db.error(f"DB ERROR WHILE DELETE USER {user.user_id}: {e}")
        raise UserDBError(str(e))
