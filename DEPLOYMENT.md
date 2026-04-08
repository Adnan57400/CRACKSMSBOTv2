# Deployment Guide

Complete step-by-step deployment instructions for Railway, Heroku, Docker, and local servers.

---

## 🚀 Railway (Recommended)

### Prerequisites
- Railway account (free tier available at railway.app)
- GitHub account (for easy deployments)
- Telegram bot token

### Step 1: Create Railway Project

```bash
# Option A: Using Railway CLI
railway login
railway init

# Option B: Create via web dashboard
# Visit app.railway.app → New Project → Import Git Repository
```

### Step 2: Configure Environment Variables

In Railway Dashboard → Variables:

```
BOT_TOKEN = your_token_from_BotFather
DATABASE_URL = postgresql://[auto-provided-by-railway]
WA_BRIDGE_HOST = http://127.0.0.1:7891  # For single service
WA_PAIRING_MODE = qr
WA_LOG_LEVEL = info
IS_CHILD_BOT = false
OTP_GUI_THEME = 0
```

### Step 3: Deploy

**Via CLI:**
```bash
railway up
```

**Via Git:**
```bash
git push heroku main  # Or git push railway main
```

### Step 4: Monitor

```bash
railway logs --tail
```

### Advanced: Separate Services

**Create WA Bridge Service:**

1. New Railway project
2. Set `startCommand` to `node whatsapp_otp.js`
3. Get the service URL (e.g., `https://wa-bridge-xyz.railway.app`)

**Update Bot Service:**

```
WA_BRIDGE_HOST = https://wa-bridge-xyz.railway.app
```

**Result:**
- Bot service: `https://app-xyz.railway.app`
- WA service: `https://wa-bridge-xyz.railway.app`
- Automatic restarts if either crashes
- Independent scaling

---

## 🐳 Docker (Local or VPS)

### Option 1: Docker Compose (Easiest)

```bash
# Navigate to project directory
cd /path/to/bot

# Build and start
docker-compose up --build

# Background mode
docker-compose up -d --build

# View logs
docker-compose logs -f bot

# Stop
docker-compose down
```

**Compose file already includes:**
- PostgreSQL database
- Proper networking
- Volume mounts for persistence
- Health checks

### Option 2: Manual Docker

```bash
# Build image
docker build -t crack-sms-bot .

# Run container
docker run -d \
  --name crack-sms \
  -e BOT_TOKEN=your_token \
  -e DATABASE_URL=postgresql://user:pass@localhost/botdb \
  -p 7891:7891 \
  crack-sms-bot

# View logs
docker logs -f crack-sms

# Stop
docker stop crack-sms
docker rm crack-sms
```

### Option 3: Docker on Digital Ocean / Linode / AWS

```bash
# 1. SSH into your server
ssh root@your_server_ip

# 2. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 3. Clone repository
git clone https://github.com/your-repo/crack-sms-bot.git
cd crack-sms-bot

# 4. Create .env file
cat > .env << EOF
BOT_TOKEN=your_token
DATABASE_URL=postgresql://user:pass@localhost/botdb
WA_BRIDGE_HOST=http://localhost:7891
EOF

# 5. Start bot
docker-compose up -d --build

# 6. Verify
docker ps
docker logs -f crack-sms-bot_bot_1
```

---

## 🖥️ Heroku (Legacy)

> **Note:** Heroku free tier ended in Nov 2022. Use Railway or similar.

```bash
# 1. Install Heroku CLI
curl https://cli.heroku.com/install.sh | sh

# 2. Login
heroku login

# 3. Create app
heroku create your-app-name

# 4. Set environment variables
heroku config:set BOT_TOKEN=your_token
heroku config:set DATABASE_URL=heroku ...
heroku config:set WA_BRIDGE_HOST=http://127.0.0.1:7891

# 5. Deploy
git push heroku main

# 6. View logs
heroku logs --tail

# 7. Scale dynos (if needed)
heroku ps:scale web=1
heroku ps:scale worker=1
```

---

## 💻 Local VPS / Dedicated Server

### Ubuntu 22.04 Setup

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install Python & Node
sudo apt install -y python3.11 python3-pip nodejs npm

# 3. Clone repository
git clone https://github.com/your-repo/crack-sms-bot.git
cd crack-sms-bot

# 4. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 5. Install dependencies
pip install -r requirements.txt
npm install

# 6. Create config
cat > config.json << 'EOF'
{
  "BOT_TOKEN": "your_token",
  "BOT_USERNAME": "YourBotUsername",
  "INITIAL_ADMIN_IDS": [your_user_id],
  "CHANNEL_LINK": "https://t.me/yourgroup",
  "OTP_GROUP_LINK": "https://t.me/yourgroup"
}
EOF

# 7. Initialize database
python -c "import asyncio; from database import init_db; asyncio.run(init_db())"

# 8. Create systemd service for auto-start
sudo tee /etc/systemd/system/crack-sms.service > /dev/null << 'EOF'
[Unit]
Description=Crack SMS Bot
After=network.target

[Service]
Type=simple
User=$(whoami)
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/venv/bin/python bot.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 9. Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable crack-sms
sudo systemctl start crack-sms

