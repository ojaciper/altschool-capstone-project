from uuid import UUID
from fastapi import APIRouter, status, HTTPException, Depends
from app.dependency.deps import get_db, get_current_user, admin_only
from app.schemas.enrollment import EnrollmentCreate, EnrollmentRead, Response
from sqlalchemy.orm import Session
from app.services.enrollment import EnrollmentService

router = APIRouter()


@router.get("/", response_model=Response, status_code=200)
def enrollment(db: Session = Depends(get_db), current_user=Depends(admin_only)):
    enrollment = EnrollmentService.get_all_enrollment(db)
    if len(enrollment) <= 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not data")
    return Response(status="success", message="course", data=enrollment)


@router.post("/", response_model=EnrollmentRead, status_code=201)
def enrollment(
    enrollment_data: EnrollmentCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    if user.role == "admin":
        raise HTTPException(status_code=409, detail="admin can not enroll for a course")
    else:
        enrollment = EnrollmentService.enroll_course(db, enrollment_data)

        if enrollment == None:
            raise HTTPException(status_code=404, detail="Course Not found")
        if enrollment == "course_not_active":
            raise HTTPException(status_code=409, detail="course is not active")

        if enrollment == "course_is_full":
            raise HTTPException(status_code=409, detail="Course is full")
        if enrollment == "already_enrolled":
            raise HTTPException(
                status_code=409, detail="You have already enrolled in the is course"
            )
        return enrollment


@router.delete("/{user_id}/remove", status_code=200)
def remove_student_from_course(
    user_id: UUID,
    course_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if user.role == "student":
        raise HTTPException(
            status_code=409, detail="admin can not deregister student from a course"
        )
    else:
        enrollment = EnrollmentService.remove_student_from_enrollment(
            db, user_id, course_id
        )
        if enrollment == None:
            raise HTTPException(
                status_code=404, detail="No user or course found in the enrollment"
            )
            
        return {"message": "Remove successfully"}


@router.get("/{course_id}/enrollment", response_model=Response, status_code=200)
def course_enrollment(
    course_id: UUID, db: Session = Depends(get_db), admin=Depends(admin_only)
):
    enrollment = EnrollmentService.get_enrollment_for_a_course(db, course_id)
    if enrollment == None:
        raise HTTPException(status_code=404, detail="No Enrollment in this course")
    return Response(status="success", message="Enrollment Retrived", data=enrollment)
