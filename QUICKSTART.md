# ⚡ Quick Start Guide

Get your Crack SMS bot running in 5 minutes!

---

## 🚀 Fastest Path: Railway (Recommended)

### Step 1: Prepare Your Files (2 min)

No setup needed! If you have the files, skip to Step 2.

### Step 2: Create Railway Project (1 min)

```bash
# Visit: https://railway.app
# Click: New Project → Deploy from Git
# Select: Your GitHub repo
```

### Step 3: Set Environment Variables (1 min)

In Railway Dashboard → Variables:

```
BOT_TOKEN=7952943119:AAFGuZiurY4yia...
```

That's it! Railway auto-provides `DATABASE_URL`.

### Step 4: Deploy (1 min)

Click **Deploy** button. Bot starts automatically.

### Step 5: Verify It Works (1 min)

Open Telegram → find your bot → /start

✅ **Done!** Your bot is live!

---

## 💻 Local Testing (5 min)

### Prerequisites
- Python 3.9+ → `python --version`
- npm → `npm --version`

### Setup

```bash
# 1. Clone repo
git clone <your-repo>
cd <your-repo>

# 2. Install dependencies
pip install -r requirements.txt
npm install

# 3. Create config file
cat > config.json << 'EOF'
{
  "BOT_TOKEN": "get_from_BotFather",
  "BOT_USERNAME": "YourBotUsername",
  "INITIAL_ADMIN_IDS": [your_telegram_id],
  "CHANNEL_LINK": "https://t.me/yourchannel",
  "OTP_GROUP_LINK": "https://t.me/yourgroup",
  "SUPPORT_USER": "@yourname",
  "DEVELOPER": "@yourname"
}
EOF

# 4. Run bot (Terminal 1)
python bot.py

# 5. Run WhatsApp bridge (Terminal 2) - OPTIONAL
node whatsapp_otp.js
```

**Your bot is now running locally!**

---

## 🐳 Docker (3 min)

```bash
# Build
docker-compose up --build

# View
docker logs -f crack-sms-bot_bot_1
```

---

## 📋 Configuration Minimum

Only 3 fields required:

```json
{
  "BOT_TOKEN": "your_token_from_BotFather",
  "INITIAL_ADMIN_IDS": [your_telegram_id],
  "CHANNEL_LINK": "https://t.me/yourgroup"
}
```

---

## 🔑 Get Your Telegram Bot Token

1. Open Telegram → @BotFather
2. Send `/mybots`
3. Select your bot (or create new with `/newbot`)
4. Click "Token"
5. Copy entire string
6. Set in config: `"BOT_TOKEN": "paste_here"`

---

## 👤 Get Your Telegram User ID

1. Message @userinfobot
2. It replies with your ID
3. Set in config: `"INITIAL_ADMIN_IDS": [your_id]`

---

## ✅ Common First Commands

After bot starts, send these:

| Command | What it does |
|---------|-------------|
| `/start` | Show main menu |
| `/admin` | Admin panel (if you're admin) |
| `/help` | Help & FAQ |
| `/buy` | Get phone numbers |

---

## 🚨 Stuck? Read These

- **"Telegram Bot Token Invalid"** → Check token in BotFather again
- **"Database not found"** → SQLite auto-created, just wait
- **"Port 7891 in use"** → Change port: `WA_BRIDGE_PORT=7892`
- **"Module not found"** → Run `pip install -r requirements.txt` again

More help: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 📚 Next Steps

1. ✅ Bot running
2. 📖 Read [README.md](README.md) for features overview
3. ⚙️ Customize in [CONFIGURATION.md](CONFIGURATION.md)
4. 🚀 Deploy to Railway/Docker using [DEPLOYMENT.md](DEPLOYMENT.md)
5. 🐛 If issues, check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

**You're ready!** 🎉

Need help? → Contact @NONEXPERTCODER on Telegram

