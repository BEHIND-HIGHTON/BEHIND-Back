from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.partner import Partner
from app.schemas.partner import PartnerCreate, PartnerUpdate


class CRUDPartner(CRUDBase[Partner, PartnerCreate, PartnerUpdate]):
    def get_by_user_id(self, db: Session, *, user_id: int) -> List[Partner]:
        return db.query(Partner).filter(Partner.user_id == user_id).all()
    
    def get_by_user_id_and_name(self, db: Session, *, user_id: int, name: str) -> Optional[Partner]:
        return db.query(Partner).filter(Partner.user_id == user_id, Partner.name == name).first()
    
    def create(self, db: Session, *, obj_in: PartnerCreate, user_id: int) -> Partner:
        obj_in_data = obj_in.dict()
        obj_in_data["user_id"] = user_id
        db_obj = Partner(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


partner_crud = CRUDPartner(Partner) 