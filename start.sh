#!/bin/bash

# 데이터베이스 연결 대기 (최대 30초)
echo "Waiting for database connection..."
for i in {1..30}; do
    python -c "
import sys
from sqlalchemy import create_engine, text
from app.core.config import settings
try:
    engine = create_engine(settings.DATABASE_URL)
    with engine.connect() as conn:
        conn.execute(text('SELECT 1'))
    print('Database connection successful!')
    sys.exit(0)
except Exception as e:
    print(f'Database connection failed: {e}')
    sys.exit(1)
"
    if [ $? -eq 0 ]; then
        break
    fi
    sleep 1
done

# 환경 변수로 마이그레이션 제어
if [ "$AUTO_MIGRATE" = "true" ]; then
    echo "Running database migrations..."
    alembic upgrade head
else
    echo "Skipping automatic migrations (AUTO_MIGRATE=false)"
fi

# 애플리케이션 시작
echo "Starting application..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 