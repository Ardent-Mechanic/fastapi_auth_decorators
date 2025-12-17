from functools import wraps
from fastapi import Depends, HTTPException
from crud.user import get_user

def Auth(required_role: str | None = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(
            *args,
            user: dict = Depends(get_user),
            **kwargs
        ):
            if required_role and user["role"] != required_role:
                raise HTTPException(status_code=403)
            return await func(*args, **kwargs)

        return wrapper
    return decorator