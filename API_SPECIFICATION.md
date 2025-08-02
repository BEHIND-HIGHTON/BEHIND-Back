# BEHIND API 명세서

## 개요
BEHIND는 대화 상대와의 관계를 분석하고 메시지 의도를 파악하여 더 나은 소통을 돕는 AI 기반 메시지 분석 서비스입니다.

## Base URL
```
http://127.0.0.1:8003/api/v1
```

## 인증
JWT 토큰 기반 인증을 사용합니다. 헤더에 `Authorization: Bearer {token}` 형식으로 포함해야 합니다.

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

**Headers:**
```
Authorization: Bearer {token}
```

---

## 2. 상대 관리 API

### 2.1 상대 생성
```http
POST /partners
```

**Headers:**
```
Authorization: Bearer {token}
```

**Request Body:**
```json
{
  "name": "김철수",
  "relationship": "친구",
  "intimacy_level": 8,
  "swearing_level": 3,
  "gender": "male",
  "mbti": "ENFP",
  "speech_style": "반말",
  "description": "대학 동기 친구"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "김철수",
  "relationship": "친구",
  "intimacy_level": 8,
  "swearing_level": 3,
  "gender": "male",
  "mbti": "ENFP",
  "speech_style": "반말",
  "description": "대학 동기 친구",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### 2.2 상대 목록 조회
```http
GET /partners
```

**Headers:**
```
Authorization: Bearer {token}
```

**Response:**
```json
{
  "partners": [
    {
      "id": 1,
      "name": "김철수",
      "relationship": "친구",
      "intimacy_level": 8,
      "swearing_level": 3,
      "gender": "male",
      "mbti": "ENFP",
      "speech_style": "반말",
      "description": "대학 동기 친구",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1
}
```

### 2.3 상대 정보 수정
```http
PUT /partners/{partner_id}
```

**Headers:**
```
Authorization: Bearer {token}
```

**Request Body:**
```json
{
  "name": "김철수",
  "relationship": "친구",
  "intimacy_level": 9,
  "swearing_level": 4,
  "gender": "male",
  "mbti": "ENFP",
  "speech_style": "반말",
  "description": "대학 동기 친구"
}
```

### 2.4 상대 삭제
```http
DELETE /partners/{partner_id}
```

**Headers:**
```
Authorization: Bearer {token}
```

---

## 3. 받은 메시지 분석 API

### 3.1 받은 메시지 의도 분석
```http
POST /messages/received/analyze
```

**Headers:**
```
Authorization: Bearer {token}
```

**Request Body:**
```json
{
  "partner_id": 1,
  "message": "아오 진짜 너 오늘 개못했음 ㄹㅇ",
  "timestamp": "2024-01-01T14:30:00Z",
  "context": "게임 중 대화"
}
```

**Response:**
```json
{
  "analysis": {
    "intent": "장난",
    "sentiment": "positive",
    "confidence": 0.95,
    "explanation": "상대방과의 관계에서 '개못했음'은 악의적 표현이 아닌 친근한 농담으로 사용되었습니다. 평소 관계가 친밀하고 서로 장난을 자주 주고받는 사이임을 고려할 때, 이는 부정적 의도가 아닙니다.",
    "relationship_context": {
      "intimacy_level": 8,
      "communication_style": "친근한 농담",
      "usual_tone": "반말과 친근한 표현"
    }
  },
  "partner_info": {
    "name": "김철수",
    "relationship": "친구",
    "intimacy_level": 8
  }
}
```

### 3.2 받은 메시지 저장
```http
POST /messages/received
```

**Headers:**
```
Authorization: Bearer {token}
```

**Request Body:**
```json
{
  "partner_id": 1,
  "message": "아오 진짜 너 오늘 개못했음 ㄹㅇ",
  "timestamp": "2024-01-01T14:30:00Z",
  "analysis_id": "analysis_123"
}
```

---

## 4. 보낼 메시지 검토 API

### 4.1 보낼 메시지 검토
```http
POST /messages/send/review
```

**Headers:**
```
Authorization: Bearer {token}
```

**Request Body:**
```json
{
  "partner_id": 1,
  "message": "너 진짜 광대였음 ㄹㅇ",
  "context": "재미있는 상황에 대한 반응"
}
```

**Response:**
```json
{
  "review": {
    "original_message": "너 진짜 광대였음 ㄹㅇ",
    "suggested_message": "너 진짜 개웃겼어 ㄹㅇ",
    "reason": "상대방의 성향을 고려하여 '광대'라는 표현을 '웃겼어'로 변경하는 것이 더 친근하고 부정적 뉘앙스가 없습니다.",
    "risk_level": "low",
    "suggestions": [
      "너 진짜 개웃겼어 ㄹㅇ",
      "너 진짜 재밌었어 ㄹㅇ",
      "너 진짜 웃겨 ㄹㅇ"
    ]
  },
  "partner_analysis": {
    "name": "김철수",
    "sensitivity_level": 3,
    "preferred_style": "친근한 농담"
  }
}
```

### 4.2 보낼 메시지 저장
```http
POST /messages/send
```

**Headers:**
```
Authorization: Bearer {token}
```

**Request Body:**
```json
{
  "partner_id": 1,
  "original_message": "너 진짜 광대였음 ㄹㅇ",
  "final_message": "너 진짜 개웃겼어 ㄹㅇ",
  "review_id": "review_123",
  "timestamp": "2024-01-01T15:00:00Z"
}
```

---

## 5. 대시보드 API

### 5.1 메시지 기록 조회
```http
GET /dashboard/messages
```

**Headers:**
```
Authorization: Bearer {token}
```

**Query Parameters:**
- `partner_id` (optional): 특정 상대의 메시지만 조회
- `type` (optional): "received" 또는 "sent"
- `page` (optional): 페이지 번호 (기본값: 1)
- `limit` (optional): 페이지당 항목 수 (기본값: 20)

**Response:**
```json
{
  "messages": [
    {
      "id": 1,
      "type": "received",
      "partner_name": "김철수",
      "message": "아오 진짜 너 오늘 개못했음 ㄹㅇ",
      "analysis": {
        "intent": "장난",
        "sentiment": "positive"
      },
      "timestamp": "2024-01-01T14:30:00Z"
    },
    {
      "id": 2,
      "type": "sent",
      "partner_name": "김철수",
      "original_message": "너 진짜 광대였음 ㄹㅇ",
      "final_message": "너 진짜 개웃겼어 ㄹㅇ",
      "timestamp": "2024-01-01T15:00:00Z"
    }
  ],
  "total": 2,
  "page": 1,
  "limit": 20
}
```

### 5.2 상대별 통계
```http
GET /dashboard/partners/{partner_id}/stats
```

**Headers:**
```
Authorization: Bearer {token}
```

**Response:**
```json
{
  "partner": {
    "id": 1,
    "name": "김철수",
    "relationship": "친구"
  },
  "stats": {
    "total_messages": 50,
    "received_messages": 25,
    "sent_messages": 25,
    "most_active_time": "오후",
    "common_intents": [
      {"intent": "장난", "count": 15},
      {"intent": "일상", "count": 10}
    ],
    "sentiment_distribution": {
      "positive": 30,
      "neutral": 15,
      "negative": 5
    }
  }
}
```

### 5.3 전체 통계
```http
GET /dashboard/stats
```

**Headers:**
```
Authorization: Bearer {token}
```

**Response:**
```json
{
  "total_partners": 5,
  "total_messages": 200,
  "most_active_partner": {
    "name": "김철수",
    "message_count": 50
  },
  "most_active_time": "오후",
  "recent_activity": [
    {
      "date": "2024-01-01",
      "message_count": 10
    }
  ]
}
```

---

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

---

## 7. 데이터 모델

### 7.1 사용자 (User)
```json
{
  "id": "integer",
  "email": "string",
  "full_name": "string",
  "is_active": "boolean",
  "created_at": "datetime"
}
```

### 7.2 상대 (Partner)
```json
{
  "id": "integer",
  "user_id": "integer",
  "name": "string",
  "relationship": "string",
  "intimacy_level": "integer (1-10)",
  "swearing_level": "integer (1-10)",
  "gender": "string (male/female/other)",
  "mbti": "string",
  "speech_style": "string (존댓말/반말/경어)",
  "description": "string",
  "created_at": "datetime"
}
```

### 7.3 받은 메시지 (ReceivedMessage)
```json
{
  "id": "integer",
  "user_id": "integer",
  "partner_id": "integer",
  "message": "string",
  "timestamp": "datetime",
  "intent": "string",
  "sentiment": "string",
  "confidence": "float",
  "explanation": "string"
}
```

### 7.4 보낸 메시지 (SentMessage)
```json
{
  "id": "integer",
  "user_id": "integer",
  "partner_id": "integer",
  "original_message": "string",
  "final_message": "string",
  "timestamp": "datetime",
  "review_reason": "string"
}
```

---

## 8. 상태 코드

- `200`: 성공
- `201`: 생성됨
- `400`: 잘못된 요청
- `401`: 인증 필요
- `403`: 권한 없음
- `404`: 리소스 없음
- `422`: 유효성 검사 오류
- `500`: 서버 오류 