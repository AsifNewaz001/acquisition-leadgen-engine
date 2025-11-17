"""Lead management API endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.schemas.lead import LeadCreate, LeadResponse, LeadUpdate
from app.services.lead_service import LeadService

router = APIRouter()


@router.post("/", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
async def create_lead(
    lead: LeadCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new lead"""
    service = LeadService(db)
    return await service.create_lead(lead)


@router.get("/", response_model=List[LeadResponse])
async def get_leads(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get all leads with pagination"""
    service = LeadService(db)
    return await service.get_leads(skip=skip, limit=limit)


@router.get("/{lead_id}", response_model=LeadResponse)
async def get_lead(
    lead_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific lead by ID"""
    service = LeadService(db)
    lead = await service.get_lead(lead_id)
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    return lead


@router.put("/{lead_id}", response_model=LeadResponse)
async def update_lead(
    lead_id: int,
    lead_update: LeadUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a lead"""
    service = LeadService(db)
    lead = await service.update_lead(lead_id, lead_update)
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    return lead


@router.delete("/{lead_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lead(
    lead_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a lead"""
    service = LeadService(db)
    success = await service.delete_lead(lead_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )


@router.post("/{lead_id}/score")
async def score_lead(
    lead_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Calculate and update lead score"""
    service = LeadService(db)
    score = await service.calculate_lead_score(lead_id)
    return {"lead_id": lead_id, "score": score}


@router.post("/{lead_id}/sync/{crm}")
async def sync_to_crm(
    lead_id: int,
    crm: str,
    db: AsyncSession = Depends(get_db)
):
    """Sync lead to external CRM (hubspot or salesforce)"""
    service = LeadService(db)
    result = await service.sync_to_crm(lead_id, crm)
    return result
