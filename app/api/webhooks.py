"""Webhook endpoints for lead capture"""

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.webhook_service import WebhookService

router = APIRouter()


@router.post("/form-submission")
async def handle_form_submission(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Handle form submission webhook"""
    data = await request.json()
    service = WebhookService(db)
    lead = await service.process_form_submission(data)
    return {"status": "success", "lead_id": lead.id}


@router.post("/landing-page")
async def handle_landing_page(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Handle landing page conversion"""
    data = await request.json()
    service = WebhookService(db)
    lead = await service.process_landing_page_conversion(data)
    return {"status": "success", "lead_id": lead.id}


@router.post("/chat-widget")
async def handle_chat_widget(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Handle chat widget lead capture"""
    data = await request.json()
    service = WebhookService(db)
    lead = await service.process_chat_conversation(data)
    return {"status": "success", "lead_id": lead.id}
