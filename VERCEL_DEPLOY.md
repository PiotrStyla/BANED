# 🚀 BANED Double Power - Vercel Deployment Guide

## ✅ Ready for Deployment

All files are configured for Vercel serverless deployment!

---

## 📦 What's Included

### Vercel Configuration:
- ✅ `vercel.json` - Deployment configuration
- ✅ `api_vercel.py` - Serverless API handler
- ✅ `requirements.txt` - Minimal dependencies (no PyTorch)
- ✅ `.vercelignore` - Files to exclude from deployment

### Features in Serverless Mode:
- ✅ **Logical Consistency Checking** (contradictions, temporal logic)
- ✅ **Fact Database Verification** (historical accuracy, impossible claims)
- ✅ **Double Power Verification** (without CNN - verification-only)
- ✅ **Bilingual Support** (Polish & English)
- ✅ **Auto Language Detection**
- ✅ **CORS Enabled** (works from any domain)

### What's NOT Included (to keep it lightweight):
- ❌ PyTorch (too large for serverless)
- ❌ CNN Models (verification-only mode)
- ❌ NumPy (not needed for verification)

---

## 🚀 Deployment Steps

### Option 1: Deploy via Vercel CLI (Recommended)

#### 1. Install Vercel CLI:
```bash
npm install -g vercel
```

#### 2. Login to Vercel:
```bash
vercel login
```

#### 3. Deploy:
```bash
vercel
```

Follow the prompts:
- **Set up and deploy?** Yes
- **Which scope?** Your account
- **Link to existing project?** No
- **Project name?** baned-double-power (or your choice)
- **Directory?** ./ (current directory)
- **Override settings?** No

#### 4. Deploy to Production:
```bash
vercel --prod
```

---

### Option 2: Deploy via Vercel Dashboard

#### 1. Push to GitHub:
```bash
git add .
git commit -m "feat: Add Vercel deployment configuration"
git push origin main
```

#### 2. Go to Vercel Dashboard:
- Visit: https://vercel.com/dashboard
- Click **"Add New Project"**
- Import your GitHub repository
- Click **"Deploy"**

#### 3. Configure (if needed):
- **Framework Preset**: Other
- **Root Directory**: ./
- **Build Command**: (leave empty)
- **Output Directory**: (leave empty)

---

## 🌐 After Deployment

### Your API will be available at:
```
https://your-project-name.vercel.app/
```

### Endpoints:
- **GET** `/` - API status
- **POST** `/predict` - Fake news prediction
- **GET** `/health` - Health check

### Test it:
```bash
curl https://your-project-name.vercel.app/

curl -X POST https://your-project-name.vercel.app/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"Scientists reveal 200% effective miracle cure!"}'
```

---

## 📱 Update Web Interface

After deployment, update the API URL in `static/double_power.html`:

**Line 433** - Change from:
```javascript
const API_URL = 'http://localhost:8000';
```

To:
```javascript
const API_URL = 'https://your-project-name.vercel.app';
```

Then redeploy or host the HTML separately.

---

## 🔧 Troubleshooting

### Issue: "Module not found"
**Solution**: Make sure `verification/` folder is included in deployment

### Issue: "Function timeout"
**Solution**: Verification-only mode is fast (<1s). If timeout occurs, check logs.

### Issue: "CORS error"
**Solution**: CORS is already enabled in `api_vercel.py`. Check browser console.

### Issue: "Import error"
**Solution**: The serverless function doesn't need PyTorch. Only verification modules are used.

---

## 📊 Performance

### Serverless Mode:
- **Cold Start**: ~1-2 seconds (first request)
- **Warm**: <500ms (subsequent requests)
- **Memory**: ~128MB (very lightweight)
- **Cost**: Free tier covers most usage

### Verification Capabilities:
- ✅ Contradiction detection
- ✅ Historical accuracy
- ✅ Impossible claims
- ✅ Fake news patterns
- ✅ Temporal logic
- ✅ Numerical sanity

**Note**: Without CNN, the system relies purely on logical verification. This is still very effective for obvious fake news!

---

## 🎯 Example Deployment

### 1. Deploy:
```bash
vercel --prod
```

### 2. Output:
```
🔍  Inspect: https://vercel.com/your-account/baned-double-power/...
✅  Production: https://baned-double-power.vercel.app
```

### 3. Test:
```bash
curl https://baned-double-power.vercel.app/
```

### 4. Response:
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

---

## 📝 Environment Variables (Optional)

If you want to add configuration:

### In Vercel Dashboard:
1. Go to **Project Settings**
2. Click **Environment Variables**
3. Add variables:
   - `API_VERSION`: 4.0.0-vercel
   - `MAX_TEXT_LENGTH`: 5000
   - etc.

### Access in code:
```python
import os
version = os.getenv('API_VERSION', '4.0.0')
```

---

## 🔒 Security

### Already Configured:
- ✅ CORS headers (controlled access)
- ✅ Input validation (min/max length)
- ✅ Error handling (no stack traces exposed)
- ✅ Rate limiting (Vercel default)

### Recommended:
- Add API key authentication for production
- Monitor usage in Vercel dashboard
- Set up alerts for errors

---

## 📚 Resources

- **Vercel Docs**: https://vercel.com/docs
- **Python on Vercel**: https://vercel.com/docs/functions/serverless-functions/runtimes/python
- **Vercel CLI**: https://vercel.com/docs/cli

---

## ✅ Deployment Checklist

Before deploying:
- [x] `vercel.json` configured
- [x] `api_vercel.py` created
- [x] `requirements.txt` minimal (no PyTorch)
- [x] `.vercelignore` set up
- [x] Verification modules working
- [x] Tests passing locally
- [x] Git committed and pushed

After deploying:
- [ ] Test API endpoints
- [ ] Update web interface API_URL
- [ ] Test with real examples
- [ ] Monitor logs in Vercel dashboard
- [ ] Share the URL!

---

## 🎉 Ready to Deploy!

Everything is configured and ready. Just run:

```bash
vercel --prod
```

And your BANED Double Power API will be live on Vercel! 🚀

---

**Note**: The serverless version runs in **verification-only mode** (no CNN models) to keep it lightweight and fast. This is perfect for detecting obvious fake news through logical analysis!
