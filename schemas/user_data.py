from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False

class AddUserData(UserBase):
    password: str = Field(min_length=8, max_length=128)
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "strongpassword",
                "is_active": True,
                "is_superuser": False
            }
        }

class PutUserData(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(default=None, min_length=8)
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None

class GetUserData(BaseModel):
    user_id: int
    email: EmailStr
    is_active: bool
    is_superuser: bool
    created_at: datetime

    class Config:
        from_attributes = True 

class DeleteUserData(BaseModel):
    user_id: int