# 🚀 Crack SMS v20 — Professional OTP Bot

**Enterprise-grade Telegram OTP bot with WhatsApp bridge integration, multi-panel support, child bots, and advanced admin features.**

---

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)
- [Support](#support)

---

## ✨ Features

### Core OTP Management
- ✅ **Real-time SMS capture** from multiple SMS panels (API, IVAS, custom)
- ✅ **30 unique OTP GUI themes** — premium animations for Telegram Premium users
- ✅ **Auto-detect country** from phone numbers using phonenumbers library
- ✅ **OTP storage** with copy buttons and full SMS text
- ✅ **Country-based filtering** with 238+ countries and animated flag emojis

### Multi-Panel Support
- ✅ **Multiple SMS panels** — run 10+ simultaneously
- ✅ **Isolated sessions** — each panel account fully isolated (no cookie mixing)
- ✅ **Auto-reconnect** — retry logic with exponential backoff
- ✅ **Real-time stats** — live panel status, OTP count, uptime

### WhatsApp Bridge (Professional)
- ✅ **Phone number pairing** — no QR code needed
- ✅ **Pairing code mode** — secure multi-device
- ✅ **QR code mode** — traditional method
- ✅ **Auto-forward OTPs** to WhatsApp groups
- ✅ **Webhook integration** — receive OTPs from external sources
- ✅ **Group management** — set target groups, manage auto-forward

### Child Bots (Enterprise)
- ✅ **Create unlimited child bots** — each with own database & config
- ✅ **Isolated environments** — no data sharing between bots
- ✅ **Admin approval workflow** — manage bot creation requests
- ✅ **Per-bot statistics** — track OTPs, panels, users independently
- ✅ **Dynamic folder structure** — bots auto-created in `child_bots/` directory

### Admin Panel
- ✅ **Super admin controls** — manage all bots, users, and settings
- ✅ **User management** — assign numbers, set OTP limits, manage prefixes
- ✅ **Panel control** — add/remove/monitor SMS panels in real-time
- ✅ **Broadcast & notifications** — send announcements to users and groups
- ✅ **Logs & reports** — full SMS history, OTP stats, analytics

### Premium Tier System
- 🆓 **Free** — 50 OTPs/day, 2 panels max
- 💎 **Pro** — 500 OTPs/day, 10 panels, analytics & webhooks
- 🏆 **Enterprise** — 5000 OTPs/day, 50 panels, WA Business, API access

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    TELEGRAM BOT (Python)                   │
│  • Main bot or child bot (IS_CHILD_BOT flag)               │
│  • Receives /commands and callback queries                  │
│  • Manages user numbers, prefixes, OTP storage              │
└──────────────┬──────────────────────────────────────────────┘
               │
        ┌──────▼──────┐
        │  DATABASE   │  (SQLite on Railway or PostgreSQL)
        │  bot_database.db                │
        │  • Users    │                   │
        │  • Numbers  │                   │
        │  • History  │
        │  • Permissions                  │
        └─────────────┘
               │
        ┌──────▼──────────────────────┐
        │   SMS PANEL WORKERS         │  (Async polling)
        │  • API-based panels         │  (aiohttp ClientSession per panel)
        │  • IVAS panels              │
        │  • Custom integration       │
        │  (Each has isolated session)│
        └──────┬───────────────────────┘
               │ (extract OTP → process_incoming_sms)
               │
        ┌──────▼──────────────────────┐
        │  OTP PROCESSING ENGINE      │
        │  • Country detection        │  (phonenumbers)
        │  • OTP extraction (regex)   │  (Format: 000-000 or 000000)
        │  • DM to assigned user      │
        │  • Log group forwarding     │  (15-min auto-delete)
        └──────┬───────────────────────┘
               │
        ┌──────▴──────────────────────┐
        │  WHATSAPP BRIDGE (Node.js)  │  (Optional, separate service)
        │  whatsapp_otp.js            │
        │  • Phone/code/QR pairing    │
        │  • Receives OTP webhook     │
        │  • Forwards to WA groups    │
        └─────────────────────────────┘
```

### Data Flow

1. **SMS In** → Panel worker captures SMS
2. **Extract** → Regex + OTP detection
3. **Route** → Find assigned user (database lookup)
4. **DM** → Send to user with copy button
5. **Log** → Broadcast to log groups (15-min TTL)
6. **WA** → Forward to WhatsApp bridge (if configured)

---

## 📦 Installation

### Prerequisites

- **Python 3.9+**
- **Node.js 16+** (for WhatsApp bridge)
- **Telegram Bot Token** (create via @BotFather)

### Local Setup

```bash
# 1. Clone or download repository
git clone <your-repo> && cd <your-repo>

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Install Node.js dependencies (optional, for WA bridge)
npm install

# 5. Create config.json (see Configuration section)
cp config.example.json config.json
# Edit config.json with your settings

# 6. Initialize database
python -c "import asyncio; from database import init_db; asyncio.run(init_db())"

# 7. Run bot
python bot.py

# 8. (Optional) Run WhatsApp bridge in another terminal
node whatsapp_otp.js
```

### Docker Setup (Local)

```bash
docker-compose up --build
```

---

## ⚙️ Configuration

### `config.json` Structure

```json
{
  "BOT_TOKEN": "7952943119:AAFGuZiurY4yiaTCPwkrmsH51EUayr_DUFU",
  "BOT_USERNAME": "CrackSMSReBot",
  "INITIAL_ADMIN_IDS": [7763727542, 7057157722],
  "CHANNEL_LINK": "https://t.me/crackotp",
  "OTP_GROUP_LINK": "https://t.me/crackotpgroup",
  "SUPPORT_USER": "@NONEXPERTCODER",
  "DEVELOPER": "@ownersigma",
  "OTP_GUI_THEME": 0,
  "IS_CHILD_BOT": false,
  "DATABASE_URL": "bot_database.db"
}
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BOT_TOKEN` | (required) | Telegram bot token from @BotFather |
| `DATABASE_URL` | `bot_database.db` | SQLite file or PostgreSQL URL (Railway) |
| `WA_BRIDGE_HOST` | `http://127.0.0.1:7891` | WhatsApp bridge URL (change for separate service) |
| `WA_BRIDGE_PORT` | `7890` | Port for bot to receive OTP webhooks |
| `WA_PAIRING_MODE` | `qr` | WhatsApp pairing: `qr`, `code`, or `phone` |
| `WA_PHONE_NUMBER` | (empty) | Phone number for direct pairing (format: `+1234567890`) |
| `WA_LOG_LEVEL` | `info` | Log level: `debug`, `info`, `warn`, `error` |
| `IS_CHILD_BOT` | `false` | Set to `true` for child bot instances |
| `OTP_GUI_THEME` | `0` | OTP message theme (0-29) |

### Countries Database

**Built-in file: `countries.json`** — 238 countries with dial codes and flag emojis.

If using a custom list:
```json
[
  {
    "name": "United States",
    "dial_code": "+1",
    "code": "US",
    "flag": "🇺🇸"
  }
]
```

Bot also has **embedded fallback** (`_EMBEDDED_COUNTRIES` in bot.py) — works even without the file.

---

## 🚀 Deployment

### Option 1: Railway (Recommended for Production)

#### Single Service (Bot + WA Bridge Together)

```toml
# railway.toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "node whatsapp_otp.js & sleep 5 && exec python bot.py"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

**Environment variables to set in Railway dashboard:**

```
BOT_TOKEN=your_token_here
DATABASE_URL=postgresql://...  # Railway auto-provides this
WA_BRIDGE_HOST=http://127.0.0.1:7891
```

#### Two Separate Services (Best for Scaling)

**Service 1: Telegram Bot**
```toml
[deploy]
startCommand = "python bot.py"
```
Env vars:
```
WA_BRIDGE_HOST=https://your-wa-service.railway.app
```

**Service 2: WhatsApp Bridge**
```toml
[deploy]
startCommand = "node whatsapp_otp.js"
```

### Option 2: Heroku (Legacy)

```procfile
web: node whatsapp_otp.js & sleep 5 && exec python bot.py
```

### Option 3: Render

Create `render.yaml`:
```yaml
services:
  - type: web
    name: crack-sms-bot
    buildCommand: "pip install -r requirements.txt && npm install"
    startCommand: "node whatsapp_otp.js & sleep 5 && exec python bot.py"
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y nodejs npm

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN npm install

CMD ["sh", "-c", "node whatsapp_otp.js & sleep 5 && exec python bot.py"]
```

---

## 📡 API Reference

### WhatsApp Bridge Endpoints

#### `POST /forward_otp`
Forward OTP to WhatsApp group.

**Request:**
```json
{
  "phone": "+1234567890",
  "otp": "123456",
  "service": "WhatsApp",
  "region": "US",
  "full_message": "Your WhatsApp code is: 123456",
  "secret": "cracksms_wa_secret_2026"
}
```

**Response:**
```json
{
  "success": true,
  "message": "OTP forwarded to group"
}
```

#### `POST /control`
Admin control panel for bridge.

**Example:**
```json
{
  "action": "status",
  "secret": "cracksms_wa_secret_2026"
}
```

#### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "connected": true,
  "phone": "+1234567890",
  "uptime": 3600,
  "otpsToday": 42
}
```

### Telegram Bot Commands

| Command | Role | Description |
|---------|------|-------------|
| `/start` | Any | Main menu |
| `/otpfor <phone>` | Admin | Find OTP by phone |
| `/panel add` | Super Admin | Add SMS panel |
| `/panel list` | Super Admin | List panels |
| `/bot create` | User | Request new bot |
| `/admin` | Admin | Admin panel |
| `/broadcast <msg>` | Super Admin | Send to all users |

---

## 🔧 Troubleshooting

### Issue 1: "No OTP received" / Country shows "Unknown"

**Cause:** `countries.json` missing or empty.

**Fix:**
- Ensure `countries.json` is in the working directory
- Bot has embedded fallback with 188 countries — fallback used automatically
- If using phonenumbers library, ensure it's installed: `pip install phonenumbers`

**Verify:**
```bash
python -c "import phonenumbers; print('✓ phonenumbers OK')"
```

### Issue 2: WhatsApp Bridge Not Reachable on Railway

**Cause:** Bridge binds to `127.0.0.1` (localhost only) — inaccessible from other containers/services.

**Fix:**
1. In `whatsapp_otp.js` line ~1032, change:
   ```javascript
   // BEFORE
   server.listen('127.0.0.1', 7891)
   
   // AFTER
   server.listen('0.0.0.0', 7891)  // Bind to all interfaces
   ```

2. Deploy with proper startup delay in `railway.toml`:
   ```toml
   startCommand = "node whatsapp_otp.js & sleep 5 && exec python bot.py"
   ```

3. Or run as separate services with env var:
   ```
   WA_BRIDGE_HOST=https://your-wa-service.railway.app
   ```

### Issue 3: Webhook Timeout / HTTP Errors

**Cause:** `ClientTimeout(seconds=N)` is wrong parameter name — should be `total=`.

**Fix:** Already applied in bot.py lines 455 & 490. If you see timeout errors:

```python
# WRONG
timeout = aiohttp.ClientTimeout(seconds=5)

# CORRECT
timeout = aiohttp.ClientTimeout(total=5)
```

### Issue 4: Bot Crashes on Startup

**Check logs:**
```bash
# Railway
railway logs

# Docker
docker logs <container-id>

# Local
python bot.py 2>&1 | tee bot.log
```

**Common causes:**
- Missing `BOT_TOKEN` env var
- Database file permissions
- Port 7891 already in use

### Issue 5: Child Bots Not Starting

**Check:**
```bash
# Verify folder structure
ls -la child_bots/

# Check logs
tail -f child_bots/bot_*/bot.log
```

**Common causes:**
- Super admin hasn't approved bot request yet
- Folder permissions issue
- Missing `registry.json`

---

## 📊 Monitoring

### View Bot Logs (Local)

```bash
tail -f bot.log
```

### View Database Stats

```bash
python -c "
import asyncio
from database import get_stats
stats = asyncio.run(get_stats())
print(stats)
"
```

### Monitor Panels

```bash
# Check active panels
python -c "
from bot import PANELS
for p in PANELS:
    print(f'{p.name}: is_logged_in={p.is_logged_in}, fail_count={p.fail_count}')
"
```

---

## 🔐 Security Best Practices

1. **Never commit secrets:**
   ```bash
   # Add to .gitignore
   config.json
   .env
   bot.log
   bot_database.db
   wa_bridge_state.json
   ```

2. **Use environment variables** for sensitive data:
   ```bash
   export BOT_TOKEN="your_token"
   export WA_OTP_SECRET="your_secret"
   ```

3. **Rotate admin IDs** periodically — remove old admins:
   ```python
   INITIAL_ADMIN_IDS = [new_admin_id_1, new_admin_id_2]
   ```

4. **Set strong database password** if using PostgreSQL on Railway

5. **Enable 2-step verification** on your Telegram account

---

## 📞 Support

- **Issues / Bugs:** Create GitHub issue
- **Questions:** Contact @NONEXPERTCODER or @ownersigma on Telegram
- **Join Community:** [CrackOTP Group](https://t.me/crackotpgroup)
- **Documentation:** [Full Docs](https://t.me/crackotp)

---

## 📄 License

Proprietary — Crack SMS v20 Professional Edition

---

## 🎯 Roadmap

- [ ] Web dashboard for analytics
- [ ] SMS panel auto-discovery
- [ ] Machine learning for OTP extraction
- [ ] Multi-language support
- [ ] REST API with API keys
- [ ] Slack integration

---

**Last Updated:** April 7, 2026  
**Version:** 20.0.0 (Professional Edition)  
**Maintainer:** @NONEXPERTCODER

