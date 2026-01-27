from core.exceptions.base import ApiException


class NotFoundError(ApiException):
    __slots__ = ()

    def __init__(self, **kwargs):
        super().__init__(status_code=404, detail="Resource not found", error_code="NOT_FOUND", **kwargs)

class UserAlreadyExistsError(ApiException):
    __slots__ = ()
    def __init__(self, **kwargs):
        super().__init__(status_code=409, detail="User already exists", error_code="USER_EXISTS", **kwargs)

class ValidationError(ApiException):
    __slots__ = ()
    def __init__(self, **kwargs):
        super().__init__(status_code=422, detail="Validation failed", error_code="VALIDATION_ERROR", **kwargs)

class DatabaseError(ApiException):
    __slots__ = ()
    def __init__(self, **kwargs):
        super().__init__(status_code=500, detail="Database operation failed", error_code="DATABASE_ERROR", **kwargs)

class UnauthorizedError(ApiException):
    __slots__ = ()
    def __init__(self, **kwargs):
        super().__init__(status_code=401, detail="Unauthorized access", error_code="UNAUTHORIZED", **kwargs)