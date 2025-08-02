# Railway 배포 가이드

## 1. 프로젝트 설정

### 1.1 Railway 프로젝트 생성
- [Railway](https://railway.app/)에서 새 프로젝트 생성
- GitHub 저장소 연결

### 1.2 MySQL 서비스 추가
- **중요**: MySQL 서비스를 먼저 추가해야 합니다!
- "New Service" → "Database" → "MySQL" 선택
- 서비스 이름: `behind-mysql` (선택사항)

## 2. 환경 변수 설정

### 2.1 MySQL 환경 변수 (자동 설정)
Railway가 자동으로 다음 환경 변수를 설정합니다:
```
MYSQL_URL=mysql://root:password@host:port/railway
MYSQL_DATABASE=railway
MYSQL_PUBLIC_URL=mysql://host:port
MYSQL_ROOT_PASSWORD=root_password
MYSQLDATABASE=railway
MYSQLHOST=host
MYSQLPASSWORD=password
MYSQLPORT=port
MYSQLUSER=username
```

**중요**: Railway MySQL의 기본 데이터베이스 이름은 `railway`입니다!

### 2.2 애플리케이션 환경 변수
애플리케이션 서비스에 다음 환경 변수를 추가:

```
# JWT 설정
SECRET_KEY=your-secret-key-here-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS 설정
BACKEND_CORS_ORIGINS=["http://localhost:3000","https://your-frontend-domain.com"]

# 환경 설정
ENVIRONMENT=production
DEBUG=false
```

## 3. 배포 설정

### 3.1 Dockerfile 설정
- 프로젝트 루트에 `Dockerfile` 존재 확인
- `start.sh` 스크립트가 자동으로 데이터베이스 연결 확인

### 3.2 직접 테이블 생성 (MySQL 터미널에서)
Railway MySQL 서비스의 터미널에서 직접 테이블을 생성:

```sql
-- 사용자 테이블
CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 아이템 테이블
CREATE TABLE IF NOT EXISTS item (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    owner_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES user(id)
);

-- 파트너 테이블
CREATE TABLE IF NOT EXISTS partner (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    user_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- 받은 메시지 테이블
CREATE TABLE IF NOT EXISTS receivedmessage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT NOT NULL,
    sender_id INT,
    receiver_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES user(id),
    FOREIGN KEY (receiver_id) REFERENCES user(id)
);

-- 보낸 메시지 테이블
CREATE TABLE IF NOT EXISTS sentmessage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT NOT NULL,
    sender_id INT,
    receiver_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES user(id),
    FOREIGN KEY (receiver_id) REFERENCES user(id)
);
```

## 4. 배포 후 확인

### 4.1 배포 상태 확인
- **"Deployments"** 탭에서 배포 상태 확인
- 로그에서 "MySQL connection successful!" 메시지 확인

### 4.2 테이블 생성 확인
```sql
-- Railway MySQL 터미널에서
SHOW TABLES;
DESCRIBE user;
DESCRIBE item;
DESCRIBE partner;
DESCRIBE receivedmessage;
DESCRIBE sentmessage;
```

### 4.3 API 테스트
```bash
# 헬스 체크
curl https://your-app-url.railway.app/health

# API 문서
curl https://your-app-url.railway.app/docs
```

## 5. 문제 해결

### 5.1 MySQL 연결 실패
- MySQL 서비스가 실행 중인지 확인
- 환경 변수가 올바르게 설정되었는지 확인
- Railway 대시보드에서 MySQL 서비스 상태 확인

### 5.2 테이블이 없는 경우
- Railway MySQL 터미널에서 위의 SQL 스크립트 실행
- 테이블 생성 후 애플리케이션 재시작

### 5.3 권한 문제
- MySQL 사용자에게 적절한 권한 부여:
```sql
GRANT ALL PRIVILEGES ON database_name.* TO 'username'@'%';
FLUSH PRIVILEGES;
```

## 6. 모니터링 및 업데이트

### 6.1 로그 모니터링
- Railway 대시보드에서 실시간 로그 확인
- 에러 발생 시 즉시 확인

### 6.2 업데이트
- 코드 변경 시 자동 재배포
- 데이터베이스 스키마 변경 시 수동으로 SQL 실행

## 7. 중요 사항

⚠️ **주의사항:**
- MySQL 서비스가 먼저 배포되어야 애플리케이션이 정상 작동
- 테이블은 Railway MySQL 터미널에서 직접 생성
- 코드 기반 테이블 생성은 사용하지 않음
- 데이터베이스 백업은 Railway에서 자동으로 제공
- 배포 환경에서는 DEBUG=false로 설정됨
- SECRET_KEY는 반드시 안전한 값으로 변경

## 8. 최종 배포 체크리스트

- [ ] MySQL 서비스 추가 및 실행
- [ ] 환경 변수 설정 (SECRET_KEY, ENVIRONMENT=production, DEBUG=false)
- [ ] 테이블 생성 (MySQL 터미널에서)
- [ ] 애플리케이션 서비스 배포
- [ ] 헬스 체크 통과 확인
- [ ] API 테스트 (회원가입/로그인/로그아웃)
- [ ] 로그 모니터링 설정 