# Acquisition Lead Generation Engine

An AI-powered lead generation and customer acquisition engine built with Python, FastAPI, and PostgreSQL. This system captures, enriches, scores, and manages leads with seamless CRM integrations.

## Features

### Core Capabilities
- **Lead Capture** - Multi-channel lead ingestion (web forms, landing pages, chat widgets, API)
- **AI-Powered Enrichment** - Automatic data enrichment using email and domain lookups
- **Intelligent Lead Scoring** - ML-based scoring system to prioritize high-quality leads
- **CRM Integrations** - Bi-directional sync with HubSpot and Salesforce
- **Activity Tracking** - Complete timeline of lead interactions and engagement
- **Analytics Dashboard** - Real-time insights into conversion rates and performance
- **Webhook Support** - Real-time lead capture from external sources
- **Async Processing** - Background tasks with Celery for scalable operations

### Tech Stack
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL with async SQLAlchemy
- **Cache/Queue**: Redis + Celery
- **AI/ML**: OpenAI GPT, Anthropic Claude, LangChain
- **CRM**: HubSpot API, Salesforce API
- **Testing**: pytest, pytest-asyncio
- **Deployment**: Docker + Docker Compose

## Project Structure

```
acquisition-leadgen-engine/
├── app/
│   ├── api/                    # API endpoints
│   │   ├── leads.py           # Lead management routes
│   │   ├── enrichment.py      # Data enrichment routes
│   │   ├── webhooks.py        # Webhook handlers
│   │   └── analytics.py       # Analytics endpoints
│   ├── core/                   # Core configurations
│   │   ├── config.py          # Settings and environment
│   │   └── database.py        # Database connection
│   ├── models/                 # SQLAlchemy models
│   │   ├── lead.py            # Lead model
│   │   ├── company.py         # Company model
│   │   └── activity.py        # Activity tracking
│   ├── schemas/                # Pydantic schemas
│   │   ├── lead.py            # Lead validation schemas
│   │   └── enrichment.py      # Enrichment schemas
│   ├── services/               # Business logic
│   │   ├── lead_service.py    # Lead operations
│   │   ├── enrichment_service.py  # Data enrichment
│   │   ├── scoring_service.py     # Lead scoring
│   │   ├── webhook_service.py     # Webhook processing
│   │   └── analytics_service.py   # Analytics
│   ├── integrations/           # External integrations
│   │   ├── hubspot_integration.py   # HubSpot CRM
│   │   └── salesforce_integration.py # Salesforce CRM
│   └── main.py                 # Application entry point
├── tests/                      # Test suite
├── alembic/                    # Database migrations
├── config/                     # Configuration files
├── docker-compose.yml          # Docker orchestration
├── Dockerfile                  # Container definition
├── requirements.txt            # Python dependencies
├── pyproject.toml             # Poetry configuration
├── Makefile                   # Development commands
└── README.md                  # This file
```

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (optional but recommended)

### Installation

