from sqlalchemy import Column, Text, String, Enum as SQLEnum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum
import uuid
from app.db.base import Base



class Role(str, Enum):
    STUDENT = 'student'
    ADMIN = "admin"


class User(Base):
    __tablename__ ="users"
    id = Column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4)
    full_name = Column(String(50),nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255),unique=True, nullable=False)
    role = Column(String(255), default="student")
    is_active=Column(Boolean, default=False)
