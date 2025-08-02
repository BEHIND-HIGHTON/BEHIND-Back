from sqlalchemy.orm import Session
from app.crud.user import user_crud
from app.schemas.user import UserCreate
from app.core.config import settings
from app.db import base


def init_db(db: Session) -> None:
    """데이터베이스 초기화"""
    # 테이블 생성
    base.Base.metadata.create_all(bind=db)
    
    # 관리자 사용자 생성
    user = user_crud.get_by_email(db, email="admin@example.com")
    if not user:
        user_in = UserCreate(
            email="admin@example.com",
            password="admin123",
            is_superuser=True,
            full_name="관리자"
        )
        user = user_crud.create(db, obj_in=user_in) 