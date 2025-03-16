import logging
import requests
import telegram
from telegram.ext import Updater, CommandHandler
from apscheduler.schedulers.background import BackgroundScheduler
import os

# Config
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Stocké dans les variables d’environnement
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")  # ID du canal

# Initialisation du bot
bot = telegram.Bot(token=TOKEN)
logging.basicConfig(level=logging.INFO)

# Fonction pour envoyer un pronostic gratuit
def send_free_pronostic():
    pronostic = "📢 Pronostic Gratuit du Jour 📢\n\n🔹 Équipe A vs Équipe B\n🔹 Pari conseillé : Victoire Équipe A\n🔹 Confiance : ⭐⭐⭐⭐"
    bot.send_message(chat_id=CHANNEL_ID, text=pronostic)

# Fonction pour envoyer un pronostic VIP
def send_vip_pronostic():
    pronostic = "🔥 Pronostic VIP 🔥\n\n🔹 Match : Équipe X vs Équipe Y\n🔹 Pari : Over 2.5 Buts\n🔹 Confiance : ⭐⭐⭐⭐⭐\n\n📩 Contacte @admin pour l’abonnement VIP."
    bot.send_message(chat_id=CHANNEL_ID, text=pronostic)

# Planifier l’envoi automatique
scheduler = BackgroundScheduler()
scheduler.add_job(send_free_pronostic, 'cron', hour=12)  # Pronostic gratuit à midi
scheduler.add_job(send_vip_pronostic, 'cron', hour=18)   # Pronostic VIP à 18h
scheduler.start()

if __name__ == "__main__":
    print("Bot en cours d'exécution...")