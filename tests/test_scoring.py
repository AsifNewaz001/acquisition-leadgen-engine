"""Tests for lead scoring service"""

import pytest
from app.services.scoring_service import ScoringService


@pytest.fixture
def scoring_service():
    """Create scoring service instance"""
    return ScoringService()


@pytest.mark.asyncio
async def test_score_calculation_ceo(scoring_service):
    """Test scoring for CEO with business email"""
    lead_data = {
        "email": "ceo@company.com",
        "job_title": "CEO",
        "source": "referral",
        "company_id": 1,
        "phone": "+1234567890",
        "linkedin_url": "https://linkedin.com/in/user",
    }
    score = await scoring_service.calculate_score(lead_data)
    assert score >= 50  # Should be high score


@pytest.mark.asyncio
async def test_score_calculation_low(scoring_service):
    """Test scoring for low-value lead"""
    lead_data = {
        "email": "user@gmail.com",
        "job_title": "Student",
        "source": "cold_outreach",
    }
    score = await scoring_service.calculate_score(lead_data)
    assert score < 30  # Should be low score


@pytest.mark.asyncio
async def test_score_breakdown(scoring_service):
    """Test getting score breakdown"""
    lead_data = {
        "email": "cto@company.com",
        "job_title": "CTO",
        "source": "webinar",
        "company_id": 1,
    }
    breakdown = scoring_service.get_score_breakdown(lead_data)
    assert isinstance(breakdown, dict)
    assert "job_title" in breakdown
    assert breakdown["job_title"] == 15  # CTO should get 15 points


@pytest.mark.asyncio
async def test_free_email_penalty(scoring_service):
    """Test that free emails get lower scores"""
    business_lead = {
        "email": "john@company.com",
        "job_title": "Manager",
        "source": "website",
    }
    free_email_lead = {
        "email": "john@gmail.com",
        "job_title": "Manager",
        "source": "website",
    }

    business_score = await scoring_service.calculate_score(business_lead)
    free_score = await scoring_service.calculate_score(free_email_lead)

    assert business_score > free_score
