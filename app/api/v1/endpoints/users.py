from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.schemas.user import User, UserUpdate
from app.crud.user import user_crud
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """현재 로그인한 사용자 정보 조회"""
    return current_user


@router.put("/me", response_model=User)
async def update_user_me(
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user)
):
    """현재 사용자 정보 업데이트"""
    user = await user_crud.update(current_user.id, user_in.dict(exclude_unset=True))
    return user


@router.get("/{user_id}", response_model=User)
async def read_user(user_id: int):
    """특정 사용자 정보 조회"""
    user = await user_crud.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다."
        )
    return user 