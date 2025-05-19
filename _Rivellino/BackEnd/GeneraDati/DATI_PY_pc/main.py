from Funzioni import *

# Esegui il programma
if __name__ == "__main__":
    print("\n--- Avvio app ---\n")
    timesleep = 10
    try:
        aggiorna_dati_continuamente(timesleep)
    except KeyboardInterrupt:
        print("\n --- Interruzione manuale rilevata. Uscita dal programma ---\n")
