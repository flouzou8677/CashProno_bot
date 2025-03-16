from flask import Flask
from telegram import Bot
import schedule
import time

# Ton token API Telegram
TOKEN = 'TON_TOKEN_API'

# L'ID de ton canal Telegram
CHAT_ID = '@TON_CANAL_TG'

# Créer un objet bot
bot = Bot(token=TOKEN)

# Créer une application Flask
app = Flask(__name__)

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

# Route simple pour tester que l'application est en ligne
@app.route('/')
def home():
    return "Bot Telegram en fonctionnement."

# Planifier l'envoi du message tous les jours à 10h00
schedule.every().day.at("10:00").do(envoyer_pronostic)

# Fonction pour maintenir le bot actif en arrière-plan
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)  # Vérifie toutes les minutes

if __name__ == '__main__':
    from threading import Thread
    # Lancer le planificateur dans un thread séparé pour qu'il fonctionne en continu
    Thread(target=run_scheduler).start()
    # Lancer le serveur Flask
    app.run(host="0.0.0.0", port=5000)  # Choisir un port, par exemple 5000
    
# Envoi d'un message de test immédiatement
bot.send_message(chat_id=CHAT_ID, text="Le bot est en ligne et fonctionne !") 