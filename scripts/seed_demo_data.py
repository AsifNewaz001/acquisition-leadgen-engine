"""Seed demo data for business presentations"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal, engine, Base
from app.models.lead import Lead, LeadStatus, LeadSource
from app.models.company import Company


async def create_demo_companies(db: AsyncSession):
    """Create demo companies"""
    companies = [
        Company(
            name="TechCorp Inc",
            domain="techcorp.com",
            industry="Technology",
            size="51-200",
            country="United States",
            city="San Francisco",
        ),
        Company(
            name="FinanceHub",
            domain="financehub.com",
            industry="Financial Services",
            size="201-500",
            country="United States",
            city="New York",
        ),
        Company(
            name="HealthPlus",
            domain="healthplus.com",
            industry="Healthcare",
            size="11-50",
            country="United Kingdom",
            city="London",
        ),
    ]

    for company in companies:
        db.add(company)
    await db.commit()

    print(f"✅ Created {len(companies)} demo companies")
    return companies


async def create_demo_leads(db: AsyncSession, companies):
    """Create demo leads"""
    leads = [
        # High-value leads
        Lead(
            first_name="John",
            last_name="Smith",
            email="john.smith@techcorp.com",
            phone="+1-555-0101",
            job_title="CEO",
            company_id=companies[0].id,
            source=LeadSource.REFERRAL,
            campaign="Enterprise Q1 2025",
            status=LeadStatus.QUALIFIED,
            lead_score=95,
            is_qualified=True,
            linkedin_url="https://linkedin.com/in/johnsmith",
            location="San Francisco, CA",
        ),
        Lead(
            first_name="Sarah",
            last_name="Johnson",
            email="sarah.j@financehub.com",
            phone="+1-555-0102",
            job_title="CTO",
            company_id=companies[1].id,
            source=LeadSource.WEBINAR,
            campaign="Tech Leaders Webinar",
            status=LeadStatus.CONTACTED,
            lead_score=88,
            is_qualified=True,
            linkedin_url="https://linkedin.com/in/sarahjohnson",
            location="New York, NY",
        ),
        # Medium-value leads
        Lead(
            first_name="Michael",
            last_name="Brown",
            email="m.brown@healthplus.com",
            phone="+44-20-1234-5678",
            job_title="Director of Operations",
            company_id=companies[2].id,
            source=LeadSource.LANDING_PAGE,
            campaign="Healthcare Summit 2025",
            status=LeadStatus.NEW,
            lead_score=72,
            is_qualified=True,
            location="London, UK",
        ),
        Lead(
            first_name="Emily",
            last_name="Davis",
            email="emily.davis@startup.io",
            job_title="VP of Marketing",
            source=LeadSource.SOCIAL_MEDIA,
            campaign="LinkedIn Campaign",
            status=LeadStatus.CONTACTED,
            lead_score=65,
            location="Austin, TX",
        ),
        Lead(
            first_name="David",
            last_name="Wilson",
            email="david.w@company.com",
            job_title="Product Manager",
            source=LeadSource.WEBSITE,
            campaign="Organic Traffic",
            status=LeadStatus.NEW,
            lead_score=58,
            location="Seattle, WA",
        ),
        # Lower-value leads
        Lead(
            first_name="Jessica",
            last_name="Martinez",
            email="jess.martinez@gmail.com",
            job_title="Marketing Coordinator",
            source=LeadSource.COLD_OUTREACH,
            campaign="Cold Email Q1",
            status=LeadStatus.NEW,
            lead_score=35,
            location="Chicago, IL",
        ),
        Lead(
            first_name="Robert",
            last_name="Taylor",
            email="robert.t@hotmail.com",
            job_title="Sales Representative",
            source=LeadSource.WEBSITE,
            campaign="Blog Readers",
            status=LeadStatus.NEW,
            lead_score=28,
        ),
        # Recent conversions
        Lead(
            first_name="Lisa",
            last_name="Anderson",
            email="l.anderson@enterprise.com",
            phone="+1-555-0199",
            job_title="VP of Sales",
            source=LeadSource.REFERRAL,
            campaign="Partner Referral",
            status=LeadStatus.CONVERTED,
            lead_score=92,
            is_qualified=True,
            linkedin_url="https://linkedin.com/in/lisaanderson",
            location="Boston, MA",
        ),
        Lead(
            first_name="James",
            last_name="Thomas",
            email="james@techstartup.co",
            phone="+1-555-0150",
            job_title="Founder",
            source=LeadSource.WEBINAR,
            campaign="Startup Founders Event",
            status=LeadStatus.CONVERTED,
            lead_score=87,
            is_qualified=True,
            location="San Francisco, CA",
        ),
    ]

    for lead in leads:
        db.add(lead)
    await db.commit()

    print(f"✅ Created {len(leads)} demo leads")
    print("\n📊 Lead Distribution:")
    print(f"   - High Score (80+): {sum(1 for l in leads if l.lead_score >= 80)}")
    print(f"   - Medium Score (60-79): {sum(1 for l in leads if 60 <= l.lead_score < 80)}")
    print(f"   - Low Score (<60): {sum(1 for l in leads if l.lead_score < 60)}")
    print(f"   - Qualified: {sum(1 for l in leads if l.is_qualified)}")
    print(f"   - Converted: {sum(1 for l in leads if l.status == LeadStatus.CONVERTED)}")


async def seed_demo_data():
    """Main function to seed demo data"""
    print("🌱 Seeding demo data...\n")

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create session and seed data
    async with AsyncSessionLocal() as db:
        try:
            # Create companies
            companies = await create_demo_companies(db)

            # Create leads
            await create_demo_leads(db, companies)

            print("\n✨ Demo data seeded successfully!")
            print("\n🚀 You can now start the API and demo to your team!")
            print("   - API Docs: http://localhost:8000/docs")
            print("   - Health: http://localhost:8000/health")

        except Exception as e:
            print(f"❌ Error seeding data: {e}")
            await db.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(seed_demo_data())
