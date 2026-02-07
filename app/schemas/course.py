from pydantic import BaseModel, ConfigDict, UUID4
from typing import Optional


class CourseBase(BaseModel):
    title: str
    course_code: str
    capacity: int
    is_active: bool


class CourseCreate(CourseBase):
    pass


class CourseUpdate(CourseBase):
    title: str
    course_code: str
    capacity: int

class CourseActivate(BaseModel):
    is_active: bool


class CourseRead(CourseBase):
    id: UUID4
    model_config = ConfigDict(from_attributes=True)


class Response(BaseModel):
    success: bool = True
    message: str
    data: Optional[CourseRead | list[CourseRead]] = None
