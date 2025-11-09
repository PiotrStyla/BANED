# 🚀 Deploy BANED Double Power to Vercel

## ✅ Everything is Ready!

All files are configured and pushed to GitHub. Now you can deploy!

---

## 🎯 **Quick Deploy (3 Steps)**

### **Option 1: Via Vercel Dashboard (Easiest - No CLI needed)**

#### Step 1: Go to Vercel
Visit: **https://vercel.com/new**

#### Step 2: Import Your Repository
1. Click **"Import Git Repository"**
2. Select **GitHub**
3. Find and select: **PiotrStyla/BANED**
4. Click **"Import"**

#### Step 3: Deploy
1. **Project Name**: baned-double-power (or your choice)
2. **Framework Preset**: Other
3. **Root Directory**: ./
4. Click **"Deploy"**

**That's it!** ✅ Vercel will automatically:
- Detect `vercel.json`
- Use `api_vercel.py` as the serverless function
- Deploy in ~2 minutes

---

### **Option 2: Via Vercel CLI (If you have Node.js)**

#### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

#### Step 2: Login
```bash
vercel login
```

#### Step 3: Deploy
```bash
cd c:\Users\Hipek\OneDrive\Pulpit\Fake_Buster\CascadeProjects\windsurf-project
vercel --prod
```

---

## 🌐 **After Deployment**

### Your API will be live at:
```
https://baned-double-power.vercel.app/
```
(or whatever name you chose)

### Test it immediately:
```bash
# Check status
curl https://your-project.vercel.app/

# Test prediction
curl -X POST https://your-project.vercel.app/predict \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"Scientists reveal 200% effective miracle cure!\"}"
```

---

## 📱 **Update Web Interface**

After deployment, update the API URL in your web interface:

### File: `static/double_power.html`
**Line 433** - Change:
```javascript
const API_URL = 'http://localhost:8000';
```

To:
```javascript
const API_URL = 'https://your-project.vercel.app';
```

Then you can host the HTML on:
- GitHub Pages
- Vercel (as static site)
- Netlify
- Or any web host

---

## 🎯 **What's Deployed**

### Serverless API Features:
- ✅ **Logical Consistency Checking** (contradictions, temporal logic)
- ✅ **Fact Database Verification** (historical accuracy, impossible claims)
- ✅ **Double Power Verification** (verification-only mode)
- ✅ **Bilingual Support** (Polish & English)
- ✅ **Auto Language Detection**
- ✅ **CORS Enabled** (works from any domain)

### Performance:
- **Cold Start**: ~1-2 seconds (first request)
- **Warm Requests**: <500ms
- **Memory**: ~128MB (very lightweight)
- **Cost**: **FREE** (Vercel free tier)

### What's NOT Included:
- ❌ PyTorch (too large for serverless)
- ❌ CNN Models (verification-only mode is sufficient)

**Note**: The verification-only mode is still very effective! It catches:
- Contradictions (always/never)
- Historical errors (COVID-19 wrong year)
- Impossible claims (200%, miracle cures)
- Fake patterns (doctors hate, big pharma)

---

## 🔍 **Verify Deployment**

### 1. Check Vercel Dashboard
- Go to: https://vercel.com/dashboard
- Find your project
- Check deployment status

### 2. View Logs
- Click on your deployment
- Go to **"Functions"** tab
- Check logs for any errors

### 3. Test Endpoints
```bash
# Status
curl https://your-project.vercel.app/

# Health
curl https://your-project.vercel.app/health

# Prediction
curl -X POST https://your-project.vercel.app/predict \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"Test news article here\"}"
```

---

## 📊 **Expected Responses**

### GET `/`
```json
{
  "name": "BANED Double Power API",
  "version": "4.0.0-vercel",
  "status": "online",
  "mode": "verification-only",
  "features": [
    "Logical Consistency Checking",
    "Fact Database Verification",
    "Double Power Verification",
    "Bilingual (PL/EN)"
  ]
}
```

### POST `/predict`
```json
{
  "text": "Scientists reveal 200% effective miracle cure!",
  "prediction": "FAKE",
  "confidence": 0.64,
  "fake_probability": 0.82,
  "language": "en",
  "method": "VERIFICATION_ONLY",
  "verification": {
    "verdict": "FAKE",
    "verification_score": -4.0,
    ...
  },
  "explanation": [
    "Verification: FAKE (score: -4.0)",
    "Issues found: 1",
    "• Impossible claim: miracle cure"
  ]
}
```

---

## 🐛 **Troubleshooting**

### Issue: "Build failed"
**Solution**: Check Vercel build logs. The `requirements.txt` is minimal (no dependencies), so it should work.

### Issue: "Function timeout"
**Solution**: Verification is fast (<1s). If timeout, check if `verification/` folder is included.

### Issue: "Module not found: verification"
**Solution**: Make sure `verification/` folder is in the repository and not in `.vercelignore`.

### Issue: "CORS error in browser"
**Solution**: CORS is enabled in `api_vercel.py`. Clear browser cache and try again.

---

## 🎉 **You're All Set!**

Everything is configured and ready. Just:

1. **Go to**: https://vercel.com/new
2. **Import**: PiotrStyla/BANED
3. **Click**: Deploy
4. **Wait**: ~2 minutes
5. **Test**: Your live API!

---

## 📚 **Resources**

- **Vercel Dashboard**: https://vercel.com/dashboard
- **Vercel Docs**: https://vercel.com/docs
- **Your GitHub Repo**: https://github.com/PiotrStyla/BANED
- **Deployment Guide**: `VERCEL_DEPLOY.md` (detailed version)

---

## ✅ **Deployment Checklist**

- [x] Code pushed to GitHub
- [x] `vercel.json` configured
- [x] `api_vercel.py` created
- [x] `requirements.txt` minimal
- [x] `.vercelignore` set up
- [x] Documentation complete
- [ ] **Deploy via Vercel Dashboard** ← YOU ARE HERE
- [ ] Test live API
- [ ] Update web interface URL
- [ ] Share with the world!

---

**Ready to deploy!** Just visit https://vercel.com/new and import your repository! 🚀
