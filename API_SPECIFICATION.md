# BEHIND API 명세서

## 개요
BEHIND는 대화 상대와의 관계를 분석하고 메시지 의도를 파악하여 더 나은 소통을 돕는 AI 기반 메시지 분석 서비스입니다.

**중요**: 파트너 관리 및 메시지 관련 API는 JWT 토큰 인증 없이 자유롭게 사용할 수 있습니다.

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

**Response:**
```json
{
  "message": "로그아웃되었습니다."
}
```

---

## 2. 상대 관리 API

### 2.1 상대 목록 조회
```http
GET /partners/{user_id}
```

**Path Variables:**
- `user_id` (integer): 사용자 ID

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

**Request Body:**
```json
{
  "name": "김철수",
  "mbti": "ENFP",
  "gender": "남성",
  "age": 25,
  "relation": "친구",
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

**Request Body:**
```json
{
  "name": "김철수",
  "mbti": "ENFP",
  "gender": "남성",
  "age": 25,
  "relation": "친구",
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

**Response:**
```json
{
  "message": "Partner deleted successfully"
}
```

## 3. 채팅 기록

### 3.1 채팅 기록 조회
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

### 3.2 채팅 기록 업데이트
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

## 4. 에러 응답

### 4.1 리소스 없음
```json
{
  "detail": "Partner not found"
}
```

### 4.2 유효성 검사 오류
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

## 5. 사용 예시

### 5.1 상대 목록 조회
```bash
curl -X GET "https://behind-back-production.up.railway.app/partners/1"
```

### 5.2 상대 생성
```bash
curl -X POST "https://behind-back-production.up.railway.app/partners/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "김철수",
    "mbti": "ENFP",
    "gender": "남성",
    "age": 25,
    "relation": "친구",
    "closeness": 8
  }'
```

### 5.3 채팅 기록 조회
```bash
curl -X GET "https://behind-back-production.up.railway.app/messages/1"
```

### 5.4 채팅 기록 업데이트
```bash
curl -X POST "https://behind-back-production.up.railway.app/messages/update" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "partner_name": "김현호",
    "messages": [
      {
        "content": "안녕하세요!",
        "timestamp": "2025-01-15T10:00:00Z",
        "type": "user"
      }
    ]
  }'
```
