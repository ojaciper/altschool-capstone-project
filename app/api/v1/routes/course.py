from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.course import (
    CourseRead,
    CourseCreate,
    Response,
    CourseUpdate,
    CourseActivate,
)
from app.dependency.deps import get_current_user, get_db, get_user_role, admin_only
from app.services.course import CouserServices
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("", response_model=CourseRead, status_code=201)
def course(
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only),
):
    course = CouserServices.create_course(db, course_data)
    if course_data.capacity <= 0:
        raise HTTPException(
            status_code=409, detail="capacity should not be less than 0"
        )
    if course == "code_already_exist":
        raise HTTPException(status_code=409, detail="course code already exists")
    if course == "title_already_exist":
        raise HTTPException(status_code=409, detail="course title already exists")
    return course


@router.get("/", response_model=Response, status_code=200)
def active_course(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    course = CouserServices.active_course(db)
    return Response(
        message="success",
        data=course,
    )



@router.get("/all", response_model=Response, status_code=200)
def all_course(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    course = CouserServices.all_course(db)
    return Response(
        message="success",
        data=course,
    )

@router.get("", response_model=Response, status_code=200)
def in_active_course(db: Session = Depends(get_db), admin=Depends(admin_only)):
    course = CouserServices.inactive_course(db)
    return Response(message="success", data=course)


@router.get("/{course_id}", response_model=Response, status_code=200)
def get_course_by_id(
    course_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    course = CouserServices.get_course_by_id(db, course_id)
    if course == None:
        raise HTTPException(status_code=404, detail="Course not found")
    return Response(message="Success", data=course)


@router.patch("/{coure_id}", response_model=CourseRead, status_code=200)
def edit_course(
    course_data: CourseUpdate,
    course_id: UUID,
    db: Session = Depends(get_db),
    admin=Depends(admin_only),
):
    course = CouserServices.update_course(course_id, db, course_data)
    if course == None:
        raise HTTPException(status_code=404, detail="Course not found")
    if course == "code_exist":
        raise HTTPException(
            status_code=409,
            detail=f"Course with code {course_data.course_code} already exist",
        )
    return course


@router.patch("/{course_id}/activate", status_code=200)
def activate_course(
    course_data: CourseActivate,
    course_id: UUID,
    db: Session = Depends(get_db),
    admin=Depends(admin_only),
):
    course = CouserServices.activate_course(db, course_id, course_data.is_active)
    if course == None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.delete("/{course_id}/remove", status_code=200)
def remove_course(
    course_id: UUID, db: Session = Depends(get_db), admin=Depends(admin_only)
):

    course = CouserServices.get_course_by_id(db, course_id)
    if course == None:
        raise HTTPException(status_code=404, detail="Course not found")
    is_enrolled = CouserServices.is_enrolled(db, course_id)

    if is_enrolled:
        raise HTTPException(
            status_code=409, detail="You can not remove course that is enrolled"
        )
    CouserServices.remove_course(db, course_id)
    return {"message": "course remove successfully"}


@router.get("/all", response_model=Response, status_code=200)
def all_course(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    course = CouserServices.all_course(db)
    return Response(
        message="success",
        data=course,
    )