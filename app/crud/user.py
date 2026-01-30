from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.decorators.exceptions_decorator import db_exception_handler
from app.model.user import User


@db_exception_handler
async def get_user_by_id_db(
    session: AsyncSession,
    user_id: int,
) -> User | None:
    stmt = select(User).where(User.user_id == user_id)
    result = await session.scalars(stmt)
    return result.one_or_none()


@db_exception_handler
async def get_user_by_email_db(
    session: AsyncSession,
    email: str,
) -> User | None:
    stmt = select(User).where(User.email == email)
    result = await session.scalars(stmt)
    return result.one_or_none()


@db_exception_handler
async def add_user_db(
    session: AsyncSession,
    user: User,
) -> User:
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@db_exception_handler
async def update_user_db(
    session: AsyncSession,
    user: User,
) -> User:
    await session.commit()
    await session.refresh(user)
    return user


@db_exception_handler
async def delete_user_db(
    session: AsyncSession,
    user: User,
) -> User:
    await session.delete(user)
    await session.commit()
    return user
