from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.crud.base import CRUDBase
from app.models.message import ReceivedMessage, SentMessage
from app.models.chat_history import ChatHistory
from app.schemas.message import ChatUpdateRequest


class CRUDMessage:
    def get_chat_history_by_user_id(self, db: Session, *, user_id: int) -> List[Dict[str, Any]]:
        """사용자의 채팅 기록을 조회합니다."""
        # 채팅 기록과 파트너 정보를 함께 조회
        query = text("""
            SELECT ch.*, p.name as partner_name
            FROM chat_history ch
            LEFT JOIN partner p ON ch.user_id = p.user_id
            WHERE ch.user_id = :user_id
            ORDER BY ch.created_at DESC
        """)
        
        result = db.execute(query, {"user_id": user_id})
        return [dict(row) for row in result]
    
    def update_chat_history(self, db: Session, *, user_id: int, partner_name: str, messages: List[Dict[str, Any]]) -> int:
        """채팅 기록을 업데이트합니다."""
        # 파트너가 존재하는지 확인
        from app.crud.partner import partner
        partner_obj = partner.get_by_user_id_and_name(db, user_id=user_id, name=partner_name)
        
        if not partner_obj:
            # 파트너가 없으면 생성
            from app.schemas.partner import PartnerCreate
            partner_data = PartnerCreate(name=partner_name)
            partner_obj = partner.create(db, obj_in=partner_data, user_id=user_id)
        
        # 기존 채팅 기록 삭제 (덮어쓰기)
        db.query(ChatHistory).filter(ChatHistory.user_id == user_id).delete()
        
        # 새로운 채팅 기록 생성
        chat_history = ChatHistory(
            chat_file=messages,
            user_id=user_id
        )
        
        db.add(chat_history)
        db.commit()
        db.refresh(chat_history)
        
        return len(messages)


message = CRUDMessage() 