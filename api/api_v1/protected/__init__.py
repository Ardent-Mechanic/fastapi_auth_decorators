from fastapi import APIRouter, Depends
from api.api_v1.dependencies.guards import auth_guard

from .user import router as user_router
from core.config import settings

router = APIRouter(dependencies=[Depends(auth_guard)])  # guard на весь protected роутер

# Собираем все protected роутеры
router.include_router(user_router, prefix=settings.api.v1.user)
