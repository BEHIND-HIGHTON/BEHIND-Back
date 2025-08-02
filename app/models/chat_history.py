from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime


class ChatHistory(Base):
    id = Column(Integer, primary_key=True, index=True)
    chat_file = Column(JSON, nullable=False)  # JSON 형태로 채팅 데이터 저장
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 