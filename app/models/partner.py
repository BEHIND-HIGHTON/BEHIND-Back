from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Partner(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    name = Column(String(100), nullable=False)
    relationship_type = Column(String(100), nullable=False)  # 친구, 연인, 가족 등
    intimacy_level = Column(Integer, nullable=False)  # 1-10 친밀도
    swearing_level = Column(Integer, nullable=False)  # 1-10 욕설 수준
    gender = Column(String(20))  # male, female, other
    mbti = Column(String(10))  # ENFP, ISTJ 등
    speech_style = Column(String(50))  # 존댓말, 반말, 경어
    description = Column(Text)  # 상대에 대한 설명
    
    # 관계 설정
    received_messages = relationship("ReceivedMessage", back_populates="partner")
    sent_messages = relationship("SentMessage", back_populates="partner") 