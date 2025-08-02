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

# 테스트용 파트너 데이터
test_partner_data = {
    "name": "김철수",
    "mbti": "ENFP",
    "gender": "male",
    "age": 25,
    "relation": "친구",
    "intimacy": 0.8,
    "affection": 0.7,
    "aggression": 0.2,
    "dominance": 0.5,
    "closeness": 8
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

class TestPartnersAPI:
    """파트너 API 테스트 클래스"""
    
    def test_create_partner(self, auth_headers):
        """파트너 생성 테스트"""
        response = client.post(
            "/partners/",
            json=test_partner_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == test_partner_data["name"]
        assert data["mbti"] == test_partner_data["mbti"]
        assert "id" in data
    
    def test_get_partners(self, auth_headers):
        """파트너 목록 조회 테스트"""
        # 먼저 파트너 생성
        client.post(
            "/partners/",
            json=test_partner_data,
            headers=auth_headers
        )
        
        # 파트너 목록 조회
        response = client.get("/partners/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "partners" in data
        assert "total" in data
        assert data["total"] >= 1
        assert len(data["partners"]) >= 1
    
    def test_get_partner_by_id(self, auth_headers):
        """특정 파트너 조회 테스트"""
        # 파트너 생성
        create_response = client.post(
            "/partners/",
            json=test_partner_data,
            headers=auth_headers
        )
        partner_id = create_response.json()["id"]
        
        # 특정 파트너 조회
        response = client.get(f"/partners/{partner_id}", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == partner_id
        assert data["name"] == test_partner_data["name"]
    
    def test_update_partner(self, auth_headers):
        """파트너 정보 업데이트 테스트"""
        # 파트너 생성
        create_response = client.post(
            "/partners/",
            json=test_partner_data,
            headers=auth_headers
        )
        partner_id = create_response.json()["id"]
        
        # 업데이트할 데이터
        update_data = {
            "name": "김영희",
            "mbti": "ISTJ",
            "closeness": 9
        }
        
        # 파트너 정보 업데이트
        response = client.put(
            f"/partners/{partner_id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["mbti"] == update_data["mbti"]
        assert data["closeness"] == update_data["closeness"]
    
    def test_delete_partner(self, auth_headers):
        """파트너 삭제 테스트"""
        # 파트너 생성
        create_response = client.post(
            "/partners/",
            json=test_partner_data,
            headers=auth_headers
        )
        partner_id = create_response.json()["id"]
        
        # 파트너 삭제
        response = client.delete(f"/partners/{partner_id}", headers=auth_headers)
        
        assert response.status_code == 200
        assert response.json()["message"] == "Partner deleted successfully"
        
        # 삭제 확인
        get_response = client.get(f"/partners/{partner_id}", headers=auth_headers)
        assert get_response.status_code == 404
    
    def test_unauthorized_access(self):
        """인증되지 않은 접근 테스트"""
        response = client.get("/partners/")
        assert response.status_code == 401
    
    def test_invalid_partner_id(self, auth_headers):
        """존재하지 않는 파트너 ID 테스트"""
        response = client.get("/partners/999", headers=auth_headers)
        assert response.status_code == 404

if __name__ == "__main__":
    pytest.main([__file__]) 