from app.db.models.enrollment import Enrollment
from app.db.models.course import Course
from app.db.models.user import User
from sqlalchemy.orm import Session
from uuid import UUID
# from typing import List
from app.schemas.enrollment import EnrollmentCreate


class EnrollmentService:

    @staticmethod
    def get_all_enrollment(db: Session) -> list:
        enrollment = db.query(Enrollment).all()
        print(enrollment)
        return list(enrollment)

    @staticmethod
    def get_enrollment_by_id(enrollment_id: UUID, db: Session):
        enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
        if not enrollment:
            return None
        return enrollment

    @staticmethod
    def enroll_course(db: Session, enrollment_data: EnrollmentCreate):
        course = db.query(Course).filter(Course.id == enrollment_data.course_id).first()
        print(course)
        if not course:
            return None

        if course.is_active != True:
            return "course_not_active"

        count = (
            db.query(Enrollment)
            .filter(Enrollment.course_id == enrollment_data.course_id)
            .count()
        )

        if count >= course.capacity:
            return "course_is_full"

        exists = (
            db.query(Enrollment)
            .filter(
                Enrollment.user_id == enrollment_data.user_id,
                Enrollment.course_id == enrollment_data.course_id,
            )
            .first()
        )
        if exists:
            return "already_enrolled"

        enrollment = Enrollment(
            user_id=enrollment_data.user_id, course_id=enrollment_data.course_id
        )
        db.add(enrollment)
        db.commit()
        db.refresh(enrollment)
        return enrollment

    @staticmethod
    def remove_student_from_enrollment(db: Session, user_id: UUID, course_id: UUID):
        enrollment = (
            db.query(Enrollment)
            .filter(Enrollment.user_id == user_id, Enrollment.course_id == course_id)
            .first()
        )
        if not enrollment:
            return None
        db.delete(enrollment)
        db.commit()
        return True

    @staticmethod
    def get_enrollment_for_a_course(db:Session, course_id:UUID):
        enrollment = db.query(Enrollment).filter(Enrollment.course_id == course_id).all()
        if not enrollment:
            return None
        return enrollment
