import time
import pandas as pd
import mysql.connector
from datetime import datetime
import threading

stop_event = threading.Event()
threads = []

from config import *

def sqlCeck(sensor_type):
    table = STRUCTURE[sensor_type]["query"]
    return f"""
        SELECT 1
        FROM {table}
        WHERE NameSensore = %s AND Data = %s AND Ora = %s
        ORDER BY Data, Ora
    """

def sqlInsert(sensor_type):
    table = STRUCTURE[sensor_type]["query"]
    columns = STRUCTURE[sensor_type]["dbStructure"]
    placeholders = ", ".join(["%s"] * len(columns))
    return f"""
        INSERT INTO {table} ({', '.join(columns)})
        VALUES ({placeholders})
    """

def connect_db():
    return mysql.connector.connect(**DB_CONFIG)

def insert(sensor_type):
    structure = STRUCTURE[sensor_type]
    path = structure["path"]
    df = pd.read_csv(path, sep=',', encoding='latin1')
    df.columns = structure["fileColoumn"]
    df = df[::-1].reset_index(drop=True)

    conn = connect_db()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        timestamp = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S')
        case = row['modulo']
        try:
            sensor_info = structure[case]
        except KeyError:
            print(f"Modulo non riconosciuto: {case}")
            continue

        name_sensor = sensor_info[0]
        name_sensor_clean = name_sensor.strip().lower()

        cursor.execute(sqlCeck(sensor_type), (name_sensor, timestamp.date(), timestamp.time()))
        if cursor.fetchone():
            print(f"I dati sono aggiornati - {sensor_type}")
            break

        sql_insert = sqlInsert(sensor_type)

        if sensor_type == "vibrazione":
            frequenza = str(row[sensor_info[4]])
            ampiezza = str(row[sensor_info[3]])
            cursor.execute(sql_insert, (timestamp.date(), timestamp.time(), frequenza, ampiezza, name_sensor))
            print(f"Dato inserito (vibrazione): {timestamp.date()} {timestamp.time()} :{frequenza} - {ampiezza}: {name_sensor}")
        elif sensor_type == "aria":
            a_name = structure.get("a", [""])[0].strip().lower()
            b_name = structure.get("b", [""])[0].strip().lower()
            value = str(row[sensor_info[2]])
            if name_sensor_clean == a_name:
                cursor.execute(sql_insert, (timestamp.date(), timestamp.time(), value, -1, name_sensor))
            elif name_sensor_clean == b_name:
                cursor.execute(sql_insert, (timestamp.date(), timestamp.time(), -1, value, name_sensor))
            else:
                print(f"Nome sensore aria non riconosciuto: {name_sensor}")
                continue
            print(f"Dato inserito (aria): {timestamp.date()} {timestamp.time()} :{value}: {name_sensor}")
        else:
            value = str(row[sensor_info[2]])
            cursor.execute(sql_insert, (timestamp.date(), timestamp.time(), value, name_sensor))
            print(f"Dato inserito ({sensor_type}): {timestamp.date()} {timestamp.time()} :{value}: {name_sensor}")

    conn.commit()
    cursor.close()
    conn.close()



def start_thread(sensor_type, interval):
    def loop():
        while not stop_event.is_set():
            insert(sensor_type)

            if stop_event.wait(interval):
                break
    thread = threading.Thread(target=loop)
    thread.start()
    threads.append(thread)

if __name__ == "__main__":
    frequenzaAggiornamento_TEMP = 600
    frequenzaAggiornamento_UMID = 600
    frequenzaAggiornamento_ARIA = 600
    frequenzaAggiornamento_Vibr = 0.5
    frequenzaAggiornamento_Allag = 60

    start_thread("temp", 10)
    start_thread("umid", 10)
    start_thread("aria", 10)
    start_thread("vibrazione", 1)
    start_thread("allagamento", 5)

    try:
        while True:
            time.sleep(1)  # loop leggero, lascia tempo al main thread per ricevere KeyboardInterrupt
    except KeyboardInterrupt:
        print("\nInterruzione rilevata. Chiusura dei thread...")
        stop_event.set()
        for t in threads:
            t.join()
        print("Terminato correttamente.")

