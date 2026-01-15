from typing import Any, Optional


class ApiException(Exception):
    __slots__ = ("status_code", "detail", "headers", "error_code", "data")
    
    status_code: int = 500
    detail: str = "Internal server error"
    headers: Optional[dict[str, Any]] = None
    error_code: Optional[str] = None
    data: Optional[dict[str, Any]] = None

    def __init__(self, **kwargs: Any):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        super().__init__(self.detail)

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}(status_code={self.status_code}, "
            f"detail={self.detail}, error_code={self.error_code})"
        )

    def to_dict(self) -> dict[str, Any]:
        response = {"detail": self.detail}  # было "respose"
        if self.error_code:
            response["error_code"] = self.error_code
        if self.data:
            response["data"] = self.data
        return response
