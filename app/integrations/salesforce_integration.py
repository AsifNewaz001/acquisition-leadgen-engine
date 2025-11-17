"""Salesforce CRM integration"""

from typing import Dict, Any
from simple_salesforce import Salesforce

from app.core.config import settings
from app.models.lead import Lead


class SalesforceIntegration:
    """Integration with Salesforce CRM"""

    def __init__(self):
        if not all([settings.SALESFORCE_USERNAME, settings.SALESFORCE_PASSWORD]):
            raise ValueError("Salesforce credentials not configured")

        self.client = Salesforce(
            username=settings.SALESFORCE_USERNAME,
            password=settings.SALESFORCE_PASSWORD,
            security_token=settings.SALESFORCE_SECURITY_TOKEN,
        )

    async def sync_lead(self, lead: Lead) -> Dict[str, Any]:
        """Sync lead to Salesforce"""
        try:
            # Prepare lead data
            lead_data = {
                "Email": lead.email,
                "FirstName": lead.first_name,
                "LastName": lead.last_name or "Unknown",  # LastName is required
                "Phone": lead.phone,
                "Title": lead.job_title,
                "Company": lead.company.name if lead.company else "Unknown",
                "Status": self._map_lead_status(lead.status),
                "LeadSource": self._map_lead_source(lead.source),
                "Rating": self._calculate_rating(lead.lead_score),
            }

            # Remove None values
            lead_data = {k: v for k, v in lead_data.items() if v is not None}

            # Check if lead already exists
            if lead.salesforce_id:
                # Update existing lead
                self.client.Lead.update(lead.salesforce_id, lead_data)
                return {"id": lead.salesforce_id, "status": "updated"}
            else:
                # Create new lead
                result = self.client.Lead.create(lead_data)
                return {"id": result["id"], "status": "created"}

        except Exception as e:
            return {"error": str(e), "status": "failed"}

    async def get_lead(self, lead_id: str) -> Dict[str, Any]:
        """Get lead from Salesforce"""
        try:
            lead = self.client.Lead.get(lead_id)
            return dict(lead)
        except Exception as e:
            return {"error": str(e)}

    async def convert_lead(self, lead: Lead) -> Dict[str, Any]:
        """Convert Salesforce lead to Contact/Account/Opportunity"""
        try:
            if not lead.salesforce_id:
                return {"error": "Lead not synced to Salesforce"}

            # This requires the Salesforce SOAP API or REST API with specific endpoints
            # For now, we'll return a placeholder
            return {
                "status": "conversion_requires_additional_implementation",
                "message": "Lead conversion requires Salesforce SOAP API implementation",
            }

        except Exception as e:
            return {"error": str(e), "status": "failed"}

    async def create_opportunity(
        self, lead: Lead, opportunity_name: str, amount: float = None
    ) -> Dict[str, Any]:
        """Create an opportunity in Salesforce"""
        try:
            opportunity_data = {
                "Name": opportunity_name,
                "StageName": "Prospecting",
                "CloseDate": "2025-12-31",  # Example close date
                "Amount": amount,
            }

            if lead.salesforce_id:
                # If lead has been converted, link to Contact
                # This requires additional logic to get Contact ID
                pass

            result = self.client.Opportunity.create(opportunity_data)
            return {"id": result["id"], "status": "created"}

        except Exception as e:
            return {"error": str(e), "status": "failed"}

    def _map_lead_status(self, status: str) -> str:
        """Map internal lead status to Salesforce lead status"""
        status_mapping = {
            "new": "Open - Not Contacted",
            "contacted": "Working - Contacted",
            "qualified": "Qualified",
            "unqualified": "Unqualified",
            "converted": "Closed - Converted",
            "lost": "Closed - Not Converted",
        }
        return status_mapping.get(status, "Open - Not Contacted")

    def _map_lead_source(self, source: str) -> str:
        """Map internal lead source to Salesforce lead source"""
        source_mapping = {
            "website": "Web",
            "landing_page": "Web",
            "social_media": "Social Media",
            "referral": "Partner Referral",
            "cold_outreach": "Cold Call",
            "webinar": "Webinar",
            "chat_widget": "Web",
            "api": "Other",
            "manual": "Other",
        }
        return source_mapping.get(source, "Other")

    def _calculate_rating(self, lead_score: int) -> str:
        """Calculate Salesforce rating based on lead score"""
        if lead_score >= 80:
            return "Hot"
        elif lead_score >= 60:
            return "Warm"
        else:
            return "Cold"
