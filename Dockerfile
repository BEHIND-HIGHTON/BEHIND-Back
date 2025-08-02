FROM python:3.12-slim

WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 시작 스크립트 실행 권한 부여
RUN chmod +x start.sh

# 포트 노출
EXPOSE 8000

# 시작 스크립트 실행
CMD ["./start.sh"] 