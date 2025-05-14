# Importazione delle librerie necessarie
import requests  # Per inviare richieste HTTP (ad esempio, verso le API di Telegram)
import mysql.connector  # Per connettersi a un database MySQL
import json
import os

from Config import *  # Importa le variabili di configurazione


# Funzione per connettersi al database MySQL
def connect_db():
    try:
        return mysql.connector.connect(**DB_CONFIG)  # Usa il dizionario DB_CONFIG per stabilire la connessione
    except mysql.connector.Error as err:
        print(f"[ERRORE DB] {err}")  # Stampa un messaggio d’errore se la connessione fallisce
        return None  # Ritorna None in caso di errore

# Funzione per inviare un messaggio via Telegram
def send_message(token, chat_id, text):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    response = requests.post(url, data=payload)
    res_json = response.json()

    # Salva l'ID del messaggio se l'invio ha avuto successo
    if 'result' in res_json:
        message_id = res_json['result']['message_id']
        save_message_id(message_id)
        return res_json
    else:
        print("Errore nell'invio del messaggio:", res_json)
        return res_json
    
# Funzione per salvare l'ID dei messaggi inviati nella chat
def save_message_id(message_id):
    filename = 'sent_messages.json'
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
    else:
        data = []

    if message_id not in data:
        data.append(message_id)
        with open(filename, 'w') as file:
            json.dump(data, file)


# Funzione per verificare eventi: allagamento, batteria scarica, vibrazione
def verifica(type, events, message, last):
    event = False  # Flag per determinare se c'è un evento nuovo

    conn = connect_db()  # Tenta la connessione al DB
    if not conn:
        return  # Esce se la connessione fallisce
    cursor = conn.cursor()

    try:
        # Verifica Allagamento
        if(type == "allag"):
            query = """
                    SELECT *
                    FROM allagamento
                    WHERE NameSensore = 'SensAllagamento'
                    ORDER BY Data DESC, Ora DESC
                    LIMIT 1
                    """
            cursor.execute(query)
            row = cursor.fetchone()  # Ottiene l'ultima riga (evento più recente)
            if row:
                date = row[0]
                hour = row[1]
                val = bool(row[2])  # Valore booleano che indica se c'è allagamento
                timestamp_event = f"{date} {hour}"

                if timestamp_event != last[0]:  # Verifica se l’evento è già stato gestito
                    event = val  # Se vero, si tratta di un nuovo evento di allagamento
                    last[0] = timestamp_event  # Salva il timestamp per evitare duplicazioni
                if event:
                    MESSAGE =   (
                                f"🚨💧 <b>ALLERTA ALLAGAMENTO</b>\n"
                                f"📅 Data: <i>{date}</i>\n"
                                f"🕒 Ora: <i>{hour}</i>"
                                )
                    message[0] = MESSAGE
                    events[0] = True  # Segna l’evento come rilevato
            else:
                print("Nessun dato trovato")

        # Verifica Batterie
        if(type == "batt"):
            query = """
                    SELECT *
                    FROM scatola
                    WHERE NomeScatola = 'Scatola Galleria' OR NomeScatola = 'Scatola Polveriera'
                    """
            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                sG = ""  # Segnaposto per indicare se la galleria è coinvolta
                sP = ""  # Segnaposto per la polveriera
                valGalleria = results[0][1]
                valPolveriera = results[1][1]

                if(valGalleria < 10):
                    if(valGalleria != last[1]):
                        event = True
                        sG = " galleria"
                        last[1] = valGalleria
                else:
                    last[1] = None

                if(valPolveriera < 10):
                    if(valPolveriera != last[2]):
                        event = True
                        sP = " polveriera"
                        last[2] = valPolveriera
                else:
                    last[2] = None

                if(event):
                    MESSAGE =   (
                                f"🚨🪫 <b>BATTERIA SCARICA</b>\n"
                                f"🧰 Case interessate:{sG}{sP}\n"
                                f"⚠️ È necessaria la sostituzione"
                                )
                    message[1] = MESSAGE
                    events[1] = True
            else:
                print("Nessun dato trovato")

        # Verifica Vibrazione
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
                timestamp_event = f"{date} {hour}"

                if timestamp_event != last[3]:  # Se è un nuovo evento
                    event = True
                    last[3] = timestamp_event
                if event:
                    MESSAGE =   (
                                f"🚨📡 <b>ALLERTA VIBRAZIONE RILEVATA</b>\n"
                                f"📅 Data: <i>{date}</i>\n"
                                f"🕒 Ora: <i>{hour}</i>"
                                )
                    message[2] = MESSAGE
                    events[2] = True
            else:
                print("Nessun dato trovato")

    except Exception as e:
        print(f"[ERRORE] - {e}")  # Gestione generica degli errori
    finally:
        cursor.close()  # Chiude il cursore dopo l’uso
        conn.close()  # Chiude la connessione al DB
        