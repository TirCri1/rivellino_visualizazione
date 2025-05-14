import time
from datetime import datetime, timedelta
from Config import *
from Funzioni import *

if __name__ == "__main__":
    events = [False, False, False]
    message = ["", "", ""]
    last = [None, None, None, None]
    resend = [None, None, None]

    lastHour = {
        "allag": datetime.now() - timedelta(seconds=interval["allag"]),
        "batt": datetime.now() - timedelta(seconds=interval["batt"]),
        "vibr": datetime.now() - timedelta(seconds=interval["vibr"])
    }

    try:
        print("💬 Chat avviato. Premi Ctrl+C per terminare.")
        while True:
            events = [False, False, False]
            now = datetime.now()

            for tipo in ["allag", "batt", "vibr"]:
                if (now - lastHour[tipo]).total_seconds() >= interval[tipo]:
                    verifica(tipo, events, message, last)
                    lastHour[tipo] = now

            for i in range(len(resend)):
                if resend[i] is not None and resend[i] <= now - timedelta(seconds=interval['resend']):
                    events[i] = True

            for i in range(len(events)):
                if events[i]:
                    response = send_message(TOKEN, CHAT_ID, message[i])
                    print(f"Messaggio inviato: {response}")
                    resend[i] = now

            time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Interruzione ricevuta. Chiusura chat...")
