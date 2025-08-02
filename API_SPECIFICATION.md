# BEHIND API 명세서

## 개요
BEHIND는 대화 상대와의 관계를 분석하고 메시지 의도를 파악하여 더 나은 소통을 돕는 AI 기반 메시지 분석 서비스입니다.

## Base URL
```
https://behind-back-production.up.railway.app
```

---

## 1. 인증 API

### 1.1 회원가입
```http
POST /auth/register
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "홍길동"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "홍길동",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

### 1.2 로그인
```http
POST /auth/login
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "홍길동"
  }
}
```

### 1.3 로그아웃
```http
POST /auth/logout
```

---

## 2. 상대 관리 API

### 2.1 상대 목록 조회
```http
GET /partners/{user_id}
```

**Path Variables:**
- `user_id` (integer): 사용자 ID

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "partners": [
    {
      "id": 1,
      "name": "김철수",
      "mbti": "ENFP",
      "gender": "남성",
      "age": 25,
      "relation": "친구",
      "intimacy": 0.8,
      "affection": 0.7,
      "aggression": 0.2,
      "dominance": 0.5,
      "closeness": 8,
      "user_id": 1,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1
}
```

### 2.2 상대 생성
```http
POST /partners/{user_id}
```

**Path Variables:**
- `user_id` (integer): 사용자 ID

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "name": "김철수",
  "mbti": "ENFP",
  "gender": "남성",
  "age": 25,
  "relation": "친구",
  "intimacy": 0.8,
  "affection": 0.7,
  "aggression": 0.2,
  "dominance": 0.5,
  "closeness": 8
}
```

**Response:**
```json
{
  "id": 1,
  "name": "김철수",
  "mbti": "ENFP",
  "gender": "남성",
  "age": 25,
  "relation": "친구",
  "intimacy": 0.8,
  "affection": 0.7,
  "aggression": 0.2,
  "dominance": 0.5,
  "closeness": 8,
  "user_id": 1,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### 2.3 상대 수정
```http
PUT /partners/{user_id}/{partner_id}
```

**Path Variables:**
- `user_id` (integer): 사용자 ID
- `partner_id` (integer): 상대 ID

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "name": "김철수",
  "mbti": "ENFP",
  "gender": "남성",
  "age": 25,
  "relation": "친구",
  "intimacy": 0.8,
  "affection": 0.7,
  "aggression": 0.2,
  "dominance": 0.5,
  "closeness": 8
}
```

**Response:**
```json
{
  "id": 1,
  "name": "김철수",
  "mbti": "ENFP",
  "gender": "남성",
  "age": 25,
  "relation": "친구",
  "intimacy": 0.8,
  "affection": 0.7,
  "aggression": 0.2,
  "dominance": 0.5,
  "closeness": 8,
  "user_id": 1,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### 2.4 상대 삭제
```http
DELETE /partners/{user_id}/{partner_id}
```

**Path Variables:**
- `user_id` (integer): 사용자 ID
- `partner_id` (integer): 상대 ID

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "message": "Partner deleted successfully"
}
```

## 5. 채팅 기록

### 5.1 채팅 기록 조회
```http
GET /messages/{user_id}
```

**Path Variable**
```
  user_id
```

**Response:**
```json
{
  "messages": [
    {
      "id": 1,
      "name": "김현호",
      "chat_file": [
        {
          "content": "조상철님, 오늘 김태현님과의 대화에서 검토할 내용을 선택해주세요!",
          "timestamp": "2025-08-03T05:41:00Z",
          "type": "user"
        },
        {
          "content": "네, 알겠습니다. 어떤 내용을 검토하고 싶으신가요?",
          "timestamp": "2025-08-03T05:42:00Z",
          "type": "ai"
        }
      ],
      "user_id": 1,
      "created_at": "2025-08-03T05:41:00Z",
      "updated_at": "2025-08-03T05:41:00Z"
    }
  ]
}
```

### 5.2 채팅 기록 업데이트
```http
POST /messages/update
```

**Request Body:**
```json
{
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
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "message": "채팅 기록이 성공적으로 업데이트되었습니다. 2개의 메시지가 처리되었습니다.",
  "updated_count": 2
}
```

## 6. 에러 응답

### 6.1 인증 오류
```json
{
  "detail": "Not authenticated"
}
```

### 6.2 권한 오류
```json
{
  "detail": "Not enough permissions"
}
```

### 6.3 리소스 없음
```json
{
  "detail": "Partner not found"
}
```

### 6.4 유효성 검사 오류
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

```
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

-- 파트너 테이블
CREATE TABLE IF NOT EXISTS partner (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    mbti VARCHAR(4),
    gender VARCHAR(10),
    age INT,
    relation VARCHAR(50),
    intimacy FLOAT CHECK (intimacy BETWEEN 0 AND 1),
    affection FLOAT CHECK (affection BETWEEN 0 AND 1),
    aggression FLOAT CHECK (aggression BETWEEN 0 AND 1), 
    dominance FLOAT CHECK (dominance BETWEEN 0 AND 1),
    closeness INT CHECK (closeness BETWEEN 0 AND 10),
    user_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS chat_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    chat_file JSON NOT NULL,
    user_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id)
);
```