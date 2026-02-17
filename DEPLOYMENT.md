# 🚀 Production Deployment Guide

This guide explains how to deploy your HD Store application to production with **reliable webhook support**.

---

## ⚠️ The Problem with ngrok

**ngrok** is great for development but **NOT for production**:

❌ URLs change every time you restart ngrok (unless you have a paid plan)  
❌ Connections can drop randomly  
❌ Free tier has limits on concurrent connections  
❌ Not reliable for business-critical webhooks  

**Your ERPNext webhook needs a PERMANENT URL that never changes!**

---

## 🌟 Production Deployment Options

### **Option 1: Railway (Recommended - Easiest)**

✅ Free tier available  
✅ Automatic HTTPS  
✅ Direct GitHub integration  
✅ PostgreSQL database included  
✅ Permanent URL  

**Steps:**

1. **Sign up at [railway.app](https://railway.app)**

2. **Create a new project from GitHub**
   - Connect your GitHub repository
   - Railway will auto-detect Django

3. **Add PostgreSQL database**
   - Click "New" → "Database" → "PostgreSQL"
   - Railway will add `DATABASE_URL` environment variable

4. **Set environment variables** (click on your service → Variables):
   ```bash
   DJANGO_SECRET_KEY=<generate a new secure key>
   DJANGO_DEBUG=0
   ALLOWED_HOSTS=<your-app>.railway.app
   
   # Database (automatically set by Railway)
   DATABASE_URL=postgresql://...
   
   # ERPNext
   ERPNEXT_BASE_URL=https://your-erpnext.com
   ERPNEXT_API_KEY=your_api_key
   ERPNEXT_API_SECRET=your_api_secret
   ERPNEXT_DEFAULT_WAREHOUSE=Your Warehouse
   ERPNEXT_WEBHOOK_SECRET=<same as you'll set in ERPNext>
   
   # WhatsApp (optional)
   WHATSAPP_AUTOMATION_ENABLED=1
   WASENDER_API_KEY=your_key
   ```

5. **Update `requirements.txt`** (add PostgreSQL support):
   ```
   psycopg2-binary==2.9.9
   gunicorn==21.2.0
   whitenoise==6.6.0
   ```

6. **Create `Procfile`** in project root:
   ```
   web: gunicorn config.wsgi --bind 0.0.0.0:$PORT
   release: python manage.py migrate
   ```

7. **Update `settings.py`** for PostgreSQL:
   ```python
   import dj_database_url
   
   # Add dj-database-url to requirements.txt first
   DATABASES = {
       'default': dj_database_url.config(
           default='sqlite:///db.sqlite3',
           conn_max_age=600
       )
   }
   ```

8. **Deploy**
   - Push to GitHub
   - Railway auto-deploys
   - Your app will be at: `https://your-app.railway.app`

9. **Configure ERPNext webhook** *(see section below)*

---

### **Option 2: DigitalOcean App Platform**

✅ $5/month starter tier  
✅ Managed PostgreSQL  
✅ Automatic SSL

**Steps:**
1. Sign up at [digitalocean.com](https://digitalocean.com)
2. Create new app from GitHub
3. Add managed PostgreSQL database
4. Similar environment variable setup as Railway
5. Deploy and use the provided URL

---

### **Option 3: Render**

✅ Free tier available  
✅ Database included  
✅ Easy setup

**Steps:**
1. Sign up at [render.com](https://render.com)
2. Create Web Service from GitHub
3. Add PostgreSQL database (free tier)
4. Set environment variables
5. Deploy

---

### **Option 4: Traditional VPS (More Control)**

For advanced users who want full control:

**Providers:**
- DigitalOcean Droplets ($6/month)
- Linode ($5/month)
- Vultr ($5/month)
- AWS EC2 (variable pricing)

**You'll need to:**
- Set up Ubuntu server
- Install Nginx reverse proxy
- Configure SSL with Let's Encrypt
- Set up Gunicorn + systemd
- Configure firewall
- Handle database backups

**Not recommended unless you have DevOps experience.**

---

### **Option 5: Cloudflare Tunnel (Free ngrok Alternative)**

If you must run on your local machine but need a permanent URL:

✅ Free forever  
✅ Permanent subdomain  
✅ Automatic HTTPS  
✅ Better than ngrok

**Steps:**

1. **Install Cloudflare Tunnel**
   ```bash
   # Download from: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/
   ```

2. **Login**
   ```bash
   cloudflared tunnel login
   ```

3. **Create tunnel**
   ```bash
   cloudflared tunnel create hdstore
   ```

4. **Configure tunnel** (create `config.yml`):
   ```yaml
   tunnel: <tunnel-id>
   credentials-file: /path/to/credentials.json

   ingress:
     - hostname: hdstore.yourdomain.com
       service: http://localhost:8000
     - service: http_status:404
   ```

5. **Run tunnel**
   ```bash
   cloudflared tunnel run hdstore
   ```

6. **Set up as Windows service** (so it runs automatically):
   ```powershell
   cloudflared service install
   ```

**Pros:** Free and permanent  
**Cons:** Still running on your machine (not truly "production")

---

## 🔗 Configure ERPNext Webhook

Once your app is deployed and you have a **permanent URL**, configure the webhook in ERPNext:

### Steps:

1. **Open ERPNext** → **Integrations** → **Webhook**

2. **Create New Webhook**:
   - **Webhook Name:** `Sales Invoice to Django`
   - **Status:** ✅ Enabled
   - **Document Type:** `Sales Invoice`
   - **Document Event:** `on_submit`
   - **Request URL:** 
     ```
     https://your-app.railway.app/api/webhooks/erpnext/sales-invoice/
     ```
     *(Replace with your actual deployment URL)*

3. **Request Structure:**
   - **Request Method:** `POST`
   - **Webhook Data:**
     ```json
     {
       "name": "{{ doc.name }}"
     }
     ```

4. **Webhook Headers:**
   ```
   X-Webhook-Secret: <paste the same secret from your .env>
   ```

5. **Click Save**

### Test the Webhook:

1. Create and submit a Sales Invoice in ERPNext
2. Check Django logs - you should see:
   ```
   Received Sales Invoice webhook for: SINV-XXXX-XXXX
   ```

---

## 🔐 Security Checklist for Production

- [ ] Set `DJANGO_DEBUG=0` in production
- [ ] Use a strong `DJANGO_SECRET_KEY` (generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- [ ] Set `ALLOWED_HOSTS` to your actual domain
- [ ] Use `ERPNEXT_WEBHOOK_SECRET` to verify webhook requests
- [ ] Store all secrets in environment variables (never commit `.env`)
- [ ] Use HTTPS (all deployment options above provide it automatically)
- [ ] Set up database backups (most platforms do this automatically)
- [ ] Monitor your application logs
- [ ] Set up error tracking (Sentry, etc.)

---

## 📊 Database Migration (SQLite → PostgreSQL)

If you have existing data in SQLite and want to migrate:

```bash
# 1. Export data
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > backup.json

# 2. Switch to PostgreSQL in settings.py

# 3. Run migrations
python manage.py migrate

# 4. Import data
python manage.py loaddata backup.json
```

---

## 🧪 Testing Webhooks Locally (Development Only)

For development, you can still use ngrok:

```bash
# Start Django
python manage.py runserver

# In another terminal, start ngrok
ngrok http 8000

# Use the ngrok HTTPS URL in ERPNext webhook
# https://xyz123.ngrok-free.app/api/webhooks/erpnext/sales-invoice/
```

**Remember:** ngrok URL changes every restart unless you have a paid plan!

---

## 🆘 Troubleshooting

### Webhook Returns 404

✅ **Fixed!** Make sure you updated `config/urls.py` to include:
```python
path('api/webhooks/erpnext/sales-invoice/', ERPNextSalesInvoiceWebhook.as_view())
```

### Webhook Returns 403 (Forbidden)

- Check that `ERPNEXT_WEBHOOK_SECRET` in `.env` matches the `X-Webhook-Secret` header in ERPNext webhook configuration
- Or temporarily disable secret verification by setting `ERPNEXT_WEBHOOK_SECRET=""` (not recommended for production)

### Webhook Times Out

- Check Django logs for errors
- Ensure ERPNext can reach your server (firewall, network issues)
- Verify the URL is correct and accessible

### Database Connection Issues

- Verify `DATABASE_URL` is set correctly
- Check that PostgreSQL is running
- Verify firewall allows database connections

---

## 📚 Recommended Production Stack

```
┌─────────────────────────────────────────┐
│  Client Browser (Customer)              │
└─────────────────┬───────────────────────┘
                  │ HTTPS
┌─────────────────▼───────────────────────┐
│  Django App (Railway/Render/DO)         │
│  - Gunicorn WSGI Server                 │
│  - WhiteNoise (Static Files)            │
│  - Webhook Endpoint                     │
└─────────┬──────────────────┬────────────┘
          │                  │
          │ API              │ Webhook
          ▼                  ▼
┌──────────────────┐  ┌──────────────────┐
│  PostgreSQL DB   │  │    ERPNext       │
│  (User Orders)   │  │   (Inventory)    │
└──────────────────┘  └──────────────────┘
```

---

## 🎯 Next Steps

1. ✅ Choose a deployment platform (Railway recommended)
2. ✅ Deploy your application
3. ✅ Get your permanent production URL
4. ✅ Update ERPNext webhook configuration
5. ✅ Test by creating a Sales Invoice
6. ✅ Monitor logs and fix any issues
7. ✅ Set up database backups
8. ✅ Configure domain name (optional)

---

## 💡 Pro Tips

- **Use staging environment:** Create a separate deployment for testing before production
- **Monitor uptime:** Use UptimeRobot (free) to monitor your site
- **Set up alerts:** Get notified when your site goes down
- **Regular backups:** Export database weekly (most platforms automate this)
- **Log monitoring:** Use Papertrail or Logtail for centralized logging

---

**Need help?** Check the logs first! Most issues show up in:
- Django logs (check your deployment platform's logs viewer)
- ERPNext webhook logs (Integrations → Webhook → View Logs)

Good luck with your deployment! 🚀
