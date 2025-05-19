import random
import datetime
import time

from Config import *

# Funzione che genererà dati di allagamento
def genera_dati_allagamento(datatime):
    with open(file_allagamento, 'w', encoding='utf-8') as outfile:
        modulo = 'b'
        valore_sensore = random.randint(0, 1)
        
        outfile.write(f'timestamp,modulo,allagamento\n')
        outfile.write(f'{datatime},{modulo},{valore_sensore}\n')
    print(f"File allagamento aggiornato: {datatime}")

#Funzione che genererà dati di qualità dell'aria
def genera_dati_ariaCo(datatime):
    with open(file_ariaCo, 'w', encoding='utf-8') as outfile:
        valore = random.randint(0,10)
        outfile.write(f'timestamp,modulo,CO (ppm)\n')
        outfile.write(f'{datatime},a,{valore}\n')       
    print(f"File aria Co aggiornato: {datatime}")
def genera_dati_ariaNo2(datatime):
    with open(file_ariaNo2, 'w', encoding='utf-8') as outfile:
        valore = random.randint(0,10)
        outfile.write(f'timestamp,modulo,NO2 (ppm)\n')
        outfile.write(f'{datatime},b,{valore}\n')
    print(f"File aria No2 aggiornato: {datatime}")

# Funzione che genererà dati di vibrazioni
def genera_dati_vibrazioni(datatime):
    with open(file_vibrazioni, 'w', encoding='utf-8') as outfile:
        modulo = 'a'
        valore_sensore_Hz = random.randint(0,10)
        valore_sensore_ms = random.randint(0,10)
        
        outfile.write(f'timestamp,modulo,vibrazione (m/s²),frequenza (Hz)\n')
        outfile.write(f'{datatime},{modulo},{valore_sensore_ms},{valore_sensore_Hz}\n')
    print(f"File vibrazioni aggiornato: {datatime}")

# Funzione che genererà dati di temperatura e umidità
def genera_dati_temp_umid(datatime):
    with open(file_temp_umid, 'w', encoding='utf-8') as outfile:
        moduli = ["a", "b", "c"]
        modulo = random.choice(moduli)
        valore_sensore_T = random.randint(-10,40)
        valore_sensore_U = random.randint(0,100)
        
        outfile.write(f'timestamp,modulo,temperatura (°C),umidità (%)\n')
        outfile.write(f'{datatime},{modulo},{valore_sensore_T},{valore_sensore_U}\n')
    print(f"File temperatura aggiornato: {datatime}")

# Funzione che genererà dati di batterie
def genera_dati_batterie(datatipe):
    with open(file_batterie, 'w', encoding='utf-8') as outfile:
        moduli = ["b", "c"]
        modulo = random.choice(moduli)
        valore_batteria = random.randint(0,99)
        
        outfile.write(f'timestamp,modulo,batteria (%)\n')
        outfile.write(f'{datatipe},{modulo},{valore_batteria}\n')
    print(f"File batterie aggiornato: {datatipe}")

# Funzione per eseguire continuamente l'aggiornamento dei dati
def aggiorna_dati_continuamente(intervallo):
    while True:
        try:
            datatime = datetime.datetime.now().replace(microsecond=0)
            genera_dati_allagamento(datatime)
            genera_dati_ariaCo(datatime)
            genera_dati_ariaNo2(datatime)
            genera_dati_vibrazioni(datatime)
            genera_dati_temp_umid(datatime)
            genera_dati_batterie(datatime)
            print(f"Tutti i file aggiornati - {datetime.datetime.now().strftime('%H:%M:%S')}\n")
            time.sleep(intervallo)
        except Exception as e:
            print(f"Si è verificato un errore: {e}")
            time.sleep(intervallo)