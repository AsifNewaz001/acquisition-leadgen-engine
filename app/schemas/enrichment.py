"""Enrichment Pydantic schemas"""

from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any


class EnrichmentRequest(BaseModel):
    """Schema for enrichment request"""
    email: Optional[EmailStr] = None
    domain: Optional[str] = None
    company_name: Optional[str] = None


class EnrichmentResponse(BaseModel):
    """Schema for enrichment response"""
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    job_title: Optional[str] = None
    company: Optional[str] = None
    domain: Optional[str] = None
    linkedin_url: Optional[str] = None
    twitter_handle: Optional[str] = None
    location: Optional[str] = None
    company_info: Optional[Dict[str, Any]] = None
    enrichment_source: Optional[str] = None
    confidence_score: Optional[float] = None
