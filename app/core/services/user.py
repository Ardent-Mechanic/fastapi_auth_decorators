from app.core.exceptions.custom_exceptions import NotFoundError, UserAlreadyExistsError
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.user import (
    add_user_db,
    delete_user_db,
    get_user_by_email_db,
    get_user_by_id_db,
    update_user_db,
)
from app.model.user import User
from app.schemas.user import AddUserData, UpdateUserData
from app.core.security.password_hasher import hash_password


async def get_user_by_id_service(
    session: AsyncSession,
    user_id: int,
) -> User:
    user = await get_user_by_id_db(session, user_id)
    if not user:
        raise NotFoundError()
    return user


async def add_user_service(
    session: AsyncSession,
    user_new: AddUserData,
) -> User:
    user = User(
        email=user_new.email,
        hashed_password=hash_password(user_new.password),
        is_active=user_new.is_active,
        is_superuser=user_new.is_superuser,
    )
    user_in_db = await get_user_by_email_db(session, email=user_new.email)
    if user_in_db:
        raise UserAlreadyExistsError()
    return await add_user_db(session, user)


async def update_user_service(
    session: AsyncSession,
    user_update: UpdateUserData,
) -> User:
    user = await get_user_by_id_db(session, user_update.user_id)
    if not user:
        raise NotFoundError()

    update_data = user_update.model_dump(
        exclude_unset=True,
        exclude={"user_id", "created_at"},
    )

    for field, value in update_data.items():
        if field == "password":
            value = hash_password(value)
            field = "hashed_password"
        setattr(user, field, value)

    return await update_user_db(session, user)


async def delete_user_service(
    session: AsyncSession,
    user_id: int,
) -> User:
    user = await get_user_by_id_db(session, user_id)
    if not user:
        raise NotFoundError()

    return await delete_user_db(session, user)
