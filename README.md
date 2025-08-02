# BEHIND Backend

FastAPI 기반의 BEHIND 프로젝트 백엔드 API입니다.

## 기능

- 사용자 인증 (JWT)
- 사용자 관리
- 아이템 관리
- PostgreSQL 데이터베이스
- Redis 캐싱
- Celery 비동기 작업

## 설치 및 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

```bash
cp env.example .env
```

`.env` 파일을 편집하여 데이터베이스 연결 정보와 기타 설정을 구성하세요.

### 3. 데이터베이스 설정

PostgreSQL 데이터베이스를 생성하고 연결 정보를 `.env` 파일에 설정하세요.

### 4. 데이터베이스 마이그레이션

```bash
# Alembic 초기화 (최초 1회만)
alembic init alembic

# 마이그레이션 생성
alembic revision --autogenerate -m "Initial migration"

# 마이그레이션 실행
alembic upgrade head
```

### 5. 서버 실행

```bash
# 개발 모드
uvicorn main:app --reload

# 프로덕션 모드
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API 문서

서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 프로젝트 구조

```
BEHIND-Back/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py
│   │       │   ├── users.py
│   │       │   └── items.py
│   │       └── api.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── crud/
│   │   ├── base.py
│   │   ├── user.py
│   │   └── item.py
│   ├── db/
│   │   ├── base.py
│   │   ├── base_class.py
│   │   ├── init_db.py
│   │   └── session.py
│   ├── models/
│   │   ├── user.py
│   │   └── item.py
│   └── schemas/
│       ├── auth.py
│       ├── user.py
│       └── item.py
├── alembic/
├── main.py
├── requirements.txt
├── alembic.ini
└── README.md
```

## 테스트

```bash
pytest
```

## 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다. 