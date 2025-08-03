from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class PartnerBase(BaseModel):
    name: str
    mbti: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    relation: Optional[str] = None
    closeness: Optional[int] = None


class PartnerCreate(PartnerBase):
    pass


class PartnerUpdate(PartnerBase):
    pass


class PartnerInDBBase(PartnerBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Partner(PartnerInDBBase):
    pass


class PartnerList(BaseModel):
    partners: List[Partner]
    total: int 