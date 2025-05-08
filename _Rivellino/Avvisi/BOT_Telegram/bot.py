from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import asyncio

# ====== CONFIG ======
TOKEN = "7903372067:AAEhRKtv0YzKnc5o2BRaElduv5lNxw3HuzY"
USERNAME_CORRETTO = "Rivellino"
PASSWORD_CORRETTA = "Allert"
LINK_CANALI_PRIVATO = "https://t.me/+u0I2o9VZ9JA4MzM0"
CLEANUP_DELAY_SECONDS = 60  # ⏱ Tempo in secondi prima della cancellazione della chat

# ====== VARIABILI STATO ======
stato_utenti = {}    # chat_id: "attesa_username" / "attesa_password"
dati_utente = {}     # chat_id: {"username": ..., "password": ...}
messaggi_utente = {} # chat_id: [message_ids]

# ====== /start ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    stato_utenti[chat_id] = "attesa_username"
    dati_utente[chat_id] = {}
    messaggi_utente[chat_id] = []

    bot_msg = await update.message.reply_text("Benvenuto! Inserisci il tuo username:")
    messaggi_utente[chat_id].append(update.message.message_id)
    messaggi_utente[chat_id].append(bot_msg.message_id)

# ====== Gestione messaggi ======
async def gestisci_messaggi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.effective_user
    testo = update.message.text

    # Memorizza il messaggio utente
    messaggi_utente.setdefault(chat_id, []).append(update.message.message_id)

    if chat_id not in stato_utenti:
        msg = await update.message.reply_text("Per iniziare, usa /start")
        messaggi_utente[chat_id].append(msg.message_id)
        return

    stato = stato_utenti[chat_id]

    if stato == "attesa_username":
        dati_utente[chat_id]["username"] = testo
        stato_utenti[chat_id] = "attesa_password"
        msg = await update.message.reply_text("Ora inserisci la password:")
        messaggi_utente[chat_id].append(msg.message_id)

    elif stato == "attesa_password":
        dati_utente[chat_id]["password"] = testo
        username = dati_utente[chat_id]["username"]
        password = dati_utente[chat_id]["password"]

        if username == USERNAME_CORRETTO and password == PASSWORD_CORRETTA:
            msg = await update.message.reply_text(
                f"✅ Accesso consentito! Ecco il link: {LINK_CANALI_PRIVATO}"
            )
            messaggi_utente[chat_id].append(msg.message_id)

            # Log su terminale
            telegram_username = user.username or "N/A"
            full_name = user.full_name or "N/A"
            print(f"[✅ LOGIN EFFETUATO CON SUCESSO]   Dati utente: @{telegram_username} - {full_name} ")

            # Avvia il timer di pulizia
            asyncio.create_task(pulisci_chat_dopo_delay(context, chat_id))
        else:
            msg = await update.message.reply_text("❌ Username o password errati. Riprova con /start")
            messaggi_utente[chat_id].append(msg.message_id)

        # Pulisce lo stato
        stato_utenti.pop(chat_id, None)
        dati_utente.pop(chat_id, None)

# ====== Pulizia chat ======
async def pulisci_chat_dopo_delay(context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    await asyncio.sleep(CLEANUP_DELAY_SECONDS)
    if chat_id in messaggi_utente:
        for msg_id in messaggi_utente[chat_id]:
            try:
                await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
            except:
                pass
        messaggi_utente.pop(chat_id, None)

# ====== Avvio bot ======
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, gestisci_messaggi))

    print("🤖 Bot avviato.")
    app.run_polling()
