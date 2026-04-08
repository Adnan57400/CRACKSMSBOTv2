# Troubleshooting Guide

Common issues and solutions for Crack SMS v20 bot.

---

## 🔴 Critical Issues

### 1. Bot Doesn't Start or Immediately Crashes

**Symptoms:**
```
Traceback (most recent call last):
  File "bot.py", line X, in <module>
    ...
ModuleNotFoundError: No module named 'X'
```

**Solutions:**

A) **Missing Dependencies**
```bash
pip install -r requirements.txt
pip list  # Verify all installed
```

B) **Python Version Wrong**
```bash
python --version  # Must be 3.9+
python3.11 -m pip install -r requirements.txt
```

C) **Virtual Environment Not Activated**
```bash
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

---

### 2. "Telegram Bot Token Invalid"

**Symptoms:**
```
telegram.error.Unauthorized: Unauthorized
```

**Checklist:**
- [ ] Token copied exactly from @BotFather
- [ ] No leading/trailing spaces
- [ ] Token not expired (try getting new one)
- [ ] `BOT_TOKEN` env var set correctly

**Fix:**
```bash
# Get fresh token
# 1. Open Telegram → @BotFather
# 2. /mybots → select bot → Edit Bot → Token
# 3. Copy entire token

export BOT_TOKEN="7952943119:AAFGuZiurY4yiaTCPwkrmsH51EUayr_DUFU"
python bot.py
```

---

### 3. Database Connection Error

**Symptoms:**
```
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) unable to open database file
```

**Causes & Fixes:**

| Cause | Fix |
|-------|-----|
| File permissions | `chmod 666 bot_database.db` |
| Wrong path | Use absolute path in DATABASE_URL |
| No write access | Create db in `/tmp` temporarily |
| PostgreSQL not running | `sudo service postgresql start` |
| Connection string wrong | Use `postgresql://user:pass@host/db` format |

**Test database connection:**
```python
import asyncio
from database import AsyncSessionLocal, init_db

asyncio.run(init_db())
print("✓ Database OK")
```

---

### 4. "Address already in use" (Port 7891)

**Symptoms:**
```
OSError: [Errno 48] Address already in use
```

**Find process using port:**
```bash
# Linux/Mac
lsof -i :7891
netstat -tlnp | grep 7891

# Windows
netstat -ano | findstr :7891
```

**Kill process:**
```bash
# Linux/Mac
kill -9 <PID>

# Windows
taskkill /PID <PID> /F
```

**Or use different port:**
```bash
export WA_OTP_PORT=7892
python bot.py
```

---

## ⚠️ Common Operational Issues

### 5. No OTPs Received / "Unknown Country"

**Symptoms:**
- OTP not appearing in bot
- Country shows "Unknown" 🌍 instead of actual country

**Root Cause:** `countries.json` missing or empty

**Check:**
```bash
ls -la countries.json
cat countries.json | head -20

# Should show 238+ countries
python -c "import json; print(len(json.load(open('countries.json'))))"
```

**Solutions:**

A) **If file missing:** Download from GitHub or bot.py has embedded backup with 188 countries

B) **If empty:** Recreate file:
```bash
# Copy from source
cp countries.json.bak countries.json

# Or use embedded fallback (automatic)
```

C) **Verify phonenumbers library:**
```bash
pip install phonenumbers
python -c "import phonenumbers; print('✓ OK')"
```

**Test detection:**
```python
from bot import detect_country_from_numbers
result = detect_country_from_numbers(["+12125551234"])
print(result)  # Should show: ("United States", "🇺🇸")
```

---

### 6. WhatsApp Bridge Not Connecting

**Symptoms:**
- WA status shows 🔴 Disconnected
- Can't set WhatsApp group
- OTPs not forwarding to Telegram

**Check Bridge Health:**
```bash
curl http://127.0.0.1:7891/health
# Should return JSON with status
```

**If timeout/connection refused:**

A) **Bridge not started:**
```bash
# Check if running
ps aux | grep whatsapp_otp.js

# If not, start it:
node whatsapp_otp.js
```

B) **Bridge binding to localhost only (Railway issue):**
- Edit `whatsapp_otp.js` line ~1032:
```javascript
// WRONG - inaccessible from other containers
server.listen('127.0.0.1', 7891)

// CORRECT - accessible from any service
server.listen('0.0.0.0', 7891)
```

C) **Firewall blocking port 7891:**
```bash
sudo ufw allow 7891
sudo firewall-cmd --permanent --add-port=7891/tcp
```

D) **Wrong bridge URL:**
```bash
# Check env var
echo $WA_BRIDGE_HOST

# Should be http://127.0.0.1:7891 (local) or
# https://your-wa-service.railway.app (separate service)
```

**Bridge logs:**
```bash
# Check error output
tail -f wa_bridge.log  # If logging to file

# Or start with verbose logging
WA_LOG_LEVEL=debug node whatsapp_otp.js
```

---

### 7. Admin Commands Not Working

**Symptoms:**
- `/admin` returns "Unauthorized"
- Can't manage panels

**Check:**
```python
# Verify admin ID
from bot import INITIAL_ADMIN_IDS, is_super_admin
print(f"Admins: {INITIAL_ADMIN_IDS}")
print(f"Your ID: {7763727542}")  # Replace with your ID
print(is_super_admin(7763727542))  # Should print True
```

