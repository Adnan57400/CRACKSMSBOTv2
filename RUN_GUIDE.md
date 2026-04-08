# 🚀 RUN.PY QUICK SETUP GUIDE

## What is run.py?

`run.py` is an intelligent launcher that:
- ✅ Automatically installs all Python dependencies from `requirements.txt`
- ✅ Automatically installs all Node.js packages from `package.json`
- ✅ Validates your configuration
- ✅ Starts both services (WhatsApp bridge + Bot simultaneously)
- ✅ Handles Windows & Linux/Mac ports

## Installation & Setup

### 1. **Install Node.js** (One-time setup)
If you haven't already:
- Visit: https://nodejs.org/ (LTS version recommended)
- Download and install

### 2. **Configure your bot**

Edit `config.json`:
```json
{
  "BOT_TOKEN": "YOUR_TELEGRAM_BOT_TOKEN",
  "BOT_USERNAME": "YourBotHandle",
  "ADMIN_IDS": [123456789, 987654321],
  "OTP_GROUP_LINK": "https://t.me/yourgroup",
  "CHANNEL_LINK": "https://t.me/yourchannel"
}
```

## Running the Bot

### **Option 1: Python (Recommended)**
```bash
python run.py
```

### **Option 2: Windows Command Prompt**
```cmd
python run.py
```

### **Option 3: With Python Launcher**
```bash
python3 run.py
```

## What Happens When You Run run.py

```
╔══════════════════════════════════════════════════════════╗
║     🔐 CRACK SMS BOT LAUNCHER - v3.0 (Premium)          ║
║          Intelligent Dependency Installer               ║
╚══════════════════════════════════════════════════════════╝

✓ Checking Python dependencies...
  • Installing: python-telegram-bot, aiohttp, sqlalchemy, etc.

✓ Checking Node.js dependencies...
  • npm installing @whiskeysockets/baileys, axios, pino, etc.

✓ Configuration validated
  ✓ BOT_TOKEN configured
  ✓ All settings OK

🚀 Starting bot services
  → WhatsApp bridge starting (port 7891)
  → Waiting 5 seconds for bridge to initialize...
  → Python bot starting...

✨ Both services are now running!
```

## Troubleshooting

### ❌ "Python not found"
**Solution:** Add Python to PATH or use full path:
```bash
C:\Python39\python.exe run.py
```

### ❌ "Node.js not found"
**Solution:** Install Node.js from https://nodejs.org/

### ❌ "pip permission denied"
**Solution:** Try with --user flag or use virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
python run.py
```

### ❌ "Port 7891 already in use"
**Solution:** Change PORT in whatsapp_otp.js or kill the process using it

### ❌ "BOT_TOKEN not configured"
**Solution:** Create `config.json` with proper BOT_TOKEN from @BotFather

## Manual Alternative (Without run.py)

If run.py doesn't work:

```bash
# Terminal 1: Install Python dependencies
pip install -r requirements.txt

# Terminal 2: Install Node dependencies  
npm install

# Terminal 3: Start WhatsApp bridge
node whatsapp_otp.js

# Terminal 4: Start the bot (after 5 second delay)
python bot.py
```

## File Structure

```
├── run.py                 ← THE LAUNCHER (use this!)
├── bot.py                 ← Main bot code
├── whatsapp_otp.js       ← WhatsApp bridge
├── bot_manager.py        ← Child bot manager
├── database.py           ← Database ORM
├── utils.py              ← Helper functions
├── countries.json        ← 238 countries data
├── requirements.txt      ← Python dependencies
├── package.json          ← Node dependencies
├── config.json           ← Your configuration
└── bot.log               ← Auto-generated logs
```

## Environment Variables (Optional)

Create `.env` file for sensitive data:
```
BOT_TOKEN=7952943119:AAFGuZiurY4yiaTCPwkrmsH51EUayr_DUFU
DATABASE_URL=sqlite:///bot.db
WA_FORWARD_URL=http://localhost:7891
```

Then in `config.json`:
```json
{
  "BOT_TOKEN": "${BOT_TOKEN}"
}
```

## Features After Installation

✅ **100% Free Numbers**
- No payment required
- Real-time OTP delivery
- 200+ countries

✅ **Admin Panel**
- Manage SMS panels
- Monitor statistics
- Create child bots
- View logs

✅ **Premium Tiers** (Optional)
- Free: 50 OTPs/day, 2 panels
- Pro: 500 OTPs/day, 10 panels
- Enterprise: 5000 OTPs/day, 50 panels

✅ **Multiple Integrations**
- Telegram OTP
- WhatsApp OTP
- SMS panels
- Webhooks

## Getting Help

Check these files for detailed information:
- 📖 **README.md** - Full feature overview
- 🚀 **DEPLOYMENT.md** - Production setup
- 🔧 **CONFIGURATION.md** - All config options
- ⚠️ **TROUBLESHOOTING.md** - Common issues
- 🎯 **QUICKSTART.md** - 5-minute setup

## Next Steps

1. ✅ Run `python run.py`
2. ✅ Check logs for any errors
3. ✅ Get your bot username from console
4. ✅ Start using `/start` in Telegram
5. ✅ Access admin panel with `/admin`

Happy botting! 🎉

---
**Version:** 3.0 (Premium)  
**Last Updated:** 2026-04-08  
**Status:** ✨ Production Ready
