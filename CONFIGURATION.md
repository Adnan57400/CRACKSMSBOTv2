# Configuration Reference

Complete guide to all configuration options for Crack SMS v20 bot.

---

## 📝 Configuration File (`config.json`)

### Required Fields

```json
{
  "BOT_TOKEN": "7952943119:AAFGuZiurY4yiaTCPwkrmsH51EUayr_DUFU",
  "BOT_USERNAME": "CrackSMSReBot",
  "INITIAL_ADMIN_IDS": [7763727542, 7057157722],
  "CHANNEL_LINK": "https://t.me/crackotp",
  "OTP_GROUP_LINK": "https://t.me/crackotpgroup",
  "SUPPORT_USER": "@NONEXPERTCODER",
  "DEVELOPER": "@ownersigma"
}
```

### Optional Fields

```json
{
  "OTP_GUI_THEME": 0,
  "IS_CHILD_BOT": false,
  "DATABASE_URL": "bot_database.db",
  "DEFAULT_ASSIGN_LIMIT": 5,
  "NUMBER_BOT_LINK": "https://t.me/CrackSMSReBot"
}
```

---

## 🔑 Field Reference

### `BOT_TOKEN` (string, required)

**Description:** Telegram bot token from @BotFather

**How to get:**
1. Open Telegram → search @BotFather
2. Send `/mybots`
3. Select your bot
4. Click "Token"
5. Copy the entire string

**Example:**
```json
"BOT_TOKEN": "1234567890:ABCDefGHIjKLmnoPQRstUVwxYZ"
```

**⚠️ Security:**
- Never commit this to Git
- Store in `.env` file
- Use environment variable: `export BOT_TOKEN="..."`

---

### `BOT_USERNAME` (string, required)

**Description:** Your bot's Telegram username (without @)

**Example:**
```json
"BOT_USERNAME": "CrackSMSReBot"
```

**How to find:** Check your bot's profile or @BotFather `/mybots`

---

### `INITIAL_ADMIN_IDS` (array of integers, required)

**Description:** Telegram user IDs with admin access

**Example:**
```json
"INITIAL_ADMIN_IDS": [7763727542, 7057157722, 7968271742]
```

**How to get your ID:**
1. Message @userinfobot on Telegram
2. It replies with your ID
3. Copy the number

**Format:** Array of integers (NO QUOTES around numbers)

**⚠️ Wrong format:**
```json
"INITIAL_ADMIN_IDS": "123,456"  // ❌ String, wrong
"INITIAL_ADMIN_IDS": ["123", "456"]  // ❌ String array, wrong
"INITIAL_ADMIN_IDS": [123, 456]  // ✅ Integer array, correct
```

---

### `CHANNEL_LINK` (string, required)

**Description:** Link to your Telegram channel (shown in /start menu)

**Example:**
```json
"CHANNEL_LINK": "https://t.me/crackotp"
```

**Format:** Full URL starting with `https://t.me/`

---

### `OTP_GROUP_LINK` (string, required)

**Description:** Link to your OTP community group

**Example:**
```json
"OTP_GROUP_LINK": "https://t.me/crackotpgroup"
```

---

### `SUPPORT_USER` (string, required)

**Description:** Telegram username for support inquiries

**Example:**
```json
"SUPPORT_USER": "@NONEXPERTCODER"
```

**Format:** Include the `@` symbol

---

### `DEVELOPER` (string, required)

**Description:** Bot developer's Telegram username

**Example:**
```json
"DEVELOPER": "@ownersigma"
```

---

### `OTP_GUI_THEME` (integer, optional)

**Description:** OTP message display theme (0-29)

**Default:** `0` (Sami OTP - Classic)

**25 Themes Available:**
- **0-5:** Classic family (SAMI, TEMPNUM, Neon Electric, Premium Dark, Minimal Clean, Royal Gold)
- **6-9:** Bold family (JACK-X, Cyber Matrix, Fire Storm, Ice Blue)
- **10-15:** Premium family (Shadow Dark, Crypto, Sakura, Military, Hacker Green, Diamond)
- **16-19:** Modern family (Sigma Classic, Pulse, Bolt, Rose Gold)
- **20-29:** Extended themes (Astro, Retro, Neon Box, Vault, Steel, Aurora, Phantom, Emerald, Sunset, UltraPrime)

