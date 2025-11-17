"""Analytics and reporting API endpoints"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from app.core.database import get_db
from app.services.analytics_service import AnalyticsService

router = APIRouter()


@router.get("/dashboard")
async def get_dashboard_stats(
    days: int = Query(30, description="Number of days to analyze"),
    db: AsyncSession = Depends(get_db)
):
    """Get dashboard statistics"""
    service = AnalyticsService(db)
    start_date = datetime.now() - timedelta(days=days)
    stats = await service.get_dashboard_stats(start_date)
    return stats


@router.get("/conversion-rate")
async def get_conversion_rate(
    start_date: datetime = Query(None),
    end_date: datetime = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Calculate conversion rates"""
    service = AnalyticsService(db)
    rate = await service.calculate_conversion_rate(start_date, end_date)
    return rate


@router.get("/lead-sources")
async def get_lead_sources(
    days: int = Query(30),
    db: AsyncSession = Depends(get_db)
):
    """Get lead distribution by source"""
    service = AnalyticsService(db)
    sources = await service.get_lead_sources_breakdown(days)
    return sources


@router.get("/top-performing-campaigns")
async def get_top_campaigns(
    limit: int = Query(10),
    db: AsyncSession = Depends(get_db)
):
    """Get top performing campaigns"""
    service = AnalyticsService(db)
    campaigns = await service.get_top_campaigns(limit)
    return campaigns
