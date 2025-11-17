"""Activity tracking database model"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base


class ActivityType(str, enum.Enum):
    EMAIL_SENT = "email_sent"
    EMAIL_OPENED = "email_opened"
    EMAIL_CLICKED = "email_clicked"
    CALL = "call"
    MEETING = "meeting"
    NOTE = "note"
    STATUS_CHANGE = "status_change"
    FORM_SUBMISSION = "form_submission"
    PAGE_VIEW = "page_view"
    DOCUMENT_DOWNLOAD = "document_download"
    CRM_SYNC = "crm_sync"


class Activity(Base):
    __tablename__ = "activities"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False, index=True)

    # Activity Details
    activity_type = Column(Enum(ActivityType), nullable=False)
    title = Column(String(200))
    description = Column(Text)

    # Metadata
    metadata = Column(Text)  # JSON string for additional data
    user_agent = Column(String(500))
    ip_address = Column(String(50))

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    lead = relationship("Lead", back_populates="activities")

    def __repr__(self):
        return f"<Activity {self.activity_type} for Lead {self.lead_id}>"
