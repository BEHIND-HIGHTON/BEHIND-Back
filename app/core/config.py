from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "BEHIND Backend"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "BEHIND 프로젝트 백엔드 API"
    API_V1_STR: str = "/api/v1"
    
    # CORS 설정
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Railway MySQL 환경 변수
    MYSQL_URL: str = ""
    MYSQL_DATABASE: str = ""
    MYSQL_PUBLIC_URL: str = ""
    MYSQL_ROOT_PASSWORD: str = ""
    MYSQLDATABASE: str = ""
    MYSQLHOST: str = ""
    MYSQLPASSWORD: str = ""
    MYSQLPORT: str = ""
    MYSQLUSER: str = ""
    
    # 데이터베이스 URL 생성
    @property
    def DATABASE_URL(self) -> str:
        # Railway에서 MYSQL_URL이 제공되면 사용
        if self.MYSQL_URL:
            return self.MYSQL_URL.replace("mysql://", "mysql+pymysql://")
        
        # 개별 환경 변수로 구성
        if all([self.MYSQLHOST, self.MYSQLUSER, self.MYSQLPASSWORD, self.MYSQLDATABASE, self.MYSQLPORT]):
            return f"mysql+pymysql://{self.MYSQLUSER}:{self.MYSQLPASSWORD}@{self.MYSQLHOST}:{self.MYSQLPORT}/{self.MYSQLDATABASE}"
        
        # 개발 환경용 SQLite
        return "sqlite:///./behind.db"
    
    # Redis 설정
    REDIS_URL: str = "redis://localhost:6379"
    
    # JWT 설정
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 환경 설정
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # 마이그레이션 설정
    AUTO_MIGRATE: bool = False  # Railway에서는 False로 설정
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings() 