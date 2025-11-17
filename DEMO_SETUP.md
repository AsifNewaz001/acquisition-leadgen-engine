# Demo Setup with ngrok

This guide shows how to demo the Lead Generation Engine to your business team using ngrok.

## What is ngrok?

ngrok creates a secure tunnel from a public URL to your local development server, perfect for demos and testing webhooks.

## Prerequisites

1. Install ngrok: https://ngrok.com/download
2. Sign up for free account (optional but recommended): https://dashboard.ngrok.com/signup
3. Have the application running locally

## Quick Setup

### Step 1: Start the Application

#### Option A: Using Docker (Recommended)
```bash
# Start all services
docker-compose up -d

# Check if running
docker-compose ps

# View logs
docker-compose logs -f api
```

#### Option B: Local Development
```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Start the application
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Or use Make
make run
```

### Step 2: Start ngrok Tunnel

In a new terminal:

```bash
# Basic tunnel (HTTP only)
ngrok http 8000

# With custom subdomain (requires paid plan)
ngrok http 8000 --subdomain=yourcompany-leadgen

# With authentication (recommended for demos)
ngrok http 8000 --basic-auth="demo:password123"
```

### Step 3: Access Your Public URL

ngrok will display something like:
```
Forwarding   https://abc123.ngrok.io -> http://localhost:8000
```

Your demo URLs:
- **API Docs**: `https://abc123.ngrok.io/docs`
- **API Root**: `https://abc123.ngrok.io/`
- **Health Check**: `https://abc123.ngrok.io/health`

## Update CORS Settings

To allow ngrok URLs, update your `.env`:

```bash
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000,https://abc123.ngrok.io,https://*.ngrok.io
```

Or update `app/core/config.py` to allow all origins (for demo only):

```python
ALLOWED_ORIGINS: List[str] = ["*"]  # WARNING: Demo only!
```

Restart the application after changes.

## Demo Checklist

### Before the Demo

- [ ] Start PostgreSQL and Redis (if not using Docker)
- [ ] Start the FastAPI application
- [ ] Start ngrok tunnel
- [ ] Copy the ngrok URL
- [ ] Test the URL in browser
- [ ] Prepare sample data/demo script

### Demo Flow Suggestions

#### 1. Show Interactive API Docs
- Navigate to `https://your-ngrok-url/docs`
- Demonstrate the Swagger UI
- Show all available endpoints organized by category

#### 2. Create a Lead (Live Demo)
```bash
# Use the "Try it out" button in Swagger UI, or use curl:
curl -X POST "https://your-ngrok-url/api/v1/leads" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo@businessclient.com",
    "first_name": "John",
    "last_name": "Doe",
    "job_title": "CEO",
    "source": "website",
    "campaign": "Q1-2025-Demo"
  }'
```

#### 3. Show Lead Scoring
```bash
# Calculate score for the created lead
curl -X POST "https://your-ngrok-url/api/v1/leads/1/score"
```

#### 4. Demonstrate Enrichment
```bash
# Enrich by email
curl -X POST "https://your-ngrok-url/api/v1/enrichment/email" \
  -H "Content-Type: application/json" \
  -d '{"email": "ceo@apple.com"}'
```

#### 5. Show Analytics Dashboard
```bash
# Get dashboard stats
curl "https://your-ngrok-url/api/v1/analytics/dashboard?days=30"
```

#### 6. Simulate Webhook (Form Submission)
```bash
curl -X POST "https://your-ngrok-url/api/v1/webhooks/form-submission" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "webhook-lead@example.com",
    "first_name": "Jane",
    "last_name": "Smith",
    "form_name": "Contact Form",
    "utm_source": "google",
    "utm_campaign": "demo-campaign"
  }'
```

## Using Postman for Better Demos

### Import API to Postman

1. Open Postman
2. Go to your ngrok URL: `https://your-ngrok-url/openapi.json`
3. Copy the JSON
4. In Postman: Import > Raw Text > Paste JSON
5. Create a collection with pre-configured requests

