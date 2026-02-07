from typing import Optional
from pydantic import BaseModel,ConfigDict
from datetime import datetime
from sqlalchemy import UUID


class EnrollmentBase(BaseModel):
    user_id:UUID
    course_id:UUID
    create_at:datetime
    
class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentRead(EnrollmentBase):
    id:UUID
    model_config= ConfigDict(from_attributes=True)
    
class Response:
    status: str
    message:str
    data: Optional[EnrollmentRead | list[EnrollmentRead]] = None