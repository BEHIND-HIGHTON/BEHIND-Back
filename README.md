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

### 1. 가상환경 생성 및 활성화

```bash
# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate

# 가상환경 활성화 (Windows)
venv\Scripts\activate
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정

```bash
cp env.example .env
```

`.env` 파일을 편집하여 데이터베이스 연결 정보와 기타 설정을 구성하세요.

### 4. 데이터베이스 설정

PostgreSQL 데이터베이스를 생성하고 연결 정보를 `.env` 파일에 설정하세요.

### 5. 데이터베이스 테이블 생성

```bash
# Railway MySQL 터미널에서 직접 테이블 생성
# create_tables.sql 파일의 내용을 실행
```

### 6. 서버 실행

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

## 개발 가이드

### Git Flow 브랜치 전략

이 프로젝트는 Git Flow 브랜치 전략을 따릅니다:

#### 주요 브랜치
- `main`: 프로덕션 배포용 브랜치
- `develop`: 개발 통합 브랜치

#### 보조 브랜치
- `feature/*`: 새로운 기능 개발
- `release/*`: 릴리스 준비
- `hotfix/*`: 긴급 수정

#### 브랜치 사용법

```bash
# 새로운 기능 개발 시작
git checkout develop
git checkout -b feature/user-authentication

# 기능 개발 완료 후 develop에 병합
git checkout develop
git merge feature/user-authentication
git branch -d feature/user-authentication

# 릴리스 준비
git checkout develop
git checkout -b release/v1.0.0

# 릴리스 완료 후 main과 develop에 병합
git checkout main
git merge release/v1.0.0
git tag -a v1.0.0 -m "Release version 1.0.0"
git checkout develop
git merge release/v1.0.0
git branch -d release/v1.0.0

# 긴급 수정
git checkout main
git checkout -b hotfix/critical-bug-fix
# 수정 후 main과 develop에 병합
```

### Conventional Commits

커밋 메시지는 [Conventional Commits](https://www.conventionalcommits.org/) 규칙을 따릅니다:

#### 커밋 타입
- `feat`: 새로운 기능
- `fix`: 버그 수정
- `docs`: 문서 변경
- `style`: 코드 포맷팅, 세미콜론 누락 등
- `refactor`: 코드 리팩토링
- `test`: 테스트 추가 또는 수정
- `chore`: 빌드 프로세스 또는 보조 도구 변경

#### 커밋 메시지 형식
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

#### 예시
```bash
feat(auth): 사용자 로그인 기능 추가

- JWT 토큰 기반 인증 구현
- 비밀번호 해싱 기능 추가

Closes #123

fix(api): 사용자 조회 API 응답 오류 수정

docs: README 파일 업데이트

style: 코드 포맷팅 적용

refactor(user): 사용자 모델 리팩토링

test: 사용자 인증 테스트 추가

chore: 의존성 패키지 업데이트
```

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
├── main.py
├── requirements.txt
├── Dockerfile
├── start.sh
├── create_tables.sql
└── README.md
```

## 테스트

```bash
pytest
```

## 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다. 