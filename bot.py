import logging
import asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, CallbackContext

# Configuration du logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# Token du bot
TOKEN = "8181308468:AAFmC567gtnZucX5VXo1S9mRSYyzmbK25CU"

# Liste des abonnés
VIP_USERS = set()
SUBSCRIBED_USERS = set()

# Création de l'application Telegram
app = Application.builder().token(TOKEN).build()

# Gestion des tâches asynchrones
tasks = set()

# Fonction d'accueil avec boutons
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
        "📅 Chaque jour, un prono gratuit est envoyé.\n"
        "💎 Accède à l’abonnement VIP pour des pronos premium !",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# Gestion des boutons interactifs
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
            "🎯 *Avantages* : Tous les pronostics premium, combinés, et analyses\n"
            "📩 *Pour s'inscrire* : Contacte @Admin",
            parse_mode="Markdown"
        )
    elif query.data == "vip":
        if user_id in VIP_USERS:
            await query.message.reply_text("🔥 Pronostic VIP : Bayern gagne + les deux équipes marquent !")
        else:
            await query.message.reply_text("❌ Accès refusé. Tape /info_vip pour plus d’infos.")

# Envoi automatique du prono gratuit chaque jour
async def send_daily_prono():
    for user_id in SUBSCRIBED_USERS:
        try:
            await app.bot.send_message(user_id, "🔥 Pronostic du jour : Real Madrid gagne + plus de 1.5 buts !")
        except Exception as e:
            logging.error(f"Erreur d'envoi du prono : {e}")

# Envoi automatique du prono VIP
async def send_vip_prono():
    for user_id in VIP_USERS:
        try:
            await app.bot.send_message(user_id, "🔥 Pronostic VIP : Chelsea gagne + les deux équipes marquent !")
        except Exception as e:
            logging.error(f"Erreur d'envoi du prono VIP : {e}")

# Tâche planifiée pour envoyer les pronos chaque jour
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

# Gestion des tâches pour éviter les erreurs
async def main():
    task = asyncio.create_task(daily_task())  # Création de la tâche d'envoi auto
    tasks.add(task)
    try:
        await app.run_polling()
    finally:
        task.cancel()  # Annulation propre de la tâche
        try:
            await task
        except asyncio.CancelledError:
            logging.info("Tâche daily_task annulée proprement.")

# Correction de l'erreur "Task was destroyed but it is pending!"
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())