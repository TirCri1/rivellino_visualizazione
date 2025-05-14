import signal
import sys
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from Config import *  # contiene TOKEN, ecc.
from Funzioni import *  # contiene funzioni come start e gestisci_messaggi

def stop_bot(signum, frame):
    print("\n🛑 Interruzione ricevuta. Il bot si sta chiudendo...")
    sys.exit(0)

if __name__ == "__main__":
    # Registra il gestore del segnale
    signal.signal(signal.SIGINT, stop_bot)

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, gestisci_messaggi))

    print("\n🤖 Bot avviato. Premi Ctrl+C per terminare.")
    app.run_polling()
