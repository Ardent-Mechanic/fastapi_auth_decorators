from fastapi import APIRouter

from .user import router as user_router
from .auth import router as auth_router
from app.core.config import settings

router = APIRouter()  # Можно добавить общий тег или prefix, если нужно

# Собираем все public роутеры

router.include_router(user_router, prefix=settings.api.v1.user)
router.include_router(auth_router, prefix=settings.api.v1.auth)
