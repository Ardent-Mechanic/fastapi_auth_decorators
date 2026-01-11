import logging

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import UserDBError
from model.user import User
from schemas.user import AddUserData, UpdateUserData

# from utils import convert_to_date
from utils.password_hasher import hash_password

# import logging.config

# logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

logger_db = logging.getLogger("db")
logger_main = logging.getLogger("main")


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
    user_new: AddUserData,
) -> User:
    try:
        user_db = User(
            email=user_new.email,
            hashed_password=hash_password(user_new.password),
            is_active=user_new.is_active,
            is_superuser=user_new.is_superuser,
        )
        session.add(user_db)
        await session.commit()
        await session.refresh(user_db)
        return user_db
    except SQLAlchemyError as e:
        await session.rollback()
        logger_db.error(f"DB ERROR WHILE ADD USER: {e}")
        raise UserDBError(str(e))


async def update_user_db(
    session: AsyncSession,
    user_update: UpdateUserData,
) -> User | None:
    try:
        user_db = await get_user_by_id_db(session, user_update.user_id)

        if not user_db:
            return None

        update_data = user_update.model_dump(
            exclude_unset=True,
            exclude={"user_id", "created_at"},
        )

        for field, value in update_data.items():
            if field == "password":
                value = hash_password(value)
            setattr(user_db, field, value)

        await session.commit()
        await session.refresh(user_db)
        return user_db

    except SQLAlchemyError as e:
        await session.rollback()
        logger_db.error(f"DB ERROR WHILE UPDATE USER {user_update.user_id}: {e}")
        raise UserDBError(str(e))


async def delete_user_db(
    session: AsyncSession,
    user_id: int,
) -> User | None:
    try:
        user_db = await get_user_by_id_db(session, user_id)

        if not user_db:
            return None

        await session.delete(user_db)
        await session.commit()
        return user_db
    except SQLAlchemyError as e:
        await session.rollback()
        logger_db.error(f"DB ERROR WHILE DELETE USER {user_id}: {e}")
        raise UserDBError(str(e))
