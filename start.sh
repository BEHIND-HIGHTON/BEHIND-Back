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

# 직접 테이블 생성
echo "Creating database tables directly..."
python -c "
import sys
from sqlalchemy import create_engine, text
from app.db.session import get_database_url
from app.db.base import Base

try:
    engine = create_engine(get_database_url())
    
    # 테이블 생성
    Base.metadata.create_all(bind=engine)
    print('Database tables created successfully!')
    
    # 테이블 확인
    with engine.connect() as conn:
        result = conn.execute(text(\"\"\"
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = DATABASE()
        \"\"\"))
        tables = [row[0] for row in result]
        print(f'Created tables: {tables}')
    
except Exception as e:
    print(f'Error creating tables: {e}')
    sys.exit(1)
"

# 애플리케이션 시작
echo "Starting application..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 