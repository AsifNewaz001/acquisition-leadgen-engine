# 🎬 Your Live Demo is Ready!

**Your ngrok URL:** https://kacie-marshy-unalleviatingly.ngrok-free.dev/

## 📋 Quick Links for Your Business Team

### Interactive Documentation
- **Swagger UI**: https://kacie-marshy-unalleviatingly.ngrok-free.dev/docs
- **ReDoc**: https://kacie-marshy-unalleviatingly.ngrok-free.dev/redoc
- **Health Check**: https://kacie-marshy-unalleviatingly.ngrok-free.dev/health

### Demo Resources Created
1. **Interactive HTML Demo Page**: `scripts/demo_page.html` - Open in browser for live testing
2. **Bash Demo Script**: `scripts/demo_script.sh` - Run automated demos
3. **Postman Collection**: `scripts/postman_collection.json` - Import into Postman

---

## 🚀 How to Use These Resources

### Option 1: Interactive HTML Demo (Best for Business Team) ⭐

**Open the demo page:**
```bash
open scripts/demo_page.html
# Or on Linux:
xdg-open scripts/demo_page.html
```

**Features:**
- ✅ Live statistics dashboard
- ✅ One-click API testing
- ✅ Beautiful UI with real-time responses
- ✅ No technical knowledge needed
- ✅ Perfect for screen sharing in meetings

**Host it online (optional):**
```bash
# Serve it locally and share via another ngrok tunnel
cd scripts
python3 -m http.server 8080

# In another terminal:
ngrok http 8080
# Share the HTML page URL with your team
```

---

### Option 2: Bash Script Demo (For Technical Demos)

**Make it executable:**
```bash
chmod +x scripts/demo_script.sh
```

**Run the demo:**
```bash
./scripts/demo_script.sh
```

**This will automatically:**
1. Test health check
2. Get API info
3. Fetch all leads
4. Create a new CEO lead
5. Calculate lead scores
6. Test enrichment
7. Simulate webhooks
8. Show analytics

Perfect for live terminal demos!

---

### Option 3: Postman Collection (For API Testing)

**Import to Postman:**
1. Open Postman
2. Click "Import"
3. Select `scripts/postman_collection.json`
4. All endpoints will be ready to use!

**The collection includes:**
- ✅ 20+ pre-configured requests
- ✅ Organized by category (Leads, Enrichment, Webhooks, Analytics)
- ✅ Sample request bodies
- ✅ Environment variable already set

---

## 🎯 Recommended Demo Flow

### For Non-Technical Stakeholders (Use HTML Page)

1. **Open** `scripts/demo_page.html` in browser
2. **Share screen** in video call
3. **Show live stats** at the top
4. **Click buttons** to demonstrate:
   - Create high-value lead (shows scoring)
   - View all leads (shows data)
   - Enrich email (shows data enrichment)
   - Webhook simulation (shows integrations)
   - Analytics (shows insights)

### For Technical Stakeholders (Use Swagger/Postman)

1. **Share** https://kacie-marshy-unalleviatingly.ngrok-free.dev/docs
2. **Demonstrate** API endpoints live
3. **Show** automatic documentation
4. **Explain** authentication, rate limiting, etc.

---

## 📧 Email Template for Your Team

```
Subject: Lead Generation Engine - Live Demo Access

Hi Team,

I've set up a live demo of our new Lead Generation Engine. You can test it right now!

🌐 Interactive Demo Page: [Attach or host demo_page.html]
📚 API Documentation: https://kacie-marshy-unalleviatingly.ngrok-free.dev/docs

Key Features to Try:
✅ Create leads with automatic scoring (0-100)
✅ Real-time data enrichment
✅ Analytics dashboard
✅ Webhook integrations
✅ CRM sync capabilities

The demo page has one-click buttons to test everything - no technical knowledge needed!

Let me know if you have any questions or feedback.

Best regards,
```

---

## 🎤 Presentation Script

**Slide 1: Introduction**
"Today I'm going to show you our new AI-powered Lead Generation Engine that automates lead capture, scoring, and qualification."

**Slide 2: Live Demo** *(Share screen with demo_page.html)*
"Let me show you this live. Here's our dashboard with real-time statistics..."

**[Click "Create High-Value Lead"]**
"When a lead comes in - let's say a CEO from a tech company - the system automatically scores them. Notice this lead got a score of 95 out of 100 because they're a CEO from a business email."

**[Click "View All Leads"]**
"Here are all our leads, sorted by recency, with their scores and status."

**[Click "Enrich Email"]**
"We can also enrich leads automatically. Just from an email address, we can pull company information..."

**[Click "Webhook Capture"]**
"This simulates a form submission from your website. The lead is captured instantly and automatically scored."

**[Click "View Analytics"]**
"And here's the analytics dashboard showing conversion rates, lead quality, and source performance."

**Slide 3: CRM Integration**
"All of this syncs automatically with HubSpot and Salesforce..."

**Slide 4: Q&A**

---

## 🔧 Troubleshooting

### If ngrok URL stops working:
```bash
# Restart ngrok
ngrok http 8000

# Update the URL in files (I can help with this if needed)
```

### If API returns errors:
```bash
# Check if services are running
make docker-up

# Check logs
make docker-logs
```

### If demo page doesn't load:
- Open `scripts/demo_page.html` directly in browser
- Check browser console for errors
- Ensure CORS is enabled (CORS_ALLOW_ALL=true in .env)

---

## 📊 Demo Statistics

Your seeded database includes:
- **9 leads** (3 high-value, 3 medium, 3 low)
- **3 companies** (Tech, Finance, Healthcare)
- **2 conversions** (22% conversion rate)
- **Multiple sources** (referral, webinar, website, etc.)

Perfect for showing realistic analytics!

---

## 🎁 Bonus: Screenshots/Recording

Consider recording your demo:
```bash
# Mac
# Use QuickTime Player > File > New Screen Recording

# Windows
# Windows Key + G (Game Bar)

# Linux
# Use SimpleScreenRecorder or OBS
```

Share the video with team members who can't attend live!

---

## 💡 Tips for a Great Demo

1. **Test first** - Run through everything yourself before the meeting
2. **Have backup** - Keep Postman ready in case HTML demo has issues
3. **Tell a story** - Show a lead journey from capture → scoring → conversion
4. **Show value** - Emphasize time saved, automation, insights gained
5. **Be interactive** - Let them suggest test cases (emails, names, etc.)

---

**Ready to impress? Your demo is live right now!** 🚀

Need me to customize anything? Just let me know!
