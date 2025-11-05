# 🌐 Deploy Web Interface to GitHub Pages

Complete guide to deploy your BANED web interface to GitHub Pages for free hosting.

---

## 🎯 What You'll Get

- ✅ Free web hosting (GitHub Pages)
- ✅ Custom URL: `https://piotrstyla.github.io/BANED/`
- ✅ Automatic HTTPS
- ✅ Fast global CDN
- ✅ Auto-deploys on git push

---

## 📋 Prerequisites

Before deploying the web interface, you MUST deploy the API first!

### Step 1: Deploy API to Render
Follow `QUICK_DEPLOY.md` to deploy your API to Render.com (5 minutes)

**You'll get:** `https://baned-api.onrender.com`

### Step 2: Wait for API to be Live
Test your API:
```bash
curl https://baned-api.onrender.com/
```

Should return: `{"status":"online","model_loaded":true,...}`

✅ Once API is live, proceed below!

---

## 🚀 Option A: Deploy via GitHub Web Interface (Easiest!)

### Step 1: Push Changes
```bash
cd C:\baned-test
git add .
git commit -m "Prepare for GitHub Pages deployment"
git push origin minimal-standalone
```

### Step 2: Enable GitHub Pages
1. Go to your repo: https://github.com/PiotrStyla/BANED
2. Click **"Settings"** (top menu)
3. Scroll down to **"Pages"** (left sidebar)
4. Under **"Source"**:
   - Branch: `minimal-standalone`
   - Folder: `/docs`
5. Click **"Save"**

### Step 3: Wait for Deployment
- GitHub will build and deploy (1-2 minutes)
- You'll see: ✅ "Your site is published at..."

### Step 4: Access Your Live App!
```
https://piotrstyla.github.io/BANED/
```

**✅ DONE! Your web interface is live!**

---

## 🔧 Option B: Deploy via Command Line

### Step 1: Update API URL in HTML
The file `docs/index.html` is already configured with:
```javascript
const API_URL = 'https://baned-api.onrender.com';
```

If you used a different URL, update line 408 in `docs/index.html`

### Step 2: Commit and Push
```bash
cd C:\baned-test

# Add the docs folder
git add docs/

# Commit
git commit -m "Add GitHub Pages deployment"

# Push
git push origin minimal-standalone
```

### Step 3: Enable Pages via GitHub CLI (Optional)
```bash
# Install GitHub CLI: https://cli.github.com/
gh auth login
gh pages deploy --source minimal-standalone --directory docs
```

### Step 4: Or Enable Manually
1. Visit: https://github.com/PiotrStyla/BANED/settings/pages
2. Source: `minimal-standalone` branch, `/docs` folder
3. Save

---

## 📱 What's Deployed

### Your Live URLs:

**Web Interface:**
```
https://piotrstyla.github.io/BANED/
```

**API Backend:**
```
https://baned-api.onrender.com
```

**API Documentation:**
```
https://baned-api.onrender.com/docs
```

---

## 🎨 Customization

### Change Site Title
Edit `docs/index.html` line 5:
```html
<title>Your Custom Title - Fake News Detection</title>
```

### Change Colors
Edit the CSS gradient (lines 15-16):
```css
background: linear-gradient(135deg, #YOUR_COLOR1 0%, #YOUR_COLOR2 100%);
```

### Add Google Analytics
Add before `</head>` in `docs/index.html`:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR_GA_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'YOUR_GA_ID');
</script>
```

---

## 🔄 Update Deployment

After making changes:

```bash
# Edit files
code docs/index.html

# Commit and push
git add docs/
git commit -m "Update web interface"
git push origin minimal-standalone

# GitHub Pages auto-deploys in 1-2 minutes!
```

---

## 🌐 Custom Domain (Optional)

### Add Your Own Domain

1. Buy a domain (e.g., from Namecheap, GoDaddy)

2. Add DNS records:
```
Type: CNAME
Host: www
Value: piotrstyla.github.io
```

3. In your repo, create `docs/CNAME`:
```
www.yourdomain.com
```

4. Push to GitHub:
```bash
echo "www.yourdomain.com" > docs/CNAME
git add docs/CNAME
git commit -m "Add custom domain"
git push origin minimal-standalone
```

5. In GitHub Settings → Pages:
   - Enter your domain
   - Enable HTTPS

**Your site will be at:** `https://www.yourdomain.com`

---

## 🔒 HTTPS & Security

GitHub Pages provides:
- ✅ Automatic HTTPS
- ✅ Valid SSL certificate
- ✅ Secure by default

No configuration needed!

---

## 📊 Monitoring & Analytics

### View Deployment Status
1. Go to: https://github.com/PiotrStyla/BANED/deployments
2. See all deployments and their status
3. Click on latest deployment to see logs

