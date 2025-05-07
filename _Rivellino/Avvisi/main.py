import requests
import time
import mysql.connector
import numpy as np

from Config import *

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

def verifica(type,events,message):
    event = False
    conn = connect_db()  # Crea la connessione al database
    if not conn:  # Se la connessione fallisce, termina
        return
    cursor = conn.cursor()
    
    try:
        if(type == "a"):
            query=  """
                    SELECT *
                    FROM allagamento
                    WHERE NameSensore = 'SensAllagamento'
                    ORDER BY Data DESC, Ora DESC
                    LIMIT 1
                    """
            cursor.execute(query)
            row = cursor.fetchone()
            if row:
                val = False
                date = row[0]
                hour = row[1]
                val = bool(row[2])
                event = val
                if(event):
                    MESSAGE = f"ALLERT! - Registrato allagamento --- data: {date} ora: {hour}"
                    message[0] = MESSAGE
                    events[0] = True
            else:
                print("Nessun dato trovato")
                
        if(type == "b"):
            query = """
                        SELECT *
                        FROM scatola
                        WHERE NomeScatola = 'Scatola Galleria' OR NomeScatola = 'Scatola Polveriera'
                    """

            cursor.execute(query)
            results = cursor.fetchall()
            if results:
                sG=""
                sP=""
                valGalleria = results[0][1]
                valPolveriera = results[1][1]
                if(valGalleria<10):
                    event = True
                    sG = " galleria"
                if(valPolveriera<10):
                    event = True
                    sP = " polveriera"
                if(event):
                    MESSAGE = f"AVVISO! - Batterie case {sG} {sP} da sostituire"
                    message[1] = MESSAGE
                    events[1] = True
            else:
                print("Nessun dato trovato")

    except Exception as e:
        print(f"[ERRORE] - {e}")
    finally:
        cursor.close()  # Chiude il cursore
        conn.close()  # Chiude la connessione al database



if __name__ == "__main__": # Esecuzione
    events = [False,False,False]
    message = ["","",""]
    
    while(True):
        events = [False,False,False]
        message = ["","",""]
        verifica("a",events,message)
        verifica("b",events,message)
    
        if(bool(events[0])):
            response = send_message(TOKEN, CHAT_ID, message[0])
            print(f"Messaggio inviato: {response}")
        
        if(bool(events[1])):
            response = send_message(TOKEN, CHAT_ID, message[1])
            print(f"Messaggio inviato: {response}")
        
        time.sleep(10)
