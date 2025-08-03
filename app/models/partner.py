from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime


class Partner(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    name = Column(String(255), nullable=False)
    mbti = Column(String(4))  # ENFP, ISTJ 등
    gender = Column(String(10))  # male, female, other
    age = Column(Integer)
    relation = Column(String(50))  # 친구, 연인, 가족 등
    closeness = Column(Integer)  # 0-10 친밀도
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 관계 설정
    received_messages = relationship("ReceivedMessage", back_populates="partner")
    sent_messages = relationship("SentMessage", back_populates="partner") 