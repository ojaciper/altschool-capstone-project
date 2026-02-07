from fastapi import APIRouter, status,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.dependency.deps import get_db
from fastapi import Depends
from app.schemas.user import UserCreate,UserRead
from app.schemas.auth import Token
from app.services.user import UserService
from app.core.security import verify_password, create_access_token

router = APIRouter()

@router.post("/signup", response_model=UserRead, status_code=201)
def signup(user_data:UserCreate, db:Session=Depends(get_db)):
    existing_user = UserService.get_user_by_email(db,user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exist")
    try:
        user = UserService.create_user(db, user_data)
        db.commit()
        return user
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500,detail='Internal Server Error')
        

@router.post("/login", response_model=Token, status_code=200)
def login(login_data:OAuth2PasswordRequestForm=Depends(), db_session:Session=Depends(get_db)):
    user = UserService.get_user_by_email(db_session, login_data.username)
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if user.is_active == False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please active your account")
    access_token = create_access_token(email=user.email)
    return {
        "access_token":access_token,
        "token_type":"bearer"
    }
    
        