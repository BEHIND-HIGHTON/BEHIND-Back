from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.security import create_access_token
from app.schemas.auth import Token, UserRegister, UserLogin
from app.schemas.user import UserCreate, User
from app.crud.user import user_crud
from app.core.security import get_password_hash, verify_password
from app.api.deps import get_current_user
from app.db.session import get_db

router = APIRouter()


@router.get("/test")
def test_endpoint():
    """테스트 엔드포인트"""
    return {"message": "Auth endpoint is working"}


@router.post("/register", response_model=User)
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    """사용자 등록"""
    # 이미 존재하는 사용자인지 확인
    existing_user = user_crud.get_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 등록된 이메일입니다."
        )
    
    # 새 사용자 생성
    hashed_password = get_password_hash(user_in.password)
    user_data = UserCreate(
        email=user_in.email,
        password=user_in.password,
        hashed_password=hashed_password,
        full_name=user_in.full_name
    )
    
    user = user_crud.create(db, obj_in=user_data)
    return user


@router.post("/login", response_model=Token)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    """사용자 로그인"""
    user = user_crud.get_by_email(db, email=user_in.email)
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="잘못된 이메일 또는 비밀번호입니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser,
            "created_at": user.created_at
        }
    }


@router.post("/logout")
def logout(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """사용자 로그아웃"""
    # JWT 토큰은 클라이언트에서 삭제하므로 서버에서는 성공 응답만 반환
    return {"message": "로그아웃되었습니다."} 