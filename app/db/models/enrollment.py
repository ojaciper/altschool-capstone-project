from sqlalchemy import Column, String, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import timezone, datetime
import uuid
from app.db.base import Base


class Enrollment(Base):
    __tablename__ = "enrollement"
    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
