#!/usr/bin/env python3
"""
Railway MySQL 연결 테스트 스크립트
"""

import os
import sys
from sqlalchemy import create_engine, text

# .env 파일 로드
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ .env 파일 로드됨")
except ImportError:
    print("⚠️  python-dotenv가 설치되지 않음. pip install python-dotenv")
except Exception as e:
    print(f"⚠️  .env 파일 로드 실패: {e}")

def test_railway_connection():
    """Railway MySQL 연결 테스트"""
    
    print("\n=== Railway MySQL 연결 테스트 ===")
    
    # 환경 변수 확인
    mysql_vars = [
        'MYSQL_URL',
        'MYSQLHOST', 
        'MYSQLUSER',
        'MYSQLPASSWORD',
        'MYSQLDATABASE',
        'MYSQLPORT'
    ]
    
    print("\n1. 환경 변수 확인:")
    for var in mysql_vars:
        value = os.getenv(var, 'NOT_SET')
        # 비밀번호는 마스킹
        if 'PASSWORD' in var and value != 'NOT_SET':
            value = value[:3] + '*' * (len(value) - 3)
        print(f"  {var}: {value}")
    
    # MYSQL_URL이 있으면 사용
    mysql_url = os.getenv('MYSQL_URL')
    if mysql_url:
        print(f"\n2. MYSQL_URL 사용: {mysql_url}")
        database_url = mysql_url.replace("mysql://", "mysql+pymysql://")
        print(f"   변환된 URL: {database_url}")
    else:
        # 개별 변수로 구성
        host = os.getenv('MYSQLHOST')
        user = os.getenv('MYSQLUSER')
        password = os.getenv('MYSQLPASSWORD')
        database = os.getenv('MYSQLDATABASE')
        port = os.getenv('MYSQLPORT')
        
        if all([host, user, password, database, port]):
            database_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
            print(f"\n2. 개별 변수로 구성: {database_url}")
        else:
            print("\n❌ MySQL 환경 변수가 부족합니다!")
            return False
    
    # 연결 테스트
    print(f"\n3. Railway MySQL 연결 테스트...")
    try:
        engine = create_engine(database_url, pool_pre_ping=True)
        
        with engine.connect() as conn:
            # 연결 확인
            result = conn.execute(text("SELECT 1"))
            print("✅ Railway MySQL 연결 성공!")
            
            # 현재 데이터베이스 확인
            result = conn.execute(text("SELECT DATABASE()"))
            current_db = result.fetchone()[0]
            print(f"   현재 데이터베이스: {current_db}")
            
            # 테이블 목록 확인
            result = conn.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result.fetchall()]
            print(f"   기존 테이블: {tables}")
            
            return True
            
    except Exception as e:
        print(f"❌ Railway MySQL 연결 실패: {e}")
        return False

if __name__ == "__main__":
    success = test_railway_connection()
    sys.exit(0 if success else 1) 