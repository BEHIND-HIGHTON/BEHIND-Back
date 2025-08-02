from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import create_access_token
from app.schemas.auth import Token
from app.schemas.user import UserCreate, User
from app.crud.user import user_crud
from app.core.security import get_password_hash, verify_password

router = APIRouter()


@router.post("/register", response_model=User)
async def register(user_in: UserCreate):
    """사용자 등록"""
    # 이미 존재하는 사용자인지 확인
    existing_user = await user_crud.get_by_email(user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 등록된 이메일입니다."
        )
    
    # 새 사용자 생성
    user_data = user_in.dict()
    user_data["hashed_password"] = get_password_hash(user_in.password)
    del user_data["password"]
    
    user = await user_crud.create(user_data)
    return user


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """사용자 로그인"""
    user = await user_crud.get_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="잘못된 이메일 또는 비밀번호입니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"} 