"""Lead scoring service"""

from typing import Dict, Any


class ScoringService:
    """Service for calculating lead scores"""

    def __init__(self):
        # Define scoring rules
        self.scoring_rules = {
            "job_title": {
                "keywords": {
                    "ceo": 15,
                    "cto": 15,
                    "founder": 15,
                    "director": 12,
                    "manager": 10,
                    "vp": 12,
                    "head": 10,
                    "lead": 8,
                },
                "max_score": 15,
            },
            "email_domain": {
                "business": 10,  # Non-free email
                "free": 0,  # Gmail, Yahoo, etc.
            },
            "source": {
                "referral": 20,
                "webinar": 15,
                "landing_page": 12,
                "website": 10,
                "social_media": 8,
                "cold_outreach": 5,
            },
            "company_size": {
                "enterprise": 20,
                "medium": 15,
                "small": 10,
                "startup": 5,
            },
        }

    async def calculate_score(self, lead_data: Dict[str, Any]) -> int:
        """Calculate lead score based on various factors"""
        score = 0

        # Score based on job title
        job_title = lead_data.get("job_title", "").lower()
        for keyword, points in self.scoring_rules["job_title"]["keywords"].items():
            if keyword in job_title:
                score += points
                break  # Only count the highest matching keyword

        # Score based on email domain
        email = lead_data.get("email", "")
        if email:
            domain = email.split("@")[1] if "@" in email else ""
            free_domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]
            if domain not in free_domains and domain:
                score += self.scoring_rules["email_domain"]["business"]

        # Score based on source
        source = lead_data.get("source", "")
        if source:
            score += self.scoring_rules["source"].get(source, 5)

        # Score based on company
        if lead_data.get("company_id"):
            score += 15  # Has associated company

        # Additional engagement factors
        if lead_data.get("phone"):
            score += 5  # Provided phone number

        if lead_data.get("linkedin_url"):
            score += 8  # Has LinkedIn profile

        # Cap score at 100
        return min(score, 100)

    def get_score_breakdown(self, lead_data: Dict[str, Any]) -> Dict[str, int]:
        """Get detailed breakdown of score calculation"""
        breakdown = {}

        # Job title score
        job_title = lead_data.get("job_title", "").lower()
        for keyword, points in self.scoring_rules["job_title"]["keywords"].items():
            if keyword in job_title:
                breakdown["job_title"] = points
                break

        # Email domain score
        email = lead_data.get("email", "")
        if email:
            domain = email.split("@")[1] if "@" in email else ""
            free_domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]
            if domain not in free_domains and domain:
                breakdown["email_domain"] = self.scoring_rules["email_domain"]["business"]

        # Source score
        source = lead_data.get("source", "")
        if source:
            breakdown["source"] = self.scoring_rules["source"].get(source, 5)

        # Company score
        if lead_data.get("company_id"):
            breakdown["company"] = 15

        # Additional fields
        if lead_data.get("phone"):
            breakdown["phone"] = 5
        if lead_data.get("linkedin_url"):
            breakdown["linkedin"] = 8

        return breakdown
