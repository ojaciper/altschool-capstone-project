from uuid import UUID
from app.db.session import SessionLocal
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.core.security import decode_access_token
from app.db.models.user import User

oauth2_schema = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
def get_current_user(token:str=Depends(oauth2_schema), db:Session=Depends(get_db))->User:
    token = decode_access_token(token=token)
    if token is None:
        raise HTTPException(status_code=401, detail="Invalide authentication credentials")
    user = db.query(User).filter(User.email == token.get("sub")).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_user_role(db:Session, user_id:UUID)->str:
    user = db.query(User).filter(User.id == user_id).first()
    return user.role

def admin_only(admin_user:User = Depends(get_current_user)):
    if admin_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Admin Privilages required"
        )