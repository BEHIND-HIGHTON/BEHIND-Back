from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.config import settings
from app.crud.user import user_crud
from app.schemas.user import User
from app.db.session import get_db

# JWT 인증 제거 - 파트너 및 메시지 API에서 자유롭게 사용 가능
async def get_current_user(
    db: Session = Depends(get_db)
) -> User:
    """인증 없이 기본 사용자 반환 (파트너 및 메시지 API 자유 사용을 위해)"""
    # 기본 사용자 ID 1을 반환하거나, 첫 번째 사용자를 반환
    user = user_crud.get(db, id=1)
    if user is None:
        # 사용자가 없으면 기본 사용자 생성
        from app.schemas.user import UserCreate
        user_data = UserCreate(
            email="default@example.com",
            password="default123",
            full_name="Default User"
        )
        user = user_crud.create(db, obj_in=user_data)
    return user 