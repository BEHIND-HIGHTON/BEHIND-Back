# Railway 배포 가이드

## 1. Railway 프로젝트 설정

### 1.1 새 프로젝트 생성
1. Railway 대시보드에서 **"New Project"** 클릭
2. **"Deploy from GitHub repo"** 선택
3. GitHub 저장소 연결

### 1.2 MySQL 서비스 추가
1. 프로젝트에서 **"New Service"** 클릭
2. **"Database"** → **"MySQL"** 선택
3. MySQL 서비스가 자동으로 생성됨
4. **중요**: MySQL 서비스가 애플리케이션 서비스보다 먼저 배포되도록 설정

## 2. 환경 변수 설정

**중요**: 이 애플리케이션은 MySQL을 필수로 사용합니다. SQLite fallback이 없습니다.

Railway 대시보드에서 다음 환경 변수들을 설정:

### 필수 환경 변수
```bash
# JWT 설정
SECRET_KEY=your-super-secure-secret-key-here

# 환경 설정
ENVIRONMENT=production
DEBUG=false

# 마이그레이션 설정 (선택사항)
AUTO_MIGRATE=true
```

### 자동 설정되는 MySQL 환경 변수
Railway가 자동으로 설정하는 변수들:
- `MYSQL_URL`
- `MYSQL_DATABASE`
- `MYSQL_PUBLIC_URL`
- `MYSQL_ROOT_PASSWORD`
- `MYSQLDATABASE`
- `MYSQLHOST`
- `MYSQLPASSWORD`
- `MYSQLPORT`
- `MYSQLUSER`

## 3. 배포 설정

### 3.1 Dockerfile 사용 (권장)
- 프로젝트에 `Dockerfile`이 있으면 자동으로 사용됨
- `start.sh` 스크립트가 자동으로 마이그레이션 실행

### 3.2 직접 테이블 생성
- 배포 시 자동으로 모든 테이블이 생성됨
- 마이그레이션 없이 SQLAlchemy 모델 기반으로 테이블 생성

## 4. 배포 후 확인

### 4.1 배포 상태 확인
- Railway 대시보드에서 배포 로그 확인
- **"Deployments"** 탭에서 배포 상태 확인

### 4.2 테이블 생성 확인
```bash
# Railway 터미널에서 (필요시)
python -c "
from app.db.session import get_database_url
from app.db.base import Base
from sqlalchemy import create_engine
engine = create_engine(get_database_url())
Base.metadata.create_all(bind=engine)
print('Tables created successfully!')
"
```

### 4.3 API 테스트
```bash
# 헬스 체크
curl https://your-app.railway.app/health

# API 문서
https://your-app.railway.app/docs
```

## 5. 문제 해결

### 5.1 배포 실패
1. **로그 확인**: Railway 대시보드 → Deployments → View Logs
2. **환경 변수 확인**: 모든 필수 변수가 설정되었는지 확인
3. **MySQL 연결 확인**: MySQL 서비스가 실행 중인지 확인

### 5.2 마이그레이션 실패
1. **데이터베이스 연결 확인**
2. **수동 마이그레이션 실행**
3. **마이그레이션 파일 확인**

### 5.3 API 응답 없음
1. **애플리케이션 로그 확인**
2. **포트 설정 확인**
3. **환경 변수 확인**

## 6. 모니터링

### 6.1 로그 확인
- Railway 대시보드 → **"Deployments"** → **"View Logs"**

### 6.2 메트릭 확인
- Railway 대시보드 → **"Metrics"** 탭

### 6.3 알림 설정
- Railway 대시보드 → **"Settings"** → **"Notifications"**

## 7. 업데이트 배포

### 7.1 자동 배포
- GitHub에 push하면 자동으로 배포됨

### 7.2 수동 배포
- Railway 대시보드 → **"Deployments"** → **"Deploy Now"**

## 8. 롤백

### 8.1 이전 버전으로 롤백
- Railway 대시보드 → **"Deployments"** → 이전 배포 선택 → **"Redeploy"** 