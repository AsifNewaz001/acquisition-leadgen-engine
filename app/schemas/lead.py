"""Lead Pydantic schemas"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

from app.models.lead import LeadStatus, LeadSource


class LeadBase(BaseModel):
    """Base lead schema"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    job_title: Optional[str] = None
    company_id: Optional[int] = None
    source: LeadSource
    campaign: Optional[str] = None
    linkedin_url: Optional[str] = None
    location: Optional[str] = None
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[str] = None


class LeadCreate(LeadBase):
    """Schema for creating a lead"""
    pass


class LeadUpdate(BaseModel):
    """Schema for updating a lead"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    job_title: Optional[str] = None
    status: Optional[LeadStatus] = None
    lead_score: Optional[int] = None
    is_qualified: Optional[bool] = None
    qualification_notes: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[str] = None


class LeadResponse(LeadBase):
    """Schema for lead response"""
    id: int
    status: LeadStatus
    lead_score: int
    is_qualified: bool
    hubspot_id: Optional[str] = None
    salesforce_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    last_contacted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
