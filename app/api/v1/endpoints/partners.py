from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/{user_id}", response_model=schemas.PartnerList)
def read_partners(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    특정 사용자의 상대 목록을 조회합니다.
    """
    # 권한 검사: 현재 사용자만 자신의 파트너 목록을 조회할 수 있음
    if current_user.id != user_id:
        raise HTTPException(
            status_code=403, 
            detail="자신의 파트너 목록만 조회할 수 있습니다."
        )
    
    partners = crud.partner_crud.get_by_user_id(db, user_id=user_id)
    return {
        "partners": partners,
        "total": len(partners)
    }


@router.post("/{user_id}", response_model=schemas.Partner)
def create_partner(
    user_id: int,
    *,
    db: Session = Depends(deps.get_db),
    partner_in: schemas.PartnerCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    새로운 상대를 생성합니다.
    """
    # 권한 검사: 현재 사용자만 자신의 파트너를 생성할 수 있음
    if current_user.id != user_id:
        raise HTTPException(
            status_code=403, 
            detail="자신의 파트너만 생성할 수 있습니다."
        )
    
    partner = crud.partner_crud.create(db, obj_in=partner_in, user_id=user_id)
    return partner


@router.put("/{user_id}/{partner_id}", response_model=schemas.Partner)
def update_partner(
    user_id: int,
    partner_id: int,
    *,
    db: Session = Depends(deps.get_db),
    partner_in: schemas.PartnerUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    상대 정보를 업데이트합니다.
    """
    # 권한 검사: 현재 사용자만 자신의 파트너를 수정할 수 있음
    if current_user.id != user_id:
        raise HTTPException(
            status_code=403, 
            detail="자신의 파트너만 수정할 수 있습니다."
        )
    
    partner = crud.partner_crud.get(db, id=partner_id)
    if not partner or partner.user_id != user_id:
        raise HTTPException(status_code=404, detail="Partner not found")
    partner = crud.partner_crud.update(db, db_obj=partner, obj_in=partner_in)
    return partner


@router.delete("/{user_id}/{partner_id}")
def delete_partner(
    user_id: int,
    partner_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    상대를 삭제합니다.
    """
    # 권한 검사: 현재 사용자만 자신의 파트너를 삭제할 수 있음
    if current_user.id != user_id:
        raise HTTPException(
            status_code=403, 
            detail="자신의 파트너만 삭제할 수 있습니다."
        )
    
    partner = crud.partner_crud.get(db, id=partner_id)
    if not partner or partner.user_id != user_id:
        raise HTTPException(status_code=404, detail="Partner not found")
    crud.partner_crud.remove(db, id=partner_id)
    return {"message": "Partner deleted successfully"} 