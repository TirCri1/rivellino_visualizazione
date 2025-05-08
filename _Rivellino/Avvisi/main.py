import requests
import time
from datetime import datetime, timedelta
import mysql.connector
import numpy as np

from Config import *
from Funzioni import *

# Funzione per connettersi al database MySQL
def connect_db():
    try:
        return mysql.connector.connect(**DB_CONFIG)  # Usa le credenziali dal config.py
    except mysql.connector.Error as err:
        print(f"[ERRORE DB] {err}")  # In caso di errore nella connessione, stampa il messaggio
        return None

def send_message(token, chat_id, text):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, data=payload)
    return response.json()

def verifica(type, events, message, last):
    timestamp = time.time()
    datatime = time.localtime(timestamp)

    event = False
    
    conn = connect_db()  # Crea la connessione al database
    if not conn:  # Se la connessione fallisce, termina
        return
    cursor = conn.cursor()
    
    try:
        if(type == "allag"):
            query = """
                    SELECT *
                    FROM allagamento
                    WHERE NameSensore = 'SensAllagamento'
                    ORDER BY Data DESC, Ora DESC
                    LIMIT 1
                    """
            cursor.execute(query)
            row = cursor.fetchone()
            if row:
                date = row[0]
                hour = row[1]
                val = bool(row[2])
                timestamp_event = f"{date} {hour}"  # Creiamo il timestamp completo data+ora

                if timestamp_event != last[0]:
                    event = val
                    last[0] = timestamp_event  # Aggiorniamo last[0] con il nuovo timestamp
                if event:
                    MESSAGE = f"ALLERT! - Registrato allagamento --- data: {date} ora: {hour}"
                    message[0] = MESSAGE
                    events[0] = True
                    resend[0] = datatime
            else:
                print("Nessun dato trovato")

        if(type == "batt"):
            query = """
                    SELECT *
                    FROM scatola
                    WHERE NomeScatola = 'Scatola Galleria' OR NomeScatola = 'Scatola Polveriera'
                    """
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                sG = ""
                sP = ""
                valGalleria = results[0][1]
                valPolveriera = results[1][1]
                
                if(valGalleria < 10 and valGalleria != last[1]):
                    event = True
                    sG = " galleria"
                    last[1] = valGalleria
                if(valPolveriera < 10 and valPolveriera != last[2]):
                    event = True
                    sP = " polveriera"
                    last[2] = valPolveriera
                if(event):
                    MESSAGE = f"AVVISO! - Batterie case {sG} {sP} da sostituire"
                    message[1] = MESSAGE
                    events[1] = True
                    resend[1] = datatime
            else:
                print("Nessun dato trovato")

        if(type == "vibr"):
            query = """
                    SELECT Data, Ora
                    FROM vibrazione
                    WHERE NameSensore = 'SensVibrazione'
                    ORDER BY Data DESC, Ora DESC
                    LIMIT 1
                    """
            cursor.execute(query)
            row = cursor.fetchone()
            if row:
                date = row[0]
                hour = row[1]
                timestamp_event = f"{date} {hour}"  # Creiamo il timestamp completo data+ora

                if timestamp_event != last[3]:
                    event = True
                    last[3] = timestamp_event  # Aggiorniamo last[4] con il nuovo timestamp
                if event:
                    MESSAGE = f"ALLERT! - Registrata vibrazione --- data: {date} ora: {hour}"
                    message[2] = MESSAGE
                    events[2] = True
                    resend[1] = datatime
            else:
                print("Nessun dato trovato")

    except Exception as e:
        print(f"[ERRORE] - {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":  # Esecuzione
    events = [False, False, False]
    message = ["", "", ""]
    last = [None, None, None, None]
    resend = [None,None,None]
    
    lastHour = {
    "allag": datetime.now() - timedelta(seconds=interval["allag"]),
    "batt": datetime.now() - timedelta(seconds=interval["batt"]),
    "vibr": datetime.now() - timedelta(seconds=interval["vibr"])
    }

    while True:
        events = [False, False, False]
        message = ["", "", ""]
        now = datetime.now()

        for tipo in ["allag", "batt", "vibr"]:
            if (now - lastHour[tipo]).total_seconds() >= interval[tipo]:
                verifica(tipo, events, message, last)
                lastHour[tipo] = now

        # Invia i messaggi se ci sono eventi
        for i in range(len(events)):
            if events[i]:
                response = send_message(TOKEN, CHAT_ID, message[i])
                print(f"Messaggio inviato: {response}")

        time.sleep(1)
