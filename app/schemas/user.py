from enum import Enum
from pydantic import BaseModel, EmailStr, ConfigDict, UUID4
from typing import Optional
from app.db.models.user import Role



# class UserRole(str, Enum):
#     STUDENT = "student"
#     ADMIN ="admin"
    


class UserBase(BaseModel):
    full_name:str
    email:EmailStr
    role:str = "student"
    is_active:bool = False
    
class UserCreate(UserBase):
    password:str
    
class UserActivate(BaseModel):
    is_active:bool
    
class UserRead(UserBase):
    id:UUID4
    model_config = ConfigDict(from_attributes=True)
    