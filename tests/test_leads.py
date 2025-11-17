"""Tests for lead management endpoints"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_create_lead(client: AsyncClient, sample_lead_data):
    """Test creating a new lead"""
    response = await client.post("/api/v1/leads", json=sample_lead_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == sample_lead_data["email"]
    assert data["first_name"] == sample_lead_data["first_name"]
    assert "id" in data
    assert data["status"] == "new"
    assert data["lead_score"] >= 0


@pytest.mark.asyncio
async def test_get_leads(client: AsyncClient, sample_lead_data):
    """Test getting all leads"""
    # Create a lead first
    await client.post("/api/v1/leads", json=sample_lead_data)

    # Get all leads
    response = await client.get("/api/v1/leads")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


@pytest.mark.asyncio
async def test_get_lead_by_id(client: AsyncClient, sample_lead_data):
    """Test getting a specific lead by ID"""
    # Create a lead
    create_response = await client.post("/api/v1/leads", json=sample_lead_data)
    lead_id = create_response.json()["id"]

    # Get the lead
    response = await client.get(f"/api/v1/leads/{lead_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == lead_id
    assert data["email"] == sample_lead_data["email"]


@pytest.mark.asyncio
async def test_get_nonexistent_lead(client: AsyncClient):
    """Test getting a lead that doesn't exist"""
    response = await client.get("/api/v1/leads/99999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_lead(client: AsyncClient, sample_lead_data):
    """Test updating a lead"""
    # Create a lead
    create_response = await client.post("/api/v1/leads", json=sample_lead_data)
    lead_id = create_response.json()["id"]

    # Update the lead
    update_data = {"first_name": "Jane", "status": "contacted"}
    response = await client.put(f"/api/v1/leads/{lead_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Jane"
    assert data["status"] == "contacted"


@pytest.mark.asyncio
async def test_delete_lead(client: AsyncClient, sample_lead_data):
    """Test deleting a lead"""
    # Create a lead
    create_response = await client.post("/api/v1/leads", json=sample_lead_data)
    lead_id = create_response.json()["id"]

    # Delete the lead
    response = await client.delete(f"/api/v1/leads/{lead_id}")
    assert response.status_code == 204

    # Verify it's deleted
    get_response = await client.get(f"/api/v1/leads/{lead_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_duplicate_email(client: AsyncClient, sample_lead_data):
    """Test creating leads with duplicate emails"""
    # Create first lead
    response1 = await client.post("/api/v1/leads", json=sample_lead_data)
    assert response1.status_code == 201

    # Try to create lead with same email
    response2 = await client.post("/api/v1/leads", json=sample_lead_data)
    # Should fail due to unique email constraint
    assert response2.status_code in [400, 409, 422]


@pytest.mark.asyncio
async def test_lead_scoring(client: AsyncClient, sample_lead_data):
    """Test lead scoring calculation"""
    # Create a lead with high-value attributes
    high_value_lead = {
        **sample_lead_data,
        "job_title": "CEO",
        "source": "referral",
    }
    response = await client.post("/api/v1/leads", json=high_value_lead)
    data = response.json()

    # CEO + referral should score high
    assert data["lead_score"] > 30
