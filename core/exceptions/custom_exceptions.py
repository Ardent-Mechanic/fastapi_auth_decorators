from exceptions.base import ApiException


class NotFoundError(ApiException):
    __slots__ = ()
    status_code = 404
    detail = "Resource not found"
    error_code = "NOT_FOUND"

class UserAlreadyExistsError(ApiException):
    __slots__ = ()
    status_code = 409
    detail = "User already exists"
    error_code = "USER_EXISTS"

class ValidationError(ApiException):
    __slots__ = ()
    status_code = 422
    detail = "Validation failed"
    error_code = "VALIDATION_ERROR"

class DatabaseError(ApiException):
    __slots__ = ()
    status_code = 500
    detail = "Database operation failed"
    error_code = "DATABASE_ERROR"
