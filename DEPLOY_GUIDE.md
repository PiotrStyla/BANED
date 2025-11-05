# 🚀 Deploy BANED API - 24/7 Online Guide

Complete guide to deploy your BANED Fake News Detection API to run 24/7 online.

---

## 🎯 Quick Comparison

| Platform | Free Tier | Setup Time | Difficulty | Best For |
|----------|-----------|------------|------------|----------|
| **Render** | ✅ Yes | 5 min | ⭐ Easy | Beginners |
| **Railway** | ✅ Yes | 5 min | ⭐ Easy | Quick deploy |
| **Heroku** | ⚠️ Limited | 10 min | ⭐⭐ Medium | Traditional |
| **AWS Lambda** | ✅ Yes | 20 min | ⭐⭐⭐ Hard | Serverless |
| **Google Cloud Run** | ✅ Yes | 15 min | ⭐⭐ Medium | Auto-scaling |
| **DigitalOcean** | ❌ No | 30 min | ⭐⭐⭐ Hard | Full control |

---

## 🌟 Option A: Render.com (RECOMMENDED)

**Why:** Free tier, automatic HTTPS, easy setup, perfect for APIs

### Step 1: Prepare Repository
```bash
# Make sure everything is committed
cd C:\baned-test
git add .
git commit -m "Prepare for Render deployment"
git push origin minimal-standalone
```

### Step 2: Create Render Account
1. Go to https://render.com
2. Sign up with GitHub
3. Authorize Render to access your repositories

### Step 3: Create New Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `PiotrStyla/BANED`
3. Select branch: `minimal-standalone`

### Step 4: Configure Service
```
Name:           baned-api
Environment:    Python 3
Region:         Choose closest to you
Branch:         minimal-standalone
Build Command:  pip install -r requirements.txt
Start Command:  uvicorn api:app --host 0.0.0.0 --port $PORT
```

### Step 5: Environment Variables
Add these in Render dashboard:
```
PYTHON_VERSION = 3.11.0
```

### Step 6: Deploy!
- Click **"Create Web Service"**
- Wait 2-3 minutes for deployment
- Your API will be live at: `https://baned-api.onrender.com`

### Step 7: Test
```bash
curl https://baned-api.onrender.com/
curl -X POST https://baned-api.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Department announces new policy", "use_fusion": true}'
```

**✅ Done! Your API is now online 24/7!**

**Free Tier Limits:**
- ✅ Unlimited requests
- ✅ Automatic HTTPS
- ✅ Custom domains
- ⚠️ Spins down after 15 min inactivity (restarts in ~30s on request)

---

## 🚂 Option B: Railway.app

**Why:** Modern, simple, generous free tier

### Step 1: Create Account
1. Go to https://railway.app
2. Sign up with GitHub

### Step 2: New Project
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose `PiotrStyla/BANED`
4. Select `minimal-standalone` branch

### Step 3: Configure
Railway auto-detects Python and requirements.txt

Add start command:
```bash
uvicorn api:app --host 0.0.0.0 --port $PORT
```

### Step 4: Deploy
- Click **"Deploy"**
- Wait 2-3 minutes
- Your API will be at: `https://your-app.railway.app`

**✅ Done! API is live!**

**Free Tier:**
- $5 free credit/month
- Automatic HTTPS
- Custom domains
- No sleep mode

---

## 🐳 Option C: Docker + Any Platform

**Why:** Maximum portability, works everywhere

### Step 1: Create Dockerfile
Already created at `C:\baned-test\Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Step 2: Build & Test Locally
```bash
# Build image
docker build -t baned-api .

# Run container
docker run -p 8000:8000 baned-api

# Test
curl http://localhost:8000/
```

### Step 3: Deploy to Any Platform
This Docker image works on:
- Google Cloud Run
- AWS ECS
- Azure Container Instances
- DigitalOcean App Platform
- Fly.io

---

## ☁️ Option D: Google Cloud Run (Serverless)

**Why:** Free tier, auto-scaling, pay only for usage

### Step 1: Install Google Cloud SDK
Download from: https://cloud.google.com/sdk/docs/install

### Step 2: Login & Setup
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### Step 3: Deploy
```bash
cd C:\baned-test

gcloud run deploy baned-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Step 4: Get URL
Cloud Run will give you a URL like:
```
https://baned-api-xxxxx.run.app
```

**✅ Live in 5 minutes!**

**Free Tier:**
- 2 million requests/month
- 360,000 GB-seconds memory
- 180,000 vCPU-seconds
- Automatic scaling to zero

---

## 🔥 Option E: Heroku (Traditional)

**Why:** Well-established, lots of documentation

### Step 1: Create Procfile
```bash
web: uvicorn api:app --host 0.0.0.0 --port $PORT
```

### Step 2: Install Heroku CLI
Download from: https://devcenter.heroku.com/articles/heroku-cli

### Step 3: Login & Create App
```bash
heroku login
heroku create baned-api
```

### Step 4: Deploy
```bash
git push heroku minimal-standalone:main
```

### Step 5: Scale
```bash
heroku ps:scale web=1
```

**✅ Your app is at:** `https://baned-api.herokuapp.com`

**Note:** Heroku removed free tier in 2022, now requires paid plan ($5-7/month)

---

## 🌍 Option F: Fly.io (Global Edge)

**Why:** Deploy globally, very fast, generous free tier

### Step 1: Install Fly CLI
```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex
```

### Step 2: Sign Up & Login
```bash
fly auth signup
fly auth login
```

### Step 3: Launch App
```bash
cd C:\baned-test
fly launch
```

