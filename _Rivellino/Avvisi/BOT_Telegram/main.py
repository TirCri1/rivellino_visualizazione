from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import asyncio
import requests
import json

from Config import *  # USERNAME_CORRETTO, PASSWORD_CORRETTA, TOKEN, CHAT_ID, MESSAGES_FILE, CLEANUP_DELAY_SECONDS, etc.

# ====== VARIABILI STATO ======
stato_utenti = {}
dati_utente = {}
messaggi_utente = {}

# ====== FUNZIONI DI UTILITÀ ======
async def invia_e_memorizza(update, chat_id, testo, reply_markup=None):
    msg = await update.message.reply_text(testo, reply_markup=reply_markup)
    messaggi_utente.setdefault(chat_id, []).append(msg.message_id)
    return msg

async def pulisci_chat_dopo_delay(context: ContextTypes.DEFAULT_TYPE, chat_id: int, time):
    print(f"[🕒] Inizio sleep per {time} secondi per la chat {chat_id}")
    await asyncio.sleep(time)
    for msg_id in messaggi_utente.get(chat_id, []):
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except Exception as e:
            print(f"[⚠️] Errore cancellazione messaggio {msg_id}: {e}")
    messaggi_utente.pop(chat_id, None)

async def elimina_messaggi_canale(update, chat_id):
    try:
        with open(MESSAGES_FILE, 'r') as f:
            message_ids = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("[⚠️] File messaggi non trovato o vuoto.")
        return

    await invia_e_memorizza(update, chat_id, "Messaggi delle ultime 48 ore eliminati con successo")
    
    for msg_id in message_ids:
        response = requests.post(
            f'https://api.telegram.org/bot{TOKEN}/deleteMessage',
            data={'chat_id': CHAT_ID, 'message_id': msg_id}
        )
        if response.ok and response.json().get("ok"):
            print(f"[✓] Messaggio {msg_id} eliminato.")
        else:
            print(f"[X] Errore eliminazione {msg_id}: {response.text}")
        await asyncio.sleep(1)

    open(MESSAGES_FILE, 'w').write('[]')
    print("[✅] Tutti i messaggi gestiti ed eliminati.")

# ====== /start ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    stato_utenti[chat_id] = "attesa_username"
    dati_utente[chat_id] = {}
    messaggi_utente[chat_id] = [update.message.message_id]
    
    await invia_e_memorizza(update, chat_id, "Benvenuto!")
    await invia_e_memorizza(update, chat_id, "Inserisci il tuo username:")

# ====== Gestione messaggi ======
async def gestisci_messaggi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.effective_user
    testo = update.message.text
    messaggi_utente.setdefault(chat_id, []).append(update.message.message_id)

    stato = stato_utenti.get(chat_id)
    if not stato:
        await invia_e_memorizza(update, chat_id, "Per iniziare, usa /start")
        return

    # ====== Inserimento Username ======
    if stato == "attesa_username":
        dati_utente[chat_id]["username"] = testo
        stato_utenti[chat_id] = "attesa_password"
        await invia_e_memorizza(update, chat_id, "Ora inserisci la password:")
        return

    # ====== Inserimento Password ======
    elif stato == "attesa_password":
        dati_utente[chat_id]["password"] = testo
        username = dati_utente[chat_id]["username"]
        password = dati_utente[chat_id]["password"]

        if username == USERNAME_CORRETTO and password == PASSWORD_CORRETTA:
            await invia_e_memorizza(update, chat_id, f"✅ Accesso consentito! Ecco il link: {LINK_CANALI_PRIVATO}")
            print(f"[✅ LOGIN UTENTE] @{user.username or 'N/A'} - {user.full_name or 'N/A'}")
            asyncio.create_task(pulisci_chat_dopo_delay(context, chat_id, time = CLEANUP_DELAY_SECONDS_CHAT))

        elif username == USERNAME_ADMIN and password == PASSWORD_ADMIN:
            keyboard = [["🧹 Elimina messaggi canale"], ["❌ Esci"]]
            await invia_e_memorizza(update, chat_id, "✅ Accesso ADMIN. Scegli un'operazione:",
                                    reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
            stato_utenti[chat_id] = "menu_admin"
            print(f"[🔐 LOGIN ADMIN] {user.username}")
            return

        else:
            await invia_e_memorizza(update, chat_id, "❌ Username o password errati. Riprova con /start")

        stato_utenti.pop(chat_id, None)
        dati_utente.pop(chat_id, None)

    # ====== Menu Admin ======
    elif stato == "menu_admin":
        if testo == "🧹 Elimina messaggi canale":
            await invia_e_memorizza(update, chat_id, "🔄 Pulizia in corso...")
            await elimina_messaggi_canale(update, chat_id)

        elif testo == "❌ Esci":
            await invia_e_memorizza(update, chat_id, "🔒 Uscita dalla modalità admin. Tutti i messaggi saranno eliminati.")
            stato_utenti.pop(chat_id, None)
            dati_utente.pop(chat_id, None)
            asyncio.create_task(pulisci_chat_dopo_delay(context, chat_id, time = CLEANUP_DELAY_SECONDS_EXIT))
            return

        else:
            await invia_e_memorizza(update, chat_id, "❓ Comando non riconosciuto. Usa uno dei pulsanti disponibili.")

# ====== MAIN BOT ======
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, gestisci_messaggi))

    print("🤖 Bot avviato.")
    app.run_polling()
