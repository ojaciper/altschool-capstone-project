from typing import Optional
from pydantic import BaseModel,ConfigDict
from datetime import datetime
from uuid import UUID


class EnrollmentBase(BaseModel):
    user_id:UUID
    course_id:UUID
    created_at:datetime
    
class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentRead(EnrollmentBase):
    id:UUID
    model_config= ConfigDict(from_attributes=True)
    
class Response(BaseModel):
    status: str
    message:str
    data: Optional[EnrollmentRead | list[EnrollmentRead]] = None