Answer prompts:
```
App name: baned-api
Region: Choose closest
Deploy now? Yes
```

### Step 4: Deploy
```bash
fly deploy
```

**✅ Live at:** `https://baned-api.fly.dev`

**Free Tier:**
- 3 shared VMs
- 160GB bandwidth/month
- Automatic HTTPS
- Global deployment

---

## 🔧 Update Web Interface for Online API

Update `static/index.html` to use your live API:

```javascript
// Change this line:
const API_URL = 'http://localhost:8000';

// To your deployed URL:
const API_URL = 'https://baned-api.onrender.com';
// or
const API_URL = 'https://your-app.railway.app';
```

Then host the web interface on:
- **GitHub Pages** (free, static hosting)
- **Netlify** (free, automatic deployment)
- **Vercel** (free, very fast)

---

## 📱 GitHub Pages for Web Interface

### Step 1: Create gh-pages Branch
```bash
cd C:\baned-test
git checkout -b gh-pages
```

### Step 2: Update index.html
```javascript
// Update API URL to your deployed endpoint
const API_URL = 'https://baned-api.onrender.com';
```

### Step 3: Push
```bash
git add static/index.html
git commit -m "Update API URL for production"
git push origin gh-pages
```

### Step 4: Enable GitHub Pages
1. Go to your repo settings
2. Pages → Source → `gh-pages` branch → `/static` folder
3. Save

**✅ Web interface live at:**
`https://piotrstyla.github.io/BANED/index.html`

---

## 🎯 My Recommendation: Render.com

**Best Overall:**
```
Platform:    Render.com
API:         https://baned-api.onrender.com
Web UI:      GitHub Pages
Time:        10 minutes total
Cost:        FREE
Uptime:      24/7 (with 30s cold start after inactivity)
```

**Setup Steps:**
1. ✅ Push code to GitHub (already done)
2. ✅ Create Render account (2 min)
3. ✅ Connect repo & deploy (3 min)
4. ✅ Update web interface URL (1 min)
5. ✅ Deploy web interface to GitHub Pages (2 min)
6. ✅ Test both API and web interface (2 min)

**Total:** 10 minutes to 24/7 online!

---

## 🔒 Production Checklist

Before going live, ensure:

- [ ] Model file exists (`models/model.pth`)
- [ ] Vocabulary file exists (`models/vocab.txt`)
- [ ] KB patterns exist (`kb/real_patterns.csv`, `kb/fake_patterns.csv`)
- [ ] All dependencies in `requirements.txt`
- [ ] Environment variables set (if needed)
- [ ] CORS configured in `api.py` ✅ (already done)
- [ ] Error handling in place ✅
- [ ] Health endpoint working ✅
- [ ] Documentation accessible (`/docs`) ✅

---

## 📊 Monitoring Your Live API

### Check Health
```bash
curl https://your-api-url.com/
```

### Check Stats
```bash
curl https://your-api-url.com/stats
```

### View Logs
- **Render:** Dashboard → Logs
- **Railway:** Dashboard → Deployments → Logs
- **Heroku:** `heroku logs --tail`
- **Google Cloud:** Cloud Console → Logging

---

## 💰 Cost Comparison

| Platform | Free Tier | Paid Tier | Best For |
|----------|-----------|-----------|----------|
| **Render** | Free forever | $7/mo | APIs |
| **Railway** | $5 credit/mo | $5/mo+ | Quick deploys |
| **Fly.io** | 3 VMs free | $0.0000008/s | Edge computing |
| **Google Cloud Run** | 2M req/mo | Pay per use | Auto-scaling |
| **Heroku** | None | $7/mo | Traditional apps |
| **AWS Lambda** | 1M req/mo | Pay per use | Serverless |

**Recommendation:** Start with Render (free), upgrade if needed.

---

## 🚀 Quick Deploy Commands

### Render (via CLI)
```bash
# Install Render CLI
npm install -g render

# Deploy
render deploy
```

### Railway (via CLI)
```bash
# Install Railway CLI
npm i -g @railway/cli

# Deploy
railway up
```

### Fly.io
```bash
fly deploy
```

### Google Cloud Run
```bash
gcloud run deploy baned-api --source .
```

---

## 🔄 Auto-Deploy on Git Push

Set up CI/CD for automatic deployment:

### GitHub Actions (Render)
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Render

on:
  push:
    branches: [minimal-standalone]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Render
        run: curl ${{ secrets.RENDER_DEPLOY_HOOK }}
```

**Setup:**
1. Get deploy hook from Render dashboard
2. Add as GitHub secret: `RENDER_DEPLOY_HOOK`
3. Every push auto-deploys!

---

## 📱 Mobile App Integration

Once API is online, integrate with mobile apps:

### React Native
```javascript
const response = await fetch('https://baned-api.onrender.com/predict', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    text: newsText,
    use_fusion: true
  })
});
const result = await response.json();
```

### Flutter
```dart
final response = await http.post(
  Uri.parse('https://baned-api.onrender.com/predict'),
  body: jsonEncode({'text': newsText, 'use_fusion': true}),
);
final result = jsonDecode(response.body);
```

---

## 🎉 Next Steps

1. **Choose platform** (I recommend Render)
2. **Deploy API** (10 minutes)
3. **Deploy web interface** (GitHub Pages)
4. **Test everything**
5. **Share your live app!**

**Your API will be:**
- ✅ Online 24/7
- ✅ Accessible from anywhere
- ✅ HTTPS encrypted
- ✅ Auto-scaling
- ✅ Free (with Render/Railway)

---

**Need help?** Follow the Render.com guide above - it's the easiest!

**Status:** Ready to deploy! 🚀
