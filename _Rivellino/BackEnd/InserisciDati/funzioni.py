import os
import pandas as pd
import mysql.connector
from datetime import datetime
from config import DB_CONFIG, STRUCTURE  # Importa la configurazione del DB e la struttura dei sensori

# Funzione per connettersi al database MySQL
def connect_db():
    try:
        return mysql.connector.connect(**DB_CONFIG)  # Usa le credenziali dal config.py
    except mysql.connector.Error as err:
        print(f"[ERRORE DB] {err}")  # In caso di errore nella connessione, stampa il messaggio
        return None

# Funzione per leggere il file CSV relativo ai sensori
def read_file(structure):
    path = structure["filePath"]  # Prende il percorso del file dai dati di configurazione
    if not os.path.exists(path):  # Se il file non esiste, restituisce un DataFrame vuoto
        print(f"[ERRORE] File non trovato: {path}")
        return pd.DataFrame()
    try:
        df = pd.read_csv(path, sep=',', encoding='latin1')  # Legge il file CSV con pandas
        df.columns = structure["fileStructure"]  # Assegna i nomi delle colonne specificati nella struttura
        return df[::-1].reset_index(drop=True)  # Inverte il DataFrame e resetta l'indice
    except Exception as e:
        print(f"[ERRORE LETTURA FILE] {path} - {e}")  # Gestisce eventuali errori durante la lettura del file
        return pd.DataFrame()

# Funzione per generare una query SQL per controllare se un dato esiste già nel database
def sql_check(structure):
    table = structure["tabellaQuery"]
    return f"""
        SELECT 1 FROM {table} WHERE NameSensore = %s AND Data = %s AND Ora = %s
    """

# Funzione per generare una query SQL di inserimento
def sql_insert(structure):
    table = structure["tabellaQuery"]
    columns = structure["dbStructure"]
    placeholders = ", ".join(["%s"] * len(columns))  # Crea i placeholders per i valori
    return f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"

# Funzione per inserire i dati nel database
def insert(sensor_type):
    structure = STRUCTURE[sensor_type]  # Prende la struttura del sensore dal dizionario STRUCTURE
    df = read_file(structure)  # Legge il file dei dati
    if df.empty:  # Se non ci sono dati, termina
        return

    conn = connect_db()  # Crea la connessione al database
    if not conn:  # Se la connessione fallisce, termina
        return
    cursor = conn.cursor()

    try:
        # Itera sulle righe del DataFrame
        for _, row in df.iterrows():
            try:
                timestamp = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S')  # Converte il timestamp in formato datetime
            except ValueError:
                print(f"[ERRORE DATA] Formato non valido in riga: {row}")  # Gestisce errori nel formato della data
                continue

            case = row['modulo']  # Ottiene il modulo del sensore
            case_data = structure.get("sensori", {}).get(case)  # Ottiene i dati del sensore in base al modulo
            if not case_data:
                continue  # Se non ci sono dati per il sensore, passa alla riga successiva

            for sensor_name, value_info in case_data.items():
                cursor.execute(sql_check(structure), (sensor_name, timestamp.date(), timestamp.time()))  # Controlla se i dati esistono già nel DB
                if cursor.fetchone():
                    print(f"Dati già presenti: {sensor_name}")
                    continue  # Se i dati sono già presenti, salta l'inserimento

                query = sql_insert(structure)  # Crea la query di inserimento

                # Inserisce i dati specifici per ogni tipo di sensore
                if sensor_type == "vibrazione":
                    freq = row.get("frequenza")
                    amp = float(row.get("vibrazione"))
                    cursor.execute(query, (timestamp.date(), timestamp.time(), freq, amp, sensor_name))

                elif sensor_type == "ariaCO":
                    co = row.get("CO")
                    cursor.execute(query, (timestamp.date(), timestamp.time(), co, -1, sensor_name))
                elif sensor_type == "ariaNO2":
                    no2 = row.get("NO2")
                    cursor.execute(query, (timestamp.date(), timestamp.time(), -1, no2, sensor_name))
                
                else:
                    value = row.get(value_info)
                    cursor.execute(query, (timestamp.date(), timestamp.time(), value, sensor_name))

                print(f"Inserito {sensor_type}: {sensor_name} {timestamp}")

        conn.commit()  # Esegue il commit delle modifiche al database
    except Exception as e:
        print(f"[ERRORE INSERIMENTO] {sensor_type} - {e}")
    finally:
        cursor.close()  # Chiude il cursore
        conn.close()  # Chiude la connessione al database

# Funzione per aggiornare lo stato della batteria
def update_battery_charger(sensor_type):
    structure = STRUCTURE[sensor_type]  # Ottiene la struttura per il sensore
    df = read_file(structure)  # Legge i dati
    if df.empty:  # Se non ci sono dati, termina
        return

    conn = connect_db()  # Connessione al database
    if not conn:  # Se non riesce a connettersi, termina
        return
    cursor = conn.cursor()

    try:
        # Itera sui sensori e aggiorna il valore della batteria
        for key, sensor_dict in structure["sensori"].items():
            for scatola, colonna in sensor_dict.items():
                row = df[df['modulo'] == key]
                if row.empty:
                    continue

                last_row = row.iloc[0]  # Ottiene l'ultima riga
                valore = last_row.get(colonna)  # Ottiene il valore della batteria
                if valore is None:
                    continue

                query = f"""
                    UPDATE {structure['tabellaQuery']} SET {structure['dbStructure'][1]} = %s
                    WHERE {structure['dbStructure'][0]} = %s
                """
                cursor.execute(query, (int(valore), scatola))  # Esegue l'aggiornamento nel DB
                print(f"Aggiornata batteria {scatola}: {valore}%")

        conn.commit()  # Esegue il commit delle modifiche
    except Exception as e:
        print(f"[ERRORE BATTERIA] - {e}")
    finally:
        cursor.close()  # Chiude il cursore
        conn.close()  # Chiude la connessione al DB
