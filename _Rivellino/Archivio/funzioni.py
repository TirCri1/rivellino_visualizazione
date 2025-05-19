from datetime import datetime, timedelta
import os
import pandas as pd

from config import *


def get_date_range(now):
    year = now.year - 1     # L'anno di interesse è l'anno precedente a quello corrente
    month = now.month - 1   # Il mese di interesse è il mese precedente a quello corrente
    if month == 0:          # Se il mese è 0 (cioè gennaio - 1), vai a dicembre dell'anno precedente
        month = 12
        year -= 1

    # Calcola la data di inizio: primo giorno del mese/anno calcolati
    start = datetime(year, month, 1)

    # Calcola la data di fine: primo giorno del mese successivo (o 1 gennaio anno successivo se dicembre)
    end = datetime(year + 1, 1, 1) if month == 12 else datetime(year, month + 1, 1)

    return start, end, month, year

def process_table(cursor, config, start_date, end_date, month, year):
    # Estrae dal dizionario di configurazione i dettagli della tabella e colonne
    table = config["tabellaQuery"]        # Nome della tabella da interrogare
    file_cols = config["fileStructure"]   # Colonne da selezionare dal DB
    sensori = config["sensori"]            # Sensori associati alla tabella
    output_cols = config["dbStructure"]   # Struttura/colonne per il file di output

    # Query SQL per selezionare i dati nell'intervallo temporale definito
    query = f"""
        SELECT {', '.join(file_cols)} FROM {table}
        WHERE CONCAT(Data, ' ', Ora) >= %s AND CONCAT(Data, ' ', Ora) < %s
        """

    cursor.execute(query, (start_date, end_date))
    rows = cursor.fetchall()

    if not rows:
        print(f"[{table}] Nessun dato.")  # Messaggio se non ci sono dati per il range
        return

    # Crea un DataFrame pandas con i dati estratti
    df = pd.DataFrame(rows, columns=file_cols)

    # Converte le colonne "Data" e "Ora" in datetime per facilitare l'elaborazione
    df["Data"] = pd.to_datetime(df["Data"])
    df["Ora"] = df["Ora"].apply(lambda x: (datetime.min + x).time() if isinstance(x, timedelta) else x)

    records = []  # Lista per memorizzare i dati elaborati per l'output

    # Cicla su ogni riga del DataFrame e per ogni sensore crea un record differente
    for _, row in df.iterrows():
        for sensore in sensori:
            # Per ogni tabella, costruisce una lista di valori diversa a seconda dei dati disponibili
            if table == "temperatura":
                if(row["Valore"] <= 1 or row["Valore"] >= 25):
                    records.append([row["Data"].day, row["Ora"], row["Valore"], sensore])
            elif table == "umidita":
                if(row["Valore"] <= 40 or row["Valore"] >= 75):
                    records.append([row["Data"].day, row["Ora"], row["Valore"], sensore])
            elif table == "qualita":
                if(row["ValoreCo"] >= 50 or row["ValoreNo2"] >= 30):
                    records.append([row["Data"].day, row["Ora"], row["ValoreCo"], row["ValoreNo2"], sensore])
            elif table == "vibrazione":
                    records.append([row["Data"].day, row["Ora"], row["ValoreFrequenza"], row["ValoreAmpiezza"], sensore])
            elif table == "allagamento":
                    records.append([row["Data"].day, row["Ora"], row["Valore"], sensore])

    # Crea un DataFrame con i dati pronti per essere salvati
    output_df = pd.DataFrame(records, columns=output_cols)

    # Crea la cartella per l'anno se non esiste, ad esempio "PATH/dati_2024"
    year_folder = os.path.join(PATH, f"dati_{year}")
    os.makedirs(year_folder, exist_ok=True)

    # Costruisce il nome del file CSV con mese e nome base da config
    filename = os.path.join(year_folder, f"{config['file'].split('.')[0]}_{str(month).zfill(2)}.csv")

    # Salva il DataFrame in formato CSV senza l'indice
    output_df.to_csv(filename, index=False)
    print(f"[{table}] Salvato: {filename}")

    # Dopo aver salvato i dati, elimina quelli già processati dal database
    delete_query = f"""
    DELETE FROM {table}
    WHERE CONCAT(Data, ' ', Ora) >= %s AND CONCAT(Data, ' ', Ora) < %s
    """
    cursor.execute(delete_query, (start_date, end_date))
