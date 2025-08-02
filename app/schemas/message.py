from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel


class ChatMessage(BaseModel):
    content: str
    timestamp: datetime
    type: str  # "user" or "ai"


class ChatHistoryItem(BaseModel):
    id: int
    name: str  # 파트너 이름
    chat_file: List[Dict[str, Any]]  # JSON 형태의 채팅 데이터
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ChatHistoryResponse(BaseModel):
    messages: List[ChatHistoryItem]


class ChatUpdateRequest(BaseModel):
    user_id: int
    partner_name: str
    messages: List[Dict[str, Any]]  # JSON 형태의 채팅 데이터


class ChatUpdateResponse(BaseModel):
    success: bool
    message: str
    updated_count: int 