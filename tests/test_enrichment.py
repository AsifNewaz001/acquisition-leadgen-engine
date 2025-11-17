"""Tests for enrichment endpoints"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_enrich_by_email(client: AsyncClient):
    """Test email enrichment"""
    response = await client.post(
        "/api/v1/enrichment/email", json={"email": "test@example.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "domain" in data or data["domain"] is not None


@pytest.mark.asyncio
async def test_enrich_by_domain(client: AsyncClient):
    """Test domain enrichment"""
    response = await client.post(
        "/api/v1/enrichment/domain", json={"domain": "example.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["domain"] == "example.com"


@pytest.mark.asyncio
async def test_validate_email_valid(client: AsyncClient):
    """Test email validation with valid email"""
    response = await client.post(
        "/api/v1/enrichment/validate-email?email=valid@example.com"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_valid"] is True


@pytest.mark.asyncio
async def test_validate_email_invalid(client: AsyncClient):
    """Test email validation with invalid email"""
    response = await client.post("/api/v1/enrichment/validate-email?email=invalid-email")
    assert response.status_code == 200
    data = response.json()
    assert data["is_valid"] is False
