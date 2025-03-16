import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, filters, MessageHandler, CallbackContext

# Configuration du logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# Récupération du Token depuis Render (ou mettre en dur pour tester)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "123456:ABC-DEF")  # Remplace par ton Token

# Liste des utilisateurs VIP (ajoute tes propres ID Telegram ici)
VIP_USERS = {123456789, 987654321}  # Remplace avec tes vrais ID Telegram

# Création du bot
app = Application.builder().token(TOKEN).build()

# Fonction d’accueil avec boutons
async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("📊 Pronostic Gratuit", callback_data="prono")],
        [InlineKeyboardButton("👑 Pronostic VIP", callback_data="prono_vip")],
        [InlineKeyboardButton("ℹ️ Infos VIP", callback_data="vip")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 Bienvenue sur CashProno_bot 🎉\nChoisis une option ci-dessous :",
        reply_markup=reply_markup
    )

# Gestion des boutons cliqués
async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == "prono":
        await query.message.reply_text("🔥 Pronostic gratuit : PSG gagne avec plus de 2.5 buts !")
    elif query.data == "vip":
        await query.message.reply_text(
            "👑 **Accès VIP** 👑\n"
            "Les membres VIP reçoivent des pronostics avancés et des analyses détaillées.\n\n"
            "💰 Pour rejoindre le VIP, contacte @Admin."
        )
    elif query.data == "prono_vip":
        user_id = query.from_user.id
        if user_id in VIP_USERS:
            await query.message.reply_text("🔥 Pronostic VIP : Bayern gagne + les deux équipes marquent !")
        else:
            await query.message.reply_text("❌ Accès refusé. Tape /vip pour plus d’infos.")

# Ajouter les handlers au bot
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

# Lancer le bot en mode Polling
if __name__ == "__main__":
    logging.info("Bot en cours d'exécution...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)