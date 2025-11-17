"""Lead enrichment API endpoints"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.enrichment import EnrichmentRequest, EnrichmentResponse
from app.services.enrichment_service import EnrichmentService

router = APIRouter()


@router.post("/email", response_model=EnrichmentResponse)
async def enrich_by_email(
    request: EnrichmentRequest,
    db: AsyncSession = Depends(get_db)
):
    """Enrich lead data using email address"""
    service = EnrichmentService(db)
    try:
        result = await service.enrich_by_email(request.email)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/domain", response_model=EnrichmentResponse)
async def enrich_by_domain(
    request: EnrichmentRequest,
    db: AsyncSession = Depends(get_db)
):
    """Enrich company data using domain"""
    service = EnrichmentService(db)
    try:
        result = await service.enrich_by_domain(request.domain)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/validate-email")
async def validate_email(email: str):
    """Validate email address"""
    service = EnrichmentService(None)
    is_valid = await service.validate_email(email)
    return {"email": email, "is_valid": is_valid}
