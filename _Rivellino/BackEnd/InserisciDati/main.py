import time
import pandas as pd
import mysql.connector
from datetime import datetime

DB_CONFIG = {
    "host": "10.10.60.186",
    "user": "remoteUser",
    "password": "!rivellino!RIVELLINO!",
    "database": "rivellino"
}

def connect_db():
    return mysql.connector.connect(**DB_CONFIG)

def insertTemperatura():
    path = "../RiceviDati/DatiSensori/temperatura_umidita.csv"
    df = pd.read_csv(path, sep=',', encoding='latin1') 
    df.columns = ['timestamp', 'modulo', 'temperatura', 'umidita']
    df = df[::-1].reset_index(drop=True)
    
    conn = connect_db()
    cursor = conn.cursor()
    
    for _, row in df.iterrows():
        timestamp = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S')
        modulo = row['modulo']
        temperatura = str(row['temperatura'])
            
        if(modulo == "a"):
            NameSensore = "SensTemp1"
        if(modulo == "b"):
            NameSensore = "SensTemp2"
        if(modulo == "c"):
            NameSensore = "SensTemp3"
               
        SQL =   """ SELECT 1 
                    FROM temperatura 
                    WHERE NameSensore = %s AND Data = %s AND Ora = %s
                """
        cursor.execute(SQL, (NameSensore, timestamp.date(), timestamp.time()))

        if cursor.fetchone():
            print(f"I dati sulla temperatura sono aggiornati")
            break
        else:
            SQL =   "INSERT INTO temperatura (Data, Ora, Valore, NameSensore) VALUES (%s, %s, %s, %s)"
            cursor.execute(SQL, (timestamp.date(), timestamp.time(), temperatura, NameSensore))
            print(f"Inserito nelle temperature: {timestamp.date()} {timestamp.time()} {temperatura} {NameSensore}")
    
    conn.commit()
    cursor.close()
    conn.close()

def insertUmidita():
    path = "../RiceviDati/DatiSensori/temperatura_umidita.csv"
    df = pd.read_csv(path, sep=',', encoding='latin1') 
    df.columns = ['timestamp', 'modulo', 'temperatura', 'umidita']
    df = df[::-1].reset_index(drop=True)
    
    conn = connect_db()
    cursor = conn.cursor()
    
    for _, row in df.iterrows():
        timestamp = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S')
        modulo = row['modulo']
        umidita = str(row['umidita'])
            
        if(modulo == "a"):
            NameSensore = "SensUmid1"
        if(modulo == "b"):
            NameSensore = "SensUmid2"
        if(modulo == "c"):
            NameSensore = "SensUmid3"
               
        SQL =   """ SELECT 1 
                    FROM umidita 
                    WHERE NameSensore = %s AND Data = %s AND Ora = %s
                """
        cursor.execute(SQL, (NameSensore, timestamp.date(), timestamp.time()))

        if cursor.fetchone():
            print(f"I dati sull'umidità sono aggiornati")
            break
        else:
            SQL =   "INSERT INTO umidita (Data, Ora, Valore, NameSensore) VALUES (%s, %s, %s, %s)"
            cursor.execute(SQL, (timestamp.date(), timestamp.time(), umidita, NameSensore))
            print(f"Inserito nelle umidita: {timestamp.date()} {timestamp.time()} {umidita} {NameSensore}")
    
    conn.commit()
    cursor.close()
    conn.close()

def insertQualitaAria():
    path = "../RiceviDati/DatiSensori/temperatura_umidita.csv"
    df = pd.read_csv(path, sep=',', encoding='latin1') 
    df.columns = ['timestamp', 'modulo', 'temperatura', 'umidita']
    df = df[::-1].reset_index(drop=True)
    
    conn = connect_db()
    cursor = conn.cursor()
    
    for _, row in df.iterrows():
        timestamp = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S')
        modulo = row['modulo']
        temperatura = str(row['temperatura'])
            
        if(modulo == "a"):
            NameSensore = "SensTemp1"
        if(modulo == "b"):
            NameSensore = "SensTemp2"
        if(modulo == "c"):
            NameSensore = "SensTemp3"
               
        SQL =   """ SELECT 1 
                    FROM temperatura 
                    WHERE NameSensore = %s AND Data = %s AND Ora = %s
                """
        cursor.execute(SQL, (NameSensore, timestamp.date(), timestamp.time()))

        if cursor.fetchone():
            print(f"I dati sulla temperatura sono aggiornati")
            break
        else:
            SQL =   "INSERT INTO temperatura (Data, Ora, Valore, NameSensore) VALUES (%s, %s, %s, %s)"
            cursor.execute(SQL, (timestamp.date(), timestamp.time(), temperatura, NameSensore))
            print(f"Inserito nelle temperature: {timestamp.date()} {timestamp.time()} {temperatura} {NameSensore}")
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    while True:
        insertTemperatura()
        insertUmidita()
        time.sleep(10)
