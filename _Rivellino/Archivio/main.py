import mysql.connector
from datetime import datetime, timedelta
import time

from config import *
from funzioni import *


def main(test_mode):
    already_executed = False   # Flag per evitare che l'elaborazione venga eseguita più volte nello stesso intervallo

    while True:
        # Se test_mode è attivo, simula la data come il primo giorno del mese a mezzanotte
        if test_mode:
            now = datetime(2026, 6, 1, 0, 0)
        else:
            # Altrimenti prendi la data e ora attuali reali
            now = datetime.now()

        # Se è il primo giorno del mese alla mezzanotte e non abbiamo ancora eseguito il processo
        if now.day == 1 and not already_executed:
            print(f"[{now}] Inizio elaborazione...")

            # Recupera l'intervallo di date da elaborare e informazioni di mese e anno
            start, end, month, year = get_date_range(now)

            try:
                # Connessione al database usando i parametri di configurazione
                conn = mysql.connector.connect(**DB_CONFIG)
                cursor = conn.cursor()

                # Per ogni tabella/configurazione definita in STRUCTURE, processa i dati per l'intervallo specificato
                for name, conf in STRUCTURE.items():
                    process_table(cursor, conf, start, end, month, year)
                    conn.commit()  # Salva le modifiche sul database

                cursor.close()  # Chiude il cursore
                conn.close()    # Chiude la connessione
                print("✅ Completato.")

            except Exception as e:
                # In caso di errore, stampa un messaggio
                print("❌ Errore:", e)

            already_executed = True  # Imposta il flag per non rieseguire l'elaborazione nello stesso intervallo

        # Se non è il primo giorno del mese, resetta il flag per poter rieseguire il prossimo mese
        if now.day != 1:
            already_executed = False

        # Se siamo in modalità test, esci subito dal ciclo dopo una singola iterazione
        if test_mode:
            break

        # Attendi 60 secondi prima di ricontrollare la data e ora
        time.sleep(3600)

#Main
if __name__ == "__main__":
    #!!!
    #Attenzione alla modalita test
    #Settare nel metodo process_table, le condizioni per cui i dati vengano scaricati nel file 
    #!!!
    main(test_mode = True)
