import os
import logging
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, MessageHandler, filters, CommandHandler, CallbackContext

# Configuration du logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# Récupération du token
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # URL fournie par Render

# Création du bot
app = Application.builder().token(TOKEN).build()

# Liste des utilisateurs VIP
VIP_USERS = {123456789, 987654321}  # Remplace avec les vrais ID Telegram

# Création de l’application Flask
flask_app = Flask(__name__)

# Fonction d’envoi du menu avec boutons
async def send_buttons(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("📊 Pronostic Gratuit", callback_data="prono")],
        [InlineKeyboardButton("👑 Pronostic VIP", callback_data="prono_vip")],
        [InlineKeyboardButton("ℹ️ Infos VIP", callback_data="vip")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 Bienvenue sur *CashProno_bot* 🎉\n"
        "Choisis une option ci-dessous :",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# Fonction pour envoyer un message à l'ouverture de la conversation
async def start(update: Update, context: CallbackContext):
    """Envoie un message de bienvenue dès que l'utilisateur démarre la conversation."""
    await send_buttons(update, context)

# Gestion des boutons cliqués
async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == "prono":
        await query.message.reply_text("🔥 *Pronostic gratuit* : PSG gagne avec plus de 2.5 buts !", parse_mode="Markdown")
    elif query.data == "vip":
        await query.message.reply_text(
            "👑 *Accès VIP* 👑\n"
            "Les membres VIP reçoivent des pronostics avancés et des analyses détaillées.\n\n"
            "💰 *Pour rejoindre le VIP, contacte* @Admin.",
            parse_mode="Markdown"
        )
    elif query.data == "prono_vip":
        user_id = query.from_user.id
        if user_id in VIP_USERS:
            await query.message.reply_text("🔥 *Pronostic VIP* : Bayern gagne + les deux équipes marquent !", parse_mode="Markdown")
        else:
            await query.message.reply_text("❌ *Accès refusé.* Cette option est réservée aux membres VIP. Tape /vip pour plus d’infos.", parse_mode="Markdown")

# Route pour Telegram (Webhook)
@flask_app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    """Réception des messages de Telegram."""
    update = Update.de_json(request.get_json(), app.bot)
    app.update_queue.put_nowait(update)
    return "OK", 200

# Route pour vérifier si le serveur tourne
@flask_app.route("/")
def home():
    return "Le bot tourne ! 🚀", 200

# Ajouter les handlers au bot
app.add_handler(CommandHandler("start", start))  # Handler pour /start
app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, send_buttons))
app.add_handler(CallbackQueryHandler(button_handler))

# Lancement de Flask
if __name__ == "__main__":
    logging.info("Bot en cours d'exécution avec Webhook...")
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8443)))