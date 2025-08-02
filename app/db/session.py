from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

def get_database_url() -> str:
    """동적으로 데이터베이스 URL 생성"""
    # Railway에서 MYSQL_URL이 제공되면 사용
    if settings.MYSQL_URL:
        return settings.MYSQL_URL.replace("mysql://", "mysql+pymysql://")
    
    # 개별 환경 변수로 구성
    if all([settings.MYSQLHOST, settings.MYSQLUSER, settings.MYSQLPASSWORD, settings.MYSQLDATABASE, settings.MYSQLPORT]):
        return f"mysql+pymysql://{settings.MYSQLUSER}:{settings.MYSQLPASSWORD}@{settings.MYSQLHOST}:{settings.MYSQLPORT}/{settings.MYSQLDATABASE}"
    
    # DATABASE_URL이 직접 설정된 경우
    if settings.DATABASE_URL:
        return settings.DATABASE_URL
    
    # 개발 환경용 SQLite (로컬 테스트용)
    return "sqlite:///./behind.db"

# 데이터베이스 엔진 설정
database_url = get_database_url()
if database_url.startswith("sqlite"):
    # SQLite용 설정 (로컬 개발)
    engine = create_engine(
        database_url, 
        connect_args={"check_same_thread": False},
        pool_pre_ping=True
    )
else:
    # MySQL용 설정 (Railway)
    engine = create_engine(
        database_url,
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