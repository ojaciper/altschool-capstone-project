from typing import List
from uuid import UUID
from app.db.models.course import Course
from app.db.models.enrollment import Enrollment
from app.schemas.course import CourseCreate, CourseBase, CourseUpdate
from sqlalchemy.orm import Session
from app.dependency.deps import get_user_role


class CouserServices:

    @staticmethod
    def create_course(db: Session, course_data: CourseBase):
        existing_course_code = (
            db.query(Course)
            .filter(Course.course_code == course_data.course_code)
            .first()
        )
        if existing_course_code:
            return "code_already_exist"
        existing_course_title = (
            db.query(Course).filter(Course.title == course_data.title).first()
        )
        if existing_course_title:
            return "title_already_exist"
        new_course = Course(
            title=course_data.title,
            course_code=course_data.course_code,
            capacity=course_data.capacity,
            is_active=course_data.is_active,
        )
        db.add(new_course)
        db.commit()
        db.refresh(new_course)
        return new_course

    @staticmethod
    def active_course(db: Session) -> List:
        active_course = db.query(Course).filter(Course.is_active == True).all()
        return list(active_course)

    @staticmethod
    def get_course_by_id(db: Session, course_id):
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            return None
        return course

    @staticmethod
    def update_course(course_id: UUID, db: Session, course_data: CourseUpdate):
        course = db.query(Course).filter(Course.id == course_id).first()

        if not course:
            return None
        if course_data.course_code and course_data.course_code != course.course_code:
            exist = (
                db.query(Course)
                .filter(Course.course_code == course_data.course_code)
                .first()
            )
            if exist:
                return "code_exist"

        for field, value in course_data.model_dump(exclude_unset=True).items():
            setattr(course, field, value)

        db.commit()
        db.refresh(course)
        return course

    @staticmethod
    def activate_course(db: Session, course_id: UUID, is_active: bool):
        course = db.query(Course).filter(Course.id == course_id).first()
        print(course)
        if not course:
            return None
        course.is_active = is_active
        db.commit()
        db.refresh(course)
        return course

    @staticmethod
    def remove_course(db: Session, course_id: UUID):
        course = db.query(Course).filter(Course.id == course_id).first()

        if not course:
            return None
        is_enrolled = (
            db.query(Enrollment).filter(Enrollment.course_id == course_id).first()
        )
        if is_enrolled:
            return "students_enrolled_in_the_course"
        db.delete(course)
        db.commit()
        return True

    @staticmethod
    def is_enrolled(db: Session, course_id: UUID):
        is_enrolled = (
            db.query(Enrollment).filter(Enrollment.course_id == course_id).first()
        )
        if is_enrolled:
            return True
        return False
