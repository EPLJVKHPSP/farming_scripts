# Impermanent loss calculator bot

Run your own Telegram bot with Python 3.10 or later. From this script's directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Create a bot with `@BotFather` and set `TELEGRAM_BOT_TOKEN` in `.env` to its
token. The script reads this file automatically; process environment variables
take precedence. Keep `.env` untracked.

```bash
python calculator.py
```

Open your bot and send `/start`. The calculator requests public prices from
CoinGecko. This script uses the asynchronous version 21 Telegram API. Install the
listed dependencies together in a dedicated virtual environment.