**Example - Fire Storm:**
```json
"OTP_GUI_THEME": 8
```

**Change via bot:** Super admin → /admin → OTP GUI Theme → Select 0-29

---

### `IS_CHILD_BOT` (boolean, optional)

**Description:** Set to `true` if this is a child bot instance

**Default:** `false`

**When to use:**
- `false` (default): Running main bot
- `true`: Running a child bot created from admin panel

**Example:**
```json
"IS_CHILD_BOT": true
```

**⚠️ Note:** Child bots are auto-configured. Don't set this manually unless troubleshooting.

---

### `DATABASE_URL` (string, optional)

**Description:** Database connection string

**Options:**

A) **SQLite (Local file):**
```json
"DATABASE_URL": "bot_database.db"
```
- Simple, single file
- Suitable for development/small deployments
- Default option

B) **PostgreSQL (Production):**
```json
"DATABASE_URL": "postgresql://user:password@localhost:5432/botdb"
```

C) **Railway (Auto):**
Railway provides `DATABASE_URL` automatically — don't set manually.

**Environment Variable Override:**
```bash
export DATABASE_URL="postgresql://..."
```

---

### `DEFAULT_ASSIGN_LIMIT` (integer, optional)

**Description:** Default number of phone numbers assigned per user

**Default:** `5`

**Example:**
```json
"DEFAULT_ASSIGN_LIMIT": 10
```

**What it does:**
- When user executes `/buy`, they get this many numbers
- Super admin can change per-user later

---

### `NUMBER_BOT_LINK` (string, optional)

**Description:** Link to bot for getting numbers (shown in OTP copy button)

**Example:**
```json
"NUMBER_BOT_LINK": "https://t.me/CrackSMSReBot"
```

**If not set:** Falls back to `BOT_USERNAME`

---

## 🌍 Environment Variables

### Overrides vs Config

Environment variables **override** `config.json`. Set them in:

```bash
# Local (terminal)
export BOT_TOKEN="..."
python bot.py

# Railway (Dashboard)
Settings → Variables → Add

# Docker (.env file)
BOT_TOKEN=...
DATABASE_URL=...

# Systemd (/etc/systemd/system/bot.service)
Environment="BOT_TOKEN=..."
```

---

### Available Environment Variables

| Variable | Type | Default | Purpose |
|----------|------|---------|---------|
| `BOT_TOKEN` | string | (required) | Telegram bot token |
| `DATABASE_URL` | string | `bot_database.db` | Database connection |
| `WA_BRIDGE_HOST` | string | `http://127.0.0.1:7891` | WhatsApp bridge URL |
| `WA_BRIDGE_PORT` | integer | `7890` | Port for OTP webhook receiver |
| `WA_PAIRING_MODE` | string | `qr` | WhatsApp pairing: qr, code, phone |
| `WA_PHONE_NUMBER` | string | (empty) | Phone for direct pairing (+1234567890) |
| `WA_LOG_LEVEL` | string | `info` | Logger level: debug, info, warn, error |
| `WA_OTP_SECRET` | string | `cracksms_wa_secret_2026` | Webhook secret key |
| `WA_OTP_PORT` | integer | `7890` | Webhook receiver port |
| `IS_CHILD_BOT` | boolean | `false` | Is this a child bot? |
| `OTP_GUI_THEME` | integer | `0` | Theme number 0-29 |

---

## 🔐 Security Best Practices

### 1. Never Commit Secrets to Git

```bash
# Create .gitignore
cat > .gitignore << 'EOF'
config.json
.env
*.log
bot_database.db
wa_session/
wa_bridge_state.json
child_bots/*/
venv/
__pycache__/
EOF

git add .gitignore
git commit -m "Add .gitignore"
```

