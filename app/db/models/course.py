from sqlalchemy import Column, String, ForeignKey, Text,Integer,Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base import Base
from sqlalchemy.orm import relationship


class Course(Base):
    __tablename__ = "courses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    title = Column(Text, nullable=False)
    course_code = Column(String(50), index=True,unique=True, nullable=True)
    capacity = Column(Integer)
    is_active = Column(Boolean, default=False)

    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")