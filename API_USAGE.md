# BEHIND API 사용법

## 개요
BEHIND API는 대화 상대와의 관계를 분석하고 메시지 의도를 파악하여 더 나은 소통을 돕는 AI 기반 메시지 분석 서비스입니다.

## Base URL
```
https://behind-back-production.up.railway.app
```

## 인증
모든 API 요청에는 JWT 토큰이 필요합니다. 토큰은 로그인 API를 통해 얻을 수 있습니다.

### 로그인 예시
```bash
curl -X POST "https://behind-back-production.up.railway.app/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=password123"
```

응답에서 `access_token`을 받아서 이후 요청에 사용합니다.

## API 엔드포인트

### 1. 상대 관리 API

#### 1.1 상대 목록 조회
```bash
curl -X GET "https://behind-back-production.up.railway.app/partners/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**응답 예시:**
```json
{
  "partners": [
    {
      "id": 1,
      "name": "김철수",
      "mbti": "ENFP",
      "gender": "male",
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

#### 1.2 상대 생성
```bash
curl -X POST "https://behind-back-production.up.railway.app/partners/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "김철수",
    "mbti": "ENFP",
    "gender": "male",
    "age": 25,
    "relation": "친구",
    "closeness": 8
  }'
```

#### 1.3 상대 정보 수정
```bash
curl -X PUT "https://behind-back-production.up.railway.app/partners/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "김영희",
    "mbti": "ISTJ",
    "closeness": 9
  }'
```

#### 1.4 상대 삭제
```bash
curl -X DELETE "https://behind-back-production.up.railway.app/partners/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 2. 채팅 기록 API

#### 2.1 채팅 기록 조회
```bash
curl -X GET "https://behind-back-production.up.railway.app/messages/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**응답 예시:**
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

#### 2.2 채팅 기록 업데이트
```bash
curl -X POST "https://behind-back-production.up.railway.app/messages/update" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

**응답 예시:**
```json
{
  "success": true,
  "message": "채팅 기록이 성공적으로 업데이트되었습니다. 2개의 메시지가 처리되었습니다.",
  "updated_count": 2
}
```

## 에러 처리

### 인증 오류 (401)
```json
{
  "detail": "Not authenticated"
}
```

### 권한 오류 (403)
```json
{
  "detail": "Not enough permissions"
}
```

### 리소스 없음 (404)
```json
{
  "detail": "Partner not found"
}
```

### 유효성 검사 오류 (422)
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

## 테스트

### 파트너 API 테스트
```bash
python -m pytest test_partners_api.py -v
```

### 메시지 API 테스트
```bash
python -m pytest test_messages_api.py -v
```

## 주의사항

1. **인증**: 모든 API 요청에는 유효한 JWT 토큰이 필요합니다.
2. **권한**: 사용자는 자신의 데이터만 접근할 수 있습니다.
3. **데이터 형식**: 날짜는 ISO 8601 형식(YYYY-MM-DDTHH:MM:SSZ)을 사용합니다.
4. **파트너 이름**: 채팅 기록 업데이트 시 파트너가 존재하지 않으면 자동으로 생성됩니다. 