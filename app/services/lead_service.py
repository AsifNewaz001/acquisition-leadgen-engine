"""Lead service for business logic"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.models.lead import Lead, LeadStatus
from app.schemas.lead import LeadCreate, LeadUpdate
from app.services.scoring_service import ScoringService
from app.integrations.hubspot_integration import HubSpotIntegration
from app.integrations.salesforce_integration import SalesforceIntegration


class LeadService:
    """Service for lead management operations"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.scoring_service = ScoringService()

    async def create_lead(self, lead_data: LeadCreate) -> Lead:
        """Create a new lead"""
        lead = Lead(**lead_data.model_dump())

        # Calculate initial lead score
        lead.lead_score = await self.scoring_service.calculate_score(lead_data.model_dump())

        self.db.add(lead)
        await self.db.commit()
        await self.db.refresh(lead)
        return lead

    async def get_leads(self, skip: int = 0, limit: int = 100) -> List[Lead]:
        """Get all leads with pagination"""
        result = await self.db.execute(
            select(Lead).offset(skip).limit(limit).order_by(Lead.created_at.desc())
        )
        return result.scalars().all()

    async def get_lead(self, lead_id: int) -> Optional[Lead]:
        """Get a lead by ID"""
        result = await self.db.execute(select(Lead).where(Lead.id == lead_id))
        return result.scalar_one_or_none()

    async def update_lead(self, lead_id: int, lead_update: LeadUpdate) -> Optional[Lead]:
        """Update a lead"""
        lead = await self.get_lead(lead_id)
        if not lead:
            return None

        update_data = lead_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(lead, field, value)

        await self.db.commit()
        await self.db.refresh(lead)
        return lead

    async def delete_lead(self, lead_id: int) -> bool:
        """Delete a lead"""
        lead = await self.get_lead(lead_id)
        if not lead:
            return False

        await self.db.delete(lead)
        await self.db.commit()
        return True

    async def calculate_lead_score(self, lead_id: int) -> int:
        """Calculate and update lead score"""
        lead = await self.get_lead(lead_id)
        if not lead:
            return 0

        # Convert lead to dict for scoring
        lead_data = {
            "email": lead.email,
            "job_title": lead.job_title,
            "source": lead.source,
            "company_id": lead.company_id,
        }

        score = await self.scoring_service.calculate_score(lead_data)
        lead.lead_score = score
        lead.is_qualified = score >= 70  # Threshold for qualification

        await self.db.commit()
        return score

    async def sync_to_crm(self, lead_id: int, crm: str):
        """Sync lead to external CRM"""
        lead = await self.get_lead(lead_id)
        if not lead:
            return {"error": "Lead not found"}

        if crm.lower() == "hubspot":
            integration = HubSpotIntegration()
            result = await integration.sync_lead(lead)
            lead.hubspot_id = result.get("id")
        elif crm.lower() == "salesforce":
            integration = SalesforceIntegration()
            result = await integration.sync_lead(lead)
            lead.salesforce_id = result.get("id")
        else:
            return {"error": f"Unsupported CRM: {crm}"}

        await self.db.commit()
        return {"status": "success", "crm": crm, "external_id": result.get("id")}
