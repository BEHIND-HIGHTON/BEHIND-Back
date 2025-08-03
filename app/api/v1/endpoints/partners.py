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
) -> Any:
    """
    특정 사용자의 상대 목록을 조회합니다.
    """
    # 권한 검사 제거 - 모든 사용자가 자유롭게 조회 가능
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
) -> Any:
    """
    새로운 상대를 생성합니다.
    """
    # 권한 검사 제거 - 모든 사용자가 자유롭게 생성 가능
    partner = crud.partner_crud.create(db, obj_in=partner_in, user_id=user_id)
    return partner


@router.put("/{user_id}/{partner_id}", response_model=schemas.Partner)
def update_partner(
    user_id: int,
    partner_id: int,
    *,
    db: Session = Depends(deps.get_db),
    partner_in: schemas.PartnerUpdate,
) -> Any:
    """
    상대 정보를 업데이트합니다.
    """
    # 권한 검사 제거 - 모든 사용자가 자유롭게 수정 가능
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
) -> Any:
    """
    상대를 삭제합니다.
    """
    # 권한 검사 제거 - 모든 사용자가 자유롭게 삭제 가능
    partner = crud.partner_crud.get(db, id=partner_id)
    if not partner or partner.user_id != user_id:
        raise HTTPException(status_code=404, detail="Partner not found")
    crud.partner_crud.remove(db, id=partner_id)
    return {"message": "Partner deleted successfully"} 