### GitHub Pages Status
Check if Pages is working:
```bash
# Should return 200 OK
curl -I https://piotrstyla.github.io/BANED/
```

### API Status from Web
Open your web interface, it will show:
- ✅ API Online - Model Loaded
- ❌ API Offline - Deploy to Render first!

---

## 🐛 Troubleshooting

### Problem: 404 Not Found
**Solution:** Wait 1-2 minutes for GitHub to build. Check Settings → Pages for build status.

### Problem: API Offline Message
**Solutions:**
1. Check API is deployed to Render
2. Verify API URL in `docs/index.html` line 408
3. Check CORS is enabled (already configured in api.py)
4. Test API directly: `curl https://baned-api.onrender.com/`

### Problem: Old Version Showing
**Solution:** Clear browser cache or do hard refresh:
- Windows: `Ctrl + F5`
- Mac: `Cmd + Shift + R`

### Problem: Changes Not Appearing
**Solutions:**
1. Check commit was pushed: `git log --oneline -5`
2. Check GitHub Actions succeeded: https://github.com/PiotrStyla/BANED/actions
3. Wait 2-3 minutes for deployment
4. Clear browser cache

### Problem: CORS Errors
**Already Fixed!** The API has CORS configured:
```python
# In api.py line 20-27
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📁 File Structure

```
BANED/
├── docs/                      # GitHub Pages source
│   └── index.html            # Web interface (DEPLOYED)
├── static/                   # Local development
│   └── index.html            # Local testing version
├── api.py                    # API (deployed to Render)
├── models/                   # Model files
└── GITHUB_PAGES_DEPLOY.md   # This guide
```

**Note:** 
- `docs/index.html` is for GitHub Pages (uses Render API URL)
- `static/index.html` is for local testing (uses localhost)

---

## 🎯 Complete Deployment Checklist

- [ ] API deployed to Render ✅
- [ ] API is responding (test with curl) ✅
- [ ] `docs/index.html` created with correct API URL ✅
- [ ] Changes committed to git ✅
- [ ] Changes pushed to GitHub ✅
- [ ] GitHub Pages enabled (Settings → Pages) ✅
- [ ] Source set to `minimal-standalone` branch, `/docs` folder ✅
- [ ] Wait 1-2 minutes for build ✅
- [ ] Visit `https://piotrstyla.github.io/BANED/` ✅
- [ ] Test prediction with example text ✅
- [ ] Share your live demo! 🎉

---

## 🎉 Success Criteria

Your deployment is successful when:

1. ✅ Opening `https://piotrstyla.github.io/BANED/` loads the interface
2. ✅ Top shows: "✅ API Online - Model Loaded"
3. ✅ Entering text and clicking "Analyze" returns results
4. ✅ Example buttons load text correctly
5. ✅ Predictions show confidence bars and patterns

---

## 📱 Share Your Demo

Once deployed, share these links:

**Web Interface:**
```
https://piotrstyla.github.io/BANED/
```

**Repository:**
```
https://github.com/PiotrStyla/BANED
```

**API Documentation:**
```
https://baned-api.onrender.com/docs
```

---

## 🔄 Auto-Deploy Workflow

With GitHub Pages enabled, any push triggers auto-deployment:

```bash
# Make changes
code docs/index.html

# Commit
git add docs/
git commit -m "Update interface"

# Push
git push origin minimal-standalone

# GitHub auto-deploys in 1-2 minutes! ✨
```

**Check deployment status:**
```
https://github.com/PiotrStyla/BANED/actions
```

---

## 💡 Pro Tips

1. **Test Locally First:**
   - Use `static/index.html` for local testing
   - Uses `localhost:8000` API

2. **Keep Two Versions:**
   - `static/index.html` → local development
   - `docs/index.html` → production (GitHub Pages)

3. **Monitor API:**
   - Render free tier sleeps after 15 min
   - First request after sleep takes ~30s
   - Consider UptimeRobot to keep it awake

4. **Browser Caching:**
   - Users may see old version
   - Add version number to title to verify
   - Use cache-busting for updates

5. **SEO Optimization:**
   - Add meta description
   - Add Open Graph tags
   - Submit to Google Search Console

---

## 🌟 Next Steps

After successful deployment:

1. **Test thoroughly** - Try all examples
2. **Share on social media** - Show off your work!
3. **Add to README** - Link to live demo
4. **Monitor usage** - Check Render logs
5. **Collect feedback** - Improve based on users

---

## ✨ Your Live Stack

```
Frontend:  GitHub Pages (Free)
           https://piotrstyla.github.io/BANED/

Backend:   Render.com (Free)
           https://baned-api.onrender.com

Model:     10K trained (100% accuracy)
           360 words vocabulary

Total:     FREE hosting, 24/7 online!
```

---

**Ready to deploy?** Follow the steps above!

**Status:** ✅ All files ready for GitHub Pages deployment!
