from uuid import UUID
from sqlalchemy.orm import Session
from app.db.models.user import User
from app.schemas.user import UserCreate
from app.db.models.user import Role
from app.core.security import get_password_hash


class UserService:
    @staticmethod
    def get_user_by_email(db_session: Session, email: str):
        return db_session.query(User).filter(User.email == email).first()

    def create_user(db_session: Session, user_data: UserCreate):
        new_user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            hashed_password=get_password_hash(user_data.password),
            role=user_data.role,
        )
        db_session.add(new_user)
        db_session.flush()
        db_session.refresh(new_user)
        return new_user

    @staticmethod
    def get_user(db: Session, username: str):
        user = db.query(User).filter(User.email == username).first()
        if not user:
            return None
        return user
    
    @staticmethod
    def get_all_user(db:Session)->list:
        user = db.query(User).all()
        if not user:
            return None
        return list(user)

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None
        return user
    
    @staticmethod
    def update_user_status(db:Session, user_id:UUID, is_active:bool):
        user = db.query(User).filter(User.id == str(user_id)).first()
        if not user:
            return None
        user.is_active = is_active
        db.flush()
        db.refresh(user)
        return user
    

    
    

