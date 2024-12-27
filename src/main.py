import os
import time
import requests
import asyncio
import nest_asyncio
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
from bot import start, ip, log, metrics, register_handlers
from utils import fetch_public_ip, log_ip_check, log_ip_change
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Configurazione dal file .env
TOKEN = os.getenv("TELEGRAM_TOKEN")
POLLING_INTERVAL = int(os.getenv("POLLING_INTERVAL", 120))
LOG_DIR = "log"
LOG_RETENTION_DAYS = int(os.getenv("LOG_RETENTION_DAYS", 14))
CHAT_ID = os.getenv("CHAT_ID")

# Variabile per tenere traccia dell'IP corrente
current_ip_info = None

async def check_ip_change():
    global current_ip_info
    bot = Bot(token=TOKEN)
    while True:
        new_ip_info = fetch_public_ip()
        if new_ip_info:
            log_ip_check(new_ip_info, LOG_DIR)
            if current_ip_info and new_ip_info.get("ip") != current_ip_info.get("ip"):
                log_ip_change(current_ip_info, new_ip_info, LOG_DIR, LOG_RETENTION_DAYS)
                # Notify via Telegram bot
                old_ip = current_ip_info.get("ip")
                new_ip = new_ip_info.get("ip")
                old_info = "\n".join([f"{key}: {value}" for key, value in current_ip_info.items()])
                new_info = "\n".join([f"{key}: {value}" for key, value in new_ip_info.items()])
                message = f"IP CAMBIATO DA {old_ip} A {new_ip}\n\nVecchie Info:\n{old_info}\n\nNuove Info:\n{new_info}"
                await bot.send_message(chat_id=CHAT_ID, text=message)
            current_ip_info = new_ip_info
        await asyncio.sleep(POLLING_INTERVAL)

async def main():
    """Funzione principale per avviare il bot."""
    application = Application.builder().token(TOKEN).build()

    # Aggiunta dei gestori di comando
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ip", ip))
    application.add_handler(CommandHandler("log", log))
    application.add_handler(CommandHandler("metrics", metrics))

    # Avvio del polling
    asyncio.create_task(check_ip_change())
    await application.run_polling()

if __name__ == "__main__":
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())