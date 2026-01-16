from functools import wraps
import logging
from sqlalchemy.exc import SQLAlchemyError
from core.exceptions import DatabaseError

logger_db = logging.getLogger("db")

def db_exception_handler(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except SQLAlchemyError:
            logger_db.exception("Database error")
            raise DatabaseError()
    return wrapper
