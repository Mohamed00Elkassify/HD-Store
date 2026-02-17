# 🚀 Railway Deployment - Quick Start Guide

## ✅ Prerequisites Complete!

Your project is now ready for deployment. All necessary files have been created:
- ✅ `Procfile` - Railway startup commands
- ✅ `railway.json` - Deployment configuration
- ✅ `requirements.txt` - Updated with production dependencies
- ✅ `settings.py` - Configured for production
- ✅ `.env.example` - Environment variables template

---

## 📋 Step-by-Step Deployment

### Step 1: Push to GitHub

```bash
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

If you don't have a GitHub repo yet:
```bash
git init
git add .
git commit -m "Initial commit for deployment"
git branch -M main
# Create a new repo on GitHub, then:
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
git push -u origin main
```

---

### Step 2: Sign Up for Railway

1. Go to **[railway.app](https://railway.app)**
2. Click **"Login with GitHub"**
3. Authorize Railway to access your repositories

---

### Step 3: Create New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your **HD-store** repository
4. Railway will auto-detect Django and start deploying

---

### Step 4: Add PostgreSQL Database

1. In your project dashboard, click **"New"**
2. Select **"Database"** → **"Add PostgreSQL"**
3. Railway automatically creates `DATABASE_URL` environment variable
4. Your app will connect to PostgreSQL automatically!

---

### Step 5: Set Environment Variables

1. Click on your **web service** (not the database)
2. Go to **"Variables"** tab
3. Click **"New Variable"** and add these:

**Required Variables:**

```bash
DJANGO_SECRET_KEY
```
Generate a new one with:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

```bash
DJANGO_DEBUG=0
```

```bash
ALLOWED_HOSTS=your-app-name.up.railway.app
```
*(Replace with your actual Railway domain - you'll see it in the Deployments tab)*

**ERPNext Variables:**

```bash
ERPNEXT_BASE_URL=https://your-erpnext-instance.com
ERPNEXT_API_KEY=your_api_key
ERPNEXT_API_SECRET=your_api_secret
ERPNEXT_DEFAULT_WAREHOUSE=Your Warehouse
ERPNEXT_WEBHOOK_SECRET=your-webhook-secret-123
```

**Optional (WhatsApp):**

```bash
WHATSAPP_AUTOMATION_ENABLED=1
WASENDER_API_KEY=your_key
```

---

### Step 6: Deploy!

1. Railway auto-deploys on every commit
2. Check **"Deployments"** tab for build logs
3. Wait 2-3 minutes for first deployment
4. Your app URL: `https://your-app-name.up.railway.app`

---

### Step 7: Configure ERPNext Webhook

Once deployed, update your ERPNext webhook:

1. **ERPNext** → **Integrations** → **Webhook**
2. Find **"Sales Invoice to Django"** webhook
3. Update **Request URL**:
   ```
   https://your-app-name.up.railway.app/api/webhooks/erpnext/sales-invoice/
   ```
4. Set **Webhook Headers**:
   ```
   X-Webhook-Secret: your-webhook-secret-123
   ```
   *(Use the same secret you set in Railway variables)*
5. **Save**

---

### Step 8: Test Everything

1. **Test your website:**
   - Visit `https://your-app-name.up.railway.app`
   - Browse products
   - Test checkout

2. **Test webhook:**
   - Create and submit a Sales Invoice in ERPNext
   - Check Railway logs (Observability tab)
   - You should see: `Received Sales Invoice webhook for: SINV-XXXX`

---

## 🎉 Done!

Your app is now live on Railway with:
- ✅ Permanent URL that never changes
- ✅ PostgreSQL database
- ✅ Automatic HTTPS
- ✅ Auto-deployments from GitHub
- ✅ Working webhooks from ERPNext

---

## 💰 Pricing

**Railway Free Tier:**
- $5 free credit per month
- Enough for hobby projects
- No credit card required

**If you need more:**
- Hobby Plan: $5/month (includes $5 in usage)
- Your app should cost ~$3-5/month

---

## 📊 Monitor Your App

**Railway Dashboard:**
- **Deployments** - Build logs and deployment history
- **Metrics** - CPU, Memory, Network usage
- **Variables** - Update environment variables
- **Settings** - Custom domains, restart, etc.

---

## 🔄 Future Updates

To deploy changes:
```bash
git add .
git commit -m "Your changes"
git push origin main
```

Railway automatically redeploys within 1-2 minutes!

---

## 🆘 Troubleshooting

### Build Failed
- Check **Deployments** → **Build Logs**
- Ensure all files are committed to Git
- Verify `requirements.txt` has all dependencies

### App Crashes
- Check **Observability** → **Logs**
- Common issues:
  - Missing environment variables
  - Database connection issues
  - Static files not collected

### Webhook Not Working
- Verify Railway URL is correct in ERPNext
- Check webhook secret matches
- View logs in Railway dashboard

### Database Issues
- Ensure PostgreSQL service is running
- Check `DATABASE_URL` is set automatically
- Try restarting the web service

---

## 📞 Need Help?

- Railway Docs: [docs.railway.app](https://docs.railway.app)
- Railway Discord: [discord.gg/railway](https://discord.gg/railway)
- Django Deployment: [docs.djangoproject.com/en/stable/howto/deployment/](https://docs.djangoproject.com/en/stable/howto/deployment/)

---

## 🎯 What's Different from Local?

| Feature | Local Development | Railway Production |
|---------|------------------|-------------------|
| Database | SQLite | PostgreSQL |
| Static Files | Django dev server | WhiteNoise |
| HTTPS | No | Yes (automatic) |
| Domain | localhost:8000 | your-app.railway.app |
| Debug Mode | ON | OFF |
| Webhook URL | Changes (ngrok) | **Permanent** |

---

**YOUR WEBHOOK URL WILL NEVER CHANGE AGAIN!** 🎉

No more updating ERPNext every time you restart ngrok!
