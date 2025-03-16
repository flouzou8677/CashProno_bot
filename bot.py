import os
import logging
import asyncio
import schedule
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, CallbackContext

# Configuration du logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# Token du bot
TOKEN = "8181308468:AAFmC567gtnZucX5VXo1S9mRSYyzmbK25CU"

# Base de données des utilisateurs
VIP_USERS = set()
SUBSCRIPTION_PRICE = "15€ par mois"
SUBSCRIBED_USERS = set()

# Création du bot
app = Application.builder().token(TOKEN).build()

# Fonction d’accueil
async def start(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    SUBSCRIBED_USERS.add(user_id)

    keyboard = [
        [InlineKeyboardButton("📊 Pronostic Gratuit", callback_data="prono")],
        [InlineKeyboardButton("👑 Accès VIP (15€/mois)", callback_data="vip")],
        [InlineKeyboardButton("ℹ️ Infos VIP", callback_data="info_vip")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 Bienvenue sur *CashProno_bot* 🎉\n"
        "Tous les jours, un prono gratuit est envoyé.\n"
        "Rejoins l'abonnement VIP pour plus de pronostics !",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# Gestion des boutons cliqués
async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "prono":
        await query.message.reply_text("🔥 Pronostic gratuit du jour : PSG gagne avec plus de 2.5 buts !")
    elif query.data == "info_vip":
        await query.message.reply_text(
            "👑 *Abonnement VIP* :\n"
            "💰 *Prix* : 15€/mois\n"
            "🎯 *Accès* : Tous les pronostics premium, combinés, et analyses\n"
            "📩 *Pour s'inscrire* : Contacte @Admin",
            parse_mode="Markdown"
        )
    elif query.data == "vip":
        if user_id in VIP_USERS:
            await query.message.reply_text("🔥 Pronostic VIP : Bayern gagne + les deux équipes marquent !")
        else:
            await query.message.reply_text("❌ Accès refusé. Tape /info_vip pour plus d’infos.")

# Planification des messages automatiques
async def daily_task():
    while True:
        now = datetime.now().strftime("%H:%M")
        if now == "10:00":
            await send_daily_prono()
        if now == "18:00":
            await send_vip_prono()
        await asyncio.sleep(60)

# Ajouter les handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

# Lancer le bot en mode Polling + tâches automatiques
async def main():
    asyncio.create_task(daily_task())
    await app.run_polling()

if __name__ == "__main__":
    import asyncio

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())