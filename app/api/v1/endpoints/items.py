from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.item import Item, ItemCreate, ItemUpdate
from app.crud.item import item_crud
from app.api.deps import get_current_user
from app.schemas.user import User

router = APIRouter()


@router.get("/", response_model=List[Item])
async def read_items(skip: int = 0, limit: int = 100):
    """아이템 목록 조회"""
    items = await item_crud.get_multi(skip=skip, limit=limit)
    return items


@router.post("/", response_model=Item)
async def create_item(
    item_in: ItemCreate,
    current_user: User = Depends(get_current_user)
):
    """새 아이템 생성"""
    item = await item_crud.create(item_in.dict(), owner_id=current_user.id)
    return item


@router.get("/{item_id}", response_model=Item)
async def read_item(item_id: int):
    """특정 아이템 조회"""
    item = await item_crud.get(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="아이템을 찾을 수 없습니다."
        )
    return item


@router.put("/{item_id}", response_model=Item)
async def update_item(
    item_id: int,
    item_in: ItemUpdate,
    current_user: User = Depends(get_current_user)
):
    """아이템 업데이트"""
    item = await item_crud.get(item_id)
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
    item = await item_crud.update(item_id, item_in.dict(exclude_unset=True))
    return item


@router.delete("/{item_id}")
async def delete_item(
    item_id: int,
    current_user: User = Depends(get_current_user)
):
    """아이템 삭제"""
    item = await item_crud.get(item_id)
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
    await item_crud.delete(item_id)
    return {"message": "아이템이 삭제되었습니다."} 