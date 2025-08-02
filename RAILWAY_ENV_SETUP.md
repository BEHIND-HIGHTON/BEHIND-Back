# Railway 환경 변수 로컬 설정 가이드

## 1. Railway MySQL 환경 변수 확인

### 1.1 Railway 대시보드에서 환경 변수 확인
1. Railway 대시보드 접속
2. 프로젝트 선택
3. MySQL 서비스 클릭
4. **"Variables"** 탭 클릭
5. 다음 환경 변수들을 복사:
   - `MYSQL_URL`
   - `MYSQLHOST`
   - `MYSQLUSER`
   - `MYSQLPASSWORD`
   - `MYSQLDATABASE`
   - `MYSQLPORT`

### 1.2 환경 변수 예시
```
MYSQL_URL=mysql://root:password@host.railway.internal:port/railway
MYSQLHOST=host.railway.internal
MYSQLUSER=root
MYSQLPASSWORD=password
MYSQLDATABASE=railway
MYSQLPORT=port
```

## 2. 로컬 환경 변수 설정

### 2.1 방법 1: 터미널에서 직접 설정
```bash
# Railway 환경 변수 설정
export MYSQL_URL="mysql://root:password@host.railway.internal:port/railway"
export MYSQLHOST="host.railway.internal"
export MYSQLUSER="root"
export MYSQLPASSWORD="password"
export MYSQLDATABASE="railway"
export MYSQLPORT="port"

# 테스트 실행
python test_railway_connection.py
```

### 2.2 방법 2: .env 파일 생성
```bash
# .env 파일 생성
cat > .env << EOF
# Railway MySQL 환경 변수
MYSQL_URL=mysql://root:password@host.railway.internal:port/railway
MYSQLHOST=host.railway.internal
MYSQLUSER=root
MYSQLPASSWORD=password
MYSQLDATABASE=railway
MYSQLPORT=port

# 기타 설정
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENVIRONMENT=development
DEBUG=true
EOF

# 환경 변수 로드
source .env

# 테스트 실행
python test_railway_connection.py
```

### 2.3 방법 3: python-dotenv 사용
```bash
# python-dotenv 설치
pip install python-dotenv

# .env 파일 생성 (위와 동일)
# test_railway_connection.py에서 자동으로 .env 파일 로드
python test_railway_connection.py
```

## 3. 연결 테스트

### 3.1 기본 연결 테스트
```bash
python test_railway_connection.py
```

### 3.2 애플리케이션 테스트
```bash
# 환경 변수 설정 후
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 4. 문제 해결

### 4.1 연결 실패 시
- Railway MySQL 서비스가 실행 중인지 확인
- 환경 변수가 올바르게 설정되었는지 확인
- 네트워크 연결 상태 확인
- 방화벽 설정 확인

### 4.2 환경 변수 확인
```bash
# 환경 변수 확인
env | grep MYSQL
env | grep DATABASE
```

### 4.3 Railway 상태 확인
- Railway 대시보드에서 MySQL 서비스 상태 확인
- 로그에서 에러 메시지 확인

## 5. 보안 주의사항

⚠️ **중요**: 
- `.env` 파일은 `.gitignore`에 포함되어야 함
- 실제 비밀번호는 안전하게 관리
- 프로덕션 환경에서는 환경 변수 직접 설정 권장 