# 10. View logs
sudo journalctl -u crack-sms -f
```

### CentOS / RHEL Setup

```bash
# Replace apt with yum
sudo yum update -y
sudo yum install -y python3.11 python3-pip nodejs

# Rest is the same
```

---

## 🔧 Systemd Service Management

### Start/Stop/Restart

```bash
sudo systemctl start crack-sms
sudo systemctl stop crack-sms
sudo systemctl restart crack-sms
sudo systemctl status crack-sms
```

### View Logs

```bash
# All logs
sudo journalctl -u crack-sms -n 100

# Tail (live)
sudo journalctl -u crack-sms -f

# Since specific time
sudo journalctl -u crack-sms --since "2 hours ago"

# Only errors
sudo journalctl -u crack-sms -p err
```

### Auto-restart on Reboot

```bash
# Already enabled with [Install] section above
sudo systemctl is-enabled crack-sms
# Output: enabled

# Manually enable if disabled
sudo systemctl enable crack-sms
```

---

## 📦 Database Setup

### Use SQLite (Local Development)

```python
# config.json
"DATABASE_URL": "bot_database.db"  # File-based, no setup needed
```

**Pros:** Simple, portable, works offline  
**Cons:** Not suitable for high-concurrency

### Use PostgreSQL (Production)

#### Option A: Railway PostgreSQL (Automatic)

Railway auto-provides `DATABASE_URL` — no manual setup needed.

#### Option B: Local PostgreSQL

```bash
# Install PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Create database
sudo -u postgres createdb botdb
sudo -u postgres createuser botuser -P  # Sets password
sudo -u postgres psql -c "GRANT ALL ON DATABASE botdb TO botuser;"

# Connection string
DATABASE_URL=postgresql://botuser:password@localhost/botdb
```

#### Option C: Managed PostgreSQL (AWS RDS / Azure Database)

```
DATABASE_URL=postgresql://user:pass@your-db.cxxxxxx.us-east-1.rds.amazonaws.com:5432/botdb
```

---

## 🌐 Domain & HTTPS Setup

### Using Let's Encrypt (Free)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Get certificate
sudo certbot certonly --standalone -d your-domain.com

# Auto-renewal
sudo systemctl enable certbot.timer
```

### Nginx Reverse Proxy

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location /webhook {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /wa {
        proxy_pass http://127.0.0.1:7891;
        proxy_set_header Host $host;
    }
}
```

---

## 📊 Monitoring & Alerts

### Using Uptime Robot (Free)

1. Visit uptimerobot.com
2. Create monitor → HTTPS → `https://your-app.railway.app/health`
3. Set interval to 5 minutes
4. Get alerts if bot goes down

### Using New Relic (APM)

```bash
# Install agent
pip install newrelic

# Start bot with agent
NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program python bot.py
```

### Prometheus + Grafana (Advanced)

Add to requirements.txt:
```
prometheus-client
```

Usage:
```python
from prometheus_client import Counter, Histogram

otp_counter = Counter('otp_received_total', 'Total OTPs received')
panel_response_time = Histogram('panel_response_seconds', 'Panel response time')
```

---

## 🚨 Backup & Recovery

### Backup SQLite Database

```bash
# Manual backup
cp bot_database.db bot_database.db.backup

# Automatic daily backup (cron)
0 2 * * * cp /path/to/bot_database.db /path/to/backups/bot_database_$(date +\%Y\%m\%d).db
```

### Backup PostgreSQL

```bash
# Manual
pg_dump -U botuser -h localhost botdb > backup.sql

# Restore
psql -U botuser -h localhost botdb < backup.sql

# Scheduled backup (daily at 2 AM)
(crontab -l 2>/dev/null; echo "0 2 * * * pg_dump -U botuser botdb > /backups/botdb_\$(date +\%Y\%m\%d).sql") | crontab -
```

### Backup to S3 / Cloud Storage

```bash
# Install AWS CLI
pip install awscli

# Upload backup
aws s3 cp bot_database.db s3://your-bucket/backups/bot_database.db

# Scheduled
0 3 * * * aws s3 cp /path/to/bot_database.db s3://bucket/backups/bot_\$(date +\%s).db
```

---

## 🔍 Troubleshooting Deployments

| Issue | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: No module named 'telegram'` | Missing dependencies | `pip install -r requirements.txt` |
| `Bot token invalid` | Wrong/expired token | Get new token from @BotFather |
| `Database connection refused` | DB not running | Start PostgreSQL or use SQLite |
| `Port 7891 in use` | Another service using port | `lsof -i :7891` → kill process |
| `SSL certificate error` | Cert expired | `sudo certbot renew` |
| `Command timeout` | Server slow | Increase timeout in config |

---

## ✅ Deployment Checklist

- [ ] Bot token set in environment
- [ ] Database configured and initialized
- [ ] Countries.json present (or using embedded)
- [ ] Admin IDs set correctly
- [ ] Channel/group links configured
- [ ] SSL certificate installed (if applicable)
- [ ] Backups configured
- [ ] Monitoring/alerts set up
- [ ] Logs being collected
- [ ] Systemd service enabled (if VPS)

**You're ready to deploy!** 🚀

