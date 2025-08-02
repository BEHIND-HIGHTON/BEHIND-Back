from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime


class ReceivedMessage(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    partner_id = Column(Integer, ForeignKey("partner.id"), nullable=False)
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    context = Column(String(200))  # 대화 맥락 (게임 중, 일상 등)
    
    # AI 분석 결과
    intent = Column(String(100))  # 장난, 일상, 불만 등
    sentiment = Column(String(50))  # positive, negative, neutral
    confidence = Column(Float)  # 분석 신뢰도 (0-1)
    explanation = Column(Text)  # AI 설명
    
    # 관계 설정
    partner = relationship("Partner", back_populates="received_messages")


class SentMessage(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    partner_id = Column(Integer, ForeignKey("partner.id"), nullable=False)
    original_message = Column(Text, nullable=False)  # 원본 메시지
    final_message = Column(Text, nullable=False)  # 최종 메시지
    timestamp = Column(DateTime, default=datetime.utcnow)
    context = Column(String(200))  # 대화 맥락
    
    # AI 검토 결과
    review_reason = Column(Text)  # 검토 이유
    risk_level = Column(String(20))  # low, medium, high
    suggestions = Column(Text)  # 제안된 대안들 (JSON 형태로 저장)
    
    # 관계 설정
    partner = relationship("Partner", back_populates="sent_messages") 