### Sample Postman Collection

Create these requests in a collection:

**Environment Variables:**
- `BASE_URL`: `https://your-ngrok-url.ngrok.io`

**Requests:**
1. Health Check - `GET {{BASE_URL}}/health`
2. Create Lead - `POST {{BASE_URL}}/api/v1/leads`
3. Get All Leads - `GET {{BASE_URL}}/api/v1/leads`
4. Score Lead - `POST {{BASE_URL}}/api/v1/leads/1/score`
5. Dashboard Stats - `GET {{BASE_URL}}/api/v1/analytics/dashboard`

## Seed Demo Data

Create sample leads before the demo:

```bash
# Create a script or use the API to seed data
python scripts/seed_demo_data.py
```

## ngrok Pro Features (Optional)

If you have ngrok Pro:

```bash
# Custom domain
ngrok http 8000 --hostname=leadgen.yourcompany.com

# Reserved subdomain
ngrok http 8000 --subdomain=leadgen-demo

# IP restrictions
ngrok http 8000 --cidr-allow=1.2.3.4/32
```

## Troubleshooting

### ngrok URL not accessible
- Check firewall settings
- Ensure app is running on correct port
- Verify ngrok tunnel is active

### CORS errors in browser
- Update ALLOWED_ORIGINS in .env
- Restart FastAPI application

### Database not initialized
```bash
# Run migrations
alembic upgrade head

# Or with Docker
docker-compose exec api alembic upgrade head
```

### Can't connect to PostgreSQL/Redis
```bash
# Using Docker
docker-compose up -d postgres redis

# Check status
docker-compose ps
```

## Security Notes for Demos

1. **Use temporary data** - Don't use real customer data
2. **Enable authentication** - Use ngrok's `--basic-auth` flag
3. **Time-limited** - Free ngrok URLs expire after inactivity
4. **Monitor access** - ngrok shows all requests in terminal
5. **Disable after demo** - Stop ngrok tunnel when done

## Advanced: Share-able Demo Link

Create a one-pager for your team:

```
🚀 Lead Generation Engine Demo

📍 API Documentation: https://your-ngrok-url/docs
📊 Health Check: https://your-ngrok-url/health

🔐 Auth (if enabled):
Username: demo
Password: password123

📝 Test Credentials:
- Use any email format
- Try different job titles (CEO, CTO, Manager)
- Test different sources (website, referral, webinar)

📈 Key Features to Explore:
1. Create leads via /api/v1/leads
2. Automatic lead scoring (0-100)
3. Data enrichment by email/domain
4. Analytics dashboard
5. Webhook integrations
6. CRM sync capabilities
```

## Post-Demo

After the demo:
```bash
# Stop ngrok
Ctrl+C in ngrok terminal

# Stop application (Docker)
docker-compose down

# Or stop local server
Ctrl+C in application terminal
```

## Questions Your Business Team Might Ask

**Q: Can we integrate this with our website forms?**
A: Yes! Point forms to `POST /api/v1/webhooks/form-submission`

**Q: How does lead scoring work?**
A: Show them `app/services/scoring_service.py` - scores based on job title, email domain, source, etc.

**Q: Can we customize the scoring?**
A: Yes! The scoring rules are configurable in the ScoringService class.

**Q: What CRMs do you support?**
A: Currently HubSpot and Salesforce, with easy extensibility for others.

**Q: How do we track lead activity?**
A: Show the Activity model and timeline tracking features.

**Q: Is this production-ready?**
A: Yes! With proper configuration, security hardening, and deployment setup.

## Next Steps After Successful Demo

1. **Gather Feedback** - Note feature requests and concerns
2. **Customize** - Adjust scoring, add fields, customize workflows
3. **Deploy** - Set up production environment (AWS, GCP, Azure)
4. **Integrate** - Connect to actual CRM accounts and website
5. **Train** - Onboard team on API usage and features

---

**Pro Tip**: Record the demo session using Loom or similar for team members who couldn't attend!
