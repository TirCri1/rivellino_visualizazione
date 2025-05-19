
#Attenzione al main!!!


PATH = "Archivio/Dati" #Percorso della cartella contenente lo storico dei dati

#Configurazioni del DB
DB_CONFIG = {
    "host": "localhost",
    #"host": "10.10.60.186",
    "user": "remoteUser",
    "password": "!rivellino!RIVELLINO!",
    "database": "rivellino"
}

TEMPERATURA = {
    "file": "temperatura.csv",
    "fileStructure": ["Data", "Ora", "Valore"],
    "tabellaQuery": "temperatura",
    "dbStructure": ["Data", "Ora", "Valore", "NameSensore"],
    "sensori": ["SensTemp1", "SensTemp2", "SensTemp3"]
}

UMIDITA = {
    "file": "umidita.csv",
    "fileStructure": ["Data", "Ora", "Valore"],
    "tabellaQuery": "umidita",
    "dbStructure": ["Data", "Ora", "Valore", "NameSensore"],
    "sensori": ["SensUmid1", "SensUmid2", "SensUmid3"]
}

QUALITA_ARIA = {
    "file": "aria.csv",
    "fileStructure": ["Data", "Ora", "ValoreCo", "ValoreNo2"],
    "tabellaQuery": "qualita",
    "dbStructure": ["Data", "Ora", "ValoreCo", "ValoreNo2", "NameSensore"],
    "sensori": ["SensQualitàAria1", "SensQualitàAria2"]
}

VIBRAZIONE = {
    "file": "vibrazioni.csv",
    "fileStructure": ["Data", "Ora", "ValoreFrequenza", "ValoreAmpiezza"],
    "tabellaQuery": "vibrazione",
    "dbStructure": ["Data", "Ora", "ValoreFrequenza", "ValoreAmpiezza", "NameSensore"],
    "sensori": ["SensVibrazione"]
}

ALLAGAMENTO = {
    "file": "allagamento.csv",
    "fileStructure": ["Data", "Ora", "Valore"],
    "tabellaQuery": "allagamento",
    "dbStructure": ["Data", "Ora", "Valore", "NameSensore"],
    "sensori": ["SensAllagamento"]
}

STRUCTURE = {
    "temperatura": TEMPERATURA,
    "umidita": UMIDITA,
    "qualita": QUALITA_ARIA,
    "vibrazioni": VIBRAZIONE,
    "allagamento": ALLAGAMENTO
}
