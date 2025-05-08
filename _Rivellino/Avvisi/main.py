# Importazione delle librerie necessarie
import time  # Per mettere in pausa l'esecuzione (sleep), calcolare ritardi, ecc.
from datetime import datetime, timedelta  # Per gestire date e orari

# Importazioni di configurazioni e funzioni personalizzate
from Config import *  # Importa le variabili di configurazione
from Funzioni import *  # Importa funzioni definite esternamente



# Main loop: eseguito solo se il file è lanciato direttamente
if __name__ == "__main__":
    events = [False, False, False]  # Eventi per allagamento, batteria, vibrazione
    message = ["", "", ""]  # Messaggi da inviare per ogni evento
    last = [None, None, None, None]  # Ultimi eventi noti (per evitare duplicazioni)
    resend = [None, None, None]  # Timestamps per il reinvio (se serve)

    # Imposta il tempo iniziale per ciascun tipo, simulando che il controllo sia già passato
    lastHour = {
        "allag": datetime.now() - timedelta(seconds=interval["allag"]),
        "batt": datetime.now() - timedelta(seconds=interval["batt"]),
        "vibr": datetime.now() - timedelta(seconds=interval["vibr"])
    }

    # Loop infinito di monitoraggio
    while True:
        events = [False, False, False]  # Reset degli eventi rilevati ad ogni ciclo
        now = datetime.now()  # Orario corrente

        # Verifica ogni tipo di evento, se è passato l’intervallo previsto
        for tipo in ["allag", "batt", "vibr"]:
            if (now - lastHour[tipo]).total_seconds() >= interval[tipo]:
                verifica(tipo, events, message, last)
                lastHour[tipo] = now

        # Se un evento è già stato notificato, controlla se è il momento di rinviarlo
        for i in range(len(resend)):
            if resend[i] is not None and resend[i] <= now - timedelta(seconds=interval['resend']):
                events[i] = True

        # Invio dei messaggi via Telegram per gli eventi rilevati
        for i in range(len(events)):
            if events[i]:
                response = send_message(TOKEN, CHAT_ID, message[i])
                print(f"Messaggio inviato: {response}")
                resend[i] = now  # Aggiorna timestamp per evitare reinvii troppo frequenti

        time.sleep(1)  # Attesa di un secondo prima del prossimo ciclo
