"""Analytics and reporting service"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from datetime import datetime, timedelta
from typing import Dict, Any, List

from app.models.lead import Lead, LeadStatus, LeadSource


class AnalyticsService:
    """Service for analytics and reporting"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_dashboard_stats(self, start_date: datetime) -> Dict[str, Any]:
        """Get dashboard statistics"""
        # Total leads
        total_leads_result = await self.db.execute(
            select(func.count(Lead.id)).where(Lead.created_at >= start_date)
        )
        total_leads = total_leads_result.scalar()

        # Qualified leads
        qualified_leads_result = await self.db.execute(
            select(func.count(Lead.id)).where(
                and_(Lead.created_at >= start_date, Lead.is_qualified == True)
            )
        )
        qualified_leads = qualified_leads_result.scalar()

        # Converted leads
        converted_leads_result = await self.db.execute(
            select(func.count(Lead.id)).where(
                and_(Lead.created_at >= start_date, Lead.status == LeadStatus.CONVERTED)
            )
        )
        converted_leads = converted_leads_result.scalar()

        # Average lead score
        avg_score_result = await self.db.execute(
            select(func.avg(Lead.lead_score)).where(Lead.created_at >= start_date)
        )
        avg_score = avg_score_result.scalar() or 0

        return {
            "total_leads": total_leads,
            "qualified_leads": qualified_leads,
            "converted_leads": converted_leads,
            "average_score": round(float(avg_score), 2),
            "qualification_rate": round((qualified_leads / total_leads * 100), 2)
            if total_leads > 0
            else 0,
            "conversion_rate": round((converted_leads / total_leads * 100), 2)
            if total_leads > 0
            else 0,
        }

    async def calculate_conversion_rate(
        self, start_date: datetime = None, end_date: datetime = None
    ) -> Dict[str, Any]:
        """Calculate conversion rates"""
        query = select(Lead)
        if start_date:
            query = query.where(Lead.created_at >= start_date)
        if end_date:
            query = query.where(Lead.created_at <= end_date)

        result = await self.db.execute(query)
        leads = result.scalars().all()

        total = len(leads)
        converted = sum(1 for lead in leads if lead.status == LeadStatus.CONVERTED)

        return {
            "total_leads": total,
            "converted_leads": converted,
            "conversion_rate": round((converted / total * 100), 2) if total > 0 else 0,
            "period": {
                "start": start_date.isoformat() if start_date else None,
                "end": end_date.isoformat() if end_date else None,
            },
        }

    async def get_lead_sources_breakdown(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get lead distribution by source"""
        start_date = datetime.now() - timedelta(days=days)

        result = await self.db.execute(
            select(Lead.source, func.count(Lead.id).label("count"))
            .where(Lead.created_at >= start_date)
            .group_by(Lead.source)
        )

        sources = []
        for row in result:
            sources.append({"source": row[0], "count": row[1]})

        return sources

    async def get_top_campaigns(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top performing campaigns"""
        result = await self.db.execute(
            select(
                Lead.campaign,
                func.count(Lead.id).label("total_leads"),
                func.sum(func.cast(Lead.is_qualified, func.Integer)).label(
                    "qualified_leads"
                ),
                func.avg(Lead.lead_score).label("avg_score"),
            )
            .where(Lead.campaign.isnot(None))
            .group_by(Lead.campaign)
            .order_by(func.count(Lead.id).desc())
            .limit(limit)
        )

        campaigns = []
        for row in result:
            campaigns.append(
                {
                    "campaign": row[0],
                    "total_leads": row[1],
                    "qualified_leads": row[2] or 0,
                    "avg_score": round(float(row[3]), 2) if row[3] else 0,
                }
            )

        return campaigns
