from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 데이터베이스 엔진 설정
if settings.DATABASE_URL.startswith("sqlite"):
    # SQLite용 설정 (로컬 개발)
    engine = create_engine(
        settings.DATABASE_URL, 
        connect_args={"check_same_thread": False},
        pool_pre_ping=True
    )
else:
    # MySQL용 설정 (Railway)
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=3600,  # 연결 재사용 시간 (1시간)
        pool_size=10,       # 연결 풀 크기
        max_overflow=20     # 최대 추가 연결 수
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 