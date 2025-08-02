import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.base import Base
from app.core.config import settings
from app.api.deps import get_db
from app.models.user import User
from app.core.security import get_password_hash
from datetime import datetime

# 테스트용 데이터베이스 설정
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 테스트용 데이터베이스 생성
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# 테스트용 사용자 데이터
test_user_data = {
    "email": "test@example.com",
    "password": "testpassword123",
    "full_name": "테스트 사용자"
}

# 테스트용 채팅 데이터
test_chat_data = {
    "user_id": 1,
    "partner_name": "김현호",
    "messages": [
        {
            "content": "안녕하세요! 오늘 날씨가 정말 좋네요.",
            "timestamp": "2025-01-15T10:00:00Z",
            "type": "user"
        },
        {
            "content": "네, 맞습니다! 산책하기 좋은 날씨예요.",
            "timestamp": "2025-01-15T10:01:00Z",
            "type": "ai"
        },
        {
            "content": "같이 산책하실래요?",
            "timestamp": "2025-01-15T10:02:00Z",
            "type": "user"
        }
    ]
}

@pytest.fixture
def test_user():
    """테스트용 사용자를 생성하고 반환합니다."""
    db = TestingSessionLocal()
    
    # 기존 사용자 삭제
    db.query(User).filter(User.email == test_user_data["email"]).delete()
    db.commit()
    
    # 새 사용자 생성
    hashed_password = get_password_hash(test_user_data["password"])
    user = User(
        email=test_user_data["email"],
        hashed_password=hashed_password,
        full_name=test_user_data["full_name"],
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    yield user
    
    # 정리
    db.delete(user)
    db.commit()
    db.close()

@pytest.fixture
def auth_headers(test_user):
    """인증 헤더를 생성합니다."""
    # 로그인
    login_response = client.post("/auth/login", data={
        "username": test_user_data["email"],
        "password": test_user_data["password"]
    })
    
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

class TestMessagesAPI:
    """메시지 API 테스트 클래스"""
    
    def test_get_chat_history(self, auth_headers, test_user):
        """채팅 기록 조회 테스트"""
        response = client.get(f"/messages/{test_user.id}", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "messages" in data
        assert isinstance(data["messages"], list)
        
        # 채팅 기록이 있으면 구조 확인
        if len(data["messages"]) > 0:
            message = data["messages"][0]
            assert "id" in message
            assert "name" in message  # 파트너 이름 포함
            assert "chat_file" in message
            assert "user_id" in message
            assert "created_at" in message
            assert "updated_at" in message
            assert isinstance(message["chat_file"], list)
    
    def test_update_chat_history(self, auth_headers, test_user):
        """채팅 기록 업데이트 테스트"""
        # user_id를 실제 사용자 ID로 설정
        chat_update_data = test_chat_data.copy()
        chat_update_data["user_id"] = test_user.id
        
        response = client.post(
            "/messages/update",
            json=chat_update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "message" in data
        assert data["updated_count"] == len(test_chat_data["messages"])
    
    def test_update_chat_history_with_new_partner(self, auth_headers, test_user):
        """새로운 파트너와의 채팅 기록 업데이트 테스트"""
        new_chat_data = {
            "user_id": test_user.id,
            "partner_name": "새로운파트너",
            "messages": [
                {
                    "content": "처음 뵙겠습니다!",
                    "timestamp": "2025-01-15T11:00:00Z",
                    "type": "user"
                }
            ]
        }
        
        response = client.post(
            "/messages/update",
            json=new_chat_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["updated_count"] == 1
    
    def test_unauthorized_access(self):
        """인증되지 않은 접근 테스트"""
        response = client.get("/messages/1")
        assert response.status_code == 401
    
    def test_access_other_user_chat(self, auth_headers, test_user):
        """다른 사용자의 채팅 기록 접근 테스트"""
        other_user_id = test_user.id + 999  # 다른 사용자 ID
        
        response = client.get(f"/messages/{other_user_id}", headers=auth_headers)
        assert response.status_code == 403
    
    def test_update_other_user_chat(self, auth_headers, test_user):
        """다른 사용자의 채팅 기록 업데이트 테스트"""
        other_user_id = test_user.id + 999  # 다른 사용자 ID
        
        chat_update_data = test_chat_data.copy()
        chat_update_data["user_id"] = other_user_id
        
        response = client.post(
            "/messages/update",
            json=chat_update_data,
            headers=auth_headers
        )
        assert response.status_code == 403
    
    def test_invalid_chat_data(self, auth_headers, test_user):
        """잘못된 채팅 데이터 테스트"""
        invalid_chat_data = {
            "user_id": test_user.id,
            "partner_name": "",  # 빈 이름
            "messages": []  # 빈 메시지
        }
        
        response = client.post(
            "/messages/update",
            json=invalid_chat_data,
            headers=auth_headers
        )
        
        # 빈 데이터라도 성공해야 함 (검증 로직에 따라 다를 수 있음)
        assert response.status_code in [200, 422]
    
    def test_chat_history_after_update(self, auth_headers, test_user):
        """업데이트 후 채팅 기록 조회 테스트"""
        # 먼저 채팅 기록 업데이트
        chat_update_data = test_chat_data.copy()
        chat_update_data["user_id"] = test_user.id
        
        update_response = client.post(
            "/messages/update",
            json=chat_update_data,
            headers=auth_headers
        )
        assert update_response.status_code == 200
        
        # 업데이트 후 채팅 기록 조회
        get_response = client.get(f"/messages/{test_user.id}", headers=auth_headers)
        assert get_response.status_code == 200
        
        # 업데이트된 데이터가 반환되는지 확인
        data = get_response.json()
        assert "messages" in data
        assert len(data["messages"]) > 0
        
        # 첫 번째 메시지의 구조 확인
        message = data["messages"][0]
        assert "id" in message
        assert "name" in message  # 파트너 이름 포함
        assert "chat_file" in message
        assert "user_id" in message
        assert message["user_id"] == test_user.id

if __name__ == "__main__":
    pytest.main([__file__]) 