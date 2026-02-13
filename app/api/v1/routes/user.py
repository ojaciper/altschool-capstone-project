from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependency.deps import get_current_user, get_db, admin_only
from app.schemas.user import UserRead, UserActivate, Response
from app.services.user import UserService

router = APIRouter()


@router.get("/me", response_model=UserRead, status_code=200)
def get_user(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    user = UserService.get_user(db, current_user.email)
    print(current_user)
    if user == None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("", response_model=Response, status_code=200)
def all_user(db: Session = Depends(get_db), admin=Depends(admin_only)):
    user = UserService.get_all_user(db)
    if user == None:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(status="success", message="user retrive successfully", data=user)


@router.get("/{email}", response_model=UserRead, status_code=200)
def get_user_by_email(
    email: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    user = UserService.get_user_by_email(db, email)
    if user == None:
        raise HTTPException(status_code=404, detail=f"No user with this {email} exist")
    return user


@router.patch("/{user_id}/activate", response_model=UserRead)
def activate_user(user_id: UUID, data: UserActivate, db: Session = Depends(get_db)):
    user = UserService.update_user_status(
        db,
        user_id,
        data.is_active,
    )
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user == "account_activated":
        raise HTTPException(status_code=409, detail="account activated already")
    db.commit()
    return user
