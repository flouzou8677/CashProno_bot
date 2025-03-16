import time
import schedule
from telegram import Bot

# Ton token API Telegram
TOKEN = 'TON_TOKEN_API'

# L'ID de ton canal (ou ton chat) Telegram
CHAT_ID = '@TON_CANAL_TG'

# Créer un objet bot
bot = Bot(token=TOKEN)

def envoyer_pronostic():
    # Message de pronostics pour aujourd'hui (à personnaliser chaque jour)
    message = """
    📢 **Pronostics du jour** - *Date : 17 mars 2025*

    1️⃣ **PSG vs Lorient**  
    **Pronostic** : ⚡ Victoire PSG (très probable)  
    **Confiance** : 80% ✅

    2️⃣ **Barcelone vs Atlético Madrid**  
    **Pronostic** : ⚽ Les deux équipes marquent (BTTS: Oui)  
    **Confiance** : 75% ✅

    🔥 **Conseil** : Parier sur la victoire de PSG avec plus de 2,5 buts pour plus de sécurité.    

    *Bonne chance et pariez de manière responsable !*
    """
    
    # Envoi du message dans ton canal Telegram
    bot.send_message(chat_id=CHAT_ID, text=message)

# Planifier l'envoi du message tous les jours à 10h00
schedule.every().day.at("10:00").do(envoyer_pronostic)

while True:
    # Maintenir le bot actif et exécuter le planificateur
    schedule.run_pending()
    time.sleep(60)  # Vérifier toutes les minutes