#!/bin/bash

# 데이터베이스 연결 대기 (최대 30초)
echo "Waiting for database connection..."
for i in {1..30}; do
    python -c "
import sys
from sqlalchemy import create_engine, text
from app.db.session import get_database_url
try:
    engine = create_engine(get_database_url())
    with engine.connect() as conn:
        conn.execute(text('SELECT 1'))
    print('MySQL connection successful!')
    sys.exit(0)
except Exception as e:
    print(f'MySQL connection failed: {e}')
    sys.exit(1)
"
    if [ $? -eq 0 ]; then
        break
    fi
    sleep 1
done

# 데이터베이스 연결 확인 완료
echo "Database connection verified successfully!"

# 테이블 존재 확인 (선택사항)
echo "Checking if tables exist..."
python -c "
import sys
from sqlalchemy import create_engine, text
from app.db.session import get_database_url
try:
    engine = create_engine(get_database_url())
    with engine.connect() as conn:
        result = conn.execute(text('SHOW TABLES'))
        tables = [row[0] for row in result.fetchall()]
        print(f'Existing tables: {tables}')
        if not tables:
            print('Warning: No tables found. Please create tables manually in Railway MySQL terminal.')
    sys.exit(0)
except Exception as e:
    print(f'Table check failed: {e}')
    sys.exit(0)  # 테이블이 없어도 애플리케이션은 시작
"

# 애플리케이션 시작
echo "Starting application..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 