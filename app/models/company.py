"""Company database model"""

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Company(Base):
    __tablename__ = "companies"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Company Information
    name = Column(String(200), nullable=False, index=True)
    domain = Column(String(200), unique=True, index=True)
    website = Column(String(500))

    # Business Details
    industry = Column(String(100))
    size = Column(String(50))  # e.g., "1-10", "11-50", "51-200", etc.
    revenue = Column(String(50))
    description = Column(Text)

    # Location
    country = Column(String(100))
    state = Column(String(100))
    city = Column(String(100))
    address = Column(String(500))
    postal_code = Column(String(20))

    # Social & Contact
    linkedin_url = Column(String(500))
    twitter_handle = Column(String(100))
    facebook_url = Column(String(500))
    phone = Column(String(50))

    # Enrichment Data
    founded_year = Column(Integer)
    employee_count = Column(Integer)
    tech_stack = Column(Text)  # JSON string of technologies used

    # CRM Sync
    hubspot_id = Column(String(100), unique=True)
    salesforce_id = Column(String(100), unique=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    leads = relationship("Lead", back_populates="company")

    def __repr__(self):
        return f"<Company {self.name}>"
