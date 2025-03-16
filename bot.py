import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Configuration du logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# Récupération du token depuis les variables d’environnement
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Fonction de réponse à /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Salut ! Je suis CashProno_bot 🤖. Tape /prono pour recevoir un pronostic !")

# Fonction pour générer un faux pronostic
async def prono(update: Update, context: CallbackContext):
    fake_prono = "🔥 Pronostic du jour : PSG gagne avec plus de 2.5 buts !"
    await update.message.reply_text(fake_prono)

# Création de l'application Telegram
app = Application.builder().token(TOKEN).build()

# Ajout des commandes
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("prono", prono))

# Lancement du bot
if __name__ == "__main__":
    logging.info("Bot en cours d'exécution...")
    app.run_polling()