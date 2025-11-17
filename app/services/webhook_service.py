"""Webhook processing service"""

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

from app.models.lead import Lead, LeadSource
from app.models.activity import Activity, ActivityType
from app.services.lead_service import LeadService
from app.schemas.lead import LeadCreate


class WebhookService:
    """Service for processing incoming webhooks"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.lead_service = LeadService(db)

    async def process_form_submission(self, data: Dict[str, Any]) -> Lead:
        """Process form submission webhook"""
        # Extract lead data from form submission
        lead_data = LeadCreate(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            phone=data.get("phone"),
            job_title=data.get("job_title"),
            source=LeadSource.WEBSITE,
            campaign=data.get("campaign"),
            utm_source=data.get("utm_source"),
            utm_medium=data.get("utm_medium"),
            utm_campaign=data.get("utm_campaign"),
            notes=data.get("message"),
        )

        # Create lead
        lead = await self.lead_service.create_lead(lead_data)

        # Track activity
        activity = Activity(
            lead_id=lead.id,
            activity_type=ActivityType.FORM_SUBMISSION,
            title="Form Submitted",
            description=f"Form submission from {data.get('form_name', 'unknown form')}",
            ip_address=data.get("ip_address"),
            user_agent=data.get("user_agent"),
        )
        self.db.add(activity)
        await self.db.commit()

        return lead

    async def process_landing_page_conversion(self, data: Dict[str, Any]) -> Lead:
        """Process landing page conversion"""
        lead_data = LeadCreate(
            email=data.get("email"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            source=LeadSource.LANDING_PAGE,
            campaign=data.get("page_name"),
            utm_source=data.get("utm_source"),
            utm_medium=data.get("utm_medium"),
            utm_campaign=data.get("utm_campaign"),
        )

        lead = await self.lead_service.create_lead(lead_data)

        # Track page view activity
        activity = Activity(
            lead_id=lead.id,
            activity_type=ActivityType.PAGE_VIEW,
            title="Landing Page Conversion",
            description=f"Converted on {data.get('page_name', 'landing page')}",
            ip_address=data.get("ip_address"),
        )
        self.db.add(activity)
        await self.db.commit()

        return lead

    async def process_chat_conversation(self, data: Dict[str, Any]) -> Lead:
        """Process chat widget lead capture"""
        lead_data = LeadCreate(
            email=data.get("email"),
            first_name=data.get("name"),
            source=LeadSource.CHAT_WIDGET,
            notes=data.get("message"),
        )

        lead = await self.lead_service.create_lead(lead_data)

        # Track chat activity
        activity = Activity(
            lead_id=lead.id,
            activity_type=ActivityType.NOTE,
            title="Chat Conversation",
            description=f"Chat conversation: {data.get('message', '')[:100]}",
        )
        self.db.add(activity)
        await self.db.commit()

        return lead