#### Option 1: Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/AsifNewaz001/acquisition-leadgen-engine.git
cd acquisition-leadgen-engine
```

2. Copy environment file:
```bash
cp .env.example .env
```

3. Update `.env` with your API keys and configuration

4. Start all services:
```bash
make docker-up
# or
docker-compose up -d
```

5. Access the API:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

#### Option 2: Local Development

1. Clone and setup:
```bash
git clone https://github.com/AsifNewaz001/acquisition-leadgen-engine.git
cd acquisition-leadgen-engine
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Setup environment:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Start PostgreSQL and Redis (ensure they're running)

6. Run migrations:
```bash
make migrate
# or
alembic upgrade head
```

7. Start the application:
```bash
make run
# or
uvicorn app.main:app --reload
```

## API Documentation

### Interactive API Docs
Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Key Endpoints

#### Leads Management
```bash
# Create a lead
POST /api/v1/leads
{
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "source": "website",
  "campaign": "Q1-2025-Campaign"
}

# Get all leads
GET /api/v1/leads?skip=0&limit=100

# Get specific lead
GET /api/v1/leads/{lead_id}

# Update lead
PUT /api/v1/leads/{lead_id}

# Calculate lead score
POST /api/v1/leads/{lead_id}/score

# Sync to CRM
POST /api/v1/leads/{lead_id}/sync/hubspot
POST /api/v1/leads/{lead_id}/sync/salesforce
```

#### Data Enrichment
```bash
# Enrich by email
POST /api/v1/enrichment/email
{
  "email": "john@example.com"
}

# Enrich by domain
POST /api/v1/enrichment/domain
{
  "domain": "example.com"
}

# Validate email
POST /api/v1/enrichment/validate-email?email=john@example.com
```

#### Webhooks
```bash
# Form submission
POST /api/v1/webhooks/form-submission

# Landing page conversion
POST /api/v1/webhooks/landing-page

# Chat widget
POST /api/v1/webhooks/chat-widget
```

#### Analytics
```bash
# Dashboard stats
GET /api/v1/analytics/dashboard?days=30

# Conversion rate
GET /api/v1/analytics/conversion-rate

# Lead sources breakdown
GET /api/v1/analytics/lead-sources?days=30

# Top campaigns
GET /api/v1/analytics/top-performing-campaigns?limit=10
```

## Configuration

### Environment Variables

Key configuration options in `.env`:

```bash
# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/leadgen

# Security
SECRET_KEY=your-secret-key-change-in-production

# AI Services
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# CRM Integration
HUBSPOT_API_KEY=your-hubspot-key
SALESFORCE_USERNAME=your-sf-username
SALESFORCE_PASSWORD=your-sf-password
SALESFORCE_SECURITY_TOKEN=your-sf-token

# Data Enrichment (Optional)
CLEARBIT_API_KEY=your-clearbit-key
HUNTER_API_KEY=your-hunter-key

# Lead Scoring
LEAD_SCORE_THRESHOLD=70
```

## Development

### Useful Commands

```bash
# Run tests
make test

# Run linters
make lint

# Format code
make format

# Create database migration
make migrate-create

# Run migrations
make migrate

# Rollback migration
make migrate-rollback

# Start Celery worker
make celery-worker

# Start Celery beat
make celery-beat

# View Docker logs
make docker-logs

# Clean project
make clean
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_leads.py -v
```

## Lead Scoring Algorithm

The scoring system evaluates leads based on:

- **Job Title** (0-15 points) - Executive roles score higher
- **Email Domain** (0-10 points) - Business emails vs free emails
- **Lead Source** (0-20 points) - Referrals score highest
- **Company Association** (15 points) - Has linked company
- **Contact Info** (5 points) - Provided phone number
- **Social Profiles** (8 points) - LinkedIn profile available

**Total Score**: 0-100 (leads ≥70 are auto-qualified)

## CRM Integrations

### HubSpot
- Automatic contact sync
- Deal creation
- Activity logging
- Bi-directional updates

### Salesforce
- Lead creation/update
- Opportunity management
- Lead conversion
- Custom field mapping

## Deployment

### Production Considerations

1. **Security**
   - Change `SECRET_KEY` in production
   - Use strong database passwords
   - Enable HTTPS/TLS
   - Implement rate limiting

2. **Scaling**
   - Use managed PostgreSQL (AWS RDS, Google Cloud SQL)
   - Deploy multiple API instances behind load balancer
   - Scale Celery workers horizontally
   - Use Redis cluster for high availability

3. **Monitoring**
   - Configure Sentry for error tracking
   - Set up application metrics
   - Monitor database performance
   - Track API response times

### Docker Production

```bash
# Build production image
docker build -t leadgen-api:latest .

# Run with production settings
docker-compose -f docker-compose.prod.yml up -d
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Testing

The project includes comprehensive tests:

```bash
# Run all tests
make test

# Run with coverage report
pytest --cov=app --cov-report=html --cov-report=term

# Open coverage report
open htmlcov/index.html
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/AsifNewaz001/acquisition-leadgen-engine/issues
- Documentation: See `/docs` endpoint when running

## Roadmap

- [ ] Email campaign integration (SendGrid, Mailgun)
- [ ] SMS outreach (Twilio)
- [ ] LinkedIn integration
- [ ] Advanced AI-powered lead qualification
- [ ] Automated lead nurturing workflows
- [ ] A/B testing for campaigns
- [ ] Multi-language support
- [ ] GraphQL API
- [ ] Mobile app for lead management

## Credits

Built with ❤️ using:
- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis
- Celery
- OpenAI
- HubSpot API
- Salesforce API

---

**Note**: This is a production-ready foundation. Customize based on your specific requirements and integrate with your existing systems.
