# 🚀 Quick Deploy to Render.com (5 Minutes!)

## Why Render?
- ✅ **FREE** forever tier
- ✅ **HTTPS** automatic
- ✅ **24/7** uptime
- ✅ **5 minutes** setup
- ✅ No credit card needed

---

## Step-by-Step Guide

### 1️⃣ Push to GitHub (if not already done)
```bash
cd C:\baned-test
git add .
git commit -m "Ready for deployment"
git push origin minimal-standalone
```

### 2️⃣ Create Render Account
1. Go to **https://render.com**
2. Click **"Get Started"**
3. Sign up with **GitHub** (easiest!)
4. Authorize Render to access your repos

### 3️⃣ Create Web Service
1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. Click **"Connect account"** if needed
4. Find your repo: **`BANED`**
5. Click **"Connect"**

### 4️⃣ Configure Service
Fill in these fields:

```
Name:              baned-api
Branch:            minimal-standalone
Region:            Frankfurt (Europe) or Oregon (US West)
Runtime:           Python 3

Build Command:     pip install -r requirements.txt
Start Command:     uvicorn api:app --host 0.0.0.0 --port $PORT

Instance Type:     Free
```

### 5️⃣ Environment Variables (Optional)
Click **"Advanced"** → **"Add Environment Variable"**:
```
Key:    PYTHON_VERSION
Value:  3.11.0
```

### 6️⃣ Deploy!
1. Click **"Create Web Service"**
2. Wait 2-3 minutes (watch the logs!)
3. ✅ When you see "Live" with a green dot, it's ready!

### 7️⃣ Get Your URL
Your API will be at:
```
https://baned-api.onrender.com
```
(or whatever name you chose)

### 8️⃣ Test It!
Open in browser:
```
https://baned-api.onrender.com/docs
```

Or test with curl:
```bash
curl https://baned-api.onrender.com/

curl -X POST https://baned-api.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Department announces new policy", "use_fusion": true}'
```

---

## 🎉 Done! Your API is Live 24/7!

**What you get:**
- ✅ Live API at: `https://your-app.onrender.com`
- ✅ Swagger docs at: `https://your-app.onrender.com/docs`
- ✅ Automatic HTTPS
- ✅ No server management
- ✅ Auto-deploys on git push

**Free Tier Info:**
- Spins down after 15 min inactivity
- Restarts in ~30 seconds when accessed
- Perfect for demos and testing!

---

## 🌐 Update Web Interface

Edit `static/index.html` line 216:
```javascript
// Change from:
const API_URL = 'http://localhost:8000';

// To your live URL:
const API_URL = 'https://baned-api.onrender.com';
```

Then deploy the web interface to **GitHub Pages** or **Netlify** (free!)

---

## 📊 Monitor Your API

**View Logs:**
1. Go to Render Dashboard
2. Click your service
3. Click "Logs" tab
4. See real-time requests!

**Check Health:**
```bash
curl https://your-app.onrender.com/stats
```

---

## 🔄 Auto-Deploy Updates

After initial setup, just:
```bash
git add .
git commit -m "Update model"
git push origin minimal-standalone
```

Render automatically deploys! ✨

---

## ❓ Troubleshooting

**Problem:** Build fails
- Check `requirements.txt` has all dependencies
- Check Python version is 3.11

**Problem:** API doesn't respond
- Wait 30 seconds (cold start from sleep)
- Check logs in Render dashboard

**Problem:** Model not loading
- Ensure `models/model.pth` is in repo
- Check file size < 500MB

---

## 💡 Pro Tips

1. **Keep awake:** Use UptimeRobot (free) to ping your API every 5 min
2. **Custom domain:** Add your own domain in Render settings
3. **Upgrade:** $7/mo removes sleep, adds more resources
4. **Monitor:** Set up health check alerts

---

## 🎯 Next Steps

1. ✅ Deploy API to Render
2. ✅ Test with Swagger docs
3. ✅ Update web interface URL
4. ✅ Deploy web to GitHub Pages
5. ✅ Share your live demo!

**Total time:** 5-10 minutes  
**Cost:** FREE  
**Status:** Production-ready!

---

**Need help?** Check full guide: `DEPLOY_GUIDE.md`

🚀 **Happy deploying!**