**Fix:**
```bash
# Add your user ID to config:
# Open config.json and update INITIAL_ADMIN_IDS array

# Or via command (send to bot):
# /set_admin <your_user_id>  (if this command exists)
```

**Get your Telegram ID:**
- Message @userinfobot
- It replies with your ID

---

### 8. Panels "FAILED" Status / Can't Login

**Symptoms:**
```
❌ API Panel  —  FAILED
```

**Debug:**
```python
from bot import PANELS
for panel in PANELS:
    print(f"{panel.name}: is_logged_in={panel.is_logged_in}")
    print(f"  fail_count={panel.fail_count}")
    print(f"  last_error={panel.last_error if hasattr(panel, 'last_error') else 'N/A'}")
```

**Common causes:**

| Cause | Fix |
|-------|-----|
| Wrong credentials | Check username/password in panel config |
| Panel HTTPS cert expired | Add `verify_ssl=False` (proceed with caution) |
| Panel API changed | Check panel's API documentation |
| Rate limit hit | Wait 5-10 minutes, bot auto-retries |
| Network timeout | Increase `timeout` in config |

**Re-add panel:**
```bash
# Via bot: /panel remove <panel_name>
# Then: /panel add <new_url> <username> <password>
```

---

### 9. Child Bots Not Starting

**Symptoms:**
```
Bot request approved but doesn't show in /bot list
```

**Check folder structure:**
```bash
ls -la child_bots/
# Should show: bot_XXXXXXX_XXXX/ folders

ls -la child_bots/bot_*/registry.json
```

**Verify registry:**
```python
import json
reg = json.load(open('child_bots/registry.json'))
print(json.dumps(reg, indent=2))
```

**Fix:**
```bash
# Delete broken bot
rm -rf child_bots/bot_XXXXX

# Re-approve via admin panel
/admin_bots → Add Bot
```

---

### 10. OTP Messages Too Large / Timeout

**Symptoms:**
```
Message too long. Max 4096 characters allowed
```

**Cause:** OTP message format too verbose

**Fix:**
1. Reduce OTP_GUI_THEME to simpler format
2. Reduce SMS body preview (change `body160` to shorter)
3. Split messages:

```python
# In do_sms_hit()
if len(grp_txt) > 4000:
    for chunk in [grp_txt[i:i+3500] for i in range(0, len(grp_txt), 3500)]:
        await bot_app.bot.send_message(gid, chunk, parse_mode="HTML")
```

---

## 🔧 Configuration Issues

### 11. Multiple Admin IDs Not Working

**File:** `config.json`

**Wrong:**
```json
{
  "INITIAL_ADMIN_IDS": "123,456,789"  // ← String, not array
}
```

**Correct:**
```json
{
  "INITIAL_ADMIN_IDS": [123, 456, 789]  // ← Array of numbers
}
```

---

### 12. Link Commands Don't Update

**Symptoms:** Setting channel link via `/set_channel` doesn't persist

**Check:**
```bash
ls -la config.json
grep CHANNEL_LINK config.json
```

**Fix:**
```bash
# Ensure config.json is writable
chmod 644 config.json

# Restart bot
killall python
python bot.py
```

---

## 🌐 Deployment-Specific Issues

### Railway: Bot Crashes Immediately

**Check logs:**
```bash
railway logs --tail
```

**Common causes:**
1. Missing env vars — set all in Railway dashboard
2. Bad DATABASE_URL — Railway provides automatically as: `DATABASE_URL`
3. Package installed via npm when should be pip

**Fix:**
```toml
# Ensure railway.toml has:
[deploy]
startCommand = "node whatsapp_otp.js & sleep 5 && exec python bot.py"
```

### Docker: Database Persists Across Restarts

**Solution:** Use volumes:

```yaml
services:
  bot:
    volumes:
      - ./bot_database.db:/app/bot_database.db
      - ./config.json:/app/config.json
```

### Webhook Timeout Issues

**Symptoms:**
```
aiohttp.client.ClientConnectorError: Cannot connect
```

**Fix:** Already patched in bot.py, but if you see this:

```python
# WRONG
timeout = aiohttp.ClientTimeout(seconds=5)

# CORRECT  
timeout = aiohttp.ClientTimeout(total=5)
```

Lines affected: 455, 490

---

## 📊 Monitoring & Debugging

### Enable Debug Logging

```bash
export LOGGING_LEVEL=DEBUG
python bot.py
```

**Output:** More verbose logs showing every request/response

### Save Logs to File

```bash
python bot.py > bot.log 2>&1 &
tail -f bot.log
```

### Monitor Resource Usage

```bash
# Memory & CPU
top -p $(pgrep -f "python bot.py")

# Database size
du -sh bot_database.db

# Open connections
lsof -p $(pgrep -f "python bot.py")
```

---

## 💡 Ask For Help

If issue persists:

1. **Gather logs:**
   ```bash
   python bot.py 2>&1 | tee debug.log
   ```

2. **Check environment:**
   ```bash
   python --version
   pip list | grep -E "telegram|sqlalchemy|aiohttp|phonenumbers"
   ```

3. **Contact support:**
   - Telegram: @NONEXPERTCODER or @ownersigma
   - Include: Error message + debug.log
   - Include: OS, Python version, deployment platform

---

**Last Updated:** April 7, 2026

