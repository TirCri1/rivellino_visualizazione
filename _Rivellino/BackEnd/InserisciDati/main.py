import time
import threading

from funzioni import insert, update_battery_charger  # Importa le funzioni insert e update_battery_charger dal file 'funzioni.py'

stop_event = threading.Event()  # Evento per fermare i thread
threads = []  # Lista per mantenere traccia dei thread

# Funzione per avviare un nuovo thread per ciascun tipo di sensore
def start_thread(sensor_type, interval):
    def loop():
        while not stop_event.is_set():  # Il thread continua a eseguire finché stop_event non è stato impostato
            if sensor_type == "alimentazione":
                update_battery_charger(sensor_type)  # Aggiorna lo stato della batteria se il sensore è "alimentazione"
            else:
                insert(sensor_type)  # Altrimenti, inserisce i dati del sensore nel database
            if stop_event.wait(interval):  # Aspetta per l'intervallo specificato, e poi interrompe se stop_event è impostato
                break

    # Crea e avvia un nuovo thread per eseguire la funzione loop()
    thread = threading.Thread(target=loop, name=f"Thread-{sensor_type}")
    thread.start()
    threads.append(thread)  # Aggiungi il thread alla lista

if __name__ == "__main__":  # Il codice all'interno di questo blocco viene eseguito solo se il file è eseguito come script principale
    intervals = {  # Dizionario con i tipi di sensori e il relativo intervallo di tempo
        "temp": 10,
        "umid": 10,
        "aria": 10,
        "vibrazione": 1,
        "allagamento": 5,
        "alimentazione": 15
    }

    # Avvia un thread per ogni tipo di sensore con l'intervallo specificato
    for sensor_type, interval in intervals.items():
        start_thread(sensor_type, interval)

    try:
        while True:
            time.sleep(1)  # Il ciclo principale rimane in attesa fino a un'interruzione da tastiera
    except KeyboardInterrupt:
        print("\nInterruzione rilevata. Chiusura dei thread...")
        stop_event.set()  # Imposta l'evento di stop per fermare i thread
        for t in threads:
            t.join()  # Attende che tutti i thread terminino
        print("Terminato correttamente.")   # Stampa un messaggio di terminazione
