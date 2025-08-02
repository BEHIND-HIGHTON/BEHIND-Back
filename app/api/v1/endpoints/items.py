from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.schemas.item import Item, ItemCreate, ItemUpdate
from app.crud.item import item_crud
from app.api.deps import get_current_user, get_db
from app.schemas.user import User

router = APIRouter()


@router.get("/", response_model=List[Item])
def read_items(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """아이템 목록 조회"""
    items = item_crud.get_multi(db, skip=skip, limit=limit)
    return items


@router.post("/", response_model=Item)
def create_item(
    item_in: ItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """새 아이템 생성"""
    item = item_crud.create(db, obj_in=item_in, owner_id=current_user.id)
    return item


@router.get("/{item_id}", response_model=Item)
def read_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """특정 아이템 조회"""
    item = item_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="아이템을 찾을 수 없습니다."
        )
    return item


@router.put("/{item_id}", response_model=Item)
def update_item(
    item_id: int,
    item_in: ItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """아이템 업데이트"""
    item = item_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="아이템을 찾을 수 없습니다."
        )
    if item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="권한이 없습니다."
        )
    item = item_crud.update(db, db_obj=item, obj_in=item_in)
    return item


@router.delete("/{item_id}")
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """아이템 삭제"""
    item = item_crud.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="아이템을 찾을 수 없습니다."
        )
    if item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="권한이 없습니다."
        )
    item_crud.remove(db, id=item_id)
    return {"message": "아이템이 삭제되었습니다."} 