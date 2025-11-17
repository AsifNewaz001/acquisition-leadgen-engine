"""Lead database model"""

from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base


class LeadStatus(str, enum.Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    UNQUALIFIED = "unqualified"
    CONVERTED = "converted"
    LOST = "lost"


class LeadSource(str, enum.Enum):
    WEBSITE = "website"
    LANDING_PAGE = "landing_page"
    SOCIAL_MEDIA = "social_media"
    REFERRAL = "referral"
    COLD_OUTREACH = "cold_outreach"
    WEBINAR = "webinar"
    CHAT_WIDGET = "chat_widget"
    API = "api"
    MANUAL = "manual"


class Lead(Base):
    __tablename__ = "leads"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Contact Information
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(50))
    job_title = Column(String(200))

    # Company Information
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    company = relationship("Company", back_populates="leads")

    # Lead Details
    status = Column(Enum(LeadStatus), default=LeadStatus.NEW, nullable=False)
    source = Column(Enum(LeadSource), nullable=False)
    campaign = Column(String(200))

    # Scoring & Qualification
    lead_score = Column(Integer, default=0)
    is_qualified = Column(Boolean, default=False)
    qualification_notes = Column(Text)

    # Enrichment Data
    linkedin_url = Column(String(500))
    twitter_handle = Column(String(100))
    location = Column(String(200))
    timezone = Column(String(50))

    # Tracking
    utm_source = Column(String(100))
    utm_medium = Column(String(100))
    utm_campaign = Column(String(100))
    utm_term = Column(String(100))
    utm_content = Column(String(100))

    # CRM Sync
    hubspot_id = Column(String(100), unique=True)
    salesforce_id = Column(String(100), unique=True)
    last_synced_at = Column(DateTime)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_contacted_at = Column(DateTime)

    # Additional metadata
    notes = Column(Text)
    tags = Column(String(500))  # Comma-separated tags

    # Relationships
    activities = relationship("Activity", back_populates="lead", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Lead {self.email} - {self.status}>"
