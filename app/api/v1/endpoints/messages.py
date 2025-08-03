from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/{user_id}", response_model=schemas.ChatHistoryResponse)
def read_chat_history(
    user_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    사용자의 채팅 기록을 조회합니다.
    """
    # 권한 검사 제거 - 모든 사용자가 자유롭게 조회 가능
    chat_history = crud.message_crud.get_chat_history_by_user_id(db, user_id=user_id)
    
    # 채팅 기록이 없으면 빈 리스트 반환
    if not chat_history:
        return {"messages": []}
    
    # DB에서 가져온 데이터를 스키마에 맞게 변환
    messages = []
    for chat in chat_history:
        messages.append({
            "id": chat["id"],
            "name": chat.get("partner_name", "Unknown"),  # 파트너 이름 포함
            "chat_file": chat["chat_file"],
            "user_id": chat["user_id"],
            "created_at": chat["created_at"],
            "updated_at": chat["updated_at"]
        })
    
    return {"messages": messages}


@router.post("/update", response_model=schemas.ChatUpdateResponse)
def update_chat_history(
    *,
    db: Session = Depends(deps.get_db),
    chat_update: schemas.ChatUpdateRequest,
) -> Any:
    """
    채팅 기록을 업데이트합니다.
    """
    # 권한 검사 제거 - 모든 사용자가 자유롭게 업데이트 가능
    try:
        updated_count = crud.message_crud.update_chat_history(
            db, 
            user_id=chat_update.user_id,
            partner_name=chat_update.partner_name,
            messages=chat_update.messages
        )
        
        return {
            "success": True,
            "message": f"채팅 기록이 성공적으로 업데이트되었습니다. {updated_count}개의 메시지가 처리되었습니다.",
            "updated_count": updated_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"채팅 기록 업데이트 중 오류가 발생했습니다: {str(e)}") 