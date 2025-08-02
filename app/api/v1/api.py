from fastapi import APIRouter
from app.api.v1.endpoints import users, auth, items, partners, messages

api_router = APIRouter()

# 각 엔드포인트 라우터 등록
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(partners.router, prefix="/partners", tags=["partners"])
api_router.include_router(messages.router, prefix="/messages", tags=["messages"]) 