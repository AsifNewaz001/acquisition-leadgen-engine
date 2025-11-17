"""HubSpot CRM integration"""

from typing import Dict, Any
from hubspot import HubSpot
from hubspot.crm.contacts import SimplePublicObjectInputForCreate

from app.core.config import settings
from app.models.lead import Lead


class HubSpotIntegration:
    """Integration with HubSpot CRM"""

    def __init__(self):
        if not settings.HUBSPOT_API_KEY:
            raise ValueError("HubSpot API key not configured")
        self.client = HubSpot(access_token=settings.HUBSPOT_API_KEY)

    async def sync_lead(self, lead: Lead) -> Dict[str, Any]:
        """Sync lead to HubSpot as a contact"""
        try:
            # Prepare contact properties
            properties = {
                "email": lead.email,
                "firstname": lead.first_name,
                "lastname": lead.last_name,
                "phone": lead.phone,
                "jobtitle": lead.job_title,
                "hs_lead_status": self._map_lead_status(lead.status),
                "lead_source": lead.source,
                "lead_score": str(lead.lead_score),
            }

            # Remove None values
            properties = {k: v for k, v in properties.items() if v is not None}

            # Check if contact already exists
            if lead.hubspot_id:
                # Update existing contact
                contact = self.client.crm.contacts.basic_api.update(
                    contact_id=lead.hubspot_id, simple_public_object_input={"properties": properties}
                )
            else:
                # Create new contact
                contact_input = SimplePublicObjectInputForCreate(properties=properties)
                contact = self.client.crm.contacts.basic_api.create(
                    simple_public_object_input_for_create=contact_input
                )

            return {"id": contact.id, "status": "success"}

        except Exception as e:
            return {"error": str(e), "status": "failed"}

    async def get_contact(self, contact_id: str) -> Dict[str, Any]:
        """Get contact from HubSpot"""
        try:
            contact = self.client.crm.contacts.basic_api.get_by_id(contact_id=contact_id)
            return contact.to_dict()
        except Exception as e:
            return {"error": str(e)}

    async def create_deal(self, lead: Lead, deal_amount: float = None) -> Dict[str, Any]:
        """Create a deal in HubSpot associated with the lead"""
        try:
            deal_properties = {
                "dealname": f"Deal - {lead.email}",
                "pipeline": "default",
                "dealstage": "appointmentscheduled",
                "amount": str(deal_amount) if deal_amount else "0",
            }

            deal = self.client.crm.deals.basic_api.create(
                simple_public_object_input_for_create={"properties": deal_properties}
            )

            # Associate deal with contact
            if lead.hubspot_id:
                self.client.crm.deals.associations_api.create(
                    deal_id=deal.id,
                    to_object_type="contacts",
                    to_object_id=lead.hubspot_id,
                    association_type="deal_to_contact",
                )

            return {"id": deal.id, "status": "success"}

        except Exception as e:
            return {"error": str(e), "status": "failed"}

    def _map_lead_status(self, status: str) -> str:
        """Map internal lead status to HubSpot lead status"""
        status_mapping = {
            "new": "NEW",
            "contacted": "OPEN",
            "qualified": "IN_PROGRESS",
            "unqualified": "UNQUALIFIED",
            "converted": "CONNECTED",
            "lost": "UNQUALIFIED",
        }
        return status_mapping.get(status, "NEW")
