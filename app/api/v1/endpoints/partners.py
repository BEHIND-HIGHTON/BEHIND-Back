from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.PartnerList)
def read_partners(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    현재 사용자의 상대 목록을 조회합니다.
    """
    partners = crud.partner.get_by_user_id(db, user_id=current_user.id)
    return {
        "partners": partners,
        "total": len(partners)
    }


@router.post("/", response_model=schemas.Partner)
def create_partner(
    *,
    db: Session = Depends(deps.get_db),
    partner_in: schemas.PartnerCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    새로운 상대를 생성합니다.
    """
    partner = crud.partner.create(db, obj_in=partner_in, user_id=current_user.id)
    return partner


@router.get("/{partner_id}", response_model=schemas.Partner)
def read_partner(
    *,
    db: Session = Depends(deps.get_db),
    partner_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    특정 상대 정보를 조회합니다.
    """
    partner = crud.partner.get(db, id=partner_id)
    if not partner or partner.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Partner not found")
    return partner


@router.put("/{partner_id}", response_model=schemas.Partner)
def update_partner(
    *,
    db: Session = Depends(deps.get_db),
    partner_id: int,
    partner_in: schemas.PartnerUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    상대 정보를 업데이트합니다.
    """
    partner = crud.partner.get(db, id=partner_id)
    if not partner or partner.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Partner not found")
    partner = crud.partner.update(db, db_obj=partner, obj_in=partner_in)
    return partner


@router.delete("/{partner_id}")
def delete_partner(
    *,
    db: Session = Depends(deps.get_db),
    partner_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    상대를 삭제합니다.
    """
    partner = crud.partner.get(db, id=partner_id)
    if not partner or partner.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Partner not found")
    crud.partner.remove(db, id=partner_id)
    return {"message": "Partner deleted successfully"} 