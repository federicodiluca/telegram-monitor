from telegram import Update
from telegram.ext import ContextTypes, Application, CommandHandler
from utils import fetch_public_ip, get_system_metrics, ensure_log_directory, get_log_file_path
import logging
import os
import datetime

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Inizializza il bot e invia un messaggio di benvenuto."""
    message = update.message or update.callback_query.message
    await message.reply_text(
        "Benvenuto! Usa i seguenti comandi:\n"
        "- /ip per ottenere l'IP corrente e i dettagli\n"
        "- /log [n] per visualizzare gli ultimi n log degli IP del giorno corrente (predefinito: 10)\n"
        "- /metrics per ottenere le metriche di sistema (CPU, RAM, Internet, etc.)"
    )

async def ip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Gestisce il comando /ip per recuperare l'IP pubblico."""
    ip_info = fetch_public_ip()
    message = update.message or update.callback_query.message
    if ip_info:
        ip = ip_info.get("ip")
        details = "\n".join([f"{key}: {value}" for key, value in ip_info.items()])
        await message.reply_text(f"L'IP pubblico corrente è: {ip}\nDettagli:\n{details}")
    else:
        await message.reply_text("Impossibile recuperare l'IP pubblico.")

async def log(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Gestisce il comando /log per visualizzare il log degli IP del giorno corrente."""
    num_logs = int(context.args[0]) if context.args else 10
    message = update.message or update.callback_query.message
    log_dir = "log"
    ensure_log_directory(log_dir)
    log_file = get_log_file_path(log_dir)
    logs = []

    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            logs = f.readlines()

    logs = logs[-num_logs:]  # Get the last num_logs entries
    if logs:
        await message.reply_text(f"Log degli IP:\n{''.join(logs)}")
    else:
        await message.reply_text("Nessun log disponibile per oggi.")

async def metrics(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Gestisce il comando /metrics per recuperare le metriche di sistema."""
    metrics = get_system_metrics()
    message = update.message or update.callback_query.message
    await message.reply_text(metrics)

def register_handlers(application: Application) -> None:
    """Registra i gestori dei comandi."""
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ip", ip))
    application.add_handler(CommandHandler("log", log))
    application.add_handler(CommandHandler("metrics", metrics))