### 2. Use Environment Variables

**Instead of:**
```json
{
  "BOT_TOKEN": "hardcoded_token"
}
```

**Do this:**
```bash
export BOT_TOKEN="..."
python bot.py
```

### 3. Rotate Admin IDs Regularly

```json
{
  "INITIAL_ADMIN_IDS": [
    7763727542,    // Old admin (to remove next week)
    123456789      // New admin (just added)
  ]
}
```

### 4. Use Strong Database Passwords

```bash
# PostgreSQL (change default password)
psql -U botuser -h localhost
\password botuser
# Enter strong password
```

### 5. Enable 2FA on Telegram

- Settings → Privacy & Security → Two-Step Verification
- Use strong passphrase

---

## 📦 SMS Panel Configuration

### Adding SMS Panels

**Via Bot Command:**
```
/panel add <base_url> <username> <password> <panel_type>
```

**Example:**
```
/panel add https://api.smspanel.com user123 pass123 api
/panel add https://ivas.provider.com admin pass456 ivas
```

### Panel Types

| Type | Protocol | Description |
|------|----------|-------------|
| `api` | HTTPS | REST API with JSON responses |
| `ivas` | Custom | IVAS-specific protocol |
| `custom` | Custom | Webhook/callback-based |

### Panel Requirements

**API Panels:**
- Must return JSON with fields: `phone`, `message`, `timestamp`
- Auth via header or query parameter
- Standard HTTP verbs (GET/POST)

**IVAS Panels:**
- Proprietary protocol
- Specific to IVAS provider
- Usually callback-based

---

## 🤖 Telegram Command Configuration

Commands available to different user roles:

### 🆓 Any User
- `/start` — Main menu
- `/help` — Help & FAQ
- `/profile` — View account
- `/buy` — Get numbers

### 👤 Admin Only
- `/admin` — Admin panel
- `/panel list` — View SMS panels
- `/otpfor <phone>` — Find OTP by phone

### 🔑 Super Admin Only
- `/panel add` — Add SMS panel
- `/panel remove` — Remove panel
- `/broadcast <msg>` — Send to all users
- `/set_channel <url>` — Change channel link
- `/bot list` — Manage child bots
- `/set_admin <uid>` — Add admin

---

## 🔧 Advanced Configuration

### Custom OTP Regex Pattern

**Location:** `bot.py` function `extract_otp_regex()`

**Default pattern:**
```python
def extract_otp_regex(msg: str) -> Optional[str]:
    patterns = [
        r'(?:code|otp)[\s:]*(\d{4,8})',
        r'(?:confirm|verify)[\s:]*(\d{4,8})',
        r'^\d{4,8}$',
    ]
    # ...
```

**Customize for your needs:**
```python
# Add custom pattern
patterns.append(r'(?:token|pin)[\s:]*(\d{6})')
```

### Database Indexes

For large deployments, add indexes:

```python
# In database.py
class Number(Base):
    # ...
    __table_args__ = (
        Index('idx_phone', 'phone_number'),
        Index('idx_assigned', 'assigned_to'),
        Index('idx_status', 'status'),
    )
```

### Rate Limiting

**WA Bridge per-minute limits:**

```bash
# In whatsapp_otp.js or env var
WA_RATE_LIMIT_PER_MIN=60  # Max 60 OTPs/minute
```

---

## 📋 Configuration Checklist

Before deploying:

- [ ] `BOT_TOKEN` set correctly
- [ ] `INITIAL_ADMIN_IDS` includes your ID
- [ ] `CHANNEL_LINK` points to real channel
- [ ] `OTP_GROUP_LINK` points to real group
- [ ] Database loaded (SQLite or PostgreSQL)
- [ ] `countries.json` present (or embedded backup used)
- [ ] SMS panels configured if needed
- [ ] WhatsApp bridge configured (if using WA features)
- [ ] `.gitignore` created (don't commit secrets)
- [ ] Backups configured

**Ready to deploy!** ✅

---

**Last Updated:** April 7, 2026

