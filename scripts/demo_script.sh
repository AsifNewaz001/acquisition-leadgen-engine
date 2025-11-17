#!/bin/bash

# Lead Generation Engine - Live Demo Script
# ngrok URL: https://kacie-marshy-unalleviatingly.ngrok-free.dev

NGROK_URL="https://kacie-marshy-unalleviatingly.ngrok-free.dev"

echo "🚀 Lead Generation Engine - Live Demo"
echo "====================================="
echo ""

# Test 1: Health Check
echo "1️⃣  Testing Health Check..."
curl -s "$NGROK_URL/health" | jq '.'
echo ""
echo "---"
echo ""

# Test 2: Get API Info
echo "2️⃣  Getting API Information..."
curl -s "$NGROK_URL/" | jq '.'
echo ""
echo "---"
echo ""

# Test 3: Get All Leads
echo "3️⃣  Fetching All Leads..."
curl -s "$NGROK_URL/api/v1/leads?limit=5" | jq '.'
echo ""
echo "---"
echo ""

# Test 4: Create a New Lead
echo "4️⃣  Creating New Lead (Demo CEO)..."
curl -s -X POST "$NGROK_URL/api/v1/leads" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo.ceo@techstartup.com",
    "first_name": "Alex",
    "last_name": "Johnson",
    "job_title": "CEO",
    "phone": "+1-555-9999",
    "source": "referral",
    "campaign": "Live Demo Q1 2025",
    "linkedin_url": "https://linkedin.com/in/alexjohnson"
  }' | jq '.'
echo ""
echo "---"
echo ""

# Test 5: Get Lead by ID (using ID 1)
echo "5️⃣  Fetching Specific Lead (ID: 1)..."
curl -s "$NGROK_URL/api/v1/leads/1" | jq '.'
echo ""
echo "---"
echo ""

# Test 6: Calculate Lead Score
echo "6️⃣  Calculating Lead Score (ID: 1)..."
curl -s -X POST "$NGROK_URL/api/v1/leads/1/score" | jq '.'
echo ""
echo "---"
echo ""

# Test 7: Email Enrichment
echo "7️⃣  Testing Email Enrichment..."
curl -s -X POST "$NGROK_URL/api/v1/enrichment/email" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "ceo@apple.com"
  }' | jq '.'
echo ""
echo "---"
echo ""

# Test 8: Domain Enrichment
echo "8️⃣  Testing Domain Enrichment..."
curl -s -X POST "$NGROK_URL/api/v1/enrichment/domain" \
  -H "Content-Type: application/json" \
  -d '{
    "domain": "microsoft.com"
  }' | jq '.'
echo ""
echo "---"
echo ""

# Test 9: Webhook - Form Submission
echo "9️⃣  Simulating Form Submission Webhook..."
curl -s -X POST "$NGROK_URL/api/v1/webhooks/form-submission" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "webhook.test@business.com",
    "first_name": "Sarah",
    "last_name": "Williams",
    "phone": "+1-555-7777",
    "job_title": "VP of Sales",
    "form_name": "Contact Form",
    "utm_source": "google",
    "utm_medium": "cpc",
    "utm_campaign": "demo-campaign"
  }' | jq '.'
echo ""
echo "---"
echo ""

# Test 10: Analytics Dashboard
echo "🔟 Getting Dashboard Analytics (Last 30 Days)..."
curl -s "$NGROK_URL/api/v1/analytics/dashboard?days=30" | jq '.'
echo ""
echo "---"
echo ""

# Test 11: Lead Sources Breakdown
echo "1️⃣1️⃣  Getting Lead Sources Breakdown..."
curl -s "$NGROK_URL/api/v1/analytics/lead-sources?days=30" | jq '.'
echo ""
echo "---"
echo ""

# Test 12: Top Performing Campaigns
echo "1️⃣2️⃣  Getting Top Performing Campaigns..."
curl -s "$NGROK_URL/api/v1/analytics/top-performing-campaigns?limit=5" | jq '.'
echo ""
echo "---"
echo ""

echo "✅ Demo Complete!"
echo ""
echo "📍 Interactive API Docs: $NGROK_URL/docs"
echo "📍 Alternative Docs: $NGROK_URL/redoc"
echo ""
