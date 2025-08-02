#!/usr/bin/env python3
"""
BEHIND 인증 API 테스트 스크립트
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_register():
    """회원가입 테스트"""
    print("=== 회원가입 테스트 ===")
    
    # 타임스탬프를 사용하여 고유한 이메일 생성
    timestamp = int(time.time())
    email = f"test{timestamp}@example.com"
    
    register_data = {
        "email": email,
        "password": "password123",
        "full_name": "테스트 사용자"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print(f"Status Code: {response.status_code}")
    
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response Text: {response.text}")
    print()
    
    if response.status_code == 200:
        return email
    return None

def test_login(email):
    """로그인 테스트"""
    print("=== 로그인 테스트 ===")
    
    login_data = {
        "email": email,
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Status Code: {response.status_code}")
    
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response Text: {response.text}")
    print()
    
    if response.status_code == 200:
        try:
            return response.json().get("access_token")
        except:
            return None
    return None

def test_logout(token):
    """로그아웃 테스트"""
    print("=== 로그아웃 테스트 ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/auth/logout", headers=headers)
    print(f"Status Code: {response.status_code}")
    
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response Text: {response.text}")
    print()
    
    return response.status_code == 200

def main():
    """메인 테스트 함수"""
    print("BEHIND 인증 API 테스트 시작\n")
    
    # 회원가입 테스트
    email = test_register()
    if email:
        print("✅ 회원가입 성공")
    else:
        print("❌ 회원가입 실패")
        return
    
    # 로그인 테스트
    token = test_login(email)
    if token:
        print("✅ 로그인 성공")
    else:
        print("❌ 로그인 실패")
        return
    
    # 로그아웃 테스트
    if test_logout(token):
        print("✅ 로그아웃 성공")
    else:
        print("❌ 로그아웃 실패")
    
    print("\n모든 테스트 완료!")

if __name__ == "__main__":
    main() 